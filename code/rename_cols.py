import glob 
import pandas as pd

file_list = glob.glob("imp/*")
for filename in file_list:
	df = pd.read_csv(filename)
	list(df.columns.values)[-1]
	df.rename(columns={list(df.columns.values)[-1]: "index_"+filename[10:14]},inplace=True)
	#print(list(df.columns.values))
	#df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'Unnamed: 0.1.1.1'])
	df = df[["DECLARANT_ISO","PARTNER_ISO","index_"+filename[10:14]]]
	df.to_csv(filename)
	print(list(df.columns.values))
file_list = glob.glob("exp/*")
for filename in file_list:
	df = pd.read_csv(filename)
	list(df.columns.values)[-1]
	df.rename(columns={list(df.columns.values)[-1]: "index_"+filename[11:15]},inplace=True)
	#print(list(df.columns.values))
	#df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1', 'Unnamed: 0.1.1.1'])
	df = df[["DECLARANT_ISO","PARTNER_ISO","index_"+filename[11:15]]]
	df.to_csv(filename)
	print(list(df.columns.values))

