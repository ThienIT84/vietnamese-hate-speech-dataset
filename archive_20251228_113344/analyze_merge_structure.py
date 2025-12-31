"""
Script to analyze the structure of 3 labeled files before merging.
This will help create a professional merge strategy.
"""
import pandas as pd
from pathlib import Path

def analyze_file_structure(filepath, file_label):
    """Analyze and display structure of a CSV file."""
    print("\n" + "=" * 80)
    print(f"📁 {file_label}: {Path(filepath).name}")
    print("=" * 80)
    
    # Try different encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
    df = None
    
    for enc in encodings:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            print(f"✓ Encoding: {enc}")
            break
        except:
            continue
    
    if df is None:
        print("✗ Could not read file!")
        return None
    
    # Basic info
    print(f"📊 Shape: {df.shape} (rows × columns)")
    print(f"📋 Columns ({len(df.columns)}): {df.columns.tolist()}")
    
    # Data types
    print("\n🔍 Data Types:")
    for col, dtype in df.dtypes.items():
        non_null = df[col].notna().sum()
        null_count = df[col].isna().sum()
        print(f"  • {col:20s} | {str(dtype):10s} | Non-null: {non_null:,} | Null: {null_count:,}")
    
    # Check for text columns
    print("\n📝 Text Columns Analysis:")
    text_cols = ['text', 'input_text', 'context', 'raw_comment', 'raw_title']
    for col in text_cols:
        if col in df.columns:
            non_empty = df[col].notna().sum()
            sample = df[col].dropna().iloc[0] if non_empty > 0 else "N/A"
            sample_preview = str(sample)[:60] + "..." if len(str(sample)) > 60 else str(sample)
            print(f"  • {col:20s} | {non_empty:,} non-empty rows")
            print(f"    Sample: {sample_preview}")
    
    # Check for label column
    print("\n🏷️  Label Column Analysis:")
    label_cols = ['label', 'labels', 'category', 'class']
    for col in label_cols:
        if col in df.columns:
            print(f"  • Column: {col}")
            print(f"    Data type: {df[col].dtype}")
            print(f"    Unique values: {sorted(df[col].dropna().unique())}")
            print(f"    Value counts:")
            for val, count in df[col].value_counts().sort_index().items():
                print(f"      {val}: {count:,}")
    
    # Sample rows
    print("\n📄 First 2 Rows:")
    print(df.head(2).to_string())
    
    return df

def create_merge_strategy(df1, df2, df3):
    """Create a professional merge strategy based on file structures."""
    print("\n" + "=" * 80)
    print("🎯 MERGE STRATEGY RECOMMENDATION")
    print("=" * 80)
    
    # Identify training text columns
    print("\n1️⃣  TRAINING TEXT COLUMN MAPPING:")
    print("   File 1 (final_1k_processed): 'input_text' → standardize to 'training_text'")
    print("   File 2 (labeling_task_Thien): 'text' → standardize to 'training_text'")
    print("   File 3 (labeling_task_Quang): 'text' → standardize to 'training_text'")
    
    # Check common columns
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    cols3 = set(df3.columns)
    
    common_all = cols1 & cols2 & cols3
    print(f"\n2️⃣  COMMON COLUMNS (in all 3 files): {list(common_all)}")
    
    all_cols = cols1 | cols2 | cols3
    print(f"\n3️⃣  ALL UNIQUE COLUMNS: {sorted(list(all_cols))}")
    
    # Recommend final schema
    print("\n4️⃣  RECOMMENDED FINAL SCHEMA:")
    print("   • training_text: The main text for model training")
    print("   • context: Context information (fill with '' if missing)")
    print("   • label: Integer label (0, 1, 2, etc.)")
    print("   • source_file: Track which file the data came from")
    print("   • [other common columns as needed]")
    
    print("\n5️⃣  MERGE STEPS:")
    print("   Step 1: Load each file with appropriate encoding")
    print("   Step 2: Rename columns to standard schema:")
    print("           - 'input_text' or 'text' → 'training_text'")
    print("   Step 3: Add 'source_file' column to track origin")
    print("   Step 4: Select only necessary columns")
    print("   Step 5: Concatenate all dataframes")
    print("   Step 6: Clean data (remove nulls, normalize labels, remove duplicates)")
    print("   Step 7: Save to STABLE_TRAINING_DATA.csv")

if __name__ == "__main__":
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "FILE STRUCTURE ANALYSIS & MERGE STRATEGY" + " " * 18 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # File paths
    file1 = r"c:\Học sâu\Dataset\TOXIC_COMMENT\datasets\final\final_1k_processed.csv"
    file2 = r"c:\Học sâu\Dataset\data\processed\labeling_task_Thien_CLEANED_20251224_181229.csv"
    file3 = r"c:\Học sâu\Dataset\data\processed\labeling_task_Quang_CLEANED_20251224_182202.csv"
    
    # Analyze each file
    df1 = analyze_file_structure(file1, "FILE 1 - final_1k_processed")
    df2 = analyze_file_structure(file2, "FILE 2 - labeling_task_Thien")
    df3 = analyze_file_structure(file3, "FILE 3 - labeling_task_Quang")
    
    # Create merge strategy
    if df1 is not None and df2 is not None and df3 is not None:
        create_merge_strategy(df1, df2, df3)
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
