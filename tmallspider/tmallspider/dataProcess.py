import pandas as pd
import numpy as np
import openpyxl

#jditem = pd.read_csv('spiders/itemjd.csv')
#tmallitem = pd.read_csv('spiders/itemtmall.csv')
#dditem = pd.read_csv('spiders/itemdd.csv')
#snitem = pd.read_csv('spiders/itemsn.csv')

df = pd.concat(map(pd.read_csv, ['spiders/itemjd.csv', 'spiders/itemtmall.csv','spiders/itemsn.csv']))
df.to_excel('output.xlsx')

#print(df)