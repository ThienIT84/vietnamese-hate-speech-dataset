"""
Script để gộp các file dữ liệu đã gán nhãn thành 1 file duy nhất
Mục đích: Tránh mất cân bằng dữ liệu khi training model
"""
# Project root path
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


import pandas as pd
import os

def merge_labeled_files():
    """
    Gộp các file CSV đã gán nhãn thành 1 file duy nhất
    """
    # Đường dẫn đến các file
    file1 = r"c:\Học sâu\Dataset\TOXIC_COMMENT\training_data_with_context_phobert_clean.csv"
    file2 = r"c:\Học sâu\Dataset\TOXIC_COMMENT\label1_candidates_150samples.csv"
    output_file = r"c:\Học sâu\Dataset\TOXIC_COMMENT\training_data_final_merged.csv"
    
    print("Đang đọc các file...")
    
    # Đọc các file CSV
    df1 = pd.read_csv(file1, encoding='utf-8')
    df2 = pd.read_csv(file2, encoding='utf-8')
    
    print(f"File 1: {len(df1)} samples")
    print(f"  - Label 0: {len(df1[df1['label'] == 0])} samples")
    print(f"  - Label 1: {len(df1[df1['label'] == 1])} samples")
    print(f"  - Label 2: {len(df1[df1['label'] == 2])} samples")
    
    print(f"\nFile 2: {len(df2)} samples")
    print(f"  - Label 0: {len(df2[df2['label'] == 0])} samples")
    print(f"  - Label 1: {len(df2[df2['label'] == 1])} samples")
    print(f"  - Label 2: {len(df2[df2['label'] == 2])} samples")
    
    # Gộp 2 dataframe
    df_merged = pd.concat([df1, df2], ignore_index=True)
    
    # Loại bỏ các dòng trùng lặp nếu có (dựa trên cột input_text)
    print(f"\nTổng cộng trước khi loại bỏ trùng lặp: {len(df_merged)} samples")
    df_merged = df_merged.drop_duplicates(subset=['input_text'], keep='first')
    print(f"Tổng cộng sau khi loại bỏ trùng lặp: {len(df_merged)} samples")
    
    # Thống kê phân bố nhãn sau khi merge
    print("\n=== Phân bố nhãn sau khi gộp ===")
    print(f"  - Label 0 (Không toxic): {len(df_merged[df_merged['label'] == 0])} samples ({len(df_merged[df_merged['label'] == 0])/len(df_merged)*100:.2f}%)")
    print(f"  - Label 1 (Offensive): {len(df_merged[df_merged['label'] == 1])} samples ({len(df_merged[df_merged['label'] == 1])/len(df_merged)*100:.2f}%)")
    print(f"  - Label 2 (Hate Speech): {len(df_merged[df_merged['label'] == 2])} samples ({len(df_merged[df_merged['label'] == 2])/len(df_merged)*100:.2f}%)")
    
    # Shuffle dữ liệu để trộn đều các nhãn
    df_merged = df_merged.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Lưu file với UTF-8 BOM để Excel và các editor khác hiển thị đúng tiếng Việt
    df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✅ Đã lưu file gộp tại: {output_file}")
    print(f"Tổng số samples: {len(df_merged)}")
    
    return df_merged

if __name__ == "__main__":
    df_final = merge_labeled_files()
    print("\n✅ Hoàn thành!")
