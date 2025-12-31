import pandas as pd

df = pd.DataFrame({
    'training_text': ['nguoi ta ko biet', 'dm game hay vcl'],
    'label': [0, 0]
})

df.to_excel('test_sample.xlsx', index=False)
print('✓ Created test_sample.xlsx')
