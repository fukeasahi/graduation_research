import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("/content/japan_retasu.xls")
df = df.loc[:,["農林水産関係市町村別統計","Unnamed: 24","Unnamed: 25","Unnamed: 26","Unnamed: 27","Unnamed: 28","Unnamed: 29","Unnamed: 30","Unnamed: 31"]]

df = df.fillna(0)
df = df.replace('…', 0)

df_shipment = df.loc[7:,["農林水産関係市町村別統計","Unnamed: 29"]].groupby('農林水産関係市町村別統計').sum()
df_shipment = df_shipment[1:48]

df_code = pd.read_excel("/content/12401905810_冨家旭陽.xlsx",sheet_name="Sheet3")
df_japan_engrahu = pd.merge(df_code,df_shipment, left_on="Unnamed: 0", right_on="農林水産関係市町村別統計")
df_japan_engrahu.to_excel("都道府県別レタス出荷量.xlsx")