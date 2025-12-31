"""
Test xem word segmentation có hoạt động đúng không
"""

import pandas as pd

print("="*80)
print("🔍 TESTING WORD SEGMENTATION RESULT")
print("="*80)

# Load segmented data
df = pd.read_excel("final_train_data_v3_SEGMENTED.xlsx")

print(f"\n📊 Dataset: {len(df)} rows")

# So sánh original vs segmented
print(f"\n📝 SEGMENTATION EXAMPLES (first 10 rows):")
print("="*80)

for i in range(min(10, len(df))):
    if 'training_text_original' in df.columns:
        original = df.iloc[i]['training_text_original']
        segmented = df.iloc[i]['training_text']
        
        # Chỉ hiển thị nếu có sự khác biệt
        if original != segmented and pd.notna(original) and pd.notna(segmented):
            print(f"\n{i+1}. ORIGINAL:")
            print(f"   {str(original)[:100]}")
            print(f"   SEGMENTED:")
            print(f"   {str(segmented)[:100]}")
            
            # Count underscores
            underscore_count = str(segmented).count('_')
            print(f"   → {underscore_count} compound words")

# Statistics
if 'training_text_original' in df.columns:
    # Count rows with changes
    df['has_change'] = df.apply(
        lambda x: str(x['training_text']) != str(x['training_text_original']) 
        if pd.notna(x['training_text']) and pd.notna(x['training_text_original']) 
        else False, 
        axis=1
    )
    
    changed_count = df['has_change'].sum()
    print(f"\n📊 STATISTICS:")
    print(f"   Rows with segmentation changes: {changed_count} / {len(df)} ({changed_count/len(df)*100:.1f}%)")
    
    # Count total underscores
    total_underscores = df['training_text'].fillna('').astype(str).str.count('_').sum()
    print(f"   Total compound words: {total_underscores}")
    print(f"   Avg compound words per text: {total_underscores/len(df):.2f}")

print("\n" + "="*80)
print("✅ TEST COMPLETE!")
print("="*80)
