"""
🔄 REBUILD TRAINING_TEXT FROM TEXT_RAW
Rebuild cột training_text từ text_raw với Intensity Preservation

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

def rebuild_training_text(input_file, output_file=None):
    """
    Rebuild training_text từ text_raw
    
    Args:
        input_file: File Excel có cột text_raw
        output_file: File output (tự động tạo nếu None)
    """
    print("=" * 60)
    print("🔄 REBUILD TRAINING_TEXT FROM TEXT_RAW")
    print("=" * 60)
    
    # Backup
    backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_before_rebuild.xlsx"
    shutil.copy(input_file, backup)
    print(f"\n✓ Backup: {backup}")
    
    # Load
    print(f"\n📂 Loading file: {input_file}")
    df = pd.read_excel(input_file)
    print(f"✓ Loaded {len(df)} rows")
    
    # Check columns
    if 'text_raw' not in df.columns:
        raise ValueError("File không có cột 'text_raw'!")
    
    print(f"\n📊 Stats:")
    print(f"  Rows with text_raw: {df['text_raw'].notna().sum()}")
    print(f"  Rows with training_text: {df['training_text'].notna().sum()}")
    
    # Rebuild
    print(f"\n🔧 Rebuilding training_text từ text_raw...")
    print(f"   Strategy: Intensity Preservation (giữ nguyên vcl, đm, cc...)")
    
    rebuilt_count = 0
    skipped_count = 0
    
    for idx, row in df.iterrows():
        if pd.notna(row['text_raw']):
            # Clean với advanced_text_cleaning (đã có Intensity Preservation)
            new_training_text = advanced_clean_text(row['text_raw'])
            
            # Update
            df.loc[idx, 'training_text'] = new_training_text
            rebuilt_count += 1
        else:
            # Không có text_raw, giữ nguyên training_text
            skipped_count += 1
        
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{len(df)} rows... (rebuilt: {rebuilt_count})")
    
    print(f"\n✓ Rebuilt: {rebuilt_count} rows")
    print(f"✓ Skipped (no text_raw): {skipped_count} rows")
    
    # Verify separator
    has_sep = df['training_text'].str.contains('</s>', na=False).sum()
    print(f"\n📊 VERIFICATION:")
    print(f"  Rows with </s> separator: {has_sep}/{len(df)} ({has_sep/len(df)*100:.1f}%)")
    
    # Check intensity preservation
    print(f"\n🔍 INTENSITY PRESERVATION CHECK:")
    slang_patterns = ['vcl', 'vl', 'đm', 'dm', 'cc', 'dcm', 'cmm']
    for pattern in slang_patterns:
        count = df['training_text'].str.contains(pattern, na=False, case=False).sum()
        if count > 0:
            print(f"  '{pattern}': {count} rows")
    
    # Sample
    print(f"\n📝 SAMPLE (3 rows with slang):")
    slang_mask = df['training_text'].str.contains('vcl|vl|đm|dm|cc', na=False, case=False)
    sample = df[slang_mask].head(3)
    
    for idx, row in sample.iterrows():
        print(f"\n[{idx}] Label: {row['label']}, Labeler: {row.get('labeler', 'N/A')}")
        print(f"  text_raw: {str(row['text_raw'])[:80]}...")
        print(f"  training_text: {row['training_text'][:80]}...")
    
    # Save
    if output_file is None:
        output_file = f"FINAL_TRAINING_REBUILT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df.to_excel(output_file, index=False)
    print(f"\n✓ Saved: {output_file}")
    
    # Final stats
    print(f"\n📊 FINAL STATS:")
    print(f"  Total rows: {len(df)}")
    print(f"  Labeler distribution:")
    print(df['labeler'].value_counts(dropna=False))
    print(f"\n  Label distribution:")
    print(df['label'].value_counts().sort_index())
    
    return df


if __name__ == "__main__":
    input_file = "FINAL_TRAINING_WITH_HUY_RAW_20251228_114809.xlsx"
    
    print("=" * 60)
    print("🔄 REBUILD TRAINING_TEXT FROM TEXT_RAW")
    print("=" * 60)
    print("\nStrategy:")
    print("✅ Rebuild training_text từ text_raw")
    print("✅ Intensity Preservation: Giữ nguyên vcl, đm, cc, dcm...")
    print("✅ Preserve </s> separator")
    print("✅ Apply advanced_text_cleaning.py")
    print("=" * 60)
    
    rebuild_training_text(input_file)
    
    print("\n✅ DONE!")
    print("\nBây giờ bạn có dataset với:")
    print("  - training_text đã được rebuild từ text_raw")
    print("  - Giữ nguyên từ tục tĩu (vcl, đm, cc...)")
    print("  - Có </s> separator cho PhoBERT")
