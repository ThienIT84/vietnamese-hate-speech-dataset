"""
🎯 SMART REBUILD FROM RAW CSV
Match training dataset với raw CSV và rebuild để giữ nguyên từ tục tĩu gốc

Strategy:
1. Load raw CSV (có text_raw, raw_title, raw_comment)
2. Load training XLSX (có training_text, text_raw từ file cũ)
3. Match bằng text similarity hoặc exact match
4. Rebuild những dòng match được từ raw CSV
5. Giữ nguyên những dòng không match (đã sửa chính tả)

Author: Senior AI Engineer
Date: 2025-12-28
"""

import pandas as pd
import sys
import os
from datetime import datetime
import shutil
from difflib import SequenceMatcher

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing.advanced_text_cleaning import advanced_clean_text

def similarity(a, b):
    """Calculate similarity between two strings"""
    if pd.isna(a) or pd.isna(b):
        return 0.0
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()

def build_input_text(title, comment):
    """Build input_text: 'title </s> comment'
    
    Rules:
    - If both title and comment exist → 'title </s> comment'
    - If only comment → 'comment' (no separator)
    - If only title → 'title' (rare case)
    """
    title = str(title).strip() if pd.notna(title) and str(title).strip() != 'nan' else ''
    comment = str(comment).strip() if pd.notna(comment) and str(comment).strip() != 'nan' else ''
    
    # Both exist
    if title and comment:
        return f"{title} </s> {comment}"
    
    # Only comment
    if comment:
        return comment
    
    # Only title (rare)
    if title:
        return title
    
    return ""

def smart_rebuild(training_file, raw_csv_file, output_file=None):
    """
    Smart rebuild training dataset từ raw CSV
    """
    # Backup
    backup = f"backup_before_smart_rebuild_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    shutil.copy(training_file, backup)
    print(f"✓ Backup: {backup}", flush=True)
    
    # Load files
    print("\n📂 Loading files...", flush=True)
    df_training = pd.read_excel(training_file)
    print(f"  Loaded training: {len(df_training)} rows", flush=True)
    df_raw = pd.read_csv(raw_csv_file)
    print(f"  Loaded raw CSV: {len(df_raw)} rows", flush=True)
    
    print(f"  Training: {len(df_training)} rows", flush=True)
    print(f"  Raw CSV: {len(df_raw)} rows", flush=True)
    print(f"  Raw CSV with text_raw: {df_raw['text_raw'].notna().sum()} rows", flush=True)
    
    # Create lookup dictionary từ raw CSV
    print("\n🔍 Creating lookup dictionary from raw CSV...")
    raw_lookup = {}
    
    for idx, row in df_raw.iterrows():
        if pd.notna(row['text_raw']) and pd.notna(row['raw_title']):
            # Key: normalized text_raw (để match dễ hơn)
            key = str(row['text_raw']).lower().strip()[:100]  # First 100 chars
            
            # Value: raw data
            raw_lookup[key] = {
                'text_raw': row['text_raw'],
                'raw_title': row['raw_title'],
                'raw_comment': row.get('raw_comment', row['text_raw'])
            }
    
    print(f"  Created lookup with {len(raw_lookup)} entries")
    
    # Match and rebuild
    print("\n🔧 Matching and rebuilding...", flush=True)
    matched_count = 0
    rebuilt_count = 0
    
    for idx, row in df_training.iterrows():
        # Try to match với raw CSV - CHỈ dùng exact match (nhanh)
        matched = False
        raw_data = None
        
        # Method 1: Exact match với text_raw trong training
        if pd.notna(row.get('text_raw')):
            key = str(row['text_raw']).lower().strip()[:100]
            if key in raw_lookup:
                matched = True
                raw_data = raw_lookup[key]
        
        # Rebuild if matched
        if matched and raw_data:
            matched_count += 1
            
            # Build new input_text từ raw data
            raw_input = build_input_text(raw_data['raw_title'], raw_data['raw_comment'])
            
            # Clean với logic mới (Intensity Preservation)
            new_training_text = advanced_clean_text(raw_input)
            
            # Update
            df_training.loc[idx, 'training_text'] = new_training_text
            df_training.loc[idx, 'text_raw'] = raw_input  # Update text_raw
            
            # Add note
            current_note = df_training.loc[idx, 'note']
            if pd.isna(current_note):
                df_training.loc[idx, 'note'] = "Rebuilt from raw CSV (Intensity Preservation)"
            else:
                df_training.loc[idx, 'note'] = f"{current_note}; Rebuilt from raw"
            
            rebuilt_count += 1
        
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{len(df_training)} rows... (matched: {matched_count})", flush=True)
    
    print(f"\n✓ Matched: {matched_count}/{len(df_training)} rows ({matched_count/len(df_training)*100:.1f}%)")
    print(f"✓ Rebuilt: {rebuilt_count} rows")
    print(f"✓ Kept original: {len(df_training) - rebuilt_count} rows (đã sửa chính tả)")
    
    # Save
    if output_file is None:
        output_file = f"FINAL_TRAINING_SMART_REBUILT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    df_training.to_excel(output_file, index=False)
    print(f"\n✓ Saved: {output_file}")
    
    # Verification
    print("\n📊 VERIFICATION:")
    print("Sample rebuilt rows with 'vcl' or 'đm':")
    
    # Find rows that were rebuilt and contain slang
    rebuilt_mask = df_training['note'].str.contains('Rebuilt from raw', na=False)
    slang_mask = df_training['training_text'].str.contains('vcl|đm|vl|cc', na=False, case=False)
    sample = df_training[rebuilt_mask & slang_mask].head(5)
    
    for idx, row in sample.iterrows():
        print(f"\n[Label {row['label']}]")
        print(f"Training: {row['training_text'][:100]}")
    
    return df_training

if __name__ == "__main__":
    training_file = "FINAL_TRAINING_SMART_REBUILT_20251228_015446.xlsx"  # File gần nhất
    raw_csv_file = "data/processed/merged_labeled_data_UTF8_20251224_183407.csv"
    
    print("=" * 70)
    print("🎯 SMART REBUILD FROM RAW CSV")
    print("=" * 70)
    print("\nStrategy:")
    print("1. Match training dataset với raw CSV")
    print("2. Rebuild matched rows → giữ nguyên từ tục tĩu gốc (đm, vcl...)")
    print("3. Keep unmatched rows → giữ nguyên (đã sửa chính tả, vẫn hợp lệ)")
    print("=" * 70)
    
    smart_rebuild(training_file, raw_csv_file)
    
    print("\n✅ DONE!")
    print("Dataset bây giờ:")
    print("- Matched rows: Giữ nguyên từ tục tĩu gốc (Intensity Preservation)")
    print("- Unmatched rows: Giữ nguyên (đã sửa chính tả, vẫn valid)")
