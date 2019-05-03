import pandas as pd
from multiprocessing import Pool, cpu_count

from os import listdir
from os.path import isfile, join

mypath = "../temp/exp_imp/"

data_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]




def almost_index(filename):
    data = pd.read_csv(filename).drop(columns="Unnamed: 0")
    orszag_orszag_agg = data.groupby(["DECLARANT_ISO","PARTNER_ISO"])["VALUE_IN_EUROS"].sum()
    
    partner_prod = pd.DataFrame(data.groupby(["PARTNER_ISO","PRODUCT_NC"])["VALUE_IN_EUROS"].sum()).reset_index()
    partners_agg = data.groupby("PARTNER_ISO")["VALUE_IN_EUROS"].sum()

    partner_prod["agg"] = partner_prod["PARTNER_ISO"].apply(lambda x: partners_agg[x])
    partner_prod["prod_share_EU"] = partner_prod.loc[:,["VALUE_IN_EUROS","agg"]].apply(lambda series: series["VALUE_IN_EUROS"]/series["agg"] ,axis = 1)
    partner_prod = partner_prod.set_index(["PARTNER_ISO","PRODUCT_NC"])
    
    data = data.assign(country_country_total = data.loc[:,["DECLARANT_ISO","PARTNER_ISO"]].apply(lambda df: orszag_orszag_agg[df["DECLARANT_ISO"]][df["PARTNER_ISO"]], axis=1))\
    .pipe(lambda x: x.assign(prod_share = x.loc[:,["VALUE_IN_EUROS","country_country_total"]].apply(lambda df: df["VALUE_IN_EUROS"]/df["country_country_total"], axis=1)))\
    .pipe(lambda x: x.assign(almost_index = x.loc[:,["PRODUCT_NC","prod_share","PARTNER_ISO"]].apply(lambda df: df["prod_share"]*pd.np.log(df["prod_share"]/partner_prod.loc[df["PARTNER_ISO"]].loc[df["PRODUCT_NC"]]["prod_share_EU"]), axis=1)))
    
    result = pd.read_csv("../temp/result.csv").drop("Unnamed: 0",axis = 1)
    merged = pd.merge(result,data, how="left",left_on=["PRODUCT_CODE","PARTNER","DECLARANT"],right_on=["PRODUCT_NC", "PARTNER_ISO","DECLARANT_ISO"])
    merged.to_csv("../temp/almost_index"+"MERGED_"+filename)
    
pool = Pool(processes=34)
pool.map(almost_index,data_list)
pool.close()
pool.join()
