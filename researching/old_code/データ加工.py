import pandas as pd
df = pd.read_excel("/content/data.xltx")

# "品質情報" と"均質番号"を削除
col1 = []
for i in range(1,len(df.columns)):
  if df.iloc[4,i] != "品質情報" and df.iloc[4,i] != "均質番号":
    col1.append(f"Unnamed: {i}")
df = df[col1]

# '日最高気温の平均(℃)', '日照時間(時間)', '降水量の合計(mm)', '平均気温(℃)', '最高気温(℃)', '日最高気温の最低(℃)', '日最低気温の最高(℃)', '最低気温(℃)', '日最低気温の平均(℃)'ごとにファイルを分ける
all_explanatory_variable = set(df.loc[2,:])
for explanatory_variable in all_explanatory_variable:
  col2 = []
  for column in df.columns:
    if df.loc[2,column] == explanatory_variable:
      col2.append(column)
  df2 = df[col2]
  df2.to_excel(f'/content/data_{explanatory_variable}.xlsx',index=False, header=False, encoding='utf-8')