"""
📥 IMPORT HUY RAW COLUMNS
Import các cột raw từ final_Huy_processed.csv vào file training
Giữ nguyên nhãn đã gán, chỉ thêm raw columns

Author: Senior AI Engineer
Date: 2025-12-28
"""

import pandas as pd
from datetime import datetime
import shutil

def import_huy_raw_columns(training_file, huy_file, output_file=None):
    """
    Import raw columns từ file Huy vào file training
    
    Strategy:
    1. Load cả 2 files
    2. Match dựa vào training_text hoặc input_text
    3. Import raw_comment, raw_title từ file Huy
    4. Giữ nguyên label, note từ file training
    """
    print("=" * 60)
    print("📥 IMPORT HUY RAW COLUMNS")
    print("=" * 60)
    
    # Backup
    backup = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_training.xlsx"
    shutil.copy(training_file, backup)
    print(f"\n✓ Backup: {backup}")
    
    # Load files
    print(f"\n📂 Loading files...")
    df_training = pd.read_excel(training_file)
    df_huy = pd.read_csv(huy_file)
    
    print(f"  Training file: {len(df_training)} rows")
    print(f"  Huy file: {len(df_huy)} rows")
    
    # Check labelers
    print(f"\n📊 Labeler distribution in training:")
    print(df_training['labeler'].value_counts(dropna=False))
    
    # Identify rows without labeler (likely Huy's data)
    no_labeler_mask = df_training['labeler'].isna()
    no_labeler_count = no_labeler_mask.sum()
    
    print(f"\n🔍 Rows without labeler: {no_labeler_count}")
    print(f"   (These are likely Huy's labeled data)")
    
    # Check if Huy file has raw columns
    huy_raw_cols = [col for col in df_huy.columns if 'raw' in col.lower()]
    print(f"\n📋 Raw columns in Huy file: {huy_raw_cols}")
    
    if not huy_raw_cols:
        print("\n❌ Huy file không có raw columns!")
        return None
    
    # Add raw columns to training if not exist
    for col in ['raw_comment', 'raw_title', 'text_raw']:
        if col not in df_training.columns:
            df_training[col] = None
    
    # Create lookup dictionary from Huy file
    print(f"\n🔧 Creating lookup dictionary...")
    huy_lookup = {}
    
    for idx, row in df_huy.iterrows():
        # Use training_text or input_text as key
        key_text = row.get('training_text') or row.get('input_text', '')
        if pd.notna(key_text):
            key = str(key_text).lower().strip()[:150]  # First 150 chars
            
            huy_lookup[key] = {
                'raw_comment': row.get('raw_comment'),
                'raw_title': row.get('raw_title'),
                'input_text': row.get('input_text'),
                'label': row.get('label'),  # For verification
            }
    
    print(f"  Created lookup with {len(huy_lookup)} entries")
    
    # Match and import
    print(f"\n🔄 Matching and importing raw columns...")
    matched_count = 0
    updated_count = 0
    
    for idx, row in df_training.iterrows():
        # Only process rows without labeler (Huy's data)
        if not no_labeler_mask[idx]:
            continue
        
        # Try to match
        training_text = str(row['training_text']).lower().strip()[:150]
        
        if training_text in huy_lookup:
            matched_count += 1
            huy_data = huy_lookup[training_text]
            
            # Import raw columns
            if pd.notna(huy_data['raw_comment']):
                df_training.loc[idx, 'raw_comment'] = huy_data['raw_comment']
                updated_count += 1
            
            if pd.notna(huy_data['raw_title']):
                df_training.loc[idx, 'raw_title'] = huy_data['raw_title']
            
            # Build text_raw (title </s> comment)
            title = str(huy_data['raw_title']).strip() if pd.notna(huy_data['raw_title']) else ''
            comment = str(huy_data['raw_comment']).strip() if pd.notna(huy_data['raw_comment']) else ''
            
            if title and comment:
                df_training.loc[idx, 'text_raw'] = f"{title} </s> {comment}"
            elif comment:
                df_training.loc[idx, 'text_raw'] = comment
            elif title:
                df_training.loc[idx, 'text_raw'] = title
            
            # Set labeler to Huy
            df_training.loc[idx, 'labeler'] = 'Huy'
            
            # Verify label consistency
            if pd.notna(huy_data['label']) and huy_data['label'] != row['label']:
                print(f"  ⚠️  Label mismatch at row {idx}: Training={row['label']}, Huy={huy_data['label']}")
        
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{len(df_training)} rows... (matched: {matched_count})")
    
    print(f"\n✓ Matched: {matched_count}/{no_labeler_count} rows ({matched_count/no_labeler_count*100:.1f}%)")
    print(f"✓ Updated with raw columns: {updated_count} rows")
    
    # Stats after import
    print(f"\n📊 AFTER IMPORT:")
    print(f"  Labeler distribution:")
    print(df_training['labeler'].value_counts(dropna=False))
    
    print(f"\n  Rows with raw_comment: {df_training['raw_comment'].notna().sum()}")
    print(f"  Rows with raw_title: {df_training['raw_title'].notna().sum()}")
    print(f"  Rows with text_raw: {df_training['text_raw'].notna().sum()}")
    
    # Sample
    print(f"\n📝 SAMPLE (Huy's data with raw):")
    huy_with_raw = df_training[(df_training['labeler'] == 'Huy') & (df_training['raw_comment'].notna())]
    for idx, row in huy_with_raw.head(3).iterrows():
        print(f"\n[{idx}] Label: {row['label']}")
        print(f"  training_text: {row['training_text'][:80]}...")
        print(f"  raw_comment: {str(row['raw_comment'])[:80]}...")
        print(f"  text_raw: {str(row['text_raw'])[:80]}...")
    
    # Save
    if output_file is None:
        output_file = f"FINAL_TRAINING_WITH_HUY_RAW_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df_training.to_excel(output_file, index=False)
    print(f"\n✓ Saved: {output_file}")
    
    return df_training


if __name__ == "__main__":
    training_file = "data/processed/FINAL_TRAINING_DATASET_TEENCODE_20251225_151716.xlsx"
    huy_file = "data/processed/final_Huy_processed.csv"
    
    print("=" * 60)
    print("📥 IMPORT HUY RAW COLUMNS TO TRAINING DATASET")
    print("=" * 60)
    print("\nStrategy:")
    print("1. Match training data với Huy file")
    print("2. Import raw_comment, raw_title từ Huy file")
    print("3. Giữ nguyên label đã gán trong training file")
    print("4. Set labeler = 'Huy' cho các rows được import")
    print("=" * 60)
    
    import_huy_raw_columns(training_file, huy_file)
    
    print("\n✅ DONE!")
