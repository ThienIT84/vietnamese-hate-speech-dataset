import pandas as pd
from datetime import datetime

# Đọc file FINAL_MERGED_3FILES (file gốc - 3893 dòng, 9 cột)
final_merged_path = r'data\processed\FINAL_MERGED_3FILES_20251224_184903_LABELED_ONLY_20251224_190142_TEENCODE_CONTEXT_150_fixed.csv'
df_final = pd.read_csv(final_merged_path)

print(f"FINAL_MERGED_3FILES shape: {df_final.shape}")
print(f"FINAL_MERGED_3FILES columns: {df_final.columns.tolist()}")

# Đọc file final_Huy_processed (1674 dòng đã gán nhãn)
huy_path = r'data\processed\final_Huy_processed.csv'
df_huy = pd.read_csv(huy_path)

print(f"\nfinal_Huy_processed shape: {df_huy.shape}")
print(f"final_Huy_processed columns: {df_huy.columns.tolist()}")

# Lọc chỉ lấy những dòng đã gán nhãn
df_huy_labeled = df_huy[df_huy['label'].notna()].copy()
print(f"\nSố dòng đã gán nhãn từ final_Huy_processed: {len(df_huy_labeled)}")

# Lấy các cột giống như FINAL_MERGED_3FILES
target_columns = df_final.columns.tolist()
print(f"\nCác cột cần giữ: {target_columns}")

# Chỉ lấy các cột có trong cả 2 file
available_cols = [col for col in target_columns if col in df_huy_labeled.columns]
missing_cols = [col for col in target_columns if col not in df_huy_labeled.columns]

print(f"\nCác cột có sẵn trong final_Huy_processed: {available_cols}")
print(f"Các cột thiếu trong final_Huy_processed: {missing_cols}")

# Tạo DataFrame từ df_huy_labeled với các cột giống FINAL_MERGED_3FILES
df_huy_subset = df_huy_labeled[available_cols].copy()

# Thêm các cột thiếu với giá trị NaN
for col in missing_cols:
    df_huy_subset[col] = pd.NA

# Sắp xếp lại cột theo thứ tự của FINAL_MERGED_3FILES
df_huy_subset = df_huy_subset[target_columns]

print(f"\ndf_huy_subset shape sau khi chuẩn hóa: {df_huy_subset.shape}")

# Gộp 2 DataFrame
df_combined = pd.concat([df_final, df_huy_subset], ignore_index=True)
print(f"\nSau khi concat: {df_combined.shape}")

# Loại bỏ trùng lặp dựa trên training_text, giữ dòng đầu tiên
df_combined_dedup = df_combined.drop_duplicates(subset=['training_text'], keep='first')
print(f"Sau khi loại bỏ trùng lặp: {df_combined_dedup.shape}")

# Thống kê
print(f"\nSố dòng bị loại bỏ do trùng lặp: {len(df_combined) - len(df_combined_dedup)}")
print(f"Số dòng mới được thêm vào: {len(df_combined_dedup) - len(df_final)}")

# Phân bố label
print(f"\nPhân bố label trong file cuối cùng:")
print(df_combined_dedup['label'].value_counts(dropna=False))

# Lưu file kết quả
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f'data/processed/FINAL_TRAINING_DATASET_{timestamp}.csv'
df_combined_dedup.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ Đã lưu file training cuối cùng tại: {output_path}")
print(f"Tổng số dòng: {len(df_combined_dedup)}")
print(f"Tổng số cột: {len(df_combined_dedup.columns)}")
print(f"\nFile này đã sẵn sàng để đem đi train!")
