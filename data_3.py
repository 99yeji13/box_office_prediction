import pandas as pd

df_A = pd.read_csv("boxoffice.csv", sep = ',', encoding = 'utf-8')
df_B = pd.read_csv("movie.csv", sep = ',', encoding = 'utf-8')

total = pd.merge(df_A,df_B)

total.to_csv("total.csv")

df = pd.read_csv("total.csv", sep=',')
print(df)