import csv
import pandas as pd


df = pd.read_csv('jan.csv',encoding='cp932',header=None)
print('a' in df.values)
'a' in df.values
