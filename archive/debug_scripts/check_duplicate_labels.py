"""
Check for duplicate texts with different labels
"""

import pandas as pd

df = pd.read_excel('data/final/final_train_data_v3_SEMANTIC.xlsx')

print("="*60)
print("CHECKING FOR DUPLICATE TEXTS WITH DIFFERENT LABELS")
print("="*60)

# Normalize text (lowercase, strip)
df['text_normalized'] = df['training_text'].str.lower().str.strip()

# Find duplicates
duplicates = df[df.duplicated(subset=['text_normalized'], keep=False)]

if len(duplicates) > 0:
    print(f"\n⚠️ Found {len(duplicates)} duplicate texts!")
    
    # Group by normalized text
    grouped = duplicates.groupby('text_normalized')
    
    conflicts = 0
    for text, group in grouped:
        unique_labels = group['label'].unique()
        if len(unique_labels) > 1:
            conflicts += 1
            if conflicts <= 5:  # Show first 5 conflicts
                print(f"\n❌ CONFLICT #{conflicts}:")
                print(f"Text: {text[:100]}...")
                print(f"Labels: {sorted(unique_labels)}")
                print(f"Counts: {group['label'].value_counts().to_dict()}")
    
    print(f"\n📊 Total conflicts: {conflicts} texts with multiple labels")
    print(f"   This explains why F1 is low - model is confused!")
    
    # Recommendation
    print("\n" + "="*60)
    print("RECOMMENDED FIXES")
    print("="*60)
    print("1. Remove exact duplicates, keep majority label")
    print("2. Or: Manual review to fix incorrect labels")
    print("3. Or: Remove all conflicting samples")
    
else:
    print("\n✅ No duplicate texts found")

# Check case-sensitive duplicates
print("\n" + "="*60)
print("CASE-SENSITIVE DUPLICATES")
print("="*60)

exact_duplicates = df[df.duplicated(subset=['training_text'], keep=False)]
if len(exact_duplicates) > 0:
    print(f"Found {len(exact_duplicates)} exact duplicates")
else:
    print("✅ No exact duplicates")
