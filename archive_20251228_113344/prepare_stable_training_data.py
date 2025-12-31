"""
Script to prepare stable training dataset for PhoBERT.
Handles missing values, normalizes labels, removes duplicates.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def prepare_stable_dataset(input_file):
    """
    Clean and prepare dataset for training.
    
    Issues addressed:
    1. Remove rows with missing labels or text
    2. Fill empty context with empty string
    3. Convert labels to integer format
    4. Remove duplicate rows
    """
    
    print("=" * 70)
    print("PREPARING STABLE TRAINING DATASET FOR PHOBERT")
    print("=" * 70)
    
    # Read the merged file
    print(f"\n📂 Reading file: {Path(input_file).name}")
    df = pd.read_csv(input_file, encoding='utf-8-sig')
    
    print(f"\n📊 Initial dataset shape: {df.shape}")
    print(f"   Columns: {df.columns.tolist()}")
    
    # Display initial statistics
    print("\n🔍 INITIAL DATA QUALITY CHECK")
    print("-" * 70)
    print(f"Total rows: {len(df)}")
    print(f"\nMissing values per column:")
    missing_stats = df.isnull().sum()
    for col, count in missing_stats.items():
        if count > 0:
            percentage = (count / len(df)) * 100
            print(f"  • {col}: {count} ({percentage:.1f}%)")
    
    # Check label data type
    if 'label' in df.columns:
        print(f"\nLabel data type: {df['label'].dtype}")
        print(f"Unique labels: {sorted(df['label'].dropna().unique())}")
    
    # Count duplicates
    initial_dupes = df.duplicated().sum()
    print(f"\nDuplicate rows: {initial_dupes}")
    
    # STEP 1: Remove rows with missing labels or text
    print("\n" + "=" * 70)
    print("STEP 1: REMOVING ROWS WITH MISSING LABELS OR TEXT")
    print("=" * 70)
    
    initial_count = len(df)
    
    # Remove rows where label is NaN
    if 'label' in df.columns:
        df = df[df['label'].notna()]
        print(f"✓ Removed {initial_count - len(df)} rows with missing labels")
    
    # Remove rows where text is empty or NaN
    if 'text' in df.columns:
        before = len(df)
        df = df[df['text'].notna()]
        df = df[df['text'].str.strip() != '']
        print(f"✓ Removed {before - len(df)} rows with empty/missing text")
    
    # STEP 2: Fill empty context
    print("\n" + "=" * 70)
    print("STEP 2: FILLING EMPTY CONTEXT VALUES")
    print("=" * 70)
    
    if 'context' in df.columns:
        empty_context_count = df['context'].isna().sum()
        df['context'] = df['context'].fillna('')
        print(f"✓ Filled {empty_context_count} empty context values with empty string")
    
    # STEP 3: Normalize labels to integer
    print("\n" + "=" * 70)
    print("STEP 3: NORMALIZING LABELS TO INTEGER FORMAT")
    print("=" * 70)
    
    if 'label' in df.columns:
        print(f"Before: {df['label'].dtype} - {sorted(df['label'].unique())}")
        df['label'] = df['label'].astype(int)
        print(f"After:  {df['label'].dtype} - {sorted(df['label'].unique())}")
        print(f"✓ Converted labels to integer format")
        
        # Show label distribution
        print("\nLabel distribution:")
        label_counts = df['label'].value_counts().sort_index()
        for label, count in label_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  Label {label}: {count:,} samples ({percentage:.1f}%)")
    
    # STEP 4: Remove duplicates
    print("\n" + "=" * 70)
    print("STEP 4: REMOVING DUPLICATE ROWS")
    print("=" * 70)
    
    before_dedup = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before_dedup - len(df)
    print(f"✓ Removed {duplicates_removed} duplicate rows")
    
    # STEP 5: Reset index
    df = df.reset_index(drop=True)
    
    # Final statistics
    print("\n" + "=" * 70)
    print("FINAL DATASET STATISTICS")
    print("=" * 70)
    print(f"Total rows: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    print(f"\nColumns: {', '.join(df.columns.tolist())}")
    
    print("\nMissing values check:")
    final_missing = df.isnull().sum()
    if final_missing.sum() == 0:
        print("  ✓ No missing values!")
    else:
        for col, count in final_missing.items():
            if count > 0:
                print(f"  • {col}: {count}")
    
    print("\nData types:")
    for col, dtype in df.dtypes.items():
        print(f"  • {col}: {dtype}")
    
    # Save stable dataset
    print("\n" + "=" * 70)
    print("SAVING STABLE DATASET")
    print("=" * 70)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(r"c:\Học sâu\Dataset\data\processed")
    output_file = output_dir / f"STABLE_TRAINING_DATA_{timestamp}.csv"
    
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✓ Saved to: {output_file.name}")
    print(f"✓ File size: {output_file.stat().st_size / 1024 / 1024:.2f} MB")
    
    # Display sample
    print("\n" + "=" * 70)
    print("SAMPLE DATA (First 3 rows)")
    print("=" * 70)
    print(df.head(3).to_string())
    
    print("\n" + "=" * 70)
    print("✅ DATASET PREPARATION COMPLETE!")
    print("=" * 70)
    print(f"📁 Output file: {output_file}")
    print(f"📊 Total samples: {len(df):,}")
    print(f"✓ Ready for PhoBERT training!")
    print("=" * 70)
    
    return output_file

if __name__ == "__main__":
    input_file = r"c:\Học sâu\Dataset\data\processed\merged_labeled_data_UTF8_20251224_183407.csv"
    output_path = prepare_stable_dataset(input_file)
