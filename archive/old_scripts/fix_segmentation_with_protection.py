"""
Fix word segmentation - Bảo vệ special tokens
Không segment các tokens như <person>, <emo_pos>, </s>, etc.
"""

import pandas as pd
import re
from datetime import datetime
from tqdm import tqdm

print("="*80)
print("🔧 FIXING WORD SEGMENTATION - PROTECTING SPECIAL TOKENS")
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
backup_file = f"backup_before_fixed_segmentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(backup_file, index=False)
print(f"💾 Backup saved: {backup_file}")

# Define special tokens to protect
SPECIAL_TOKENS = [
    '<person>', '<user>', '<org>', '<location>', '<time>',
    '<emo_pos>', '<emo_neg>', '<emo_neutral>',
    '</s>', '<s>'
]

def protect_special_tokens(text):
    """Replace special tokens with placeholders"""
    if pd.isna(text) or text == '':
        return text, {}
    
    text = str(text)
    placeholders = {}
    
    for i, token in enumerate(SPECIAL_TOKENS):
        if token in text:
            placeholder = f"__SPECIAL_TOKEN_{i}__"
            placeholders[placeholder] = token
            text = text.replace(token, placeholder)
    
    return text, placeholders

def restore_special_tokens(text, placeholders):
    """Restore special tokens from placeholders"""
    if pd.isna(text) or text == '':
        return text
    
    text = str(text)
    for placeholder, token in placeholders.items():
        text = text.replace(placeholder, token)
    
    return text

def segment_text_safe(text):
    """Apply word segmentation with special token protection"""
    if pd.isna(text) or text == '':
        return text
    
    try:
        # Step 1: Protect special tokens
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
print(f"\n🔧 Applying SAFE word segmentation to training_text...")
print("   This may take a few minutes...")

tqdm.pandas(desc="Segmenting")
df['training_text_segmented'] = df['training_text'].progress_apply(segment_text_safe)

# Show examples
print(f"\n📊 SEGMENTATION EXAMPLES (with special token protection):")
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
            
            # Check if special tokens are preserved
            for token in SPECIAL_TOKENS:
                if token in str(original):
                    if token in str(segmented):
                        print(f"   ✅ {token} preserved")
                    else:
                        print(f"   ❌ {token} BROKEN!")
            
            example_count += 1
            if example_count >= 5:
                break

# Replace training_text with segmented version
df['training_text_original'] = df['training_text']  # Keep original
df['training_text'] = df['training_text_segmented']
df.drop('training_text_segmented', axis=1, inplace=True)

# Verify special tokens are intact
print(f"\n🔍 VERIFYING SPECIAL TOKENS...")
for token in SPECIAL_TOKENS:
    original_count = df['training_text_original'].fillna('').astype(str).str.count(re.escape(token)).sum()
    segmented_count = df['training_text'].fillna('').astype(str).str.count(re.escape(token)).sum()
    
    if original_count > 0:
        if original_count == segmented_count:
            print(f"   ✅ {token}: {original_count} occurrences preserved")
        else:
            print(f"   ⚠️ {token}: {original_count} → {segmented_count} (MISMATCH!)")

# Save
output_file = "final_train_data_v3_SEGMENTED_FIXED.xlsx"
df.to_excel(output_file, index=False)
print(f"\n💾 Saved: {output_file}")

# Also save as CSV
csv_file = "final_train_data_v3_SEGMENTED_FIXED.csv"
df.to_csv(csv_file, index=False)
print(f"💾 Saved: {csv_file}")

# Statistics
df['underscore_count'] = df['training_text'].fillna('').astype(str).str.count('_')
total_underscores = df['underscore_count'].sum()

print("\n" + "="*80)
print("✅ SAFE WORD SEGMENTATION COMPLETE!")
print("="*80)
print(f"\n📊 STATISTICS:")
print(f"   Total compound words: {total_underscores}")
print(f"   Avg compound words per text: {total_underscores/len(df):.2f}")
print(f"\n📁 OUTPUT FILES:")
print(f"   1. {backup_file} (backup)")
print(f"   2. {output_file} (segmented Excel with protected tokens)")
print(f"   3. {csv_file} (segmented CSV)")
print(f"\n🎯 Use {output_file} for training on Kaggle!")
print(f"   Special tokens are now PROTECTED! ✅")
