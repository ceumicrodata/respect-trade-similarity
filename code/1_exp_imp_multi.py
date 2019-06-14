import pandas as pd
from multiprocessing import Pool
from os import listdir
from os.path import isfile, join

mypath = "../input/trade_data_filtered/"

data_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]


# here you can define the lenght og the product code 
digit_code = 4
print("NOW USING",digit_code,"DIGIT CODE")


def exp_imp(data_name):
    source_in = "../input/trade_data_filtered/"
    source_out = "../temp/"

    ########################################################
    data = pd.read_csv(source_in+data_name)
    #drop rows where "TOTAL" occures, filter to rows where stat_regime == 1
    data = data[data.PRODUCT_NC!="TOTAL"][data.STAT_REGIME == 1]
    #filter on product code
    data["PRODUCT_NC"] = data["PRODUCT_NC"].apply(lambda x: str(x[:digit_code]))
    # select data
    sixdigit_product_trade = pd.DataFrame(data.groupby(["FLOW",'DECLARANT_ISO','PARTNER_ISO',"PRODUCT_NC"])['VALUE_IN_EUROS'].sum().reset_index())
    ########################################################
    #separete exports and imports 
    data_EXP = sixdigit_product_trade[sixdigit_product_trade["FLOW"]==2].drop("FLOW",axis=1)
    data_IMP = sixdigit_product_trade[sixdigit_product_trade["FLOW"]==1].drop("FLOW",axis=1)

    ########################################################
    data_EXP.to_csv(source_out + '/exp_imp/'+ "EXP_" +data_name)
    data_IMP.to_csv(source_out + '/exp_imp/'+ "IMP_" +data_name)

# initiate multiprocessing
pool = Pool(processes=17)
pool.map(exp_imp,data_list)
pool.close()
pool.join()
