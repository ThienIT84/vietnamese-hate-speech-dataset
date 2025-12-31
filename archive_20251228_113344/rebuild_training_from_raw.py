"""
🔧 REBUILD TRAINING TEXT FROM RAW
Xây dựng lại training_text từ text_raw với logic mới:
- KHÔNG expand các từ tục tĩu (đm, vcl, cc...)
- CHỈ chuẩn hóa neutral words (ko → không, mh → mình...)
- Giữ nguyên nghĩa gốc của người dùng

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

from preprocessing.advanced_text_cleaning import (
    clean_text_with_special_emoji,
    advanced_clean_text
)

def rebuild_training_text(input_file, output_file=None):
    """
    Rebuild training_text từ text_raw với logic Intensity Preservation
    """
    # Backup
    backup = f"backup_before_rebuild_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    shutil.copy(input_file, backup)
    print(f"✓ Backup: {backup}")
    
    # Load
    df = pd.read_excel(input_file)
    print(f"\n📊 Loaded: {len(df)} rows")
    
    # Rebuild
    print("\n🔧 Rebuilding training_text from text_raw...")
    rebuilt_count = 0
    
    for idx, row in df.iterrows():
        if pd.notna(row['text_raw']):
            # Clean từ text_raw với logic mới (đã có TEENCODE_INTENSITY_SENSITIVE)
            new_training_text = advanced_clean_text(row['text_raw'])
            
            # Update
            df.loc[idx, 'training_text'] = new_training_text
            rebuilt_count += 1
        
        if (idx + 1) % 1000 == 0:
            print(f"  Processed {idx + 1}/{len(df)} rows...")
    
    print(f"\n✓ Rebuilt {rebuilt_count} rows")
    
    # Save
    if output_file is None:
        output_file = f"FINAL_TRAINING_REBUILT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df.to_excel(output_file, index=False)
    print(f"✓ Saved: {output_file}")
    
    # Verify
    print("\n📊 VERIFICATION:")
    print("Sample rows with 'vcl' in text_raw:")
    sample = df[df['text_raw'].str.contains('vcl|vl', na=False, case=False)].head(5)
    for idx, row in sample.iterrows():
        print(f"\n[Label {row['label']}]")
        print(f"Raw: {row['text_raw'][:80]}")
        print(f"Training: {row['training_text'][:80]}")
    
    return df

if __name__ == "__main__":
    input_file = "FINAL_TRAINING_DATASET_TEENCODE_20251225_151716.xlsx"
    
    print("=" * 60)
    print("🔧 REBUILD TRAINING TEXT FROM RAW")
    print("=" * 60)
    print("\nStrategy: Intensity Preservation")
    print("- Keep teencode slang (đm, vcl, cc...)")
    print("- Only normalize neutral words (ko → không)")
    print("- Preserve original user intent")
    print("=" * 60)
    
    rebuild_training_text(input_file)
    
    print("\n✅ DONE!")
    print("Bây giờ training_text phản ánh đúng nghĩa gốc của text_raw")
