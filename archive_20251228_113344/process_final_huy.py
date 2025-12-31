"""
Script để xử lý file final_Huy.xlsx
- Áp dụng advanced_text_cleaning cho raw_title và raw_comment
- Kết hợp thành training_text với format: "cleaned_title </s> cleaned_comment"
- Giữ nguyên emoji và xử lý teencode
"""

import pandas as pd
import sys
from pathlib import Path

# Import advanced cleaning function
sys.path.insert(0, str(Path(__file__).parent))
from src.preprocessing.advanced_text_cleaning import clean_text_with_special_emoji, build_input_text_with_context

def process_final_huy(input_file: str, output_file: str):
    """
    Xử lý file final_Huy.xlsx
    
    Args:
        input_file: Đường dẫn file Excel đầu vào
        output_file: Đường dẫn file CSV đầu ra
    """
    print("=" * 80)
    print("XỬ LÝ FILE FINAL_HUY.XLSX")
    print("=" * 80)
    
    # Đọc file Excel
    print(f"\n📖 Đọc file: {input_file}")
    df = pd.read_excel(input_file)
    print(f"✅ Đã đọc {len(df)} dòng")
    print(f"Columns: {df.columns.tolist()}")
    
    # Kiểm tra các cột cần thiết
    required_cols = ['raw_title', 'raw_comment']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"❌ Thiếu các cột: {missing_cols}")
    
    print("\n" + "=" * 80)
    print("🧹 BẮT ĐẦU XỬ LÝ TEXT CLEANING")
    print("=" * 80)
    
    # Xử lý từng dòng với progress
    cleaned_titles = []
    cleaned_comments = []
    training_texts = []
    
    for idx, row in df.iterrows():
        if (idx + 1) % 100 == 0:
            print(f"Đang xử lý: {idx + 1}/{len(df)} dòng...")
        
        # Lấy raw text
        raw_title = str(row['raw_title']) if pd.notna(row['raw_title']) else ''
        raw_comment = str(row['raw_comment']) if pd.notna(row['raw_comment']) else ''
        
        # Áp dụng advanced cleaning (giữ emoji, xử lý teencode)
        cleaned_title = clean_text_with_special_emoji(raw_title)
        cleaned_comment = clean_text_with_special_emoji(raw_comment)
        
        # Tạo training_text với context format
        training_text = build_input_text_with_context(
            title=cleaned_title,
            comment=cleaned_comment,
            max_total_length=256
        )
        
        cleaned_titles.append(cleaned_title)
        cleaned_comments.append(cleaned_comment)
        training_texts.append(training_text)
    
    print(f"✅ Hoàn thành xử lý {len(df)} dòng")
    
    # Thêm các cột mới vào DataFrame
    df['cleaned_title_advanced'] = cleaned_titles
    df['cleaned_comment_advanced'] = cleaned_comments
    df['training_text'] = training_texts
    
    # Lưu file
    print(f"\n💾 Lưu file: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ Đã lưu thành công!")
    
    # Hiển thị thống kê
    print("\n" + "=" * 80)
    print("📊 THỐNG KÊ")
    print("=" * 80)
    print(f"Tổng số dòng: {len(df)}")
    print(f"Số dòng có training_text: {df['training_text'].notna().sum()}")
    print(f"Độ dài trung bình training_text: {df['training_text'].str.len().mean():.1f} ký tự")
    
    # Hiển thị ví dụ
    print("\n" + "=" * 80)
    print("📝 VÍ DỤ KẾT QUẢ")
    print("=" * 80)
    
    for i in range(min(3, len(df))):
        print(f"\n--- Ví dụ {i+1} ---")
        print(f"Raw Title: {df.iloc[i]['raw_title'][:100]}...")
        print(f"Raw Comment: {df.iloc[i]['raw_comment'][:100]}...")
        print(f"Cleaned Title: {df.iloc[i]['cleaned_title_advanced'][:100]}...")
        print(f"Cleaned Comment: {df.iloc[i]['cleaned_comment_advanced'][:100]}...")
        print(f"Training Text: {df.iloc[i]['training_text'][:150]}...")
    
    print("\n" + "=" * 80)
    print("✅ HOÀN THÀNH!")
    print("=" * 80)

if __name__ == "__main__":
    # Đường dẫn file
    input_file = "data/processed/final_Huy.xlsx"
    output_file = "data/processed/final_Huy_processed.csv"
    
    # Chạy xử lý
    process_final_huy(input_file, output_file)
