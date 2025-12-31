"""
Export lại file gắn nhãn với cột cleaned_text_norm
"""

import pandas as pd

print("="*80)
print("📤 EXPORT LẠI FILE GẮN NHÃN VỚI CLEANED_TEXT_NORM")
print("="*80)

# Load master dataset (có cột cleaned_text_norm)
df_master = pd.read_csv('final_dataset/master_combined.csv')
print(f"✅ Loaded master: {len(df_master)} samples")

# Load file gắn nhãn đã có
df_labeled = pd.read_excel('labeled/dataset_to_label_PERSON1_250samples.xlsx')
print(f"✅ Loaded labeled: {len(df_labeled)} samples")
print(f"   Columns: {df_labeled.columns.tolist()}")

# Lấy cleaned_text_norm từ master dựa trên ID
df_merged = df_labeled.merge(
    df_master[['id', 'cleaned_text_norm']], 
    on='id', 
    how='left'
)

# Kiểm tra có match được không
matched = df_merged['cleaned_text_norm'].notna().sum()
print(f"\n📊 Matched {matched}/{len(df_labeled)} samples với master")

if matched < len(df_labeled):
    print(f"⚠️ {len(df_labeled) - matched} samples không tìm thấy trong master!")

# Sắp xếp lại cột
cols_order = ['id', 'text', 'cleaned_text_norm', 'topic', 'source_platform', 'label', 'annotator', 'notes', 'annotator_id']
cols_exist = [c for c in cols_order if c in df_merged.columns]
df_merged = df_merged[cols_exist]

# Export
output_file = 'labeled/dataset_labeled_with_norm_PERSON1.csv'
df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n💾 EXPORTED: {output_file}")
print(f"   Total: {len(df_merged)} samples")

# Show sample
print(f"\n📝 MẪU (5 dòng đầu):")
print("="*80)
for idx, row in df_merged.head(5).iterrows():
    print(f"\n🔹 Label: {row.get('label', 'N/A')}")
    print(f"   TEXT gốc: {row['text'][:60]}...")
    if pd.notna(row.get('cleaned_text_norm')):
        print(f"   NORMALIZED: {row['cleaned_text_norm'][:60]}...")

# Thống kê label
print(f"\n" + "="*80)
print(f"📊 THỐNG KÊ NHÃN:")
print("="*80)
if 'label' in df_merged.columns:
    labeled_count = df_merged['label'].notna().sum()
    print(f"Đã gắn nhãn: {labeled_count}/{len(df_merged)}")
    if labeled_count > 0:
        print(df_merged['label'].value_counts())

print("="*80)
