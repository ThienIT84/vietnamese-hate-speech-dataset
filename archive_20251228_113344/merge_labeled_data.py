"""
Script to merge three labeled CSV files into a single training dataset.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime

def merge_labeled_files():
    """Merge three labeled CSV files into one for model training."""
    
    # Define file paths
    file1 = r"c:\Học sâu\Dataset\TOXIC_COMMENT\datasets\final\final_1k_processed.csv"
    file2 = r"c:\Học sâu\Dataset\data\processed\labeling_task_Thien_CLEANED_20251224_181229.csv"
    file3 = r"c:\Học sâu\Dataset\data\processed\labeling_task_Quang_CLEANED_20251224_182202.csv"
    
    print("Reading CSV files with proper encoding...")
    
    # Try to read with different encodings
    def read_csv_safe(filepath):
        """Try reading CSV with multiple encodings."""
        encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
        for enc in encodings:
            try:
                df = pd.read_csv(filepath, encoding=enc)
                print(f"  ✓ Read {Path(filepath).name} with {enc}")
                return df
            except:
                continue
        raise ValueError(f"Could not read {filepath}")
    
    # Read all three files
    df1 = read_csv_safe(file1)
    df2 = read_csv_safe(file2)
    df3 = read_csv_safe(file3)
    
    print(f"\nFile 1 shape: {df1.shape}")
    print(f"File 1 columns: {df1.columns.tolist()}")
    print(f"\nFile 2 shape: {df2.shape}")
    print(f"File 2 columns: {df2.columns.tolist()}")
    print(f"\nFile 3 shape: {df3.shape}")
    print(f"File 3 columns: {df3.columns.tolist()}")
    
    # Concatenate all dataframes
    merged_df = pd.concat([df1, df2, df3], ignore_index=True)
    print(f"\nMerged shape (before deduplication): {merged_df.shape}")
    
    # Remove duplicates if any (based on all columns)
    initial_count = len(merged_df)
    merged_df = merged_df.drop_duplicates()
    duplicates_removed = initial_count - len(merged_df)
    
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Final shape: {merged_df.shape}")
    
    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(r"c:\Học sâu\Dataset\data\processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"merged_labeled_data_UTF8_{timestamp}.csv"
    
    # Save with proper UTF-8 encoding (with BOM for Excel compatibility)
    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ Merged data saved to: {output_file}")
    print(f"✓ Total records: {len(merged_df)}")
    print(f"✓ Encoding: UTF-8 with BOM")
    
    # Display basic statistics
    print("\n=== Dataset Statistics ===")
    print(f"Total rows: {len(merged_df)}")
    print(f"Total columns: {len(merged_df.columns)}")
    print(f"\nColumns: {', '.join(merged_df.columns.tolist())}")
    
    print("\n=== First 2 rows ===")
    print(merged_df.head(2))
    
    return output_file
    
    return output_file

if __name__ == "__main__":
    output_path = merge_labeled_files()
    print(f"\n✓ Successfully merged all labeled files!")
    print(f"✓ Output file: {output_path}")
