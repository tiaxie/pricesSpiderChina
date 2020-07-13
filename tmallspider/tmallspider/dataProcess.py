import pandas as pd
import numpy as np

jditem = pd.read_csv('spiders/jditem.csv')
tmallitem = pd.read_csv('spiders/tmallitem.csv')
dditem = pd.read_csv('spiders/dditem.csv')
snitem = pd.read_csv('spiders/snitem.csv')
lowest_price = []

dditem['product_price_dd'] = dditem['product_price_dd'].str.replace('¥', '')

price_csvs = [jditem, tmallitem, dditem]

for my_csv in price_csvs:
    my_csv.dropna(axis=0, how='any', inplace=True)
    my_csv[~my_csv.iloc[:, 0].str.contains('华为')]
    my_csv[~my_csv.iloc[:, 0].str.contains('膜')]
    my_csv[~my_csv.iloc[:, 0].str.contains('套')]
    my_csv = my_csv[my_csv.iloc[:, 0].str.contains('iPad', na=False)]
    my_csv = my_csv[my_csv.iloc[:, 0].str.contains('3', na=False)]

print(dditem)


