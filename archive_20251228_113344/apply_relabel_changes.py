"""
Script để apply các thay đổi nhãn từ file review vào file training gốc
"""

import pandas as pd
from datetime import datetime
import shutil

def apply_relabel_changes(review_file, original_file):
    """
    Apply changes từ file review vào file gốc
    """
    # Backup file gốc
    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{original_file}"
    shutil.copy(original_file, backup_file)
    print(f"✓ Đã backup file gốc: {backup_file}")
    
    # Đọc files
    review_df = pd.read_excel(review_file)
    original_df = pd.read_excel(original_file)
    
    print(f"\nFile review: {len(review_df)} dòng cần update")
    print(f"File gốc: {len(original_df)} dòng")
    
    # Apply changes
    changes_count = 0
    for _, row in review_df.iterrows():
        idx = row['index']
        new_label = row['suggested_label']
        old_label = original_df.loc[idx, 'label']
        
        if old_label != new_label:
            original_df.loc[idx, 'label'] = new_label
            # Thêm note
            current_note = original_df.loc[idx, 'note']
            if pd.isna(current_note):
                original_df.loc[idx, 'note'] = f"Re-labeled: {old_label}->{new_label} (teencode expansion)"
            else:
                original_df.loc[idx, 'note'] = f"{current_note}; Re-labeled: {old_label}->{new_label}"
            changes_count += 1
    
    print(f"\n✓ Đã update {changes_count} nhãn")
    
    # Save file mới
    output_file = f"FINAL_TRAINING_DATASET_RELABELED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    original_df.to_excel(output_file, index=False)
    print(f"✓ Đã lưu file mới: {output_file}")
    
    # Thống kê
    print("\n=== THỐNG KÊ NHÃN SAU KHI UPDATE ===")
    print(original_df['label'].value_counts().sort_index())
    
    return output_file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python apply_relabel_changes.py <review_file>")
        print("\nHoặc tự động tìm file review mới nhất:")
        import glob
        review_files = glob.glob("REVIEW_TEENCODE_EXPANSION_*.xlsx")
        if review_files:
            review_file = max(review_files)
            print(f"Sử dụng file: {review_file}")
        else:
            print("Không tìm thấy file review nào!")
            sys.exit(1)
    else:
        review_file = sys.argv[1]
    
    original_file = "FINAL_TRAINING_DATASET_TEENCODE_20251225_151716.xlsx"
    
    apply_relabel_changes(review_file, original_file)
