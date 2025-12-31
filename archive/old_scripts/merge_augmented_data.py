"""
🔥 MERGE AUGMENTED DATA VÀO TRAINING SET
Gộp HIGH (toàn bộ) + MEDIUM (378 rows đầu) vào final_train_data_v2.csv

Author: Thanh Thien
Date: 29/12/2025
"""

import pandas as pd
from datetime import datetime

print("="*80)
print("🔥 MERGE AUGMENTED DATA VÀO TRAINING SET")
print("="*80)

# ============================================================
# 1. LOAD TRAINING DATA GỐC
# ============================================================

print("\n📂 Loading original training data...")
df_train = pd.read_csv('final_train_data_v2.csv', encoding='utf-8')
print(f"✅ Original training data: {len(df_train)} rows")

# Backup
backup_file = f"backup_final_train_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df_train.to_csv(backup_file, index=False, encoding='utf-8')
print(f"💾 Backup saved: {backup_file}")

# ============================================================
# 2. LOAD HIGH CONFIDENCE (TOÀN BỘ)
# ============================================================

print("\n📂 Loading HIGH confidence data...")
df_high = pd.read_excel('AUTO_LABELED_HIGH_TRUNCATED.xlsx', engine='openpyxl')
print(f"✅ HIGH confidence: {len(df_high)} rows")

# Chỉ lấy các cột cần thiết
high_data = []
for idx, row in df_high.iterrows():
    high_data.append({
        'training_text': row['training_text'],
        'label': int(row['label']),
        'note': f"Augmented-HIGH: {row.get('pattern', '')}",
        'source_file': 'augmentation_high',
        'labeler': 'auto_reviewed',
        'confidence': 'high'
    })

df_high_clean = pd.DataFrame(high_data)
print(f"✅ Prepared HIGH data: {len(df_high_clean)} rows")

# ============================================================
# 3. LOAD MEDIUM CONFIDENCE (378 ROWS ĐẦU)
# ============================================================

print("\n📂 Loading MEDIUM confidence data (378 rows)...")
df_medium = pd.read_excel('AUTO_LABELED_MEDIUM_TRUNCATED.xlsx', engine='openpyxl')
print(f"✅ MEDIUM confidence loaded: {len(df_medium)} rows")

# Chỉ lấy 378 rows đầu (đã review)
df_medium_reviewed = df_medium.head(378)
print(f"✅ Taking first 378 rows (reviewed)")

# Chuẩn bị data
medium_data = []
for idx, row in df_medium_reviewed.iterrows():
    medium_data.append({
        'training_text': row['training_text'],
        'label': int(row['label']),
        'note': f"Augmented-MEDIUM: {row.get('pattern', '')}",
        'source_file': 'augmentation_medium',
        'labeler': 'auto_reviewed',
        'confidence': 'medium'
    })

df_medium_clean = pd.DataFrame(medium_data)
print(f"✅ Prepared MEDIUM data: {len(df_medium_clean)} rows")

# ============================================================
# 4. MERGE DATA
# ============================================================

print("\n🔄 Merging data...")

# Concat tất cả
df_merged = pd.concat([df_train, df_high_clean, df_medium_clean], ignore_index=True)

print(f"\n📊 Merge summary:")
print(f"  - Original training: {len(df_train)}")
print(f"  - HIGH confidence:   {len(df_high_clean)}")
print(f"  - MEDIUM reviewed:   {len(df_medium_clean)}")
print(f"  - Total merged:      {len(df_merged)}")
print(f"  - New samples added: {len(df_high_clean) + len(df_medium_clean)}")

# ============================================================
# 5. REMOVE DUPLICATES
# ============================================================

print("\n🔍 Removing duplicates...")

before_dedup = len(df_merged)
df_merged = df_merged.drop_duplicates(subset=['training_text'], keep='first')
after_dedup = len(df_merged)

print(f"✅ Duplicates removed: {before_dedup - after_dedup}")
print(f"✅ Final dataset: {after_dedup} rows")

# ============================================================
# 6. LABEL DISTRIBUTION
# ============================================================

print("\n📊 Label distribution:")
for label, count in df_merged['label'].value_counts().sort_index().items():
    print(f"   Label {label}: {count} ({count/len(df_merged)*100:.1f}%)")

# ============================================================
# 7. SAVE MERGED DATA
# ============================================================

print("\n💾 Saving merged data...")

# Save as CSV
output_csv = f"final_train_data_v3_AUGMENTED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df_merged.to_csv(output_csv, index=False, encoding='utf-8')
print(f"✅ Saved CSV: {output_csv}")

# Save as Excel for review
output_excel = f"final_train_data_v3_AUGMENTED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df_merged.to_excel(output_excel, index=False, engine='openpyxl')
print(f"✅ Saved Excel: {output_excel}")

# ============================================================
# 8. STATISTICS
# ============================================================

print("\n" + "="*80)
print("📊 FINAL STATISTICS")
print("="*80)

print(f"\n📈 Dataset growth:")
print(f"  Before: {len(df_train)} rows")
print(f"  After:  {len(df_merged)} rows")
print(f"  Growth: +{len(df_merged) - len(df_train)} rows ({(len(df_merged) - len(df_train))/len(df_train)*100:.1f}%)")

print(f"\n📊 Label distribution:")
for label in sorted(df_merged['label'].unique()):
    count_before = len(df_train[df_train['label'] == label])
    count_after = len(df_merged[df_merged['label'] == label])
    growth = count_after - count_before
    print(f"  Label {label}:")
    print(f"    Before: {count_before}")
    print(f"    After:  {count_after} (+{growth})")

print(f"\n🎯 Expected improvement:")
print(f"  - Current F1: 0.68")
print(f"  - Expected F1: 0.72-0.75")
print(f"  - Improvement: +4-7% F1 score")

print("\n" + "="*80)
print("✅ MERGE COMPLETE!")
print("="*80)

print(f"\n🚀 Next steps:")
print(f"  1. Review merged data: {output_excel}")
print(f"  2. Update training script DATA_PATH to: {output_csv}")
print(f"  3. Retrain model")
print(f"  4. Evaluate F1 score")

# ============================================================
# 9. CREATE SUMMARY FILE
# ============================================================

summary = f"""
# 🔥 TRAINING DATA AUGMENTATION SUMMARY

## Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Data Sources
1. Original training data: `final_train_data_v2.csv` ({len(df_train)} rows)
2. HIGH confidence augmented: `AUTO_LABELED_HIGH_TRUNCATED.xlsx` ({len(df_high_clean)} rows)
3. MEDIUM confidence reviewed: `AUTO_LABELED_MEDIUM_TRUNCATED.xlsx` (378 rows)

## Merge Results
- Total rows before: {len(df_train)}
- Total rows after: {len(df_merged)}
- New samples added: {len(df_high_clean) + len(df_medium_clean)}
- Duplicates removed: {before_dedup - after_dedup}
- Growth: +{(len(df_merged) - len(df_train))/len(df_train)*100:.1f}%

## Label Distribution

### Before
{df_train['label'].value_counts().sort_index().to_string()}

### After
{df_merged['label'].value_counts().sort_index().to_string()}

## Files Created
- CSV: `{output_csv}`
- Excel: `{output_excel}`
- Backup: `{backup_file}`

## Expected Impact
- Current F1: 0.68
- Expected F1: 0.72-0.75
- Improvement: +4-7% F1 score

## Next Steps
1. Review merged data
2. Update training script DATA_PATH
3. Retrain model
4. Evaluate performance
"""

summary_file = f"AUGMENTATION_SUMMARY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
with open(summary_file, 'w', encoding='utf-8') as f:
    f.write(summary)

print(f"\n📝 Summary saved: {summary_file}")
