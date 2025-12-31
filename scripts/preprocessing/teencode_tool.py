"""
🔧 TEENCODE PROCESSING TOOL
Công cụ xử lý teencode với 3 chức năng chính

Author: Senior AI Engineer
Date: 2025-12-28
"""

import pandas as pd
import sys
import os
from datetime import datetime
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing.advanced_text_cleaning import advanced_clean_text

# =====================================================
# CORE FUNCTIONS
# =====================================================

def process_training_text_column(input_file, output_file=None):
    """
    Chức năng 1: Teencode từ cột 'training_text'
    
    Args:
        input_file: File Excel/CSV có cột 'training_text'
        output_file: File output (tự động tạo nếu None)
    
    Returns:
        DataFrame đã xử lý
    """
    print("\n" + "="*60)
    print("📝 CHỨC NĂNG 1: TEENCODE CỘT 'training_text'")
    print("="*60)
    
    # Load file
    print(f"\n📂 Đang đọc file: {input_file}")
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    elif input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    else:
        raise ValueError("File phải là .xlsx hoặc .csv")
    
    print(f"✓ Đã đọc {len(df)} dòng")
    
    # Check column
    if 'training_text' not in df.columns:
        raise ValueError("File không có cột 'training_text'!")
    
    # Backup
    backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{Path(input_file).name}"
    shutil.copy(input_file, backup)
    print(f"✓ Đã backup: {backup}")
    
    # Process
    print(f"\n🔧 Đang xử lý teencode...")
    processed_count = 0
    
    for idx, row in df.iterrows():
        if pd.notna(row['training_text']):
            original = row['training_text']
            cleaned = advanced_clean_text(original)
            
            if cleaned != original:
                df.loc[idx, 'training_text'] = cleaned
                processed_count += 1
        
        if (idx + 1) % 500 == 0:
            print(f"  Đã xử lý {idx + 1}/{len(df)} dòng...")
    
    print(f"\n✓ Đã xử lý {processed_count} dòng có thay đổi")
    
    # Save
    if output_file is None:
        output_file = f"teencode_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    if output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)
    else:
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✓ Đã lưu: {output_file}")
    
    # Sample
    print(f"\n📊 MẪU KẾT QUẢ (3 dòng đầu):")
    for idx, row in df.head(3).iterrows():
        print(f"\n[{idx}]")
        print(f"  {row['training_text'][:100]}...")
    
    return df


def process_raw_columns(input_file, output_file=None):
    """
    Chức năng 2: Teencode từ 2 cột 'raw_comment' và 'raw_title'
    Tạo cột 'training_text' mới với format: 'title </s> comment'
    
    Args:
        input_file: File Excel/CSV có cột 'raw_comment' và 'raw_title'
        output_file: File output (tự động tạo nếu None)
    
    Returns:
        DataFrame đã xử lý
    """
    print("\n" + "="*60)
    print("📝 CHỨC NĂNG 2: TEENCODE TỪ 'raw_comment' & 'raw_title'")
    print("="*60)
    
    # Load file
    print(f"\n📂 Đang đọc file: {input_file}")
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    elif input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    else:
        raise ValueError("File phải là .xlsx hoặc .csv")
    
    print(f"✓ Đã đọc {len(df)} dòng")
    
    # Check columns
    if 'raw_comment' not in df.columns or 'raw_title' not in df.columns:
        raise ValueError("File phải có cột 'raw_comment' và 'raw_title'!")
    
    # Backup
    backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{Path(input_file).name}"
    shutil.copy(input_file, backup)
    print(f"✓ Đã backup: {backup}")
    
    # Process
    print(f"\n🔧 Đang xử lý teencode và tạo training_text...")
    
    def build_training_text(title, comment):
        """Build training_text: 'title </s> comment'"""
        title = str(title).strip() if pd.notna(title) and str(title).strip() != 'nan' else ''
        comment = str(comment).strip() if pd.notna(comment) and str(comment).strip() != 'nan' else ''
        
        # Clean both
        if title:
            title = advanced_clean_text(title)
        if comment:
            comment = advanced_clean_text(comment)
        
        # Build with separator
        if title and comment:
            return f"{title} </s> {comment}"
        elif comment:
            return comment
        elif title:
            return title
        else:
            return ""
    
    df['training_text'] = df.apply(
        lambda row: build_training_text(row['raw_title'], row['raw_comment']),
        axis=1
    )
    
    # Stats
    has_sep = df['training_text'].str.contains('</s>', na=False).sum()
    print(f"\n✓ Đã tạo {len(df)} dòng training_text")
    print(f"  - Có separator </s>: {has_sep} ({has_sep/len(df)*100:.1f}%)")
    print(f"  - Không có separator: {len(df) - has_sep} ({(len(df)-has_sep)/len(df)*100:.1f}%)")
    
    # Save
    if output_file is None:
        output_file = f"teencode_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    if output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)
    else:
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✓ Đã lưu: {output_file}")
    
    # Sample
    print(f"\n📊 MẪU KẾT QUẢ (3 dòng đầu):")
    for idx, row in df.head(3).iterrows():
        print(f"\n[{idx}]")
        print(f"  {row['training_text'][:100]}...")
    
    return df


def process_any_file(input_file, text_columns, output_file=None):
    """
    Chức năng 3: Teencode từ bất kỳ file nào (CSV, XLSX, JSON)
    
    Args:
        input_file: File input (csv, xlsx, json)
        text_columns: List các cột cần xử lý teencode
        output_file: File output (tự động tạo nếu None)
    
    Returns:
        DataFrame đã xử lý
    """
    print("\n" + "="*60)
    print("📝 CHỨC NĂNG 3: TEENCODE TỪ BẤT KỲ FILE NÀO")
    print("="*60)
    
    # Load file
    print(f"\n📂 Đang đọc file: {input_file}")
    
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    elif input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    elif input_file.endswith('.json'):
        df = pd.read_json(input_file)
    else:
        raise ValueError("File phải là .xlsx, .csv, hoặc .json")
    
    print(f"✓ Đã đọc {len(df)} dòng")
    print(f"✓ Các cột: {df.columns.tolist()}")
    
    # Check columns
    missing_cols = [col for col in text_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"File không có các cột: {missing_cols}")
    
    print(f"\n🔧 Sẽ xử lý các cột: {text_columns}")
    
    # Backup
    backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{Path(input_file).name}"
    shutil.copy(input_file, backup)
    print(f"✓ Đã backup: {backup}")
    
    # Process
    print(f"\n🔧 Đang xử lý teencode...")
    
    for col in text_columns:
        print(f"\n  Đang xử lý cột: {col}")
        processed_count = 0
        
        for idx, row in df.iterrows():
            if pd.notna(row[col]):
                original = str(row[col])
                cleaned = advanced_clean_text(original)
                
                if cleaned != original:
                    df.loc[idx, col] = cleaned
                    processed_count += 1
            
            if (idx + 1) % 500 == 0:
                print(f"    Đã xử lý {idx + 1}/{len(df)} dòng...")
        
        print(f"  ✓ Cột '{col}': {processed_count} dòng có thay đổi")
    
    # Save
    if output_file is None:
        ext = Path(input_file).suffix
        output_file = f"teencode_custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
    
    if output_file.endswith('.xlsx'):
        df.to_excel(output_file, index=False)
    elif output_file.endswith('.csv'):
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
    elif output_file.endswith('.json'):
        df.to_json(output_file, orient='records', force_ascii=False, indent=2)
    
    print(f"\n✓ Đã lưu: {output_file}")
    
    # Sample
    print(f"\n📊 MẪU KẾT QUẢ (3 dòng đầu, các cột đã xử lý):")
    for idx, row in df.head(3).iterrows():
        print(f"\n[{idx}]")
        for col in text_columns:
            print(f"  {col}: {str(row[col])[:80]}...")
    
    return df


# =====================================================
# CLI INTERFACE
# =====================================================

def print_menu():
    """In menu chính"""
    print("\n" + "="*60)
    print("🔧 TEENCODE PROCESSING TOOL")
    print("="*60)
    print("\nChọn chức năng:")
    print("  1. Teencode cột 'training_text'")
    print("  2. Teencode từ 'raw_comment' & 'raw_title' → tạo 'training_text'")
    print("  3. Teencode từ bất kỳ file nào (tùy chỉnh)")
    print("  0. Thoát")
    print("="*60)


def main():
    """Main CLI interface"""
    while True:
        print_menu()
        
        try:
            choice = input("\nNhập lựa chọn (0-3): ").strip()
            
            if choice == '0':
                print("\n👋 Tạm biệt!")
                break
            
            elif choice == '1':
                # Chức năng 1
                input_file = input("\nNhập đường dẫn file input: ").strip()
                output_file = input("Nhập đường dẫn file output (Enter để tự động): ").strip()
                
                if not output_file:
                    output_file = None
                
                process_training_text_column(input_file, output_file)
                
                input("\n✅ Hoàn thành! Nhấn Enter để tiếp tục...")
            
            elif choice == '2':
                # Chức năng 2
                input_file = input("\nNhập đường dẫn file input: ").strip()
                output_file = input("Nhập đường dẫn file output (Enter để tự động): ").strip()
                
                if not output_file:
                    output_file = None
                
                process_raw_columns(input_file, output_file)
                
                input("\n✅ Hoàn thành! Nhấn Enter để tiếp tục...")
            
            elif choice == '3':
                # Chức năng 3
                input_file = input("\nNhập đường dẫn file input: ").strip()
                
                # Đọc file để hiển thị columns
                if input_file.endswith('.xlsx'):
                    df_temp = pd.read_excel(input_file)
                elif input_file.endswith('.csv'):
                    df_temp = pd.read_csv(input_file)
                elif input_file.endswith('.json'):
                    df_temp = pd.read_json(input_file)
                else:
                    print("❌ File phải là .xlsx, .csv, hoặc .json")
                    continue
                
                print(f"\n📋 Các cột có sẵn: {df_temp.columns.tolist()}")
                
                text_columns_str = input("\nNhập các cột cần xử lý (cách nhau bởi dấu phẩy): ").strip()
                text_columns = [col.strip() for col in text_columns_str.split(',')]
                
                output_file = input("Nhập đường dẫn file output (Enter để tự động): ").strip()
                
                if not output_file:
                    output_file = None
                
                process_any_file(input_file, text_columns, output_file)
                
                input("\n✅ Hoàn thành! Nhấn Enter để tiếp tục...")
            
            else:
                print("\n❌ Lựa chọn không hợp lệ!")
        
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"\n❌ Lỗi: {e}")
            input("\nNhấn Enter để tiếp tục...")


if __name__ == "__main__":
    # Check if running with arguments (for automation)
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == '1':
            # Function 1
            input_file = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else None
            process_training_text_column(input_file, output_file)
        
        elif sys.argv[1] == '2':
            # Function 2
            input_file = sys.argv[2]
            output_file = sys.argv[3] if len(sys.argv) > 3 else None
            process_raw_columns(input_file, output_file)
        
        elif sys.argv[1] == '3':
            # Function 3
            input_file = sys.argv[2]
            text_columns = sys.argv[3].split(',')
            output_file = sys.argv[4] if len(sys.argv) > 4 else None
            process_any_file(input_file, text_columns, output_file)
        
        else:
            print("Usage:")
            print("  python teencode_tool.py 1 <input_file> [output_file]")
            print("  python teencode_tool.py 2 <input_file> [output_file]")
            print("  python teencode_tool.py 3 <input_file> <columns> [output_file]")
    else:
        # Interactive mode
        main()
