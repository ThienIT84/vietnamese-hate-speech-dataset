"""
Apply Advanced Cleaning vào toàn bộ dataset
"""

import pandas as pd
import sys
sys.path.append('.')
from src.preprocessing.advanced_text_cleaning import advanced_clean_text

print("="*80)
print("🔥 APPLY ADVANCED CLEANING VÀO DATASET")
print("="*80)

# Load master dataset
df = pd.read_csv('final_dataset/master_combined.csv')
print(f"✅ Loaded: {len(df)} samples")

# Backup
backup_file = 'final_dataset/master_combined_backup_before_advanced_clean.csv'
df.to_csv(backup_file, index=False, encoding='utf-8-sig')
print(f"💾 Backup: {backup_file}")

# Apply advanced cleaning
print(f"\n⏳ Đang apply advanced cleaning...")
df['cleaned_text_advanced'] = df['text'].apply(advanced_clean_text)

# So sánh trước/sau
print(f"\n📊 SO SÁNH TRƯỚC/SAU:")
print("="*80)

# Show samples có thay đổi lớn
samples = df[df['cleaned_text_norm'] != df['cleaned_text_advanced']].head(10)

for idx, row in samples.iterrows():
    print(f"\n🔹 ID: {row['id'][:30]}...")
    print(f"   GỐC:      {row['text'][:60]}...")
    print(f"   NORM cũ:  {str(row['cleaned_text_norm'])[:60]}...")
    print(f"   ADVANCED: {row['cleaned_text_advanced'][:60]}...")

# Thống kê
changed = (df['cleaned_text_norm'] != df['cleaned_text_advanced']).sum()
print(f"\n📈 THỐNG KÊ:")
print(f"   Tổng samples: {len(df)}")
print(f"   Số samples thay đổi: {changed} ({changed/len(df)*100:.1f}%)")

# Cập nhật cột cleaned_text_norm với advanced cleaning
df['cleaned_text_norm'] = df['cleaned_text_advanced']
df.drop(columns=['cleaned_text_advanced'], inplace=True)

# Save
output_file = 'final_dataset/master_combined.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n💾 SAVED: {output_file}")

# Cập nhật file labeled
print(f"\n" + "="*80)
print(f"📤 CẬP NHẬT FILE ĐÃ GẮN NHÃN")
print("="*80)

try:
    df_labeled = pd.read_excel('labeled/dataset_to_label_PERSON1_250samples.xlsx')
    print(f"✅ Loaded labeled: {len(df_labeled)} samples")
    
    # Apply advanced cleaning
    df_labeled['cleaned_text_norm'] = df_labeled['text'].apply(advanced_clean_text)
    
    # Save
    labeled_output = 'labeled/dataset_labeled_advanced_clean.csv'
    df_labeled.to_csv(labeled_output, index=False, encoding='utf-8-sig')
    print(f"💾 SAVED: {labeled_output}")
    
    # Show samples
    print(f"\n📝 MẪU (5 dòng đầu):")
    for idx, row in df_labeled.head(5).iterrows():
        print(f"\n   [{row.get('label', 'N/A')}]")
        print(f"   GỐC: {row['text'][:50]}...")
        print(f"   ADV: {row['cleaned_text_norm'][:50]}...")
        
except Exception as e:
    print(f"⚠️ Không load được file labeled: {e}")

print(f"\n" + "="*80)
print(f"✅ HOÀN THÀNH ADVANCED CLEANING!")
print(f"="*80)
print(f"\n📋 ĐÃ CẢI THIỆN:")
print(f"   ✅ Mở rộng teencode dictionary: 251 từ")
print(f"   ✅ Xử lý lặp ký tự (nguuuu → ngu)")
print(f"   ✅ Xử lý bypass (n.g.u → ngu)")
print(f"   ✅ Xử lý leetspeak (ch3t → chết)")
print(f"   ✅ Xử lý emoji (xóa)")
print(f"   ✅ Xử lý @mentions")
print(f"   ✅ Normalize Unicode tricks")
print("="*80)
