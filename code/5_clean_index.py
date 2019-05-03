import pandas as pd
from itertools import product


for db in ['../temp/index/dirty/INDEX_IMP.csv','../temp/index/dirty/INDEX_EXP.csv']:
	data = pd.read_csv(db)
	data = data.drop(index=[0,1,2])
	cols = ["DECLARANT","PARTNER"] + [ "TCI_"+str(x) for x in range(2001,2018)]
	data.columns = cols
	new_df = pd.DataFrame(list(product(data.DECLARANT.unique(), data.PARTNER.unique())), columns=["DECLARANT","PARTNER"])
	new_df = new_df.loc[new_df["DECLARANT"]!=new_df["PARTNER"]]
	merged = pd.merge(new_df,data, how="left",on=["DECLARANT","PARTNER"])
	merged.to_csv("../../output/TC_"+db[-13:])
