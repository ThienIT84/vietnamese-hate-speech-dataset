"""
Script xử lý unlabeled_data_for_labeling.csv:
1. Xử lý teencode cho raw_comment và raw_title
2. Gộp theo format PhoBERT: title </s> comment
3. Loại bỏ trùng lặp với final_train_data_v2.csv
"""

import pandas as pd
import sys
import os
from datetime import datetime

# Import advanced cleaning
sys.path.append('src/preprocessing')
from advanced_text_cleaning import advanced_clean_text

print("="*80)
print("🔥 PROCESSING UNLABELED DATA FOR TRAINING")
print("="*80)

# ============================================================
# 1. LOAD DATA
# ============================================================

print("\n📂 Loading data...")
unlabeled_path = r"data\interim\unlabeled_data_for_labeling.csv"
labeled_path = r"final_train_data_v2.csv"

df_unlabeled = pd.read_csv(unlabeled_path, encoding='utf-8')
df_labeled = pd.read_csv(labeled_path, encoding='utf-8')

print(f"✅ Unlabeled data: {len(df_unlabeled)} rows")
print(f"✅ Labeled data: {len(df_labeled)} rows")

# ============================================================
# 2. PROCESS UNLABELED DATA
# ============================================================

print("\n🔄 Processing unlabeled data...")
print("   - Cleaning raw_comment and raw_title")
print("   - Applying teencode normalization")
print("   - Creating training_text format")

processed_data = []

for idx, row in df_unlabeled.iterrows():
    if idx % 10000 == 0:
        print(f"   Progress: {idx}/{len(df_unlabeled)}")
    
    # Get raw text
    raw_comment = str(row.get('raw_comment', ''))
    raw_title = str(row.get('raw_title', ''))
    
    # Skip if both empty
    if not raw_comment.strip() and not raw_title.strip():
        continue
    
    # Clean comment and title using advanced_clean_text
    cleaned_comment = advanced_clean_text(raw_comment) if raw_comment.strip() else ''
    cleaned_title = advanced_clean_text(raw_title) if raw_title.strip() else ''
    
    # Create training_text format: title </s> comment
    if cleaned_title and cleaned_comment:
        training_text = f"{cleaned_title} </s> {cleaned_comment}"
    elif cleaned_title:
        training_text = cleaned_title
    elif cleaned_comment:
        training_text = cleaned_comment
    else:
        continue
    
    # Store processed data
    processed_data.append({
        'training_text': training_text,
        'raw_comment': raw_comment,
        'raw_title': raw_title,
        'cleaned_comment': cleaned_comment,
        'cleaned_title': cleaned_title,
        'source_platform': row.get('source_platform', ''),
        'id': row.get('id', ''),
        'timestamp': row.get('timestamp', ''),
        'username': row.get('username', ''),
        'topic': row.get('topic', '')
    })

df_processed = pd.DataFrame(processed_data)
print(f"\n✅ Processed: {len(df_processed)} rows")

# ============================================================
# 3. REMOVE DUPLICATES WITH LABELED DATA
# ============================================================

print("\n🔍 Removing duplicates with labeled data...")

# Get training_text from labeled data
labeled_texts = set(df_labeled['training_text'].astype(str).str.strip().str.lower())
print(f"   Labeled unique texts: {len(labeled_texts)}")

# Filter out duplicates
df_processed['training_text_lower'] = df_processed['training_text'].str.strip().str.lower()
df_unique = df_processed[~df_processed['training_text_lower'].isin(labeled_texts)].copy()
df_unique = df_unique.drop(columns=['training_text_lower'])

print(f"   Duplicates found: {len(df_processed) - len(df_unique)}")
print(f"✅ Unique unlabeled data: {len(df_unique)} rows")

# ============================================================
# 4. REMOVE INTERNAL DUPLICATES
# ============================================================

print("\n🔍 Removing internal duplicates...")
before_dedup = len(df_unique)
df_unique = df_unique.drop_duplicates(subset=['training_text'], keep='first')
print(f"   Internal duplicates removed: {before_dedup - len(df_unique)}")
print(f"✅ Final unique data: {len(df_unique)} rows")

# ============================================================
# 5. SAVE RESULTS
# ============================================================

print("\n💾 Saving results...")

# Save full processed data
output_path = f"unlabeled_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df_unique.to_csv(output_path, index=False, encoding='utf-8')
print(f"✅ Saved to: {output_path}")

# Save training-ready format (only training_text column)
training_ready_path = f"unlabeled_training_ready_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df_training = df_unique[['training_text']].copy()
df_training.to_csv(training_ready_path, index=False, encoding='utf-8')
print(f"✅ Training-ready saved to: {training_ready_path}")

# ============================================================
# 6. STATISTICS
# ============================================================

print("\n" + "="*80)
print("📊 PROCESSING SUMMARY")
print("="*80)
print(f"Original unlabeled data:        {len(df_unlabeled):,}")
print(f"After processing:               {len(df_processed):,}")
print(f"Duplicates with labeled data:   {len(df_processed) - len(df_unique):,}")
print(f"Final unique unlabeled data:    {len(df_unique):,}")
print(f"\nLabeled data (existing):        {len(df_labeled):,}")
print(f"New unlabeled data (unique):    {len(df_unique):,}")
print(f"Total potential training data:  {len(df_labeled) + len(df_unique):,}")

# Sample output
print("\n📝 Sample processed data:")
print("-" * 80)
for i in range(min(3, len(df_unique))):
    row = df_unique.iloc[i]
    print(f"\nSample {i+1}:")
    print(f"Training text: {row['training_text'][:150]}...")
    print(f"Source: {row['source_platform']}")

print("\n" + "="*80)
print("✅ PROCESSING COMPLETE!")
print("="*80)
