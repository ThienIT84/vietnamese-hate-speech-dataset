"""
Fix word segmentation FINAL - Bảo vệ special tokens với SPACE
Đảm bảo không có token nào bị nối với từ khác
"""

import pandas as pd
import re
from datetime import datetime
from tqdm import tqdm

print("="*80)
print("🔧 FINAL FIX: WORD SEGMENTATION WITH SPACE PROTECTION")
print("="*80)

# Install underthesea nếu chưa có
print("\n📦 Checking underthesea...")
try:
    from underthesea import word_tokenize
    print("✅ underthesea available!")
except:
    print("📦 Installing underthesea...")
    import subprocess
    subprocess.run(['pip', 'install', 'underthesea', '-q'], check=True)
    from underthesea import word_tokenize
    print("✅ underthesea installed!")

# Load data
file_path = "final_train_data_v3_CLEANED.xlsx"
print(f"\n📂 Loading: {file_path}")

df = pd.read_excel(file_path)
print(f"✅ Loaded: {len(df)} rows")

# Backup
backup_file = f"backup_before_final_segmentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(backup_file, index=False)
print(f"💾 Backup saved: {backup_file}")

# Define special tokens to protect
SPECIAL_TOKENS = [
    '<person>', '<user>', '<org>', '<location>', '<time>',
    '<emo_pos>', '<emo_neg>', '<emo_neutral>',
    '</s>', '<s>'
]

def protect_special_tokens(text):
    """Replace special tokens with placeholders SURROUNDED BY SPACES"""
    if pd.isna(text) or text == '':
        return text, {}
    
    text = str(text)
    placeholders = {}
    
    for i, token in enumerate(SPECIAL_TOKENS):
        if token in text:
            # Placeholder với spaces để tránh bị nối
            placeholder = f" __TOKEN{i}__ "
            placeholders[placeholder.strip()] = token
            # Replace token và đảm bảo có space xung quanh
            text = text.replace(token, placeholder)
    
    return text, placeholders

def restore_special_tokens(text, placeholders):
    """Restore special tokens from placeholders"""
    if pd.isna(text) or text == '':
        return text
    
    text = str(text)
    for placeholder, token in placeholders.items():
        # Remove underscores nếu có (do segmentation)
        placeholder_variants = [
            placeholder,
            placeholder.replace('_', ' '),  # __TOKEN0__ → __ TOKEN0 __
            f"_{placeholder}_",              # ___TOKEN0___
            f"{placeholder}_",               # __TOKEN0___
            f"_{placeholder}",               # ___TOKEN0__
        ]
        
        for variant in placeholder_variants:
            if variant in text:
                text = text.replace(variant, f" {token} ")
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def segment_text_safe(text):
    """Apply word segmentation with special token protection"""
    if pd.isna(text) or text == '':
        return text
    
    try:
        # Step 1: Protect special tokens (with spaces)
        protected_text, placeholders = protect_special_tokens(text)
        
        # Step 2: Apply word segmentation
        segmented = word_tokenize(protected_text, format="text")
        
        # Step 3: Restore special tokens
        final_text = restore_special_tokens(segmented, placeholders)
        
        return final_text
    except Exception as e:
        print(f"⚠️ Error segmenting: {text[:50]}... | Error: {e}")
        return text

# Apply segmentation with progress bar
print(f"\n🔧 Applying FINAL SAFE word segmentation...")
print("   This may take a few minutes...")

tqdm.pandas(desc="Segmenting")
df['training_text_segmented'] = df['training_text'].progress_apply(segment_text_safe)

# Show examples
print(f"\n📊 SEGMENTATION EXAMPLES:")
print("="*80)

example_count = 0
for i in range(len(df)):
    original = df.iloc[i]['training_text']
    segmented = df.iloc[i]['training_text_segmented']
    
    # Tìm examples có special tokens
    if any(token in str(original) for token in SPECIAL_TOKENS):
        if original != segmented and pd.notna(original) and pd.notna(segmented):
            print(f"\n{example_count+1}. ORIGINAL:")
            print(f"   {str(original)[:120]}")
            print(f"   SEGMENTED:")
            print(f"   {str(segmented)[:120]}")
            
            # Check for concatenation issues
            has_issue = False
            for token in SPECIAL_TOKENS:
                if token in str(original):
                    # Check if token is properly separated
                    if f"{token}_" in str(segmented) or f"_{token}" in str(segmented):
                        print(f"   ❌ {token} CONCATENATED!")
                        has_issue = True
                    elif token in str(segmented):
                        print(f"   ✅ {token} properly separated")
            
            if not has_issue:
                example_count += 1
                if example_count >= 5:
                    break

# Replace training_text with segmented version
df['training_text_original'] = df['training_text']  # Keep original
df['training_text'] = df['training_text_segmented']
df.drop('training_text_segmented', axis=1, inplace=True)

# Verify no concatenation issues
print(f"\n🔍 VERIFYING NO CONCATENATION ISSUES...")

PROBLEMATIC_PATTERNS = [
    (r'</s>_\w+', '</s>_word'),
    (r'<person>_\w+', '<person>_word'),
    (r'<user>_\w+', '<user>_word'),
    (r'<emo_pos>_\w+', '<emo_pos>_word'),
    (r'<emo_neg>_\w+', '<emo_neg>_word'),
    (r'\w+_</s>', 'word_</s>'),
    (r'\w+_<person>', 'word_<person>'),
]

total_issues = 0
for pattern, name in PROBLEMATIC_PATTERNS:
    count = df['training_text'].fillna('').astype(str).str.count(pattern).sum()
    if count > 0:
        print(f"   ❌ {name}: {count} issues")
        total_issues += count
    else:
        print(f"   ✅ {name}: 0 issues")

if total_issues == 0:
    print(f"\n✅ NO CONCATENATION ISSUES FOUND!")
else:
    print(f"\n⚠️ TOTAL ISSUES: {total_issues}")

# Verify special tokens count
print(f"\n🔍 VERIFYING SPECIAL TOKENS COUNT...")
for token in SPECIAL_TOKENS:
    original_count = df['training_text_original'].fillna('').astype(str).str.count(re.escape(token)).sum()
    segmented_count = df['training_text'].fillna('').astype(str).str.count(re.escape(token)).sum()
    
    if original_count > 0:
        if original_count == segmented_count:
            print(f"   ✅ {token}: {original_count} preserved")
        else:
            print(f"   ⚠️ {token}: {original_count} → {segmented_count}")

# Save
output_file = "final_train_data_v3_SEGMENTED_FINAL.xlsx"
df.to_excel(output_file, index=False)
print(f"\n💾 Saved: {output_file}")

# Also save as CSV
csv_file = "final_train_data_v3_SEGMENTED_FINAL.csv"
df.to_csv(csv_file, index=False)
print(f"💾 Saved: {csv_file}")

# Statistics
df['underscore_count'] = df['training_text'].fillna('').astype(str).str.count('_')
total_underscores = df['underscore_count'].sum()

print("\n" + "="*80)
print("✅ FINAL SEGMENTATION COMPLETE!")
print("="*80)
print(f"\n📊 STATISTICS:")
print(f"   Total compound words: {total_underscores}")
print(f"   Avg compound words per text: {total_underscores/len(df):.2f}")
print(f"   Concatenation issues: {total_issues}")
print(f"\n📁 OUTPUT FILES:")
print(f"   1. {backup_file} (backup)")
print(f"   2. {output_file} (FINAL segmented Excel)")
print(f"   3. {csv_file} (FINAL segmented CSV)")
print(f"\n🎯 Use {output_file} for training on Kaggle!")
if total_issues == 0:
    print(f"   ✅ NO concatenation issues! Ready for training!")
else:
    print(f"   ⚠️ Still has {total_issues} issues - needs more fixing")
