"""
Check if labels are correct
"""
import pandas as pd

df = pd.read_excel('data/final/final_train_data_v3_SEMANTIC.xlsx')

print("="*60)
print("CHECKING LABEL QUALITY")
print("="*60)

# Check samples for each label
for label in [0, 1, 2]:
    label_name = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}[label]
    samples = df[df['label'] == label].head(10)
    
    print(f"\n{'='*60}")
    print(f"LABEL {label} ({label_name}) - First 10 samples:")
    print(f"{'='*60}")
    
    for i, row in samples.iterrows():
        text = row['training_text']
        # Check for toxic words
        toxic_words = ['ngu', 'đm', 'vcl', 'vl', 'cc', 'đéo', 'mẹ', 'địt', 'chó', 'lồn', 'cặc', 'đĩ', 'khốn']
        has_toxic = any(w in text.lower() for w in toxic_words)
        
        print(f"\n[{i}] {'⚠️ HAS TOXIC WORDS' if has_toxic else '✅ Clean'}:")
        print(f"    {text[:200]}...")

# Count potential mislabels
print(f"\n{'='*60}")
print("POTENTIAL MISLABELS")
print(f"{'='*60}")

toxic_words = ['ngu', 'đm', 'vcl', 'vl', 'cc', 'đéo', 'mẹ mày', 'địt', 'chó', 'lồn', 'cặc', 'đĩ', 'khốn', 'óc chó', 'thằng', 'con']

# Clean samples with toxic words
clean_with_toxic = df[df['label'] == 0]['training_text'].apply(
    lambda x: any(w in x.lower() for w in toxic_words)
).sum()
print(f"Clean (0) samples with toxic words: {clean_with_toxic}")

# Toxic/Hate samples without toxic words
toxic_without = df[df['label'].isin([1, 2])]['training_text'].apply(
    lambda x: not any(w in x.lower() for w in toxic_words)
).sum()
print(f"Toxic/Hate (1,2) samples without toxic words: {toxic_without}")
