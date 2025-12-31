"""
Tạo dataset với 2 versions:
- training_text_original: Giữ nguyên teencode (đm, dm...)
- training_text_expanded: Expand đầy đủ (địt mẹ...)

Lúc training có thể chọn version phù hợp hoặc train cả 2
"""

import pandas as pd
from datetime import datetime
import re

def create_dual_version_dataset(input_file):
    """
    Tạo dataset với 2 versions của text
    """
    df = pd.read_excel(input_file)
    
    print(f"Đọc file: {input_file}")
    print(f"Số dòng: {len(df)}")
    
    # Teencode mapping
    teencode_map = {
        r'\b(đm|dm)\b': 'địt mẹ',
        r'\b(đcm|dcm)\b': 'địt con mẹ',
        r'\b(dmm)\b': 'địt mẹ mày',
        r'\b(đkm|dkm)\b': 'đéo kệ mày',
        r'\b(vl)\b': 'vãi lồn',
        r'\b(vcl)\b': 'vãi cái lồn',
        r'\b(clm)\b': 'cái lồn mẹ',
        r'\b(cc)\b': 'cặc',
    }
    
    # Tạo version expanded (từ text_raw)
    def expand_teencode(text):
        if pd.isna(text):
            return text
        result = text
        for pattern, replacement in teencode_map.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result
    
    # Nếu có text_raw, dùng nó làm original
    if 'text_raw' in df.columns:
        df['training_text_original'] = df['text_raw'].fillna(df['training_text'])
    else:
        # Nếu không có text_raw, cố gắng reverse expand
        df['training_text_original'] = df['training_text']
    
    # Expanded version
    df['training_text_expanded'] = df['training_text_original'].apply(expand_teencode)
    
    # Đánh dấu những dòng có sự khác biệt
    df['has_expansion'] = df['training_text_original'] != df['training_text_expanded']
    
    # Thống kê
    print(f"\n=== THỐNG KÊ ===")
    print(f"Số dòng có teencode expansion: {df['has_expansion'].sum()}")
    print(f"Phân bố nhãn:")
    print(df['label'].value_counts().sort_index())
    
    print(f"\nPhân bố nhãn trong các dòng có expansion:")
    print(df[df['has_expansion']]['label'].value_counts().sort_index())
    
    # Hiển thị mẫu
    print(f"\n=== MẪU DỮ LIỆU ===")
    sample = df[df['has_expansion']].head(5)
    for idx, row in sample.iterrows():
        print(f"\n[Label: {row['label']}]")
        print(f"Original: {row['training_text_original'][:100]}")
        print(f"Expanded: {row['training_text_expanded'][:100]}")
    
    # Save
    output_file = f"DUAL_VERSION_DATASET_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\n✓ Đã lưu file: {output_file}")
    
    # Tạo 2 file riêng cho 2 versions
    df_original = df[['training_text_original', 'label', 'note', 'source_file']].copy()
    df_original.rename(columns={'training_text_original': 'text'}, inplace=True)
    df_original.to_excel(f"TRAINING_ORIGINAL_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", index=False)
    
    df_expanded = df[['training_text_expanded', 'label', 'note', 'source_file']].copy()
    df_expanded.rename(columns={'training_text_expanded': 'text'}, inplace=True)
    df_expanded.to_excel(f"TRAINING_EXPANDED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", index=False)
    
    print(f"✓ Đã tạo 2 file training riêng biệt")
    
    return df

if __name__ == "__main__":
    input_file = "FINAL_TRAINING_DATASET_TEENCODE_20251225_151716.xlsx"
    create_dual_version_dataset(input_file)
