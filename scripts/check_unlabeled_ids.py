import pandas as pd
import base64

df = pd.read_csv(r'c:\Học sâu\Dataset\data\processed\unlabeled_data.csv', nrows=20)
print('Sample decoded IDs from unlabeled_data.csv:')
print('='*80)
for i, row in df.iterrows():
    decoded = base64.b64decode(row['id']).decode('utf-8')
    print(f'{i+1}. {decoded}')
