"""
🔧 FIX SEPARATOR FORMAT
Đảm bảo training_text có format: "title </s> comment"

Vấn đề: Thiếu dấu </s> ngăn cách giữa title và comment
"""

import pandas as pd
from datetime import datetime
import shutil
import re

def fix_separator(input_file, output_file=None):
    """
    Fix separator format trong training_text
    """
    # Backup
    backup = f"backup_before_fix_sep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    shutil.copy(input_file, backup)
    print(f"✓ Backup: {backup}")
    
    # Load
    df = pd.read_excel(input_file)
    print(f"\n📊 Loaded: {len(df)} rows")
    
    # Check current format
    print("\n🔍 Checking current format...")
    has_separator = df['training_text'].str.contains('</s>', na=False).sum()
    print(f"  Rows with </s>: {has_separator}/{len(df)}")
    
    # Sample without separator
    no_sep = df[~df['training_text'].str.contains('</s>', na=False)]
    print(f"\n📝 Sample rows WITHOUT </s> (first 3):")
    for idx, row in no_sep.head(3).iterrows():
        print(f"\n[{idx}] Label {row['label']}:")
        print(f"  {row['training_text'][:120]}...")
    
    # Check if we need to fix
    if has_separator == len(df):
        print("\n✅ All rows already have </s> separator!")
        return df
    
    print(f"\n⚠️  Need to fix {len(df) - has_separator} rows")
    
    # Strategy: Nếu text_raw có format "title </s> comment", extract và rebuild
    # Nếu không, giữ nguyên (có thể là comment-only)
    
    fixed_count = 0
    for idx, row in df.iterrows():
        training_text = str(row['training_text'])
        
        # Skip if already has separator
        if '</s>' in training_text:
            continue
        
        # Check text_raw
        text_raw = str(row.get('text_raw', ''))
        
        if '</s>' in text_raw:
            # text_raw có separator → có thể extract title và comment
            # Nhưng training_text đã được clean → cần tìm vị trí tương ứng
            
            # Simple heuristic: Nếu training_text dài và có nhiều câu,
            # thử tách thành title (câu đầu) và comment (phần còn lại)
            sentences = re.split(r'[.!?]\s+', training_text)
            
            if len(sentences) >= 2:
                # Có nhiều câu → có thể là title + comment
                title = sentences[0]
                comment = ' '.join(sentences[1:])
                
                # Rebuild với separator
                new_text = f"{title} </s> {comment}"
                df.loc[idx, 'training_text'] = new_text
                fixed_count += 1
        
        if (idx + 1) % 1000 == 0:
            print(f"  Processed {idx + 1}/{len(df)} rows... (fixed: {fixed_count})")
    
    print(f"\n✓ Fixed {fixed_count} rows")
    
    # Verify
    print("\n📊 VERIFICATION:")
    has_separator_after = df['training_text'].str.contains('</s>', na=False).sum()
    print(f"  Rows with </s> after fix: {has_separator_after}/{len(df)}")
    
    # Sample after fix
    print(f"\n📝 Sample rows WITH </s> (first 3):")
    with_sep = df[df['training_text'].str.contains('</s>', na=False)]
    for idx, row in with_sep.head(3).iterrows():
        print(f"\n[{idx}] Label {row['label']}:")
        print(f"  {row['training_text'][:150]}...")
    
    # Save
    if output_file is None:
        output_file = f"FINAL_TRAINING_FIXED_SEP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df.to_excel(output_file, index=False)
    print(f"\n✓ Saved: {output_file}")
    
    return df

if __name__ == "__main__":
    input_file = "FINAL_TRAINING_SMART_REBUILT_20251228_013652.xlsx"
    
    print("=" * 60)
    print("🔧 FIX SEPARATOR FORMAT")
    print("=" * 60)
    print("\nEnsure format: 'title </s> comment'")
    print("=" * 60)
    
    fix_separator(input_file)
    
    print("\n✅ DONE!")
