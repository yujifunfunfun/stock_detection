
import pandas as pd
data = pd.read_csv('jan.csv',header=None)


data = data.replace('jan', '')
print(data)

data.to_csv('jan.csv', index=False,header=None)