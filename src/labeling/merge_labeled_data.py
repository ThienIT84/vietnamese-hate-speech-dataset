"""
Merge kết quả gắn nhãn từ 2 người
Kiểm tra chất lượng và tạo file final
"""

import pandas as pd
import numpy as np

print("="*80)
print("🔗 MERGE KẾT QUẢ GẮN NHÃN TỪ 2 NGƯỜI")
print("="*80)

# Load 2 files
person1 = pd.read_csv('labeling/dataset_to_label_PERSON1_250samples_20251127.csv')
person2 = pd.read_csv('labeling/dataset_to_label_PERSON2_250samples_20251127.csv')

print(f"\n📥 LOADED:")
print(f"   Người 1: {len(person1)} samples")
print(f"   Người 2: {len(person2)} samples")

# Kiểm tra có gắn nhãn chưa
labeled1 = person1['label'].notna().sum()
labeled2 = person2['label'].notna().sum()

print(f"\n✅ ĐÃ GẮN NHÃN:")
print(f"   Người 1: {labeled1}/{len(person1)} ({labeled1/len(person1)*100:.1f}%)")
print(f"   Người 2: {labeled2}/{len(person2)} ({labeled2/len(person2)*100:.1f}%)")

if labeled1 < len(person1) or labeled2 < len(person2):
    print(f"\n⚠️ CẢNH BÁO: Vẫn còn mẫu chưa gắn nhãn!")
    print(f"   Người 1 thiếu: {len(person1) - labeled1}")
    print(f"   Người 2 thiếu: {len(person2) - labeled2}")
    
    response = input("\nTiếp tục merge? (y/n): ")
    if response.lower() != 'y':
        print("❌ Hủy merge. Vui lòng hoàn thành gắn nhãn trước!")
        exit()

# Merge
df_merged = pd.concat([person1, person2], ignore_index=True)
print(f"\n🔗 MERGED: {len(df_merged)} samples")

# Kiểm tra label distribution
print(f"\n📊 PHÂN BỐ NHÃN:")
label_dist = df_merged['label'].value_counts()
print(label_dist)
print(f"\nTỷ lệ:")
for label, count in label_dist.items():
    print(f"   {label}: {count/len(df_merged)*100:.1f}%")

# Kiểm tra có label lạ không
valid_labels = ['Normal', 'Offensive', 'Hate Speech', 'Toxic']
invalid = df_merged[~df_merged['label'].isin(valid_labels + [np.nan])]
if len(invalid) > 0:
    print(f"\n⚠️ PHÁT HIỆN NHÃN KHÔNG HỢP LỆ:")
    print(invalid[['id', 'text', 'label', 'annotator_id']])
    print(f"\n   Chỉ chấp nhận: {valid_labels}")

# Kiểm tra agreement giữa 2 người (nếu có overlap - thường không có)
print(f"\n✅ QUALITY CHECK:")
print(f"   Total labeled: {df_merged['label'].notna().sum()}/{len(df_merged)}")
print(f"   Người 1 contribution: {labeled1}")
print(f"   Người 2 contribution: {labeled2}")

# Export
output_file = f'labeling/dataset_labeled_merged_500samples_{pd.Timestamp.now().strftime("%Y%m%d")}.csv'
df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n💾 EXPORTED: {output_file}")
print(f"\n" + "="*80)
print(f"🎯 BƯỚC TIẾP THEO:")
print(f"="*80)
print(f"1. Kiểm tra file: {output_file}")
print(f"2. Train baseline model:")
print(f"   python train_baseline_model.py")
print(f"\n3. Đánh giá accuracy và quyết định:")
print(f"   - < 60%: Gắn thêm 500 samples nữa")
print(f"   - 60-80%: Gắn đến 2,000 samples")
print(f"   - > 80%: Dùng Active Learning")
print("="*80)

# Tạo summary stats
summary = pd.DataFrame({
    'Metric': [
        'Total Samples',
        'Person 1 Labeled',
        'Person 2 Labeled',
        'Normal',
        'Offensive',
        'Hate Speech',
        'Toxic',
        'Unlabeled'
    ],
    'Count': [
        len(df_merged),
        labeled1,
        labeled2,
        label_dist.get('Normal', 0),
        label_dist.get('Offensive', 0),
        label_dist.get('Hate Speech', 0),
        label_dist.get('Toxic', 0),
        len(df_merged) - df_merged['label'].notna().sum()
    ]
})

summary_file = f'labeling/labeling_summary_{pd.Timestamp.now().strftime("%Y%m%d")}.csv'
summary.to_csv(summary_file, index=False, encoding='utf-8-sig')
print(f"\n📈 Summary stats: {summary_file}")
