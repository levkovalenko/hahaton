import pandas as pd
import os

print(os.listdir(path='data'))
for file in os.listdir(path='data'):
    df = pd.read_csv(f'data/{file}')
    df.loc[-1] = df.columns
    df.index = df.index + 1
    df = df.sort_index()
    df.columns = ['timestamp', 'identifier', 'amount']
    df.to_csv(f'data/{file}', index = None, header=True)
    print(df.head(10))
