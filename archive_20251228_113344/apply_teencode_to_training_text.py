"""
Script để áp dụng teencode dictionary vào cột training_text
Cập nhật các từ như "bitch", "con đĩ" theo teencode dictionary
"""

import pandas as pd
import re
from pathlib import Path

# Import teencode dictionary từ advanced_text_cleaning
import sys
sys.path.append(str(Path(__file__).parent / 'src'))
from preprocessing.advanced_text_cleaning import TEENCODE_DICT, normalize_teencode

def apply_teencode_to_text(text):
    """
    Áp dụng teencode dictionary vào text và rút gọn context
    """
    if pd.isna(text) or text == "":
        return text
    
    # Tách context và comment bằng </s>
    if "</s>" in text:
        parts = text.split("</s>", 1)
        context = parts[0].strip()
        comment = parts[1].strip() if len(parts) > 1 else ""
        
        # Rút gọn context xuống 150 ký tự đầu
        context = context[:150].strip()
        
        # Apply teencode normalization cho cả context và comment
        context = normalize_teencode(context)
        comment = normalize_teencode(comment)
        
        # Ghép lại
        text = f"{context} </s> {comment}"
    else:
        # Nếu không có </s>, chỉ apply teencode bình thường
        text = normalize_teencode(text)
    
    return text

def main():
    # Đường dẫn file
    input_file = Path("data/processed/FINAL_MERGED_3FILES_20251224_184903_LABELED_ONLY_20251224_190142.csv")
    output_file = Path("data/processed/FINAL_MERGED_3FILES_20251224_184903_LABELED_ONLY_20251224_190142_TEENCODE_CONTEXT_150.csv")
    
    print(f"📖 Đọc file: {input_file}")
    df = pd.read_csv(input_file)
    print(f"   ✅ Đọc {len(df)} dòng")
    
    # Backup cột training_text gốc
    df['training_text_original'] = df['training_text'].copy()
    
    print(f"\n🔄 Rút gọn context xuống 150 ký tự và áp dụng teencode...")
    
    # Áp dụng teencode và rút gọn context
    df['training_text'] = df['training_text'].apply(apply_teencode_to_text)
    
    # Đếm số dòng thay đổi
    changed_count = (df['training_text'] != df['training_text_original']).sum()
    print(f"   ✅ Đã cập nhật {changed_count} dòng")
    
    # Kiểm tra độ dài context
    def get_context_length(text):
        if pd.isna(text) or "</s>" not in text:
            return 0
        return len(text.split("</s>", 1)[0].strip())
    
    df['context_length'] = df['training_text'].apply(get_context_length)
    avg_context_len = df['context_length'].mean()
    max_context_len = df['context_length'].max()
    
    print(f"\n📏 Thống kê độ dài context:")
    print(f"   📊 Trung bình: {avg_context_len:.1f} ký tự")
    print(f"   📊 Tối đa: {max_context_len:.0f} ký tự")
    
    # Hiển thị một số ví dụ thay đổi
    print(f"\n📊 Ví dụ các thay đổi:")
    changed_df = df[df['training_text'] != df['training_text_original']].head(5)
    for idx, row in changed_df.iterrows():
        print(f"\n   Dòng {idx}:")
        print(f"   TRƯỚC ({len(row['training_text_original'])} ký tự):")
        print(f"      {row['training_text_original'][:200]}...")
        print(f"   SAU ({len(row['training_text'])} ký tự):")
        print(f"      {row['training_text'][:200]}...")
    
    # Xóa cột context_length
    df.drop('context_length', axis=1, inplace=True)
    
    # Xóa cột backup
    df.drop('training_text_original', axis=1, inplace=True)
    
    # Lưu file
    print(f"\n💾 Lưu file: {output_file}")
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"   ✅ Đã lưu thành công!")
    
    print(f"\n✨ HOÀN TẤT!")
    print(f"   📁 File gốc: {input_file}")
    print(f"   📁 File mới: {output_file}")
    print(f"   📊 Số dòng: {len(df)}")
    print(f"   🔄 Số dòng thay đổi: {changed_count}")

if __name__ == "__main__":
    main()
