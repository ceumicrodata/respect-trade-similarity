import glob
import pandas as pd
from multiprocessing import Pool

file_list = glob.glob('../temp/index/data/index_??P_20??.csv')

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


lista = [file_list_EXP,file_list_IMP]

def make_index(file_list):
	data = pd.concat([pd.read_csv(f).rename(columns=lambda x: x.split('_')[0]).assign(FILE=f[-8:-4]) for f in file_list])
	data = data.pivot_table(index=['DECLARANT','PARTNER'],columns='FILE')
	data.to_csv('../temp/index/dirty/INDEX_'+file_list[0][-12:-8]+'.csv')

pool = Pool(processes=2)
pool.map(make_index,lista)
pool.close()
pool.join()
