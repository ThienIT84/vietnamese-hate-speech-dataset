import pandas as pd
import sys
from datetime import datetime

# Import advanced text cleaning
sys.path.append('src/preprocessing')
from advanced_text_cleaning import clean_text

# Đọc file training dataset
input_path = r'data\processed\FINAL_TRAINING_DATASET_20251225_110326.csv'
df = pd.read_csv(input_path)

print(f"File shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nSample training_text trước khi xử lý:")
print(df['training_text'].head(3))

# Áp dụng teencode cleaning cho cột training_text
print("\n🔄 Đang xử lý teencode cho cột training_text...")
df['training_text_cleaned'] = df['training_text'].apply(
    lambda x: clean_text(str(x)) if pd.notna(x) else x
)

print(f"\n✅ Đã xử lý xong!")
print(f"\nSample training_text sau khi xử lý:")
print(df['training_text_cleaned'].head(3))

# So sánh trước và sau
print("\n📊 So sánh một số ví dụ:")
for i in range(min(5, len(df))):
    if df['training_text'].iloc[i] != df['training_text_cleaned'].iloc[i]:
        print(f"\n--- Ví dụ {i+1} ---")
        print(f"Trước: {df['training_text'].iloc[i]}")
        print(f"Sau:  {df['training_text_cleaned'].iloc[i]}")

# Thay thế cột training_text bằng cột đã clean
df['training_text'] = df['training_text_cleaned']
df = df.drop(columns=['training_text_cleaned'])

# Lưu file kết quả
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f'data/processed/FINAL_TRAINING_DATASET_TEENCODE_{timestamp}.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ Đã lưu file kết quả tại: {output_path}")
print(f"Tổng số dòng: {len(df)}")
print(f"Tổng số cột: {len(df.columns)}")
