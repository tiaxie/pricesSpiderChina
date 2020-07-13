import pandas as pd
import numpy as np

jditem = pd.read_csv('/tmallspider/spiders/jditem.csv')

'''
jd_pad = pd.read_csv('jd.csv')
jd_pad.head(15)
print(jd_pad)
jd_pad = jd_pad[~jd_pad.product_name_jd.str.contains("华为")]
jd_pad = jd_pad[~jd_pad.product_name_jd.str.contains("一")]
jd_pad = jd_pad[~jd_pad.product_name_jd.str.contains("二")]
jd_pad = jd_pad[jd_pad['product_name_jd'].str.contains('iPad', na=False)]
jd_pad = jd_pad[jd_pad['product_name_jd'].str.contains('3', na=False)]
jd_pad = jd_pad.head(5)
print(jd_pad)
jd_lowest = jd_pad['product_price_jd'].min()
print(jd_lowest)

tmall_pad = pd.read_csv('tmall.csv')
tmall_pad = tmall_pad.head(15)
print(tmall_pad)
tmall_pad = tmall_pad[~tmall_pad.product_name_tmall.str.contains("华为")]
tmall_pad = tmall_pad[~tmall_pad.product_name_tmall.str.contains("一")]
tmall_pad = tmall_pad[~tmall_pad.product_name_tmall.str.contains("二")]
tmall_pad = tmall_pad[tmall_pad['product_name_tmall'].str.contains('iPad', na=False)]
tmall_pad = tmall_pad[tmall_pad['product_name_tmall'].str.contains('3', na=False)]
tmall_pad = tmall_pad.head(5)
print(tmall_pad)
tmall_lowest = tmall_pad['product_price_tmall'].min()
print(tmall_lowest)
'''

'''
data = {'product_name':  ['iPad air', 'iphone', 'iPad air3', '华为'],
        'product_price': ['100', '200', '300', '100']
        }

df = pd.DataFrame (data, columns = ['product_name','product_price'])
df.drop(df.columns[df.columns.str.contains('iphone')], axis=1, inplace=True)
print(df)
df = df[~df.product_name.str.contains("华为")]
df = df[~df.product_name.str.contains("一")]
df = df[~df.product_name.str.contains("二")]
df = df[df.columns[0].str.contains('iPad', na=False)]
print(df)
'''