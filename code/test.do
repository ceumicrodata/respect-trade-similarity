clear all
import delimited ../temp/exp_imp/IMP_cn2017.csv

do KLD.do

su KLD, d
save ../temp/KLD.dta, replace
