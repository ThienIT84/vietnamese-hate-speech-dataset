"""
🔥 CSV Text Cleaning Script
Áp dụng advanced_text_cleaning.py cho file CSV bất kỳ

USAGE:
    python clean_csv.py input.csv -o output.csv -c text_column
    python clean_csv.py data.csv -c comment -o cleaned_data.csv
    
ARGUMENTS:
    input_file: Đường dẫn file CSV đầu vào
    -o, --output: Đường dẫn file CSV đầu ra (mặc định: input_cleaned.csv)
    -c, --column: Tên cột chứa text cần clean (mặc định: 'text')
    --encoding: Encoding của file (mặc định: 'utf-8')
"""

import pandas as pd
import argparse
import sys
from pathlib import Path
from tqdm import tqdm

# Import cleaning function
from src.preprocessing.advanced_text_cleaning import advanced_clean_text


def clean_csv_file(
    input_file: str,
    output_file: str = None,
    text_column: str = 'text',
    encoding: str = 'utf-8'
):
    """
    Làm sạch text trong file CSV
    
    Args:
        input_file: Đường dẫn file CSV đầu vào
        output_file: Đường dẫn file CSV đầu ra (nếu None, tự động tạo)
        text_column: Tên cột chứa text cần clean
        encoding: Encoding của file CSV
    
    Returns:
        DataFrame đã được làm sạch
    """
    
    # Kiểm tra file tồn tại
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {input_file}")
    
    # Tạo tên file output nếu không được chỉ định
    if output_file is None:
        output_file = input_path.stem + '_cleaned' + input_path.suffix
    
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
        
        # Gợi ý cột có thể là text
        text_candidates = [col for col in df.columns if any(
            keyword in col.lower() 
            for keyword in ['text', 'content', 'comment', 'message', 'body', 'description']
        )]
        
        if text_candidates:
            print(f"💡 Gợi ý: Có thể bạn muốn dùng cột: {', '.join(text_candidates)}")
        
        sys.exit(1)
    
    # Tạo cột mới cho text đã clean
    cleaned_column = f"{text_column}_cleaned"
    
    print(f"\n🔧 Đang làm sạch cột '{text_column}'...")
    print(f"📊 Tiến độ:")
    
    # Áp dụng cleaning với progress bar
    tqdm.pandas(desc="Cleaning")
    df[cleaned_column] = df[text_column].progress_apply(
        lambda x: advanced_clean_text(str(x)) if pd.notna(x) else ""
    )
    
    # Thống kê
    print(f"\n📈 Thống kê:")
    print(f"  - Tổng số dòng: {len(df)}")
    print(f"  - Dòng có text gốc: {df[text_column].notna().sum()}")
    print(f"  - Dòng có text sau clean: {(df[cleaned_column] != '').sum()}")
    
    # Lưu file
    print(f"\n💾 Lưu kết quả vào: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ HOÀN THÀNH!")
    print(f"\n📋 Preview (5 dòng đầu):")
    print("="*100)
    
    # Hiển thị preview
    for idx, row in df.head(5).iterrows():
        print(f"\n[Dòng {idx+1}]")
        print(f"  Gốc: {str(row[text_column])[:100]}...")
        print(f"  Clean: {str(row[cleaned_column])[:100]}...")
    
    print("="*100)
    
    return df


def main():
    parser = argparse.ArgumentParser(
        description='Làm sạch text trong file CSV sử dụng advanced_text_cleaning.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  python clean_csv.py data.csv -c comment -o cleaned.csv
  python clean_csv.py input.csv --column text --output output.csv
  python clean_csv.py data.csv -c content --encoding utf-8-sig
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
        help='Đường dẫn file CSV đầu ra (mặc định: <input>_cleaned.csv)'
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
        clean_csv_file(
            input_file=args.input_file,
            output_file=args.output_file,
            text_column=args.text_column,
            encoding=args.encoding
        )
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
