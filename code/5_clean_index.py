import pandas as pd
from itertools import product
import glob

file_list = glob.glob('../temp/index/dirty/*')


for db in file_list:
	data = pd.read_csv(db)
	# cut those rows and columns which are not needed
	data = data.iloc[:,:19].drop(index=[0,1]).reset_index(drop=True).T.reset_index(drop=True).T
	# rename columns
	cols = ["DECLARANT","PARTNER"] + [ "TCI_"+str(x) for x in range(2001,2018)]
	data.columns = cols
	# create final dataframe
	# create an empty DF with all the possible country combinations
	new_df = pd.DataFrame(list(product(data.DECLARANT.unique(), data.PARTNER.unique())), columns=["DECLARANT","PARTNER"])
	new_df = new_df.loc[new_df["DECLARANT"]!=new_df["PARTNER"]]
	# merge the empty dataframe with the data
	merged = pd.merge(new_df,data, how="left",on=["DECLARANT","PARTNER"]) #.drop("Unnamed: 0",axis=1)

	merged.to_csv("../output/TC_"+db[-14:])
