"""
🔥 Teencode-Only Cleaning Script
Chỉ áp dụng teencode normalization, GIỮ NGUYÊN tất cả các tag đặc biệt

USAGE:
    python clean_teencode_only.py input.csv -c text_column -o output.csv
    
FEATURES:
    ✅ Áp dụng teencode dictionary từ advanced_text_cleaning.py
    ✅ GIỮ NGUYÊN các tag: <person>, <emo_pos>, <emo_neg>, </s>, <intense>, etc.
    ✅ KHÔNG xóa emoji, KHÔNG lowercase, KHÔNG xóa hashtag
    ✅ CHỈ thay thế teencode words
"""

import pandas as pd
import argparse
import re
from pathlib import Path
from tqdm import tqdm
from src.preprocessing.advanced_text_cleaning import TEENCODE_DICT


def teencode_only_clean(text: str) -> str:
    """
    Chỉ áp dụng teencode normalization, giữ nguyên mọi thứ khác
    
    Args:
        text: Input text
        
    Returns:
        Text với teencode đã được normalize, giữ nguyên tags và format
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # Sort teencode dictionary by length (longest first) để tránh replace sai
    sorted_teencode = sorted(TEENCODE_DICT.items(), key=lambda x: len(x[0]), reverse=True)
    
    # Apply teencode replacement với word boundary
    for teencode, replacement in sorted_teencode:
        # Sử dụng word boundary để tránh replace một phần của từ
        # Ví dụ: "ko" -> "không" nhưng không replace "ko" trong "koko"
        pattern = r'\b' + re.escape(teencode) + r'\b'
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def clean_csv_teencode_only(
    input_file: str,
    output_file: str = None,
    text_column: str = 'text',
    encoding: str = 'utf-8'
):
    """
    Làm sạch teencode trong file CSV, giữ nguyên tất cả tags
    
    Args:
        input_file: Đường dẫn file CSV đầu vào
        output_file: Đường dẫn file CSV đầu ra
        text_column: Tên cột chứa text cần clean
        encoding: Encoding của file CSV
    """
    
    # Kiểm tra file tồn tại
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {input_file}")
    
    # Tạo tên file output nếu không được chỉ định
    if output_file is None:
        output_file = input_path.stem + '_teencode_cleaned' + input_path.suffix
    
    print(f"📂 Đọc file: {input_file}")
    
    # Đọc CSV
    try:
        df = pd.read_csv(input_file, encoding=encoding)
    except UnicodeDecodeError:
        print(f"⚠️  Lỗi encoding '{encoding}', thử lại với 'utf-8-sig'...")
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    
    print(f"✅ Đã đọc {len(df)} dòng")
    
    # Kiểm tra cột text có tồn tại
    if text_column not in df.columns:
        print(f"\n❌ KHÔNG TÌM THẤY CỘT '{text_column}'")
        print(f"📋 Các cột có sẵn: {', '.join(df.columns)}")
        return
    
    # Tạo cột mới cho text đã clean
    cleaned_column = f"{text_column}_teencode_cleaned"
    
    print(f"\n🔧 Đang làm sạch teencode trong cột '{text_column}'...")
    print(f"📊 Tiến độ:")
    
    # Áp dụng teencode cleaning với progress bar
    tqdm.pandas(desc="Cleaning Teencode")
    df[cleaned_column] = df[text_column].progress_apply(
        lambda x: teencode_only_clean(str(x)) if pd.notna(x) else ""
    )
    
    # Thống kê
    print(f"\n📈 Thống kê:")
    print(f"  - Tổng số dòng: {len(df)}")
    print(f"  - Dòng có text gốc: {df[text_column].notna().sum()}")
    print(f"  - Dòng có text sau clean: {(df[cleaned_column] != '').sum()}")
    
    # Đếm số dòng có thay đổi
    changes = (df[text_column].astype(str) != df[cleaned_column].astype(str)).sum()
    print(f"  - Số dòng có thay đổi: {changes} ({changes/len(df)*100:.1f}%)")
    
    # Lưu file
    print(f"\n💾 Lưu kết quả vào: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ HOÀN THÀNH!")
    print(f"\n📋 Preview (5 dòng đầu có thay đổi):")
    print("="*100)
    
    # Hiển thị preview chỉ những dòng có thay đổi
    changed_rows = df[df[text_column].astype(str) != df[cleaned_column].astype(str)]
    for idx, row in changed_rows.head(5).iterrows():
        print(f"\n[Dòng {idx+1}]")
        print(f"  Gốc: {str(row[text_column])[:100]}...")
        print(f"  Clean: {str(row[cleaned_column])[:100]}...")
    
    print("="*100)
    
    return df


def main():
    parser = argparse.ArgumentParser(
        description='Làm sạch TEENCODE ONLY trong file CSV (giữ nguyên tags)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python clean_teencode_only.py data.csv -c training_text -o cleaned.csv
  python clean_teencode_only.py input.csv --column text --output output.csv
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Đường dẫn file CSV đầu vào'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        default=None,
        help='Đường dẫn file CSV đầu ra (mặc định: <input>_teencode_cleaned.csv)'
    )
    
    parser.add_argument(
        '-c', '--column',
        dest='text_column',
        default='text',
        help='Tên cột chứa text cần clean (mặc định: "text")'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='Encoding của file CSV (mặc định: utf-8)'
    )
    
    args = parser.parse_args()
    
    try:
        clean_csv_teencode_only(
            input_file=args.input_file,
            output_file=args.output_file,
            text_column=args.text_column,
            encoding=args.encoding
        )
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
