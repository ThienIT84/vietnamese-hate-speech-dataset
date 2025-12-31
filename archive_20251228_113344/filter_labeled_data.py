import pandas as pd
import sys
from datetime import datetime

def filter_labeled_data(input_file, output_file=None):
    """
    Lọc dữ liệu chỉ giữ lại các dòng đã được gắn nhãn.
    Loại bỏ các dòng chưa có nhãn (NaN, None, empty string).
    """
    print(f"Đang đọc file: {input_file}")
    
    # Đọc file CSV
    df = pd.read_csv(input_file)
    
    print(f"Tổng số dòng ban đầu: {len(df)}")
    print(f"Các cột trong file: {list(df.columns)}")
    
    # Tìm cột nhãn (label) - thường là 'label', 'Label', 'labels', etc.
    label_columns = [col for col in df.columns if 'label' in col.lower()]
    
    if not label_columns:
        print("\nKhông tìm thấy cột nhãn. Các cột có sẵn:")
        for col in df.columns:
            print(f"  - {col}")
        print("\nVui lòng chỉ định tên cột nhãn:")
        return
    
    # Sử dụng cột nhãn đầu tiên tìm được
    label_col = label_columns[0]
    print(f"\nSử dụng cột nhãn: '{label_col}'")
    
    # Đếm số lượng nhãn trước khi lọc
    print(f"\nPhân bố nhãn trước khi lọc:")
    print(df[label_col].value_counts(dropna=False))
    
    # Lọc: chỉ giữ các dòng có nhãn (không phải NaN, None, hoặc chuỗi rỗng)
    df_labeled = df[df[label_col].notna() & (df[label_col] != '') & (df[label_col] != ' ')]
    
    print(f"\nSố dòng sau khi lọc: {len(df_labeled)}")
    print(f"Số dòng đã loại bỏ: {len(df) - len(df_labeled)}")
    
    # Phân bố nhãn sau khi lọc
    print(f"\nPhân bố nhãn sau khi lọc:")
    print(df_labeled[label_col].value_counts())
    
    # Tạo tên file output nếu chưa có
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = input_file.replace('.csv', f'_LABELED_ONLY_{timestamp}.csv')
    
    # Lưu file
    df_labeled.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ Đã lưu file đã lọc: {output_file}")
    
    return df_labeled

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách sử dụng: python filter_labeled_data.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    filter_labeled_data(input_file, output_file)
