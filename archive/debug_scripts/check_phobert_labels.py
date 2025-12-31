"""
Check PhoBERT file labels
"""
import pandas as pd
import numpy as np

print("="*60)
print("CHECKING PHOBERT FILE LABELS")
print("="*60)

df = pd.read_excel('data/final/final_train_data_v3_READY.xlsx')

print(f"\nTotal samples: {len(df)}")
print(f"Columns: {list(df.columns)}")

print(f"\nLabel column dtype: {df['label'].dtype}")
print(f"\nUnique labels (first 20):")
print(df['label'].unique()[:20])

# Count numeric vs text labels
numeric_count = df['label'].apply(lambda x: isinstance(x, (int, float, np.integer))).sum()
text_count = len(df) - numeric_count

print(f"\nNumeric labels: {numeric_count}")
print(f"Text labels: {text_count}")

# Show text labels
if text_count > 0:
    text_labels = df[df['label'].apply(lambda x: isinstance(x, str))]['label'].unique()
    print(f"\nText label values:")
    for label in text_labels[:10]:
        print(f"  - {label}")

# Check label distribution for numeric only
numeric_df = df[df['label'].apply(lambda x: isinstance(x, (int, float, np.integer)))]
print(f"\nNumeric label distribution:")
print(numeric_df['label'].value_counts().sort_index())
