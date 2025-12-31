"""
Debug training issues
"""
import pandas as pd
from transformers import AutoTokenizer

print("="*60)
print("DEBUG TRAINING ISSUES")
print("="*60)

# 1. Load data
df = pd.read_excel('data/final/final_train_data_v3_SEMANTIC.xlsx')
print(f"\n1. DATA LOADED: {len(df)} samples")

# 2. Check tokenizer
print(f"\n2. TOKENIZER CHECK:")
tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")
print(f"   Original vocab size: {tokenizer.vocab_size}")

# Add special tokens
special_tokens = ['<sep>', '<emo_pos>', '<emo_neg>', '<person>', '<user>']
num_added = tokenizer.add_special_tokens({'additional_special_tokens': special_tokens})
print(f"   Added {num_added} special tokens")
print(f"   New vocab size: {len(tokenizer)}")

# 3. Check if special tokens are recognized
print(f"\n3. SPECIAL TOKEN RECOGNITION:")
for token in special_tokens:
    token_id = tokenizer.convert_tokens_to_ids(token)
    print(f"   {token}: ID = {token_id}")

# 4. Test tokenization
print(f"\n4. TOKENIZATION TEST:")
sample_text = df.iloc[0]['training_text']
print(f"   Sample: {sample_text[:100]}...")

tokens = tokenizer.tokenize(sample_text)
print(f"   Tokens (first 20): {tokens[:20]}")

# Check if <sep> is tokenized correctly
if '<sep>' in sample_text:
    if '<sep>' in tokens:
        print(f"   ✅ <sep> tokenized as single token")
    else:
        print(f"   ❌ <sep> NOT tokenized correctly!")
        # Find how it was tokenized
        for i, t in enumerate(tokens):
            if 'sep' in t.lower() or '<' in t:
                print(f"      Found: {tokens[max(0,i-2):i+3]}")

# 5. Check encoding
print(f"\n5. ENCODING TEST:")
encoded = tokenizer(sample_text, max_length=256, truncation=True, padding='max_length')
print(f"   Input IDs length: {len(encoded['input_ids'])}")
print(f"   First 20 IDs: {encoded['input_ids'][:20]}")

# Decode back
decoded = tokenizer.decode(encoded['input_ids'][:50])
print(f"   Decoded (first 50 tokens): {decoded}")

# 6. Check label distribution in sample
print(f"\n6. LABEL DISTRIBUTION:")
print(df['label'].value_counts().sort_index())

# 7. Check for data leakage or issues
print(f"\n7. DATA QUALITY:")
print(f"   Duplicate texts: {df['training_text'].duplicated().sum()}")
print(f"   Empty texts: {(df['training_text'].str.len() == 0).sum()}")
print(f"   Very short texts (<10 chars): {(df['training_text'].str.len() < 10).sum()}")

# 8. Check text samples per label
print(f"\n8. SAMPLES PER LABEL:")
for label in [0, 1, 2]:
    sample = df[df['label'] == label].iloc[0]['training_text']
    print(f"\n   Label {label}:")
    print(f"   {sample[:150]}...")
