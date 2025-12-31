"""
Script để kiểm tra và làm sạch file final_train_data_v3_TRUNCATED_20251229.xlsx
1. Kiểm tra độ dài post_title
2. Xử lý trùng lặp
3. Kiểm tra null trong training_text và label
4. Cắt bớt post_title nếu quá dài
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*80)
print("🔍 CHECKING & CLEANING FINAL TRAINING DATA")
print("="*80)

# Load data
file_path = "final_train_data_v3_TRUNCATED_20251229.xlsx"
print(f"\n📂 Loading: {file_path}")

df = pd.read_excel(file_path)
print(f"✅ Loaded: {len(df)} rows, {len(df.columns)} columns")
print(f"📋 Columns: {df.columns.tolist()}")

# Backup
backup_file = f"backup_before_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(backup_file, index=False)
print(f"\n💾 Backup saved: {backup_file}")

# ============================================================================
# 1. KIỂM TRA POST_TITLE
# ============================================================================
print("\n" + "="*80)
print("1️⃣ CHECKING POST_TITLE LENGTH")
print("="*80)

if 'post_title' in df.columns:
    df['post_title_length'] = df['post_title'].fillna('').astype(str).str.split().str.len()
    
    print(f"\n📊 POST_TITLE STATISTICS:")
    print(f"   Mean length: {df['post_title_length'].mean():.1f} words")
    print(f"   Max length: {df['post_title_length'].max()} words")
    print(f"   Min length: {df['post_title_length'].min()} words")
    print(f"   Median: {df['post_title_length'].median():.1f} words")
    
    # Tìm các post_title quá dài (>50 words)
    long_titles = df[df['post_title_length'] > 50]
    print(f"\n⚠️ Post titles > 50 words: {len(long_titles)}")
    
    if len(long_titles) > 0:
        print(f"\n🔪 TRUNCATING LONG POST_TITLES...")
        # Cắt post_title xuống 50 words
        def truncate_text(text, max_words=50):
            if pd.isna(text):
                return text
            words = str(text).split()
            if len(words) > max_words:
                return ' '.join(words[:max_words])
            return text
        
        df['post_title'] = df['post_title'].apply(lambda x: truncate_text(x, 50))
        print(f"✅ Truncated {len(long_titles)} post_titles to 50 words")
        
        # Recalculate
        df['post_title_length'] = df['post_title'].fillna('').astype(str).str.split().str.len()
        print(f"✅ New max length: {df['post_title_length'].max()} words")
    
    # Drop temp column
    df.drop('post_title_length', axis=1, inplace=True)
else:
    print("⚠️ Column 'post_title' not found!")

# ============================================================================
# 2. KIỂM TRA TRAINING_TEXT LENGTH
# ============================================================================
print("\n" + "="*80)
print("2️⃣ CHECKING TRAINING_TEXT LENGTH")
print("="*80)

# Define truncate function
def truncate_text(text, max_words=50):
    if pd.isna(text):
        return text
    words = str(text).split()
    if len(words) > max_words:
        return ' '.join(words[:max_words])
    return text

if 'training_text' in df.columns:
    df['training_text_length'] = df['training_text'].fillna('').astype(str).str.split().str.len()
    
    print(f"\n📊 TRAINING_TEXT STATISTICS:")
    print(f"   Mean length: {df['training_text_length'].mean():.1f} words")
    print(f"   Max length: {df['training_text_length'].max()} words")
    print(f"   Min length: {df['training_text_length'].min()} words")
    print(f"   Median: {df['training_text_length'].median():.1f} words")
    
    # PhoBERT max = 256 tokens ≈ 200 words (safe limit)
    long_texts = df[df['training_text_length'] > 200]
    print(f"\n⚠️ Training texts > 200 words: {len(long_texts)}")
    
    if len(long_texts) > 0:
        print(f"\n🔪 TRUNCATING LONG TRAINING_TEXTS...")
        df['training_text'] = df['training_text'].apply(lambda x: truncate_text(x, 200))
        print(f"✅ Truncated {len(long_texts)} training_texts to 200 words")
        
        # Recalculate
        df['training_text_length'] = df['training_text'].fillna('').astype(str).str.split().str.len()
        print(f"✅ New max length: {df['training_text_length'].max()} words")
    
    # Drop temp column
    df.drop('training_text_length', axis=1, inplace=True)
else:
    print("⚠️ Column 'training_text' not found!")

# ============================================================================
# 3. KIỂM TRA NULL VALUES
# ============================================================================
print("\n" + "="*80)
print("3️⃣ CHECKING NULL VALUES")
print("="*80)

print(f"\n📊 NULL VALUES BY COLUMN:")
null_counts = df.isnull().sum()
for col, count in null_counts.items():
    if count > 0:
        print(f"   {col}: {count} nulls ({count/len(df)*100:.1f}%)")

# Kiểm tra training_text và label
critical_nulls = []

if 'training_text' in df.columns:
    training_text_nulls = df['training_text'].isnull().sum()
    print(f"\n⚠️ training_text nulls: {training_text_nulls}")
    if training_text_nulls > 0:
        critical_nulls.append('training_text')

if 'label' in df.columns:
    label_nulls = df['label'].isnull().sum()
    print(f"⚠️ label nulls: {label_nulls}")
    if label_nulls > 0:
        critical_nulls.append('label')

if critical_nulls:
    print(f"\n🗑️ REMOVING ROWS WITH NULL training_text OR label...")
    before_len = len(df)
    df = df.dropna(subset=['training_text', 'label'])
    after_len = len(df)
    print(f"✅ Removed {before_len - after_len} rows with critical nulls")
else:
    print(f"\n✅ No critical nulls found!")

# ============================================================================
# 4. KIỂM TRA TRÙNG LẶP
# ============================================================================
print("\n" + "="*80)
print("4️⃣ CHECKING DUPLICATES")
print("="*80)

# Kiểm tra trùng lặp theo training_text
if 'training_text' in df.columns:
    duplicates = df.duplicated(subset=['training_text'], keep=False)
    dup_count = duplicates.sum()
    
    print(f"\n📊 DUPLICATE STATISTICS:")
    print(f"   Total duplicates: {dup_count} rows")
    print(f"   Unique duplicates: {df[duplicates]['training_text'].nunique()} texts")
    
    if dup_count > 0:
        print(f"\n🗑️ REMOVING DUPLICATES (keeping first occurrence)...")
        before_len = len(df)
        df = df.drop_duplicates(subset=['training_text'], keep='first')
        after_len = len(df)
        print(f"✅ Removed {before_len - after_len} duplicate rows")
    else:
        print(f"\n✅ No duplicates found!")
else:
    print("⚠️ Column 'training_text' not found!")

# ============================================================================
# 5. FINAL STATISTICS
# ============================================================================
print("\n" + "="*80)
print("5️⃣ FINAL STATISTICS")
print("="*80)

print(f"\n📊 FINAL DATASET:")
print(f"   Total rows: {len(df)}")
print(f"   Total columns: {len(df.columns)}")

if 'label' in df.columns:
    print(f"\n📊 LABEL DISTRIBUTION:")
    label_counts = df['label'].value_counts().sort_index()
    label_names = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}
    for label, count in label_counts.items():
        pct = count / len(df) * 100
        print(f"   Label {int(label)} ({label_names.get(int(label), 'Unknown')}): {count} ({pct:.1f}%)")
    
    # Balance ratio
    balance_ratio = label_counts.max() / label_counts.min()
    print(f"\n⚖️ Balance ratio: {balance_ratio:.2f}x")

# ============================================================================
# 6. SAVE CLEANED DATA
# ============================================================================
print("\n" + "="*80)
print("6️⃣ SAVING CLEANED DATA")
print("="*80)

output_file = "final_train_data_v3_CLEANED.xlsx"
df.to_excel(output_file, index=False)
print(f"\n💾 Saved: {output_file}")
print(f"   Rows: {len(df)}")
print(f"   Size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

# Also save as CSV for faster loading
csv_file = "final_train_data_v3_CLEANED.csv"
df.to_csv(csv_file, index=False)
print(f"💾 Saved: {csv_file}")

print("\n" + "="*80)
print("✅ CLEANING COMPLETE!")
print("="*80)
print(f"\n📁 OUTPUT FILES:")
print(f"   1. {backup_file} (backup)")
print(f"   2. {output_file} (cleaned Excel)")
print(f"   3. {csv_file} (cleaned CSV)")
