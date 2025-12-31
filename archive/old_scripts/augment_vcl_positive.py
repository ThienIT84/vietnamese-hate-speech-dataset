"""
Augment training data with positive VCL/VL slang examples
Target: Reduce 0→1 errors (False Positive)
"""
import pandas as pd
from datetime import datetime

print("="*80)
print("🔍 AUGMENTING VCL/VL POSITIVE DATA")
print("="*80)

# Load unlabeled data (if available)
try:
    unlabeled_df = pd.read_csv('unlabeled_processed_20251229_013303.csv')
    print(f"✅ Loaded unlabeled data: {len(unlabeled_df)} rows")
except:
    print("⚠️ No unlabeled data found, will create synthetic examples only")
    unlabeled_df = None

# Define patterns
vcl_vl_patterns = ['vcl', 'vl', 'vãi lồn', 'vãi']
positive_context = ['chất', 'hay', 'đẹp', 'tuyệt', 'ngon', 'đỉnh', 'pro', 'xịn', 
                   'peak', 'top', 'best', 'good', 'nice', 'cool', 'amazing']

augmented_samples = []

# Method 1: Filter from unlabeled data
if unlabeled_df is not None:
    print("\n📊 METHOD 1: Filter from unlabeled data")
    
    for idx, row in unlabeled_df.iterrows():
        text = str(row['training_text']).lower()
        
        # Check if has VCL/VL
        has_vcl_vl = any(pattern in text for pattern in vcl_vl_patterns)
        
        # Check if has positive context
        has_positive = any(word in text for word in positive_context)
        
        # Check if NO toxic words
        toxic_words = ['đm', 'dm', 'đcm', 'dcm', 'cc', 'lồn', 'địt', 'đụ', 'chó', 'lợn']
        has_toxic = any(word in text for word in toxic_words if word not in ['vãi lồn', 'vl', 'vcl'])
        
        if has_vcl_vl and has_positive and not has_toxic:
            augmented_samples.append({
                'training_text': row['training_text'],
                'text_raw': row.get('text_raw', ''),
                'label': 0,  # Clean/Positive
                'note': 'VCL/VL positive slang - auto-labeled',
                'source_file': 'augment_vcl_positive',
                'labeler': 'auto',
                'has_teencode': True,
                'confidence': 'HIGH',
                'sampling_strategy': 'vcl_vl_positive',
                'raw_comment': row.get('raw_comment', ''),
                'raw_title': row.get('raw_title', '')
            })
            
            if len(augmented_samples) >= 300:
                break
    
    print(f"   Found: {len(augmented_samples)} samples")

# Method 2: Create synthetic examples
print("\n📊 METHOD 2: Create synthetic examples")

synthetic_templates = [
    # Positive VCL/VL
    ("video hay vl", "chất lượng vcl luôn"),
    ("mv đẹp vl", "peak vcl"),
    ("bài hát ngon vl", "hay vl"),
    ("sản phẩm xịn vl", "chất vcl"),
    ("game pro vl", "đỉnh vcl"),
    ("phim hay vl", "tuyệt vl"),
    ("ảnh đẹp vl", "xịn vcl"),
    ("nhạc ngon vl", "chất vl"),
    ("clip hay vl", "peak vcl"),
    ("content chất vl", "pro vl"),
    
    # With title context
    ("review sản phẩm mới", "dùng thử rồi thấy chất vcl"),
    ("unboxing iphone 15", "đẹp vl luôn"),
    ("test game mới", "đồ họa đỉnh vcl"),
    ("reaction mv mới", "hay vl không chê được"),
    ("food review", "ngon vl ăn hoài không chán"),
    ("travel vlog", "cảnh đẹp vl"),
    ("makeup tutorial", "xinh vl luôn"),
    ("dance cover", "nhảy pro vl"),
    ("guitar cover", "chơi hay vl"),
    ("cooking show", "nấu ngon vl"),
]

for title, comment in synthetic_templates:
    training_text = f"{title} </s> {comment}"
    augmented_samples.append({
        'training_text': training_text,
        'text_raw': training_text,
        'label': 0,
        'note': 'VCL/VL positive slang - synthetic',
        'source_file': 'augment_vcl_positive',
        'labeler': 'synthetic',
        'has_teencode': True,
        'confidence': 'HIGH',
        'sampling_strategy': 'vcl_vl_positive_synthetic',
        'raw_comment': comment,
        'raw_title': title
    })

print(f"   Created: {len(synthetic_templates)} synthetic samples")

# Create DataFrame
augmented_df = pd.DataFrame(augmented_samples)

print(f"\n📊 TOTAL AUGMENTED: {len(augmented_df)} samples")
print(f"   Label 0: {len(augmented_df[augmented_df['label'] == 0])}")

# Save
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f'AUGMENTED_VCL_POSITIVE_{timestamp}.csv'
augmented_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n💾 Saved: {output_file}")

# Also save Excel for review
excel_file = f'AUGMENTED_VCL_POSITIVE_{timestamp}.xlsx'
augmented_df.to_excel(excel_file, index=False)
print(f"💾 Saved: {excel_file}")

print("\n" + "="*80)
print("✅ AUGMENTATION COMPLETE!")
print("="*80)
print(f"\n📋 NEXT STEPS:")
print(f"   1. Review: {excel_file}")
print(f"   2. If OK, merge with training data:")
print(f"      python merge_augmented_data.py")
