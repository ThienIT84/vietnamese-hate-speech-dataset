"""
🔧 REBUILD DATASET WITH INTENSITY PRESERVATION
Rebuild lại training_text từ text_raw với strategy mới (giữ nguyên dcm, vl, vcl...)

Author: Senior AI Engineer
Date: 2025-12-28
"""

import pandas as pd
import sys
import os
from datetime import datetime
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing.advanced_text_cleaning import advanced_clean_text

def rebuild_training_text_from_text_raw(input_file, output_file=None):
    """
    Rebuild training_text từ text_raw với Intensity Preservation strategy mới
    
    Args:
        input_file: File Excel có cột text_raw
        output_file: File output (tự động tạo nếu None)
    """
    print("\n" + "="*70)
    print("🔧 REBUILD WITH INTENSITY PRESERVATION")
    print("="*70)
    
    # Load file
    print(f"\n📂 Đang đọc file: {input_file}")
    df = pd.read_excel(input_file)
    print(f"✓ Đã đọc {len(df)} dòng")
    
    # Check columns
    if 'text_raw' not in df.columns:
        raise ValueError("File không có cột 'text_raw'!")
    
    # Backup
    backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_before_intensity_rebuild.xlsx"
    shutil.copy(input_file, backup)
    print(f"✓ Đã backup: {backup}")
    
    # Process
    print(f"\n🔧 Đang rebuild training_text với Intensity Preservation...")
    print(f"   Strategy: Giữ nguyên dcm, vl, vcl, đm, cc...")
    
    changed_count = 0
    sample_changes = []
    
    for idx, row in df.iterrows():
        if pd.notna(row['text_raw']):
            text_raw = str(row['text_raw']).strip()
            
            # Clean with NEW strategy (Intensity Preservation)
            new_training_text = advanced_clean_text(text_raw)
            
            # Compare with old
            old_training_text = str(row.get('training_text', '')).strip()
            
            if new_training_text != old_training_text:
                df.loc[idx, 'training_text'] = new_training_text
                changed_count += 1
                
                # Collect samples (first 5)
                if len(sample_changes) < 5:
                    sample_changes.append({
                        'idx': idx,
                        'text_raw': text_raw[:80],
                        'old': old_training_text[:80],
                        'new': new_training_text[:80]
                    })
        
        if (idx + 1) % 500 == 0:
            print(f"  Đã xử lý {idx + 1}/{len(df)} dòng...")
    
    print(f"\n✓ Đã rebuild {changed_count} dòng có thay đổi ({changed_count/len(df)*100:.1f}%)")
    
    # Show samples
    if sample_changes:
        print(f"\n📊 MẪU THAY ĐỔI (5 dòng đầu):")
        for s in sample_changes:
            print(f"\n[{s['idx']}]")
            print(f"  Raw:  {s['text_raw']}...")
            print(f"  Old:  {s['old']}...")
            print(f"  New:  {s['new']}...")
    
    # Verify intensity preservation
    print(f"\n🔍 KIỂM TRA INTENSITY PRESERVATION:")
    intensity_words = ['dcm', 'vl', 'vcl', 'đm', 'dm', 'cc', 'cl']
    for word in intensity_words:
        count = df['training_text'].str.contains(word, case=False, na=False).sum()
        print(f"  - '{word}': {count} dòng")
    
    # Check separator
    has_sep = df['training_text'].str.contains('</s>', na=False).sum()
    print(f"\n✓ Separator </s>: {has_sep}/{len(df)} ({has_sep/len(df)*100:.1f}%)")
    
    # Save
    if output_file is None:
        output_file = f"FINAL_TRAINING_INTENSITY_PRESERVED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df.to_excel(output_file, index=False)
    print(f"\n✓ Đã lưu: {output_file}")
    
    return df


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        # Default
        input_file = "FINAL_TRAINING_TIME_FIXED_20251228_122200.xlsx"
        output_file = None
    
    print(f"\n🎯 Input: {input_file}")
    
    try:
        df = rebuild_training_text_from_text_raw(input_file, output_file)
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH!")
        print("="*70)
        print("\n💡 Kiểm tra:")
        print("  1. Các từ dcm, vl, vcl... đã được giữ nguyên")
        print("  2. Separator </s> vẫn còn")
        print("  3. Time format 12:30 không bị lỗi")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
