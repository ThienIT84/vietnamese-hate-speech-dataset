"""
Compare labels between PhoBERT and ViDeBERTa files
"""
import pandas as pd

print("="*60)
print("COMPARING LABELS")
print("="*60)

# Load both files
phobert_file = 'data/final/final_train_data_v3_READY.xlsx'
videberta_file = 'data/final/final_train_data_v3_SEMANTIC.xlsx'

df_phobert = pd.read_excel(phobert_file)
df_videberta = pd.read_excel(videberta_file)

print(f"\nPhoBERT file: {len(df_phobert)} samples")
print(f"ViDeBERTa file: {len(df_videberta)} samples")

print(f"\nPhoBERT columns: {list(df_phobert.columns)}")
print(f"ViDeBERTa columns: {list(df_videberta.columns)}")

print(f"\nPhoBERT label distribution:")
print(df_phobert['label'].value_counts().sort_index())

print(f"\nViDeBERTa label distribution:")
print(df_videberta['label'].value_counts().sort_index())

# Check if labels match
print(f"\n" + "="*60)
print("LABEL COMPARISON")
print("="*60)

# Compare first 10 samples
print("\nFirst 10 samples comparison:")
for i in range(min(10, len(df_phobert), len(df_videberta))):
    phobert_label = df_phobert.iloc[i]['label']
    videberta_label = df_videberta.iloc[i]['label']
    match = "✅" if phobert_label == videberta_label else "❌"
    print(f"{i}: PhoBERT={phobert_label}, ViDeBERTa={videberta_label} {match}")

# Check PhoBERT sample texts
print(f"\n" + "="*60)
print("PHOBERT SAMPLES (to verify labels)")
print("="*60)

text_col = 'training_text' if 'training_text' in df_phobert.columns else df_phobert.columns[0]

for label in [0, 1, 2]:
    label_name = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}[label]
    samples = df_phobert[df_phobert['label'] == label].head(3)
    print(f"\n--- Label {label} ({label_name}) ---")
    for i, row in samples.iterrows():
        text = row[text_col]
        print(f"[{i}]: {str(text)[:150]}...")
