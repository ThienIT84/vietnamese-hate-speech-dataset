"""
Script để áp dụng word segmentation cho training data
Sử dụng underthesea để segment text trước khi train PhoBERT
"""

import pandas as pd
from datetime import datetime
from tqdm import tqdm

print("="*80)
print("🔧 APPLYING WORD SEGMENTATION TO TRAINING DATA")
print("="*80)

# Install underthesea nếu chưa có
print("\n📦 Installing underthesea...")
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
backup_file = f"backup_before_segmentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(backup_file, index=False)
print(f"💾 Backup saved: {backup_file}")

# Apply word segmentation
print(f"\n🔧 Applying word segmentation to training_text...")
print("   This may take a few minutes...")

def segment_text(text):
    """Apply word segmentation using underthesea"""
    if pd.isna(text) or text == '':
        return text
    try:
        # word_tokenize returns list of words with underscores for compounds
        # Example: "học sinh" → ["học_sinh"]
        segmented = word_tokenize(str(text), format="text")
        return segmented
    except Exception as e:
        print(f"⚠️ Error segmenting: {text[:50]}... | Error: {e}")
        return text

# Apply segmentation with progress bar
tqdm.pandas(desc="Segmenting")
df['training_text_segmented'] = df['training_text'].progress_apply(segment_text)

# Show examples
print(f"\n📊 SEGMENTATION EXAMPLES:")
print("="*80)
for i in range(min(5, len(df))):
    original = df.iloc[i]['training_text']
    segmented = df.iloc[i]['training_text_segmented']
    if original != segmented:
        print(f"\n{i+1}. ORIGINAL:")
        print(f"   {original[:100]}...")
        print(f"   SEGMENTED:")
        print(f"   {segmented[:100]}...")

# Replace training_text with segmented version
df['training_text_original'] = df['training_text']  # Keep original
df['training_text'] = df['training_text_segmented']
df.drop('training_text_segmented', axis=1, inplace=True)

# Save
output_file = "final_train_data_v3_SEGMENTED.xlsx"
df.to_excel(output_file, index=False)
print(f"\n💾 Saved: {output_file}")

# Also save as CSV
csv_file = "final_train_data_v3_SEGMENTED.csv"
df.to_csv(csv_file, index=False)
print(f"💾 Saved: {csv_file}")

print("\n" + "="*80)
print("✅ WORD SEGMENTATION COMPLETE!")
print("="*80)
print(f"\n📁 OUTPUT FILES:")
print(f"   1. {backup_file} (backup)")
print(f"   2. {output_file} (segmented Excel)")
print(f"   3. {csv_file} (segmented CSV)")
print(f"\n🎯 Use {output_file} for training on Kaggle!")
