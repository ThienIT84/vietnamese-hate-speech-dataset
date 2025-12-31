import pandas as pd

df = pd.read_csv('STRATEGIC_SAMPLES_PROCESSED_20251229_172847.csv')

print(f"Total rows: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")

print(f"\nFirst 5 training_text:")
for i in range(min(5, len(df))):
    text = str(df.iloc[i]['training_text'])
    print(f"{i+1}. [{len(text)} chars] {text[:150]}")

print(f"\nEmpty training_text: {df['training_text'].isna().sum()}")
print(f"Empty string: {(df['training_text'] == '').sum()}")
print(f"Very short (<5 chars): {(df['training_text'].str.len() < 5).sum()}")

# Check raw data
print(f"\nFirst 3 raw_comment:")
for i in range(min(3, len(df))):
    raw = str(df.iloc[i].get('raw_comment', 'N/A'))
    print(f"{i+1}. {raw[:100]}")
