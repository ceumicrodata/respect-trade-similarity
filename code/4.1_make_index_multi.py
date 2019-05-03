import glob
import pandas as pd
from multiprocessing import Pool

file_list = glob.glob('../temp/index/data/*')

#Select those which contain the export data
file_list_EXP = [db for db in file_list if "EXP" in db]

file_list_IMP = [db for db in file_list if "IMP" in db]

print(file_list_IMP[0][-20:-17],file_list_EXP[0][-20:-17])

lista = [file_list_EXP,file_list_IMP]

def make_index(file_list):
	df = pd.concat([pd.read_csv(f).drop('Unnamed: 0',axis=1).rename(columns=lambda x: x.split('_')[0]).assign(FILE=fa[-14:-10]) for f in file_list])

	df = df.pivot_table(index=['DECLARANT','PARTNER'],columns='FILE')

	df.to_csv('../temp/index/dirty/INDEX_'+file_list[0][-20:-17]+'.csv')

pool = Pool(processes=2)
pool.map(make_index,lista)
pool.close()
pool.join()
