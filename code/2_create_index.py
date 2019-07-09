import pandas as pd
from multiprocessing import Pool, cpu_count
import glob

data_list = glob.glob('../temp/exp_imp/??P_20??.csv')

def almost_index(filename):
	fn = filename.split('/')[-1]

	data = pd.read_csv(filename).drop(columns="Unnamed: 0")

	data["EU_PRODUCT_VALUE"] = data.groupby(["PARTNER_ISO","PRODUCT_NC"])["VALUE_IN_EUROS"].transform(sum)
	data["CC_AGG"] = data.groupby(["DECLARANT_ISO","PARTNER_ISO"])["VALUE_IN_EUROS"].transform(sum)
	data["EU_AGG_VALUE"] = data.groupby(["PARTNER_ISO"])["VALUE_IN_EUROS"].transform(sum)

	data["prod_share"] = data["VALUE_IN_EUROS"] / data["CC_AGG"]
	data["eu_share"] = data["EU_PRODUCT_VALUE"] / data["EU_AGG_VALUE"]
	data["leave_out_eu_share"] = (data["EU_PRODUCT_VALUE"] - data["VALUE_IN_EUROS"]) / (data["EU_AGG_VALUE"] - data["CC_AGG"])

	# baseline share is a convex combination of EU share and leave-out share
	# to ensure to baseline share is 0
	data["baseline_share"] = 0.9992 * data["leave_out_eu_share"] + 0.0008 * data["eu_share"]

	data["KLD"] = data["prod_share"]*pd.np.log(data["prod_share"]/data["baseline_share"])

	new = pd.DataFrame(data.groupby(["DECLARANT_ISO","PARTNER_ISO"])["KLD"].sum()).reset_index()
	new.columns = ["DECLARANT_ISO","PARTNER_ISO","TCI"]

	new.to_csv("../temp/index/data/index_"+fn)



pool = Pool(processes=34)
pool.map(almost_index,data_list)
pool.close()
pool.join()
