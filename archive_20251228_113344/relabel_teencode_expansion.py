"""
Script để tìm và re-label các trường hợp teencode expansion có thể sai nhãn
Vấn đề: "đm" (nhãn 0) vs "địt mẹ" (nên là nhãn 1)
"""

import pandas as pd
import re
from datetime import datetime

# Đọc file training
input_file = "FINAL_TRAINING_DATASET_TEENCODE_20251225_151716.xlsx"
df = pd.read_excel(input_file)

print(f"Tổng số dòng: {len(df)}")

# Các pattern teencode viết tắt
teencode_patterns = [
    r'\b(đm|dm|đcm|dcm|dmm|dkm|đkm)\b',  # các dạng viết tắt
]

# Các từ đã expand
expanded_words = ['địt mẹ', 'đụ má', 'đéo mẹ']

# Tìm các dòng có vấn đề
problematic_rows = []

for idx, row in df.iterrows():
    training_text = str(row['training_text']).lower()
    text_raw = str(row['text_raw']).lower() if pd.notna(row['text_raw']) else ""
    label = row['label']
    
    # Kiểm tra nếu training_text có từ expanded
    has_expanded = any(word in training_text for word in expanded_words)
    
    if has_expanded:
        # Kiểm tra xem text_raw có dạng viết tắt không
        has_teencode = any(re.search(pattern, text_raw, re.IGNORECASE) for pattern in teencode_patterns)
        
        if has_teencode:
            # Đây là trường hợp cần review
            problematic_rows.append({
                'index': idx,
                'training_text': row['training_text'],
                'text_raw': row['text_raw'],
                'current_label': label,
                'suggested_label': 1 if label == 0 else label,  # Suggest label 1 nếu đang là 0
                'reason': 'Teencode expansion: viết tắt -> từ tục tĩu rõ ràng',
                'note': row.get('note', ''),
                'source_file': row.get('source_file', '')
            })

print(f"\nTìm thấy {len(problematic_rows)} dòng cần review")

if problematic_rows:
    # Tạo DataFrame
    review_df = pd.DataFrame(problematic_rows)
    
    # Thống kê
    print("\n=== THỐNG KÊ ===")
    print(f"Nhãn 0 (cần đổi sang 1): {len(review_df[review_df['current_label'] == 0])}")
    print(f"Nhãn 1 (giữ nguyên): {len(review_df[review_df['current_label'] == 1])}")
    print(f"Nhãn 2 (giữ nguyên): {len(review_df[review_df['current_label'] == 2])}")
    
    # Hiển thị mẫu
    print("\n=== MẪU CẦN REVIEW ===")
    for i, row in review_df.head(10).iterrows():
        print(f"\n[{i+1}] Label hiện tại: {row['current_label']} -> Đề xuất: {row['suggested_label']}")
        print(f"Raw: {row['text_raw'][:100]}")
        print(f"Training: {row['training_text'][:100]}")
    
    # Export ra file để review
    output_file = f"REVIEW_TEENCODE_EXPANSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    review_df.to_excel(output_file, index=False)
    print(f"\n✓ Đã export file review: {output_file}")
    print(f"  Bạn có thể mở file này, review và sửa cột 'suggested_label' thành nhãn đúng")
    
    # Tạo script apply changes
    print("\n=== HƯỚNG DẪN ===")
    print("1. Mở file review vừa tạo")
    print("2. Kiểm tra và sửa cột 'suggested_label' nếu cần")
    print("3. Chạy script 'apply_relabel_changes.py' để apply changes vào file gốc")
else:
    print("Không tìm thấy dòng nào cần review")
