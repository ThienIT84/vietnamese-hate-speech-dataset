"""
Test script cho process_csv_with_context.py
Tạo CSV và XLSX test và chạy xử lý để demo
"""

import pandas as pd
import os
import sys

def create_test_files():
    """Tạo file CSV và XLSX test với nhiều trường hợp"""
    
    test_data = [
        # Case 1: Có title, có emoji, có teencode
        {
            'text': 'mày béo như lợn vcl 💔',
            'title': 'Hằng Du Mục về Việt Nam 🏳️‍🌈',
            'label': None,
            'note': ''
        },
        # Case 2: Có title, có hashtag
        {
            'text': '#fyp #xuhuong video này hay quá',
            'title': 'Reaction clip viral',
            'label': 0,
            'note': ''
        },
        # Case 3: Không có title
        {
            'text': 'đcm mày làm gì vậy tml',
            'title': '',
            'label': 1,
            'note': 'toxic'
        },
        # Case 4: Nhiều emoji
        {
            'text': 'Tôi yêu bạn ❤️ 😍 🥰',
            'title': 'Confession NEU',
            'label': 0,
            'note': ''
        },
        # Case 5: Body shaming
        {
            'text': 'thằng lùn này béo như con lợn',
            'title': 'Drama showbiz',
            'label': 2,
            'note': 'body_shaming'
        },
        # Case 6: Vùng miền
        {
            'text': 'mày bắc kỳ à parky cho',
            'title': 'Tranh luận vùng miền',
            'label': 2,
            'note': 'region_discrimination'
        },
    ]
    
    df = pd.DataFrame(test_data)
    
    # Lưu CSV
    csv_file = 'test_input.csv'
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print("✓ Đã tạo CSV test file:", csv_file)
    
    # Lưu XLSX
    try:
        xlsx_file = 'test_input.xlsx'
        df.to_excel(xlsx_file, index=False, engine='openpyxl')
        print("✓ Đã tạo XLSX test file:", xlsx_file)
        print(f"  Số dòng: {len(df)}")
        return csv_file, xlsx_file
    except ImportError:
        print("⚠️ Không có openpyxl, chỉ tạo CSV")
        print("  Cài đặt: pip install openpyxl")
        print(f"  Số dòng: {len(df)}")
        return csv_file, None

def run_test():
    """Chạy test"""
    print("="*80)
    print("TEST process_csv_with_context.py")
    print("="*80)
    
    # Tạo test files
    csv_file, xlsx_file = create_test_files()
    
    # Import module
    from process_csv_with_context import process_csv
    
    # Test CSV
    print("\n" + "="*80)
    print("TEST 1: XỬ LÝ FILE CSV")
    print("="*80 + "\n")
    
    csv_output = 'test_output.csv'
    result_csv = process_csv(csv_file, csv_output)
    
    if result_csv is not None:
        print(f"\n✓ CSV test PASS - Output: {csv_output}")
    
    # Test XLSX nếu có
    if xlsx_file:
        print("\n" + "="*80)
        print("TEST 2: XỬ LÝ FILE XLSX")
        print("="*80 + "\n")
        
        xlsx_output = 'test_output.xlsx'
        result_xlsx = process_csv(xlsx_file, xlsx_output)
        
        if result_xlsx is not None:
            print(f"\n✓ XLSX test PASS - Output: {xlsx_output}")
    else:
        result_xlsx = None
    
    # Chọn result để check (ưu tiên CSV)
    result_df = result_csv if result_csv is not None else result_xlsx
    
    # Kiểm tra kết quả
    print("\n" + "="*80)
    print("KIỂM TRA KẾT QUẢ")
    print("="*80)
    
    if result_df is not None:
        print(f"\n✓ Output có {len(result_df)} dòng")
        
        # Check 1: Có separator </s>?
        has_separator = result_df['input_text'].str.contains('</s>').sum()
        print(f"\n1. Separator </s>: {has_separator}/{len(result_df)} dòng có separator")
        
        # Check 2: Emoji đã convert?
        original_df = pd.read_csv(csv_file)
        original_emojis = original_df['text'].str.contains('❤️|💔|🏳️‍🌈|😍|🥰').sum()
        processed_emojis = result_df['input_text'].str.contains('❤️|💔|🏳️‍🌈|😍|🥰').sum()
        print(f"\n2. Emoji conversion:")
        print(f"   - Original: {original_emojis} dòng có emoji")
        print(f"   - Processed: {processed_emojis} dòng còn emoji")
        print(f"   - {'✓ PASS' if processed_emojis == 0 else '✗ FAIL - vẫn còn emoji'}")
        
        # Check 3: Hashtag đã xóa?
        original_hashtags = original_df['text'].str.contains('#').sum()
        processed_hashtags = result_df['input_text'].str.contains('#').sum()
        print(f"\n3. Hashtag removal:")
        print(f"   - Original: {original_hashtags} dòng có hashtag")
        print(f"   - Processed: {processed_hashtags} dòng còn hashtag")
        print(f"   - {'✓ PASS' if processed_hashtags == 0 else '✗ FAIL - vẫn còn hashtag'}")
        
        # Check 4: Teencode đã normalize?
        print(f"\n4. Teencode normalization:")
        examples = [
            ('vcl', 'vãi chưởng'),
            ('đcm', 'đụ cụ'),
            ('tml', 'thằng mặt'),
        ]
        for original, normalized in examples:
            has_original = result_df['raw_comment'].str.contains(original, case=False).sum()
            has_normalized = result_df['input_text'].str.contains(normalized, case=False).sum()
            if has_original > 0:
                print(f"   - '{original}' → '{normalized}': {'✓' if has_normalized > 0 else '✗'}")
        
        # Check 5: Label được giữ nguyên?
        original_labels = original_df['label'].notna().sum()
        processed_labels = result_df['label'].notna().sum()
        print(f"\n5. Label preservation:")
        print(f"   - Original: {original_labels} dòng có label")
        print(f"   - Processed: {processed_labels} dòng có label")
        print(f"   - {'✓ PASS' if original_labels == processed_labels else '✗ FAIL'}")
        
        # Hiển thị chi tiết một vài mẫu
        print(f"\n" + "="*80)
        print("CHI TIẾT MỘT SỐ MẪU")
        print("="*80)
        
        for i in range(min(3, len(result_df))):
            row = result_df.iloc[i]
            print(f"\n--- Mẫu {i+1} ---")
            print(f"Raw comment: {row['raw_comment']}")
            print(f"Raw title:   {row['raw_title']}")
            print(f"Input text:  {row['input_text']}")
            if pd.notna(row['label']):
                print(f"Label:       {row['label']}")
            if pd.notna(row['note']) and row['note']:
                print(f"Note:        {row['note']}")
        
        print(f"\n" + "="*80)
        print("✅ TEST HOÀN TẤT")
        print("="*80)
        print(f"\nFiles output:")
        if result_csv is not None:
            print(f"  - CSV: test_output.csv")
        if xlsx_file and result_xlsx is not None:
            print(f"  - XLSX: test_output.xlsx")
        print("\nMở file để xem chi tiết hoặc import vào Excel/Google Sheets")
        
    else:
        print("❌ Xử lý thất bại!")

if __name__ == "__main__":
    run_test()
