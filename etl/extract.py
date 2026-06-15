import pandas as pd

df = pd.read_csv("data/graduate_survey.csv")

print(df.head())
print()
print(df.info())
print()
print(df.describe())