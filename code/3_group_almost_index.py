import pandas as pd
from multiprocessing import Pool

from os import listdir
from os.path import isfile, join

mypath = "../temp/almost_index/"

data_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for file in data_list:

        pd.DataFrame(pd.read_csv(file).fillna(0).groupby(["DECLARANT_ISO","PARTNER_ISO"])["almost_index"].sum()).rename(columns= { "almost_index":"index"}).to_csv("../temp/index/data/"+file[-14:-4]+"_index.csv")




"""
pool = Pool(processes = 17)
pool.map(lambda file:  pd.DataFrame(pd.read_csv(file).fillna(0).groupby(["DECLARANT_ISO","PARTNER_ISO"])["almost_index"].sum()).rename(columns= { "almost_index":"index"}).to_csv(file[-14:-4]+"_index.csv"),data_list)
pool.close()
pool.join()
"""
