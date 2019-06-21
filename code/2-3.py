import pandas as pd
from multiprocessing import Pool, cpu_count
import glob

data_list = glob.glob('../temp/exp_imp/*')

# print(data_list)
# print(data_list[0][-14:])
def almost_index(filename):
	data = pd.read_csv(filename).drop(columns="Unnamed: 0")
	EU_shares = pd.DataFrame(data.groupby(["PARTNER_ISO","PRODUCT_NC"])["VALUE_IN_EUROS"].sum()).reset_index()
	EU_shares.name = "EU_PRODUCT_VALUE"

	EU_country_total = data.groupby(["PARTNER_ISO"])["VALUE_IN_EUROS"].sum()
	EU_country_total.name = "EU_AGG_VALUE"

	EU_shares = EU_shares.merge(EU_country_total,left_on="PARTNER_ISO", right_on="PARTNER_ISO",how="left")

	CC_total = data.groupby(["DECLARANT_ISO","PARTNER_ISO"])["VALUE_IN_EUROS"].sum()
	CC_total.name = "CC_AGG"

	data = data.merge(CC_total, left_on=["DECLARANT_ISO","PARTNER_ISO"], right_on=["DECLARANT_ISO","PARTNER_ISO"])            

	data = data.assign(prod_share = data["VALUE_IN_EUROS"]/ data["CC_AGG"])

	data = data.merge(EU_shares.loc[:, ["PARTNER_ISO", "PRODUCT_NC", "EU_AGG_VALUE", "EU_PRODUCT_VALUE"]], on=["PARTNER_ISO", "PRODUCT_NC"])
	data = data.assign(leave_out_eu_share = (data["EU_PRODUCT_VALUE"] - data["VALUE_IN_EUROS"]) / (data["EU_AGG_VALUE"] - data["CC_AGG"]))

	data = data.assign(KLD = data["prod_share"]*pd.np.log(data["prod_share"]/data["leave_out_eu_share"]))

	new = pd.DataFrame(data.groupby(["DECLARANT_ISO","PARTNER_ISO"])["KLD"].sum()).reset_index()
	new.columns = ["DECLARANT_ISO","PARTNER_ISO","TCI"]

	new.to_csv("../temp/index/data/index_"+filename[-14:])

pool = Pool(processes=34)
pool.map(almost_index,data_list)
pool.close()
pool.join()

