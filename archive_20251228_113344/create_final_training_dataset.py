import pandas as pd
from datetime import datetime

# Đọc file MERGED_FINAL_HUY (1674 dòng, 30 cột)
merged_huy_path = r'data\processed\MERGED_FINAL_HUY_20251225_105522.csv'
df_huy = pd.read_csv(merged_huy_path)

print(f"MERGED_FINAL_HUY shape: {df_huy.shape}")
print(f"MERGED_FINAL_HUY columns: {df_huy.columns.tolist()}")

# Đọc file FINAL_MERGED_3FILES (3893 dòng, 9 cột)
final_merged_path = r'data\processed\FINAL_MERGED_3FILES_20251224_184903_LABELED_ONLY_20251224_190142_TEENCODE_CONTEXT_150_fixed.csv'
df_final = pd.read_csv(final_merged_path)

print(f"\nFINAL_MERGED_3FILES shape: {df_final.shape}")
print(f"FINAL_MERGED_3FILES columns: {df_final.columns.tolist()}")

# Tìm các cột bổ sung từ MERGED_FINAL_HUY (không có trong FINAL_MERGED_3FILES)
additional_cols = [col for col in df_huy.columns if col not in df_final.columns]
print(f"\nCác cột bổ sung từ MERGED_FINAL_HUY: {additional_cols}")
print(f"Số cột bổ sung: {len(additional_cols)}")

# Lấy các cột cần thiết từ df_huy để merge
# Bao gồm: training_text (key) + các cột bổ sung
cols_to_merge = ['training_text'] + additional_cols
df_huy_subset = df_huy[cols_to_merge].copy()

print(f"\nCác cột sẽ merge từ MERGED_FINAL_HUY: {cols_to_merge}")

# Merge df_final với df_huy_subset theo training_text
result_df = pd.merge(
    df_final, 
    df_huy_subset, 
    on='training_text', 
    how='left',  # Giữ tất cả dòng từ df_final
    suffixes=('', '_from_huy')
)

print(f"\nKết quả sau merge:")
print(f"Shape: {result_df.shape}")
print(f"Columns: {result_df.columns.tolist()}")

# Kiểm tra số dòng match được
matched_rows = result_df[result_df['id'].notna()].shape[0] if 'id' in result_df.columns else 0
print(f"\nSố dòng match được từ MERGED_FINAL_HUY: {matched_rows}")
print(f"Số dòng không match (chỉ có trong FINAL_MERGED_3FILES): {result_df.shape[0] - matched_rows}")

# Kiểm tra phân bố label
print(f"\nPhân bố label:")
print(result_df['label'].value_counts(dropna=False))

# Lưu file kết quả
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f'data/processed/FINAL_TRAINING_DATASET_{timestamp}.csv'
result_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ Đã lưu file training cuối cùng tại: {output_path}")
print(f"Tổng số dòng: {len(result_df)}")
print(f"Tổng số cột: {len(result_df.columns)}")
print(f"\nFile này đã sẵn sàng để đem đi train!")
