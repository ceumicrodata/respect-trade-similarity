import glob 
import pandas as pd

file_list = glob.glob('../temp/index/data/*')

#Select those which contain the import data 
file_list = [db for db in file_list if "IMP" in db]

df = pd.concat([pd.read_csv(f).drop('Unnamed: 0',axis=1).rename(columns=lambda x: x.split('_')[0]).assign(FILE=f[10:14]) for f in file_list])

df = df.pivot_table(index=['DECLARANT','PARTNER'],columns='FILE')

print(list(df.columns.values))
df.to_csv('../temp/index/dirty/INDEX_IMP.csv')






"""
declarants = []
partners = []

for filename in file_list:
	df = pd.read_csv(filename)
	declarants + list(df["DECLARANT_ISO"].unique())
	partners + list(df["PARTNER_ISO"].unique())
	print("DECLARANCT_ISO",len(df["DECLARANT_ISO"].unique()),"PARTNER",len(df["PARTNER_ISO"].unique()))



from itertools import product
df = pd.DataFrame(list(product(list(set(declarants)), list(set(partners)))), columns=["DECLARANT_ISO","PARTNER_ISO"])

for filename in file_list:
	df = pd.merge(df,pd.read_csv(filename), left_on = ["DECLARANT_ISO","PARTNER_ISO"], right_on = ["DECLARANT_ISO","PARTNER_ISO"], how="left")
	#df = pd.concat([df,pd.read_csv(filename)], axis = 1, keys=["DECLARANT_ISO","PARTNER_ISO"],join="inner")
df.to_csv("index_IMP.csv")
"""
