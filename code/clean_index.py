import pandas as pd
for db in ['../temp/index/INDEX_IMP.csv','../temp/index/INDEX_EXP.csv']:
	data = pd.read_csv(db)
	data = data.drop(index=[0,1,2])
	cols = ["DECLARANT","PARTNER"] + [ "TCI_"+str(x) for x in range(2001,2018)]
	data.columns = cols
	data.to_csv("../../output/"+db)
