"""
Process strategic samples with proper preprocessing
Apply advanced_text_cleaning.py with Intensity Preservation
"""
import pandas as pd
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'preprocessing'))

print("="*80)
print("🔧 PROCESSING STRATEGIC SAMPLES")
print("="*80)

# Import preprocessing function
try:
    from advanced_text_cleaning import preprocess_text
    print("✅ Imported preprocess_text from advanced_text_cleaning.py")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nTrying alternative import...")
    # Try to load the module directly
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "advanced_text_cleaning",
        "src/preprocessing/advanced_text_cleaning.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    preprocess_text = module.preprocess_text
    print("✅ Loaded preprocess_text successfully")

# Load strategic samples
input_file = 'STRATEGIC_SAMPLES_FOR_REVIEW_20251229_162052.xlsx'
print(f"\n📂 Loading: {input_file}")

df = pd.read_excel(input_file)
print(f"   Loaded: {len(df)} samples")

# Process each sample
print("\n🔧 Processing with advanced_text_cleaning.py...")
print("   Strategy: Intensity Preservation")
print("   - KEEP: vcl, vl, đm, cc, dcm (toxic teencode)")
print("   - KEEP: emoji")
print("   - NORMALIZE: t→tôi, m→mình (neutral teencode)")
print("   - MASK: NER (names, locations)")

processed_samples = []

for idx, row in df.iterrows():
    if (idx + 1) % 100 == 0:
        print(f"   Processing: {idx + 1}/{len(df)}...")
    
    raw_title = str(row.get('raw_title', '')) if pd.notna(row.get('raw_title')) else ''
    raw_comment = str(row.get('raw_comment', '')) if pd.notna(row.get('raw_comment')) else ''
    
    # Process title and comment separately
    if raw_title and raw_comment:
        # Clean title
        title_clean = preprocess_text(raw_title)
        
        # Clean comment
        comment_clean = preprocess_text(raw_comment)
        
        # Combine with separator
        training_text = f"{title_clean} </s> {comment_clean}"
    elif raw_comment:
        # Only comment
        training_text = preprocess_text(raw_comment)
    elif raw_title:
        # Only title
        training_text = preprocess_text(raw_title)
    else:
        # Fallback: use text field
        text = str(row.get('text', ''))
        training_text = preprocess_text(text)
    
    processed_samples.append({
        'training_text': training_text,
        'text_raw': row.get('text', ''),
        'raw_title': raw_title,
        'raw_comment': raw_comment,
        'label': row.get('label', row.get('suggested_label', 0)),
        'confidence': row.get('confidence', 'MEDIUM'),
        'matched_groups': row.get('matched_groups', ''),
        'note': f"Strategic filter - {row.get('matched_groups', '')}",
        'source_file': 'filter_strategic_samples',
        'labeler': 'auto_strategic',
        'has_teencode': True,
        'sampling_strategy': 'strategic_keyword_filter'
    })

# Create DataFrame
processed_df = pd.DataFrame(processed_samples)

print(f"\n✅ Processed: {len(processed_df)} samples")

# Show examples
print("\n📋 EXAMPLES (Before → After):")
print("="*80)

for i in range(min(5, len(processed_df))):
    row = processed_df.iloc[i]
    print(f"\n[{i+1}] Label {row['label']} - {row['matched_groups']}")
    print(f"BEFORE: {row['text_raw'][:100]}...")
    print(f"AFTER:  {row['training_text'][:100]}...")

# Statistics
print("\n" + "="*80)
print("📊 STATISTICS")
print("="*80)

print(f"\n🎯 Label Distribution:")
for label in sorted(processed_df['label'].unique()):
    count = len(processed_df[processed_df['label'] == label])
    print(f"   Label {label}: {count} ({count/len(processed_df)*100:.1f}%)")

print(f"\n🎯 Confidence Distribution:")
for conf in processed_df['confidence'].unique():
    count = len(processed_df[processed_df['confidence'] == conf])
    print(f"   {conf}: {count} ({count/len(processed_df)*100:.1f}%)")

# Check for toxic keywords preservation
print(f"\n🎯 TOXIC KEYWORD PRESERVATION CHECK:")
toxic_keywords = ['vcl', 'vl', 'đm', 'dm', 'cc', 'dcm', 'dcm']
for keyword in toxic_keywords:
    count = processed_df['training_text'].str.contains(keyword, case=False, na=False).sum()
    if count > 0:
        print(f"   '{keyword}': {count} samples (PRESERVED ✅)")

# Save processed data
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_csv = f'STRATEGIC_SAMPLES_PROCESSED_{timestamp}.csv'
output_xlsx = f'STRATEGIC_SAMPLES_PROCESSED_{timestamp}.xlsx'

processed_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
processed_df.to_excel(output_xlsx, index=False)

print("\n" + "="*80)
print("💾 SAVED")
print("="*80)
print(f"✅ {output_csv}")
print(f"✅ {output_xlsx}")

# Save by label
for label in sorted(processed_df['label'].unique()):
    label_df = processed_df[processed_df['label'] == label]
    label_file = f'STRATEGIC_SAMPLES_PROCESSED_LABEL_{label}_{timestamp}.xlsx'
    label_df.to_excel(label_file, index=False)
    print(f"✅ {label_file}")

print("\n" + "="*80)
print("✅ PROCESSING COMPLETE!")
print("="*80)

print(f"""
📋 NEXT STEPS:

1. REVIEW PROCESSED FILE: {output_xlsx}
   - Check xem teencode toxic có được giữ lại không (vcl, vl, đm...)
   - Check xem emoji có được giữ lại không
   - Check xem NER có được mask đúng không

2. SO SÁNH VỚI RAW:
   - Mở file gốc: {input_file}
   - Mở file processed: {output_xlsx}
   - Kiểm tra xem preprocessing có đúng không

3. NẾU OK, MERGE VÀO TRAINING DATA:
   python merge_augmented_data.py

4. RETRAIN MODEL:
   - Upload lên Colab
   - Expected: F1 > 0.72

🎯 KEY POINTS:
   - Toxic teencode (vcl, vl, đm, cc) được GIỮ LẠI
   - Emoji được GIỮ LẠI
   - Neutral teencode (t→tôi) được CHUẨN HÓA
   - NER được MASK (<person>, <location>)
""")
