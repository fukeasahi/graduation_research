import pandas as pd
df = pd.read_excel("/content/12401905810_冨家旭陽.xlsx", sheet_name="佐久の天気")
a = df.loc[5:, ["ダウンロードした時刻：2021/11/22 12:52:35", "Unnamed: 1", "Unnamed: 4", "Unnamed: 7", "Unnamed: 10", "Unnamed: 13", "Unnamed: 16", "Unnamed: 19"]]
a.to_excel("佐久の天気加工後.xlsx")
