"""
Debug ViDeBERTa tokenization to understand why F1 is low
"""

import pandas as pd
from transformers import AutoTokenizer

# Load data
df = pd.read_excel('data/final/final_train_data_v3_SEMANTIC.xlsx')
print(f"Total samples: {len(df)}")
print(f"Label distribution:\n{df['label'].value_counts().sort_index()}\n")

# Load tokenizers
print("="*60)
print("COMPARING TOKENIZERS")
print("="*60)

phobert_tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
videberta_tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")

# Test sample
sample = df['training_text'].iloc[0]
print(f"\nSample text:\n{sample}\n")

# Split by <sep>
if "<sep>" in sample:
    parts = sample.split("<sep>", 1)
    title = parts[0].strip()
    comment = parts[1].strip()
    
    print(f"Title: {title}")
    print(f"Comment: {comment}\n")
    
    # PhoBERT tokenization (single text)
    print("="*60)
    print("PHOBERT (Single Text)")
    print("="*60)
    phobert_tokens = phobert_tokenizer(sample, max_length=256, truncation=True)
    print(f"Input IDs length: {len(phobert_tokens['input_ids'])}")
    print(f"Token type IDs: {phobert_tokens['token_type_ids'][:20]}...")
    print(f"Decoded: {phobert_tokenizer.decode(phobert_tokens['input_ids'][:50])}\n")
    
    # ViDeBERTa tokenization (single text)
    print("="*60)
    print("VIDEBERTA (Single Text)")
    print("="*60)
    videberta_single = videberta_tokenizer(sample, max_length=256, truncation=True)
    print(f"Input IDs length: {len(videberta_single['input_ids'])}")
    print(f"Token type IDs: {videberta_single['token_type_ids'][:20]}...")
    print(f"Decoded: {videberta_tokenizer.decode(videberta_single['input_ids'][:50])}\n")
    
    # ViDeBERTa tokenization (text_pair)
    print("="*60)
    print("VIDEBERTA (Text Pair)")
    print("="*60)
    videberta_pair = videberta_tokenizer(
        text=title, 
        text_pair=comment, 
        max_length=256, 
        truncation=True
    )
    print(f"Input IDs length: {len(videberta_pair['input_ids'])}")
    print(f"Token type IDs: {videberta_pair['token_type_ids'][:20]}...")
    print(f"Decoded: {videberta_tokenizer.decode(videberta_pair['input_ids'][:50])}\n")
    
    # Compare token_type_ids
    print("="*60)
    print("TOKEN TYPE IDS COMPARISON")
    print("="*60)
    print(f"PhoBERT (single):   All 0s? {all(t == 0 for t in phobert_tokens['token_type_ids'])}")
    print(f"ViDeBERTa (single): All 0s? {all(t == 0 for t in videberta_single['token_type_ids'])}")
    print(f"ViDeBERTa (pair):   Has 1s? {any(t == 1 for t in videberta_pair['token_type_ids'])}")
    
    # Count 0s and 1s in text_pair
    type_ids = videberta_pair['token_type_ids']
    count_0 = sum(1 for t in type_ids if t == 0)
    count_1 = sum(1 for t in type_ids if t == 1)
    print(f"\nViDeBERTa (pair) token types:")
    print(f"  Type 0 (title): {count_0} tokens")
    print(f"  Type 1 (comment): {count_1} tokens")

# Check label distribution by text length
print("\n" + "="*60)
print("LABEL DISTRIBUTION BY TEXT LENGTH")
print("="*60)

df['text_length'] = df['training_text'].str.len()
df['has_sep'] = df['training_text'].str.contains('<sep>')

print("\nWith <sep>:")
print(df[df['has_sep']]['label'].value_counts().sort_index())

print("\nWithout <sep>:")
print(df[~df['has_sep']]['label'].value_counts().sort_index())

print("\nAverage text length by label:")
for label in [0, 1, 2]:
    avg_len = df[df['label'] == label]['text_length'].mean()
    print(f"  Label {label}: {avg_len:.0f} chars")

# Check if labels are balanced
print("\n" + "="*60)
print("LABEL BALANCE CHECK")
print("="*60)
label_counts = df['label'].value_counts().sort_index()
max_count = label_counts.max()
min_count = label_counts.min()
imbalance_ratio = max_count / min_count
print(f"Imbalance ratio: {imbalance_ratio:.2f}x")
if imbalance_ratio > 2:
    print("⚠️ WARNING: Significant class imbalance! Consider using class weights.")
else:
    print("✅ Classes are relatively balanced")

# Sample some texts from each label
print("\n" + "="*60)
print("SAMPLE TEXTS BY LABEL")
print("="*60)
for label in [0, 1, 2]:
    print(f"\nLabel {label} samples:")
    samples = df[df['label'] == label]['training_text'].head(3)
    for i, text in enumerate(samples, 1):
        print(f"  {i}. {text[:100]}...")
