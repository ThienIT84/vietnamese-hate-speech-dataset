"""
Chuyển đổi file CSV sang XLSX
"""

import pandas as pd
import os
from pathlib import Path

def csv_to_xlsx(csv_path, xlsx_path=None):
    """
    Chuyển đổi file CSV sang XLSX
    
    Args:
        csv_path: Đường dẫn file CSV đầu vào
        xlsx_path: Đường dẫn file XLSX đầu ra (mặc định: cùng tên với .xlsx)
    
    Returns:
        Đường dẫn file XLSX đã tạo
    """
    # Nếu không chỉ định xlsx_path, tạo từ csv_path
    if xlsx_path is None:
        xlsx_path = str(Path(csv_path).with_suffix('.xlsx'))
    
    # Đọc CSV
    print(f"📖 Đọc file: {csv_path}")
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"   Số dòng: {len(df):,}")
    print(f"   Số cột: {len(df.columns)}")
    
    # Ghi XLSX
    print(f"💾 Lưu file: {xlsx_path}")
    df.to_excel(xlsx_path, index=False, engine='openpyxl')
    
    print(f"✅ Hoàn tất!")
    return xlsx_path


def batch_csv_to_xlsx(folder_path):
    """
    Chuyển đổi tất cả file CSV trong thư mục sang XLSX
    
    Args:
        folder_path: Đường dẫn thư mục chứa file CSV
    """
    csv_files = list(Path(folder_path).glob('*.csv'))
    
    if not csv_files:
        print(f"❌ Không tìm thấy file CSV trong {folder_path}")
        return
    
    print(f"🔍 Tìm thấy {len(csv_files)} file CSV")
    print("="*60)
    
    for csv_file in csv_files:
        csv_to_xlsx(str(csv_file))
        print()
    
    print("="*60)
    print(f"✅ Đã chuyển đổi {len(csv_files)} file!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Nếu có argument, chuyển đổi file/folder đó
        path = sys.argv[1]
        if os.path.isdir(path):
            batch_csv_to_xlsx(path)
        else:
            csv_to_xlsx(path)
    else:
        # Mặc định: chuyển đổi tất cả file trong labeling/
        print("🔄 Chuyển đổi tất cả file CSV trong labeling/")
        batch_csv_to_xlsx("labeling/")
