"""
🔧 FIX TIME FORMAT IN DATASET
Fix các trường hợp 12:30 → 120 trong dataset

Author: Senior AI Engineer
Date: 2025-12-28
"""

import pandas as pd
import sys
import os
from datetime import datetime
import shutil
import re

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing.advanced_text_cleaning import advanced_clean_text

def fix_time_format(input_file, output_file=None):
    """
    Fix time format trong dataset bằng cách rebuild từ text_raw
    """
    print("=" * 60)
    print("🔧 FIX TIME FORMAT IN DATASET")
    print("=" * 60)
    
    # Backup
    backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_before_time_fix.xlsx"
    shutil.copy(input_file, backup)
    print(f"\n✓ Backup: {backup}")
    
    # Load
    print(f"\n📂 Loading: {input_file}")
    df = pd.read_excel(input_file)
    print(f"✓ Loaded {len(df)} rows")
    
    # Find rows with broken time format
    print(f"\n🔍 Tìm các dòng có time format bị lỗi...")
    
    # Pattern: số 2-3 chữ số đứng riêng (có thể là 120, 140, 170...)
    broken_time_pattern = r'\b(1[0-2]0|1[3-9]0|[2-9]0)\b'
    
    broken_rows = []
    for idx, row in df.iterrows():
        training_text = str(row['training_text'])
        
        # Check if has broken time
        if re.search(broken_time_pattern, training_text):
            # Check if text_raw has proper time format
            text_raw = str(row.get('text_raw', ''))
            if re.search(r'\d+:\d+', text_raw):
                broken_rows.append(idx)
    
    print(f"  Tìm thấy {len(broken_rows)} dòng nghi ngờ có time format bị lỗi")
    
    if len(broken_rows) == 0:
        print("\n✅ Không có dòng nào cần fix!")
        return df
    
    # Show samples
    print(f"\n📝 MẪU (5 dòng đầu):")
    for idx in broken_rows[:5]:
        row = df.iloc[idx]
        print(f"\n[{idx}]")
        print(f"  text_raw: {str(row.get('text_raw', ''))[:80]}...")
        print(f"  training_text (OLD): {row['training_text'][:80]}...")
    
    # Rebuild
    print(f"\n🔧 Rebuilding {len(broken_rows)} rows từ text_raw...")
    
    fixed_count = 0
    for idx in broken_rows:
        row = df.iloc[idx]
        
        if pd.notna(row.get('text_raw')):
            # Rebuild với advanced_clean_text (đã fix)
            new_training_text = advanced_clean_text(row['text_raw'])
            
            # Update
            df.loc[idx, 'training_text'] = new_training_text
            fixed_count += 1
        
        if (fixed_count) % 100 == 0 and fixed_count > 0:
            print(f"  Fixed {fixed_count}/{len(broken_rows)} rows...")
    
    print(f"\n✓ Fixed {fixed_count} rows")
    
    # Verify
    print(f"\n✅ VERIFICATION:")
    print(f"  Checking time format preservation...")
    
    time_preserved = 0
    for idx in broken_rows[:10]:  # Check first 10
        training_text = df.loc[idx, 'training_text']
        if re.search(r'\d+:\d+', training_text):
            time_preserved += 1
    
    print(f"  Time preserved in {time_preserved}/10 sample rows")
    
    # Show fixed samples
    print(f"\n📝 MẪU SAU KHI FIX (5 dòng đầu):")
    for idx in broken_rows[:5]:
        row = df.iloc[idx]
        print(f"\n[{idx}]")
        print(f"  text_raw: {str(row.get('text_raw', ''))[:80]}...")
        print(f"  training_text (NEW): {row['training_text'][:80]}...")
    
    # Save
    if output_file is None:
        output_file = f"FINAL_TRAINING_TIME_FIXED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df.to_excel(output_file, index=False)
    print(f"\n✓ Saved: {output_file}")
    
    return df


if __name__ == "__main__":
    input_file = "FINAL_TRAINING_WITH_HUY_RAW_20251228_114809.xlsx"
    
    print("=" * 60)
    print("🔧 FIX TIME FORMAT (12:30 → 120)")
    print("=" * 60)
    print("\nVấn đề: Emoticon :0 và :3 đã xóa time format")
    print("Giải pháp: Rebuild từ text_raw với logic mới")
    print("=" * 60)
    
    fix_time_format(input_file)
    
    print("\n✅ DONE!")
