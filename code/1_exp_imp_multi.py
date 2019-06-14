import pandas as pd
from multiprocessing import Pool

from os import listdir
from os.path import isfile, join

mypath = "../input/trade_data_filtered/"

data_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]

def exp_imp(data_name):
    source_in = "../input/trade_data_filtered/"
    source_out = "../temp/"

    ########################################################
    data = pd.read_csv(source_in+data_name)
    data = data[data.PRODUCT_NC!="TOTAL"][data.STAT_REGIME == 1]
    data["PRODUCT_NC"] = data["PRODUCT_NC"].apply(lambda x: str(x[:4]))
    sixdigit_product_trade = pd.DataFrame(data.groupby(["FLOW",'DECLARANT_ISO','PARTNER_ISO',"PRODUCT_NC"])['VALUE_IN_EUROS'].sum().reset_index())
    ########################################################

    data_EXP = sixdigit_product_trade[sixdigit_product_trade["FLOW"]==2].drop("TRADE_TYPE",axis=1)
    data_IMP = sixdigit_product_trade[sixdigit_product_trade["FLOW"]==1].drop("TRADE_TYPE",axis=1)

    ########################################################
    data_EXP.to_csv(source_out + '/exp_imp/'+ "EXP_" +data_name)
    data_IMP.to_csv(source_out + '/exp_imp/'+ "IMP_" +data_name)
    
pool = Pool(processes=17)
pool.map(exp_imp,data_list)
pool.close()
pool.join()
