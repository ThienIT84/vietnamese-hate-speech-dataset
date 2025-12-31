"""
Simple processing of strategic samples using advanced_text_cleaning.py
"""
import pandas as pd
import sys
import os

# Add to path
sys.path.insert(0, 'src/preprocessing')

# Import
from advanced_text_cleaning import advanced_clean_text

print("="*80)
print("🔧 PROCESSING STRATEGIC SAMPLES")
print("="*80)

# Load
input_file = 'STRATEGIC_SAMPLES_FOR_REVIEW_20251229_173539.csv'
print(f"\n📂 Loading: {input_file}")
df = pd.read_csv(input_file)
print(f"   Loaded: {len(df)} samples")

# Process
print("\n🔧 Processing...")
print("   Using: advanced_clean_text() from advanced_text_cleaning.py")
print("   Strategy: Intensity Preservation")

processed_texts = []
for idx, row in df.iterrows():
    if (idx + 1) % 100 == 0:
        print(f"   Progress: {idx + 1}/{len(df)}")
    
    raw_title = str(row.get('raw_title', '')) if pd.notna(row.get('raw_title')) else ''
    raw_comment = str(row.get('raw_comment', '')) if pd.notna(row.get('raw_comment')) else ''
    
    # Clean
    if raw_title and raw_comment:
        title_clean = advanced_clean_text(raw_title)
        comment_clean = advanced_clean_text(raw_comment)
        training_text = f"{title_clean} </s> {comment_clean}"
    elif raw_comment:
        training_text = advanced_clean_text(raw_comment)
    elif raw_title:
        training_text = advanced_clean_text(raw_title)
    else:
        training_text = advanced_clean_text(str(row.get('text', '')))
    
    processed_texts.append(training_text)

df['training_text'] = processed_texts
if 'text' in df.columns:
    df['text_raw'] = df['text']
elif 'text_raw' not in df.columns:
    # Reconstruct text_raw from raw_title and raw_comment
    df['text_raw'] = df.apply(
        lambda x: f"{x.get('raw_title', '')} </s> {x.get('raw_comment', '')}" 
        if pd.notna(x.get('raw_title')) and pd.notna(x.get('raw_comment'))
        else str(x.get('raw_comment', '')),
        axis=1
    )

# Rename columns
if 'suggested_label' in df.columns:
    df = df.rename(columns={'suggested_label': 'label'})

# Add metadata
df['note'] = 'Strategic filter - ' + df['matched_groups'].astype(str)
df['source_file'] = 'filter_strategic_samples'
df['labeler'] = 'auto_strategic'
df['has_teencode'] = True
df['sampling_strategy'] = 'strategic_keyword_filter'

# Select columns
columns = ['training_text', 'text_raw', 'raw_title', 'raw_comment', 'label', 
          'confidence', 'matched_groups', 'note', 'source_file', 'labeler', 
          'has_teencode', 'sampling_strategy']
df = df[[c for c in columns if c in df.columns]]

# Save
from datetime import datetime
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_csv = f'STRATEGIC_SAMPLES_PROCESSED_{timestamp}.csv'
output_xlsx = f'STRATEGIC_SAMPLES_PROCESSED_{timestamp}.xlsx'

df.to_csv(output_csv, index=False, encoding='utf-8-sig')
df.to_excel(output_xlsx, index=False)

print(f"\n💾 Saved:")
print(f"   {output_csv}")
print(f"   {output_xlsx}")

# Show examples
print(f"\n📋 EXAMPLES (First 3):")
for i in range(min(3, len(df))):
    row = df.iloc[i]
    print(f"\n[{i+1}] Label {row['label']}")
    print(f"RAW:  {row['text_raw'][:80]}...")
    print(f"PROC: {row['training_text'][:80]}...")

# Check toxic keywords
print(f"\n🎯 TOXIC KEYWORD CHECK:")
for kw in ['vcl', 'vl', 'đm', 'cc']:
    count = df['training_text'].str.contains(kw, case=False, na=False).sum()
    if count > 0:
        print(f"   '{kw}': {count} samples ✅")

print("\n✅ DONE!")
