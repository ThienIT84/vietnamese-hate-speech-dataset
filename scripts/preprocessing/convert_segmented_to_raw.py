"""
Convert PhoBERT segmented data to ViDeBERTa raw format
Remove word segmentation underscores

Input:  "học_sinh giỏi bú_fame"  (segmented)
Output: "học sinh giỏi bú fame"  (raw)
"""

import pandas as pd
import re
import os

def remove_segmentation(text):
    """
    Remove word segmentation underscores
    
    Examples:
        "học_sinh giỏi" → "học sinh giỏi"
        "bú_fame" → "bú fame"
        "cảm_ơn" → "cảm ơn"
        "bắc_kỳ" → "bắc kỳ"
    """
    if pd.isna(text):
        return text
    
    # Replace underscore with space
    text = str(text).replace('_', ' ')
    
    # Clean multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def main():
    print("="*80)
    print("🔄 CONVERTING SEGMENTED DATA TO RAW FORMAT")
    print("="*80)
    
    # Input file
    input_file = 'data/final/final_train_data_v3_READY.xlsx'
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    # Load data
    print(f"\n📂 Loading: {input_file}")
    df = pd.read_excel(input_file)
    
    print(f"✅ Loaded: {len(df)} samples")
    print(f"📊 Columns: {df.columns.tolist()}")
    
    # Check text column
    text_col = 'training_text' if 'training_text' in df.columns else 'text'
    label_col = 'label'
    
    print(f"\n📝 Text column: {text_col}")
    print(f"📝 Label column: {label_col}")
    
    # Check if data is segmented
    sample = df[text_col].iloc[0]
    underscore_count = str(sample).count('_')
    total_underscores = df[text_col].astype(str).str.count('_').sum()
    
    print(f"\n🔍 Sample text: {sample[:80]}")
    print(f"🔍 Underscores in sample: {underscore_count}")
    print(f"🔍 Total underscores in dataset: {total_underscores}")
    
    if total_underscores == 0:
        print("\n⚠️ Data is already RAW (no underscores found)")
        print("   No conversion needed!")
        return
    
    print("\n✅ Data is SEGMENTED → Converting to RAW...")
    
    # Convert
    df['training_text_raw'] = df[text_col].apply(remove_segmentation)
    
    # Statistics
    before_underscores = df[text_col].astype(str).str.count('_').sum()
    after_underscores = df['training_text_raw'].astype(str).str.count('_').sum()
    
    print(f"\n📊 CONVERSION STATS:")
    print(f"   Underscores before: {before_underscores}")
    print(f"   Underscores after: {after_underscores}")
    print(f"   Removed: {before_underscores - after_underscores}")
    
    # Verify samples
    print("\n📋 BEFORE vs AFTER (first 10 samples):")
    print("="*80)
    for i in range(min(10, len(df))):
        before = df[text_col].iloc[i]
        after = df['training_text_raw'].iloc[i]
        label = df[label_col].iloc[i]
        
        print(f"\n{i+1}. Label: {label}")
        print(f"   BEFORE: {before[:70]}")
        print(f"   AFTER:  {after[:70]}")
        
        if before != after:
            print(f"   ✅ Changed")
        else:
            print(f"   ⚠️ No change")
    
    # Save Excel
    output_file = 'data/final/final_train_data_v3_RAW.xlsx'
    df_output = df[['training_text_raw', label_col]].copy()
    df_output.columns = ['training_text', 'label']
    
    print(f"\n💾 Saving Excel: {output_file}")
    df_output.to_excel(output_file, index=False)
    print(f"✅ Saved: {len(df_output)} samples")
    
    # Save CSV
    csv_file = output_file.replace('.xlsx', '.csv')
    print(f"\n💾 Saving CSV: {csv_file}")
    df_output.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"✅ Saved: {len(df_output)} samples")
    
    # Final verification
    print("\n" + "="*80)
    print("🔍 FINAL VERIFICATION")
    print("="*80)
    
    # Check file sizes
    input_size = os.path.getsize(input_file) / 1024 / 1024
    output_size = os.path.getsize(output_file) / 1024 / 1024
    
    print(f"\n📊 File sizes:")
    print(f"   Input (segmented):  {input_size:.2f} MB")
    print(f"   Output (raw):       {output_size:.2f} MB")
    
    # Check no underscores in output
    df_check = pd.read_excel(output_file)
    remaining_underscores = df_check['training_text'].astype(str).str.count('_').sum()
    
    print(f"\n🔍 Remaining underscores in output: {remaining_underscores}")
    
    if remaining_underscores == 0:
        print("✅ Perfect! No underscores remaining")
    else:
        print(f"⚠️ Warning: {remaining_underscores} underscores still present")
        print("   (May be in special tokens like <person>, which is OK)")
    
    # Label distribution check
    print(f"\n📊 Label distribution:")
    for label, count in df_output['label'].value_counts().sort_index().items():
        pct = count / len(df_output) * 100
        print(f"   Label {int(label)}: {count} ({pct:.1f}%)")
    
    print("\n" + "="*80)
    print("✅ CONVERSION COMPLETE!")
    print("="*80)
    
    print(f"\n📁 Output files:")
    print(f"   1. {output_file}")
    print(f"   2. {csv_file}")
    
    print(f"\n🎯 Next steps:")
    print(f"   1. Upload {output_file} to Kaggle")
    print(f"   2. Use with ViDeBERTa training script")
    print(f"   3. Model: Fsoft-AIC/videberta-base")
    
    print(f"\n📝 Note:")
    print(f"   - Original segmented data: {input_file}")
    print(f"   - New raw data: {output_file}")
    print(f"   - Both files kept for comparison")

if __name__ == '__main__':
    main()
