# import libraries
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import re

#functions
def gdp(x):

    if  "Trillion" in x:
        return float(x.replace("Trillion",""))*1000
    elif  "Billion" in x:
        return float(x.replace("Billion",""))
    elif "Million" in x:
        return float(x.replace("Million",""))/1000

#scraping
url="https://countrycode.org/"
page=get(url)

html_soup = BeautifulSoup(page.text, 'html.parser')


lista = []
kislista = []
for idx,val in enumerate(html_soup.find_all('td'),1):
    kislista.append(str(val)[4:-5])
    if len(kislista)==6:
        lista.append(kislista)
        kislista = []

CC = pd.DataFrame(lista)
#data manipulation
CC = CC.iloc[:240]

CC.columns = ["c_name","c_code_num","ISO_code","pop","area","GDP_B_USD"]

CC.ISO_code = CC.ISO_code.apply(lambda x: x[:2])

CC.area = CC.area.apply(lambda x: x.replace(",",""))

CC["pop"] = CC["pop"].apply(lambda x: x.replace(",",""))

CC.c_name = CC.c_name.apply(lambda x: re.split('<|>',x)[-3])

CC.to_csv("../../output/CC_detail.csv")
