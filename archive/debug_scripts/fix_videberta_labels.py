"""
Fix labels in ViDeBERTa training file
Remove text descriptions, keep only numeric labels
"""

import pandas as pd
import numpy as np

print("="*80)
print("🔧 FIXING VIDEBERTA LABELS")
print("="*80)

# Load file
input_file = 'data/final/final_train_data_v3_SEMANTIC.xlsx'
df = pd.read_excel(input_file)

print(f"\n📂 Loaded: {len(df)} samples")
print(f"📂 Columns: {df.columns.tolist()}")

# Check label column
print(f"\n🔍 BEFORE FIX:")
print(f"   Label dtype: {df['label'].dtype}")
print(f"   Unique values: {df['label'].unique()[:15]}")

# Count issues
numeric_labels = df['label'].apply(lambda x: isinstance(x, (int, float, np.integer)))
text_labels = ~numeric_labels

print(f"\n📊 Label types:")
print(f"   Numeric labels: {numeric_labels.sum()}")
print(f"   Text labels: {text_labels.sum()}")

if text_labels.sum() > 0:
    print(f"\n⚠️ Found {text_labels.sum()} rows with text labels!")
    print(f"\n📝 Sample text labels:")
    for i, label in enumerate(df[text_labels]['label'].unique()[:5], 1):
        print(f"   {i}. {label}")
    
    # Remove rows with text labels
    print(f"\n🗑️ Removing rows with text labels...")
    df_clean = df[numeric_labels].copy()
    
    print(f"   Removed: {len(df) - len(df_clean)} rows")
    print(f"   Remaining: {len(df_clean)} rows")
else:
    print(f"\n✅ All labels are numeric!")
    df_clean = df.copy()

# Convert to int
df_clean['label'] = df_clean['label'].astype(int)

# Verify
print(f"\n🔍 AFTER FIX:")
print(f"   Label dtype: {df_clean['label'].dtype}")
print(f"   Unique values: {sorted(df_clean['label'].unique())}")

# Label distribution
print(f"\n📊 LABEL DISTRIBUTION:")
label_counts = df_clean['label'].value_counts().sort_index()
label_names = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}
for label, count in label_counts.items():
    pct = count / len(df_clean) * 100
    print(f"   Label {label} ({label_names.get(label, 'Unknown')}): {count} ({pct:.1f}%)")

# Save
output_file = 'data/final/final_train_data_v3_SEMANTIC.xlsx'
df_clean.to_excel(output_file, index=False)
print(f"\n💾 Saved: {output_file}")
print(f"   Samples: {len(df_clean)}")

# Also save CSV
csv_file = output_file.replace('.xlsx', '.csv')
df_clean.to_csv(csv_file, index=False, encoding='utf-8')
print(f"💾 Saved: {csv_file}")

print("\n" + "="*80)
print("✅ LABELS FIXED!")
print("="*80)
print(f"\n📊 Final dataset:")
print(f"   Samples: {len(df_clean)}")
print(f"   Labels: {sorted(df_clean['label'].unique())}")
print(f"   Ready for ViDeBERTa training!")
