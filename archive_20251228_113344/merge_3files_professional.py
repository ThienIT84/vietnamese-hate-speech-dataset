"""
PROFESSIONAL MERGE STRATEGY for 3 labeled files

CHUẨN HÓA:
1. Tạo trường THỐNG NHẤT "training_text" từ:
   - File 1: input_text (đã cleaned)
   - File 2, 3: text (đã cleaned + teencode)
   
2. Giữ CẢ RAW và CLEANED versions để flexibility

3. Metadata đầy đủ: source_file, labeler, confidence, etc.

4. Deduplication thông minh theo training_text

5. Validation: check emoji conversion, label distribution
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import re

print("="*70)
print("PROFESSIONAL 3-FILE MERGE WITH STANDARDIZATION")
print("="*70)

# File paths
file1 = Path("TOXIC_COMMENT/datasets/final/final_1k_processed.csv")
file2 = Path("data/processed/labeling_task_Thien_CLEANED_20251224_181229.csv")
file3 = Path("data/processed/labeling_task_Quang_CLEANED_20251224_182202.csv")

print(f"\n[1/5] Loading files...")

# Load File 1 (final_1k_processed)
df1 = pd.read_csv(file1, encoding='utf-8')
print(f"  File 1 (final_1k_processed): {len(df1)} rows")

# Load File 2 (Thien)
df2 = pd.read_csv(file2, encoding='utf-8-sig')
print(f"  File 2 (Thien cleaned): {len(df2)} rows")

# Load File 3 (Quang)
df3 = pd.read_csv(file3, encoding='utf-8-sig')
print(f"  File 3 (Quang cleaned): {len(df3)} rows")

print(f"\n  Total before merge: {len(df1) + len(df2) + len(df3):,} rows")

# Standardize columns
print(f"\n[2/5] Standardizing columns...")

# File 1: Create training_text from input_text
df1_clean = pd.DataFrame({
    'training_text': df1['input_text'],  # Main field for training
    'text_raw': df1['text'] + ' </s> ' + df1['context'] if 'context' in df1.columns else df1['text'],
    'label': df1['label'],
    'note': df1.get('note', ''),
    'source_file': 'final_1k_processed',
    'labeler': 'Quang',  # Based on file origin
    'has_teencode': False,  # File 1 không có teencode processing
    'confidence': None,
    'sampling_strategy': 'unknown'
})

# File 2: Create training_text from text (already with teencode)
df2_clean = pd.DataFrame({
    'training_text': df2['text'],  # Main field for training
    'text_raw': df2['text_raw'],
    'label': df2['label'],
    'note': df2.get('note', ''),
    'source_file': 'labeling_task_Thien',
    'labeler': df2.get('labeler', 'Thien'),
    'has_teencode': True,  # File 2 đã qua teencode
    'confidence': df2.get('confidence', None),
    'sampling_strategy': df2.get('sampling_strategy', 'unknown')
})

# File 3: Create training_text from text (already with teencode)
df3_clean = pd.DataFrame({
    'training_text': df3['text'],  # Main field for training
    'text_raw': df3['text_raw'],
    'label': df3['label'],
    'note': df3.get('note', ''),
    'source_file': 'labeling_task_Quang',
    'labeler': df3.get('labeler', 'Quang'),
    'has_teencode': True,  # File 3 đã qua teencode
    'confidence': df3.get('confidence', None),
    'sampling_strategy': df3.get('sampling_strategy', 'unknown')
})

print(f"  Standardized File 1: {len(df1_clean)} rows")
print(f"  Standardized File 2: {len(df2_clean)} rows")
print(f"  Standardized File 3: {len(df3_clean)} rows")

# Merge all
print(f"\n[3/5] Merging files...")
merged = pd.concat([df1_clean, df2_clean, df3_clean], ignore_index=True)
print(f"  After concat: {len(merged)} rows")

# Smart deduplication by training_text
print(f"\n[4/5] Smart deduplication...")

def normalize_for_dedup(text):
    """Normalize text for deduplication"""
    if pd.isna(text) or not text:
        return ''
    return str(text).lower().strip()

merged['text_norm'] = merged['training_text'].apply(normalize_for_dedup)

# Keep first occurrence, prioritize by:
# 1. Has teencode (more processed)
# 2. Higher confidence
# 3. More metadata
merged = merged.sort_values(
    by=['has_teencode', 'confidence'],
    ascending=[False, False],
    na_position='last'
)

merged = merged.drop_duplicates(subset=['text_norm'], keep='first')
merged = merged.drop(columns=['text_norm'])

print(f"  After dedup: {len(merged)} rows")
print(f"  Removed: {(len(df1_clean) + len(df2_clean) + len(df3_clean)) - len(merged)} duplicates")

# Validation
print(f"\n[5/5] Validation...")

# Check emoji tags
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    "]+", flags=re.UNICODE)

raw_has_emoji = merged['text_raw'].str.contains(emoji_pattern, na=False).sum()
training_has_emo_tag = merged['training_text'].str.contains('<emo_', na=False).sum()
training_has_person = merged['training_text'].str.contains('<person>', na=False).sum()

print(f"  Emoji in raw: {raw_has_emoji}")
print(f"  <emo_*> tags in training: {training_has_emo_tag}")
print(f"  <person> tags in training: {training_has_person}")

# Label distribution
print(f"\n  Label distribution:")
for label, count in merged['label'].value_counts().sort_index().items():
    pct = 100 * count / len(merged)
    print(f"    Label {int(label)}: {count:,} ({pct:.1f}%)")

# By source file
print(f"\n  By source file:")
for source, count in merged['source_file'].value_counts().items():
    pct = 100 * count / len(merged)
    print(f"    {source}: {count:,} ({pct:.1f}%)")

# By labeler
print(f"\n  By labeler:")
for labeler, count in merged['labeler'].value_counts().items():
    pct = 100 * count / len(merged)
    print(f"    {labeler}: {count:,} ({pct:.1f}%)")

# By teencode processing
print(f"\n  By teencode processing:")
for has_tc, count in merged['has_teencode'].value_counts().items():
    pct = 100 * count / len(merged)
    status = "YES (cleaned + teencode)" if has_tc else "NO (only cleaned)"
    print(f"    {status}: {count:,} ({pct:.1f}%)")

# Save
print(f"\n[SAVE] Saving final merged dataset...")
output_dir = Path("data/processed")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Main file for training
csv_path = output_dir / f"FINAL_MERGED_3FILES_{timestamp}.csv"
merged.to_csv(csv_path, index=False, encoding='utf-8-sig')

# JSON format
json_path = output_dir / f"FINAL_MERGED_3FILES_{timestamp}.json"
json_data = merged.to_dict(orient='records')
import json
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

# Training-only file (chỉ có training_text và label)
training_only = merged[['training_text', 'label']].copy()
training_only.columns = ['text', 'label']  # Rename for standard format
training_csv = output_dir / f"TRAINING_READY_{timestamp}.csv"
training_only.to_csv(training_csv, index=False, encoding='utf-8-sig')

print("\n" + "="*70)
print("MERGE COMPLETE - FILES SAVED")
print("="*70)
print(f"\n1. FULL DATASET (with all metadata):")
print(f"   {csv_path.name}")
print(f"   Columns: {list(merged.columns)}")

print(f"\n2. JSON FORMAT:")
print(f"   {json_path.name}")

print(f"\n3. TRAINING-READY (text + label only):")
print(f"   {training_csv.name}")
print(f"   Columns: ['text', 'label']")

print(f"\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"Total samples: {len(merged):,}")
print(f"Labels: {merged['label'].notna().sum():,}")
print(f"With emoji tags: {training_has_emo_tag:,}")
print(f"With <person>: {training_has_person:,}")
print(f"Teencode processed: {merged['has_teencode'].sum():,}/{len(merged)}")

print("\n✓ TRAINING_TEXT field standardized and ready for model training!")
print("✓ All files preserve original data in text_raw")
print("✓ Deduplication prioritizes teencode-processed versions")
print("="*70)
