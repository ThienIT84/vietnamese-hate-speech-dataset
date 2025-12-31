"""
Deep check for training issues
"""
import pandas as pd

print("="*60)
print("DEEP CHECK FOR TRAINING ISSUES")
print("="*60)

df = pd.read_excel('data/final/final_train_data_v3_SEMANTIC.xlsx')

# 1. Check if same text has different labels
print("\n1. DUPLICATE TEXTS WITH DIFFERENT LABELS:")
text_label_groups = df.groupby('training_text')['label'].nunique()
conflicting = text_label_groups[text_label_groups > 1]
print(f"   Texts with multiple labels: {len(conflicting)}")

if len(conflicting) > 0:
    for text in conflicting.index[:5]:
        labels = df[df['training_text'] == text]['label'].unique()
        print(f"\n   Text: {text[:100]}...")
        print(f"   Labels: {labels}")

# 2. Check label 0 samples more carefully
print("\n" + "="*60)
print("2. LABEL 0 (CLEAN) SAMPLES - DETAILED CHECK")
print("="*60)

clean_samples = df[df['label'] == 0].head(20)
for i, row in clean_samples.iterrows():
    text = row['training_text']
    # Extract comment part (after <sep>)
    if '<sep>' in text:
        parts = text.split('<sep>')
        comment = parts[1].strip() if len(parts) > 1 else text
    else:
        comment = text
    
    print(f"\n[{i}] Comment: {comment[:100]}...")

# 3. Check if labels are consistent with content
print("\n" + "="*60)
print("3. LABEL CONSISTENCY CHECK")
print("="*60)

# Words that should indicate toxic/hate
toxic_indicators = ['ngu', 'đm', 'vcl', 'vl', 'cc', 'đéo', 'địt', 'lồn', 'cặc', 'đĩ', 'khốn', 'chó', 'mẹ mày', 'thằng chó', 'con chó']
hate_indicators = ['giết', 'chết đi', 'cắt lưỡi', 'trời đánh', 'đánh chết', 'xử', 'bắn']

# Check clean samples
clean_df = df[df['label'] == 0]
clean_with_toxic = 0
clean_with_hate = 0

for _, row in clean_df.iterrows():
    text = row['training_text'].lower()
    if any(w in text for w in toxic_indicators):
        clean_with_toxic += 1
    if any(w in text for w in hate_indicators):
        clean_with_hate += 1

print(f"Clean samples with toxic words: {clean_with_toxic}/{len(clean_df)} ({100*clean_with_toxic/len(clean_df):.1f}%)")
print(f"Clean samples with hate words: {clean_with_hate}/{len(clean_df)} ({100*clean_with_hate/len(clean_df):.1f}%)")

# 4. Check if the issue is with the TITLE part being labeled
print("\n" + "="*60)
print("4. TITLE VS COMMENT ANALYSIS")
print("="*60)

# The format is: [TITLE] <sep> [COMMENT]
# Labels should be based on COMMENT, not TITLE

for label in [0, 1, 2]:
    label_name = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}[label]
    samples = df[df['label'] == label].head(5)
    
    print(f"\n--- Label {label} ({label_name}) ---")
    for _, row in samples.iterrows():
        text = row['training_text']
        if '<sep>' in text:
            parts = text.split('<sep>')
            title = parts[0].strip()[:50]
            comment = parts[1].strip()[:50] if len(parts) > 1 else "N/A"
        else:
            title = "N/A"
            comment = text[:50]
        
        print(f"  Title: {title}...")
        print(f"  Comment: {comment}...")
        print()
