import pandas as pd

data = pd.read_csv("../input/trade_data_filtered/cn2014.csv")

TOTAL = data.loc[data.PRODUCT_NC == "TOTAL"]

data = data[data.PRODUCT_NC != "TOTAL"]
TOTAL.head()


data["PRODUCT_NC"] = data["PRODUCT_NC"].apply(lambda x: str(x[:6]))
sixdigit_product_trade = pd.DataFrame(data.groupby(["TRADE_TYPE",'DECLARANT_ISO','PARTNER_ISO',"PRODUCT_NC"])['VALUE_IN_EUROS'].sum().reset_index())

#generate product keys
prod_keys = sixdigit_product_trade["PRODUCT_NC"].unique()


#generate list for countries

DECLARANT_countries = data["DECLARANT_ISO"].unique()
PARTNER_countries = data["PARTNER_ISO"].unique()

#generate a dictionary with values of the product code dataframes 
d = {name: pd.DataFrame(prod_keys, columns=["PRODUCT_CODE"]) for name in PARTNER_countries}

for i in PARTNER_countries:    
    d[i]["PARTNER"]=i
    
df_list = [d[i] for i in PARTNER_countries]


#generate list for countries
DECLARANT_countries = data["DECLARANT_ISO"].unique()
PARTNER_countries = data["PARTNER_ISO"].unique()


#generate dictionary with values of dataframes of product codes and partner countries 
d_2 = {name: pd.concat(df_list) for name in DECLARANT_countries}

for i in DECLARANT_countries:    
    d_2[i]["DECLARANT"]=i
    
df_2_list = [d_2[i] for i in DECLARANT_countries]

result = pd.concat(df_2_list)


# drop those rows where the declarant country and the partner country is the same
result = result[result["DECLARANT"] != result["PARTNER"]]
result.to_csv(r'../temp/result.csv')


data_EXP = sixdigit_product_trade[sixdigit_product_trade["TRADE_TYPE"]=="E"].drop("TRADE_TYPE",axis=1)
data_IMP = sixdigit_product_trade[sixdigit_product_trade["TRADE_TYPE"]=="I"].drop("TRADE_TYPE",axis=1)

data_EXP.to_csv(r'../temp/data_EXP.csv')
data_IMP.to_csv(r'../temp/data_IMP.csv')
