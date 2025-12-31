"""
🔧 FIX MISLABELED EXPANDED TEENCODE
Vấn đề: File training đã expand teencode TRƯỚC KHI gán nhãn
→ Có thể có nhãn sai: "địt mẹ game hay" được gán Label 0 (sai!)

Giải pháp:
1. Tìm các dòng có từ explicit (địt mẹ, vãi lồn...) nhưng nhãn = 0
2. Kiểm tra text_raw có dạng viết tắt không
3. Nếu có → Đề xuất re-label hoặc revert về dạng viết tắt

Author: Senior AI Engineer
Date: 2025-12-28
"""

import pandas as pd
import re
from datetime import datetime
import shutil

# Các từ explicit (đã expand)
EXPLICIT_WORDS = [
    'địt mẹ', 'địt con mẹ', 'vãi lồn', 'vãi cái lồn', 
    'cái lồn mẹ', 'đụ má', 'đéo mẹ',
    'con mẹ nó lồn', 'địt mẹ mày',
]

# Các từ viết tắt tương ứng
TEENCODE_ABBREV = [
    r'\b(đm|dm)\b',
    r'\b(đcm|dcm)\b', 
    r'\b(vl|vcl)\b',
    r'\b(vcl)\b',
    r'\b(clm)\b',
    r'\b(dma|duma)\b',
    r'\b(đéo)\b',
    r'\b(cmnl)\b',
    r'\b(dmm)\b',
]

def check_mislabeled_expansion(input_file):
    """
    Kiểm tra các trường hợp có thể bị gán nhãn sai do expand teencode
    """
    df = pd.read_excel(input_file)
    
    print(f"📊 Tổng số dòng: {len(df)}")
    print(f"📊 Phân bố nhãn:")
    print(df['label'].value_counts().sort_index())
    
    # Tìm các dòng nghi ngờ
    suspicious_rows = []
    
    for idx, row in df.iterrows():
        training_text = str(row['training_text']).lower()
        text_raw = str(row['text_raw']).lower() if pd.notna(row['text_raw']) else ""
        label = row['label']
        
        # Chỉ check Label 0 (vì Label 1,2 có thể có từ explicit)
        if label != 0:
            continue
        
        # Kiểm tra có từ explicit không
        has_explicit = any(word in training_text for word in EXPLICIT_WORDS)
        
        if has_explicit:
            # Kiểm tra text_raw có dạng viết tắt không
            has_abbrev = any(re.search(pattern, text_raw, re.IGNORECASE) for pattern in TEENCODE_ABBREV)
            
            if has_abbrev:
                suspicious_rows.append({
                    'index': idx,
                    'training_text': row['training_text'],
                    'text_raw': row['text_raw'],
                    'current_label': label,
                    'issue': 'Expanded teencode in Label 0',
                    'suggestion': 'Revert to abbrev form OR re-check label',
                    'note': row.get('note', ''),
                    'source_file': row.get('source_file', '')
                })
    
    print(f"\n⚠️  Tìm thấy {len(suspicious_rows)} dòng nghi ngờ (Label 0 nhưng có từ explicit)")
    
    if not suspicious_rows:
        print("✅ Không có vấn đề! Dataset của bạn đã clean.")
        return None
    
    # Tạo DataFrame
    review_df = pd.DataFrame(suspicious_rows)
    
    # Hiển thị mẫu
    print("\n=== MẪU CẦN REVIEW ===")
    for i, row in review_df.head(10).iterrows():
        print(f"\n[{i+1}] Index: {row['index']}")
        print(f"Label: {row['current_label']}")
        print(f"Raw: {row['text_raw'][:100]}")
        print(f"Training: {row['training_text'][:100]}")
        print(f"Issue: {row['issue']}")
    
    # Export
    output_file = f"SUSPICIOUS_LABEL0_EXPANSION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    review_df.to_excel(output_file, index=False)
    print(f"\n✓ Đã export: {output_file}")
    
    return review_df

def revert_to_abbrev_form(input_file, output_file=None):
    """
    Revert các từ explicit về dạng viết tắt cho Label 0
    (Chỉ áp dụng nếu bạn muốn giữ nguyên nhãn)
    """
    df = pd.read_excel(input_file)
    
    # Backup
    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{input_file}"
    shutil.copy(input_file, backup_file)
    print(f"✓ Backup: {backup_file}")
    
    # Mapping để revert
    revert_map = {
        'địt mẹ': 'đm',
        'địt con mẹ': 'đcm',
        'vãi lồn': 'vl',
        'vãi cái lồn': 'vcl',
        'cái lồn mẹ': 'clm',
        'đụ má': 'duma',
        'con mẹ nó lồn': 'cmnl',
        'địt mẹ mày': 'dmm',
    }
    
    changes = 0
    for idx, row in df.iterrows():
        if row['label'] == 0:  # Chỉ revert Label 0
            training_text = row['training_text']
            
            for explicit, abbrev in revert_map.items():
                if explicit in training_text.lower():
                    # Revert
                    training_text = re.sub(
                        r'\b' + re.escape(explicit) + r'\b',
                        abbrev,
                        training_text,
                        flags=re.IGNORECASE
                    )
                    changes += 1
            
            df.loc[idx, 'training_text'] = training_text
            
            # Add note
            if changes > 0:
                current_note = df.loc[idx, 'note']
                if pd.isna(current_note):
                    df.loc[idx, 'note'] = "Reverted explicit to abbrev (Label 0)"
                else:
                    df.loc[idx, 'note'] = f"{current_note}; Reverted to abbrev"
    
    print(f"\n✓ Đã revert {changes} từ explicit → abbrev")
    
    # Save
    if output_file is None:
        output_file = f"REVERTED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df.to_excel(output_file, index=False)
    print(f"✓ Đã lưu: {output_file}")
    
    return df

if __name__ == "__main__":
    import sys
    
    input_file = "FINAL_TRAINING_DATASET_TEENCODE_20251225_151716.xlsx"
    
    print("=" * 60)
    print("🔍 KIỂM TRA MISLABELED EXPANDED TEENCODE")
    print("=" * 60)
    
    # Step 1: Check
    review_df = check_mislabeled_expansion(input_file)
    
    if review_df is not None:
        print("\n" + "=" * 60)
        print("💡 BẠN CÓ 2 LỰA CHỌN:")
        print("=" * 60)
        print("1. RE-LABEL: Mở file review, sửa nhãn 0→1 cho các dòng thực sự toxic")
        print("2. REVERT: Chạy revert_to_abbrev_form() để đổi 'địt mẹ'→'đm' (giữ nhãn 0)")
        print("\nGợi ý: Nếu < 50 dòng → RE-LABEL (chính xác hơn)")
        print("       Nếu > 100 dòng → REVERT (nhanh hơn)")
        
        # Uncomment để tự động revert
        # print("\n🔧 Đang revert...")
        # revert_to_abbrev_form(input_file)
