import glob
import pandas as pd
from multiprocessing import Pool

file_list = glob.glob('../temp/index/data/index_??P_20??.csv')

#print(len(file_list))
def colnames(df):
	try:
		cols = ["DECLARANT_ISO","PARTNER_ISO","TCI"]
		data = pd.read_csv(df)
		data.columns=cols
		data.to_csv(df)
	except:
		print("van meg 1 oszlop")

pool = Pool(processes=34)
pool.map(colnames,file_list)
pool.close()
pool.join()


#Select those which contain the export data
file_list_EXP = [db for db in file_list if "EXP" in db]

file_list_IMP = [db for db in file_list if "IMP" in db]

#print(file_list_IMP,file_list_EXP)
#print("IMP", len(file_list_IMP))
#print("EXP", len(file_list_EXP))

lista = [file_list_EXP,file_list_IMP]

def make_index(file_list):

	data = pd.concat([pd.read_csv(f).rename(columns=lambda x: x.split('_')[0]).assign(FILE=f[-8:-4]) for f in file_list])
	#data.columns = ["DESCLARANT","PARTNER","TCI"]
	data = data.pivot_table(index=['DECLARANT','PARTNER'],columns='FILE')
	data.to_csv('../temp/index/dirty/INDEX_'+file_list[0][-12:-8]+'.csv')
	# new content
	#print("new content")
	"""
	data = data.iloc[:,:19].drop(index=[0,1]).reset_index(drop=True).T.reset_index(drop=True).T
	cols = ["DECLARANT","PARTNER"] + [ "TCI_"+str(x) for x in range(2001,2018)]
	data.columns = cols
	print("generate new df")
	new_df = pd.DataFrame(list(product(data.DECLARANT.unique(), data.PARTNER.unique())), columns=["DECLARANT","PARTNER"])
	new_df = new_df.loc[new_df["DECLARANT"]!=new_df["PARTNER"]]
	print("merging")
	merged = pd.merge(new_df,data, how="left",on=["DECLARANT","PARTNER"]) #.drop("Unnamed: 0",axis=1)
	merged.to_csv("../output/TC_"+db[-14:])
	"""


pool = Pool(processes=2)
pool.map(make_index,lista)
pool.close()
pool.join()
