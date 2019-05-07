import pandas as pd
from itertools import product
import glob

file_list = glob.glob('../temp/index/dirty/*')


for db in file_list:
	data = pd.read_csv(db)
	data = data.iloc[:,:19].drop(index=[0,1]).reset_index(drop=True).T.reset_index(drop=True).T
	cols = ["DECLARANT","PARTNER"] + [ "TCI_"+str(x) for x in range(2001,2018)]
	data.columns = cols

	new_df = pd.DataFrame(list(product(data.DECLARANT.unique(), data.PARTNER.unique())), columns=["DECLARANT","PARTNER"])
	new_df = new_df.loc[new_df["DECLARANT"]!=new_df["PARTNER"]]
	merged = pd.merge(new_df,data, how="left",on=["DECLARANT","PARTNER"]) #.drop("Unnamed: 0",axis=1)
	merged.to_csv("../output/TC_"+db[-14:])
