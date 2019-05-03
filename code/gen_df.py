import pandas as pd
from itertools import product

data = pd.read_csv("../input/trade_data_filtered/cn2014.csv")
data["PRODUCT_NC"] = data["PRODUCT_NC"].apply(lambda x: str(x[:6]))
sixdigit_product_trade = pd.DataFrame(data.groupby(["TRADE_TYPE",'DECLARANT_ISO','PARTNER_ISO',"PRODUCT_NC"])['VALUE_IN_EUROS'].sum().reset_index())


prod_keys = sixdigit_product_trade["PRODUCT_NC"].unique()
DECLARANT_countries = data["DECLARANT_ISO"].unique()
PARTNER_countries = data["PARTNER_ISO"].unique()

new_df = pd.DataFrame(list(product(DECLARANT_countries, PARTNER_countries,prod_keys)), columns=["DECLARANT_ISO","PARTNER_ISO","PRODUCT_NC"])

new_df = new_df.loc[new_df["DECLARANT_ISO"]!=new_df["PARTNER_ISO"]]

new_df.to_csv(r'../temp/new_df_2.csv')
