import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

def Append():
  global df

  for i in range(10):
    df = df._append({'A': i, 'B': i+1}, ignore_index=True)


Append()

print(df)