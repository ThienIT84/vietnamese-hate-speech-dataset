import pandas as pd
from datetime import datetime

# Đọc file 1 (final_Huy_processed.csv) - có training_text và label
file1_path = r'data\processed\final_Huy_processed.csv'
df1 = pd.read_csv(file1_path)

print(f"File 1 shape: {df1.shape}")
print(f"File 1 columns: {df1.columns.tolist()}")
print(f"\nFile 1 - Số dòng có label: {df1['label'].notna().sum()}")
print(f"File 1 - Số dòng chưa có label: {df1['label'].isna().sum()}")

# Đọc file 2 (FINAL_MERGED_3FILES...) - có các trường còn lại
file2_path = r'data\processed\FINAL_MERGED_3FILES_20251224_184903_LABELED_ONLY_20251224_190142_TEENCODE_CONTEXT_150_fixed.csv'
df2 = pd.read_csv(file2_path)

print(f"\nFile 2 shape: {df2.shape}")
print(f"File 2 columns: {df2.columns.tolist()}")

# Lọc chỉ lấy những dòng đã gán nhãn từ file 1
df1_labeled = df1[df1['label'].notna()].copy()
print(f"\nSố dòng đã gán nhãn từ File 1: {len(df1_labeled)}")

# Kiểm tra xem có cột nào chung giữa 2 file để merge
common_cols = set(df1.columns) & set(df2.columns)
print(f"\nCác cột chung giữa 2 file: {common_cols}")

# Sử dụng training_text làm key để merge vì đây là cột duy nhất có ý nghĩa
merge_key = 'training_text'

if merge_key in df1_labeled.columns and merge_key in df2.columns:
    print(f"\nMerge theo cột: {merge_key}")
    
    # Lấy các cột từ file 2 mà không có trong file 1 (trừ merge_key)
    cols_to_add = [col for col in df2.columns if col not in df1_labeled.columns or col == merge_key]
    df2_subset = df2[cols_to_add].copy()
    
    # Merge
    result_df = pd.merge(df1_labeled, df2_subset, on=merge_key, how='left', suffixes=('', '_from_file2'))
    
    print(f"\nSố dòng match được: {result_df[result_df['text_raw'].notna()].shape[0] if 'text_raw' in result_df.columns else 'N/A'}")
else:
    # Fallback: merge theo index/vị trí
    print("\nKhông thể merge theo training_text, merge theo vị trí")
    min_rows = min(len(df1_labeled), len(df2))
    result_df = pd.concat([
        df1_labeled.iloc[:min_rows].reset_index(drop=True), 
        df2.iloc[:min_rows].reset_index(drop=True)
    ], axis=1)

# Loại bỏ các cột trùng lặp nếu có
result_df = result_df.loc[:, ~result_df.columns.duplicated()]

print(f"\nKết quả final shape: {result_df.shape}")
print(f"Kết quả final columns: {result_df.columns.tolist()}")

# Lưu file kết quả
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f'data/processed/MERGED_FINAL_HUY_{timestamp}.csv'
result_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ Đã lưu file kết quả tại: {output_path}")
print(f"Tổng số dòng: {len(result_df)}")
print(f"Tổng số cột: {len(result_df.columns)}")
