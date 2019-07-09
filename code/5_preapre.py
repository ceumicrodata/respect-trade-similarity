import pandas as pd

exp = pd.read_csv("../temp/TC_INDEX_EXP_.csv").drop(["Unnamed: 0"], axis = 1)
imp = pd.read_csv("../temp/TC_INDEX_IMP_.csv").drop(["Unnamed: 0"], axis = 1)

melted_EXP = pd.DataFrame(exp.melt(id_vars=["DECLARANT","PARTNER"])\
                          .assign(YEAR = lambda df: df["variable"].apply(lambda x: x[4:]))\
                          .drop(["variable"], axis = 1)\
                          .groupby(["DECLARANT","PARTNER","YEAR"])["value"].sum())\
                .pipe(lambda df:df.assign(FLOW = "EXP"))
melted_IMP = pd.DataFrame(imp.melt(id_vars=["DECLARANT","PARTNER"])\
                          .assign(YEAR = lambda df: df["variable"].apply(lambda x: x[4:]))\
                          .drop(["variable"], axis = 1)\
                          .groupby(["DECLARANT","PARTNER","YEAR"])["value"].sum())\
                .pipe(lambda df:df.assign(FLOW = "IMP"))

THETA = 8.0

final_df = pd.concat([melted_EXP,melted_IMP])\
    .reset_index().set_index(["DECLARANT","PARTNER","FLOW","YEAR"])\
    .rename(columns = {"value":"kullback_leibler_divergence"})\
    .assign(trade_similarity_index = lambda df: pd.np.exp(-1/THETA * df['kullback_leibler_divergence']))

final_df.to_csv("../output/trade_similarity_index.csv")
