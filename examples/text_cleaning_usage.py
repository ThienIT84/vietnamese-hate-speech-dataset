# -*- coding: utf-8 -*-
"""
📚 USAGE EXAMPLES - Advanced Text Cleaning V2.1

Hướng dẫn sử dụng module text cleaning cho các tình huống khác nhau
"""

import sys
import pandas as pd
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessing.advanced_text_cleaning import (
    clean_text, 
    clean_dataframe, 
    clean_file
)

# =====================================================
# EXAMPLE 1: Clean Single Text
# =====================================================

def example_single_text():
    """Xử lý một đoạn text đơn lẻ"""
    print("\n" + "="*70)
    print("📝 EXAMPLE 1: Clean Single Text")
    print("="*70)
    
    text = "Đ.m thằng Nguyễn Văn A nguuuuu vcl 😡😡"
    cleaned = clean_text(text)
    
    print(f"Input:  {text}")
    print(f"Output: {cleaned}")


# =====================================================
# EXAMPLE 2: Clean DataFrame
# =====================================================

def example_dataframe():
    """Xử lý DataFrame với nhiều dòng text"""
    print("\n" + "="*70)
    print("📊 EXAMPLE 2: Clean DataFrame")
    print("="*70)
    
    # Tạo sample DataFrame
    data = {
        'id': [1, 2, 3, 4, 5],
        'comment': [
            "Nguuuuu vcl 😡",
            "Đẹp quá @user123 ❤️",
            "Bộ Mặt Thật của người này",
            "Thạch Trang xinh :))",
            "stupid vl nguuuuu"
        ]
    }
    df = pd.DataFrame(data)
    
    print("\nOriginal DataFrame:")
    print(df)
    
    # Clean DataFrame
    df_cleaned = clean_dataframe(df, text_column='comment', show_progress=False)
    
    print("\nCleaned DataFrame:")
    print(df_cleaned[['id', 'comment', 'comment_cleaned']])


# =====================================================
# EXAMPLE 3: Clean CSV File
# =====================================================

def example_csv_file():
    """Xử lý file CSV"""
    print("\n" + "="*70)
    print("📁 EXAMPLE 3: Clean CSV File")
    print("="*70)
    
    # Tạo sample CSV
    sample_data = pd.DataFrame({
        'id': range(1, 11),
        'text': [
            f"Comment number {i} with nguuuu vcl 😡" 
            for i in range(1, 11)
        ]
    })
    
    input_file = Path('temp_input.csv')
    sample_data.to_csv(input_file, index=False)
    print(f"✅ Created sample file: {input_file}")
    
    # Clean file
    df_cleaned = clean_file(
        input_path=input_file,
        output_path='temp_output.csv',
        text_column='text',
        show_progress=True
    )
    
    print(f"\n📊 Sample output:")
    print(df_cleaned[['id', 'text', 'text_cleaned']].head(3))
    
    # Cleanup
    input_file.unlink()
    Path('temp_output.csv').unlink()
    print("\n🗑️ Cleaned up temporary files")


# =====================================================
# EXAMPLE 4: Clean Excel File
# =====================================================

def example_excel_file():
    """Xử lý file Excel"""
    print("\n" + "="*70)
    print("📗 EXAMPLE 4: Clean Excel File")
    print("="*70)
    
    # Tạo sample Excel
    sample_data = pd.DataFrame({
        'id': range(1, 6),
        'feedback': [
            "Nguyễn Văn A ngu quá",
            "Đẹp 😍❤️",
            "@user123 stupid vl",
            "Bộ Mặt Thật",
            "nguuuuuu ch3t đi"
        ]
    })
    
    input_file = Path('temp_input.xlsx')
    sample_data.to_excel(input_file, index=False)
    print(f"✅ Created sample file: {input_file}")
    
    # Clean file
    df_cleaned = clean_file(
        input_path=input_file,
        output_path='temp_output.xlsx',
        text_column='feedback',
        show_progress=True
    )
    
    print(f"\n📊 Sample output:")
    print(df_cleaned[['id', 'feedback', 'feedback_cleaned']].head())
    
    # Cleanup
    input_file.unlink()
    Path('temp_output.xlsx').unlink()
    print("\n🗑️ Cleaned up temporary files")


# =====================================================
# EXAMPLE 5: Custom Output Column
# =====================================================

def example_custom_output():
    """Tùy chỉnh tên cột output"""
    print("\n" + "="*70)
    print("⚙️ EXAMPLE 5: Custom Output Column Name")
    print("="*70)
    
    df = pd.DataFrame({
        'raw_text': ["nguuuu vcl 😡", "đẹp quá ❤️"]
    })
    
    df_cleaned = clean_dataframe(
        df, 
        text_column='raw_text',
        output_column='processed_text',
        show_progress=False
    )
    
    print(df_cleaned)


# =====================================================
# EXAMPLE 6: Error Handling
# =====================================================

def example_error_handling():
    """Xử lý lỗi khi có dữ liệu bị lỗi"""
    print("\n" + "="*70)
    print("🛡️ EXAMPLE 6: Error Handling")
    print("="*70)
    
    df = pd.DataFrame({
        'text': [
            "Normal text",
            None,  # Null value
            123,   # Number instead of string
            "Good text"
        ]
    })
    
    print("\nOriginal DataFrame:")
    print(df)
    
    # Clean with error handling (default)
    df_cleaned = clean_dataframe(df, text_column='text', show_progress=False)
    
    print("\nCleaned DataFrame (errors handled):")
    print(df_cleaned[['text', 'text_cleaned']])


# =====================================================
# RUN ALL EXAMPLES
# =====================================================

if __name__ == "__main__":
    print("\n" + "🚀"*35)
    print("ADVANCED TEXT CLEANING V2.1 - USAGE EXAMPLES")
    print("🚀"*35)
    
    examples = [
        ("Single Text", example_single_text),
        ("DataFrame", example_dataframe),
        ("CSV File", example_csv_file),
        ("Excel File", example_excel_file),
        ("Custom Output", example_custom_output),
        ("Error Handling", example_error_handling),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
    
    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70)
    print("\n📚 For more info, run: python advanced_text_cleaning.py --help")
