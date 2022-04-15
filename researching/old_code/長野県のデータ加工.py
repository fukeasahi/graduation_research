import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("/content/nagano1_retasu.xls")
df = df.loc[:,["Unnamed: 2","Unnamed: 24","Unnamed: 25","Unnamed: 26","Unnamed: 27","Unnamed: 28","Unnamed: 29","Unnamed: 30","Unnamed: 31", "Unnamed: 32"]]

df = df.fillna(0)
df = df.replace('…', 0)

df_shipment = df.loc[7:,["Unnamed: 2","Unnamed: 29"]].groupby('Unnamed: 2').sum()

df_shipment = df_shipment[1:48]
df_shipment.to_excel("市町村別レタス出荷量.xlsx")