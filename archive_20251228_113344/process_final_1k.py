"""
🔥 Process final_1k_output.csv
Áp dụng teencode cleaning và gộp context + text với separator </s>

USAGE:
    python process_final_1k.py

INPUT:
    - File: TOXIC_COMMENT/datasets/final/final_1k_output.csv
    - Columns: context, text

OUTPUT:
    - File: TOXIC_COMMENT/datasets/final/final_1k_processed.csv
    - New column: input_text (format: "context </s> text")
    - Cleaned columns: context_cleaned, text_cleaned
"""

import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Import cleaning function
from src.preprocessing.advanced_text_cleaning import advanced_clean_text


def process_final_1k():
    """
    Xử lý file final_1k_output.csv:
    1. Clean teencode cho cột context và text
    2. Gộp context + text với separator </s>
    """
    
    # Đường dẫn file
    input_file = Path("TOXIC_COMMENT/datasets/final/final_1k_output.csv")
    output_file = Path("TOXIC_COMMENT/datasets/final/final_1k_processed.csv")
    
    # Kiểm tra file tồn tại
    if not input_file.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {input_file}")
    
    print(f"📂 Đọc file: {input_file}")
    
    # Đọc CSV
    try:
        df = pd.read_csv(input_file, encoding='utf-8')
    except UnicodeDecodeError:
        print(f"⚠️  Lỗi encoding 'utf-8', thử lại với 'utf-8-sig'...")
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    
    print(f"✅ Đã đọc {len(df)} dòng")
    print(f"📋 Các cột: {', '.join(df.columns)}")
    
    # Kiểm tra các cột cần thiết
    required_columns = ['context', 'text']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Thiếu các cột: {', '.join(missing_columns)}")
    
    print(f"\n🔧 Bước 1: Làm sạch teencode cho cột 'context'...")
    tqdm.pandas(desc="Cleaning context")
    df['context_cleaned'] = df['context'].progress_apply(
        lambda x: advanced_clean_text(str(x)) if pd.notna(x) else ""
    )
    
    print(f"\n🔧 Bước 2: Làm sạch teencode cho cột 'text'...")
    tqdm.pandas(desc="Cleaning text")
    df['text_cleaned'] = df['text'].progress_apply(
        lambda x: advanced_clean_text(str(x)) if pd.notna(x) else ""
    )
    
    print(f"\n🔧 Bước 3: Gộp context + text với separator </s>...")
    
    def combine_context_text(row):
        """Gộp context và text với separator </s>"""
        context = row['context_cleaned'].strip()
        text = row['text_cleaned'].strip()
        
        # Nếu không có context, chỉ trả về text
        if not context:
            return text
        
        # Nếu không có text, chỉ trả về context
        if not text:
            return context
        
        # Gộp với separator
        return f"{context} </s> {text}"
    
    tqdm.pandas(desc="Combining")
    df['input_text'] = df.progress_apply(combine_context_text, axis=1)
    
    # Thống kê
    print(f"\n📈 Thống kê:")
    print(f"  - Tổng số dòng: {len(df)}")
    print(f"  - Dòng có context: {df['context'].notna().sum()}")
    print(f"  - Dòng có text: {df['text'].notna().sum()}")
    print(f"  - Dòng có input_text sau xử lý: {(df['input_text'] != '').sum()}")
    
    # Lưu file
    print(f"\n💾 Lưu kết quả vào: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ HOÀN THÀNH!")
    print(f"\n📋 Preview (5 dòng đầu):")
    print("="*120)
    
    # Hiển thị preview
    for idx, row in df.head(5).iterrows():
        print(f"\n[Dòng {idx+1}]")
        print(f"  Context gốc: {str(row['context'])[:80]}...")
        print(f"  Text gốc: {str(row['text'])[:80]}...")
        print(f"  Input_text (cleaned + combined): {str(row['input_text'])[:100]}...")
    
    print("="*120)
    
    return df


if __name__ == "__main__":
    try:
        process_final_1k()
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
