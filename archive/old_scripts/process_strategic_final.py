"""
Final version - process strategic samples correctly
Use 'text' column which contains the actual data
"""
import pandas as pd
import sys
sys.path.insert(0, 'src/preprocessing')
from advanced_text_cleaning import advanced_clean_text
from datetime import datetime

print("="*80)
print("🔧 PROCESSING STRATEGIC SAMPLES - FINAL VERSION")
print("="*80)

# Load
input_file = 'STRATEGIC_SAMPLES_FOR_REVIEW_20251229_173539.csv'
print(f"\n📂 Loading: {input_file}")
df = pd.read_csv(input_file)
print(f"   Loaded: {len(df)} samples")
print(f"   Columns: {df.columns.tolist()}")

# Process using 'text' column (which has the actual data)
print("\n🔧 Processing...")
print("   Using: advanced_clean_text() from advanced_text_cleaning.py")
print("   Strategy: Intensity Preservation (keep vcl, vl, đm, cc...)")

processed_texts = []
for idx, row in df.iterrows():
    if (idx + 1) % 100 == 0:
        print(f"   Progress: {idx + 1}/{len(df)}")
    
    # Use 'text' column which contains the combined title + comment
    text = str(row.get('text', ''))
    
    if not text or text == 'nan':
        # Fallback: try text_raw
        text = str(row.get('text_raw', ''))
    
    if text and text != 'nan':
        # Split by </s> if exists
        if '</s>' in text:
            parts = text.split('</s>', 1)
            title = parts[0].strip()
            comment = parts[1].strip() if len(parts) > 1 else ''
            
            # Clean separately
            title_clean = advanced_clean_text(title) if title else ''
            comment_clean = advanced_clean_text(comment) if comment else ''
            
            # Combine
            if title_clean and comment_clean:
                training_text = f"{title_clean} </s> {comment_clean}"
            elif comment_clean:
                training_text = comment_clean
            elif title_clean:
                training_text = title_clean
            else:
                training_text = ""
        else:
            # No separator, clean as is
            training_text = advanced_clean_text(text)
    else:
        training_text = ""
    
    processed_texts.append(training_text)

df['training_text'] = processed_texts

# Check results
non_empty = sum(1 for t in processed_texts if t and len(t) > 0)
print(f"\n✅ Processed: {len(processed_texts)} samples")
print(f"   Non-empty: {non_empty} ({non_empty/len(processed_texts)*100:.1f}%)")
print(f"   Empty: {len(processed_texts) - non_empty}")

# Show examples
print(f"\n📋 EXAMPLES (First 5):")
for i in range(min(5, len(df))):
    row = df.iloc[i]
    text_raw = str(row.get('text', row.get('text_raw', '')))[:80]
    training = str(row['training_text'])[:80]
    print(f"\n[{i+1}] Label {row['label']}")
    print(f"  RAW:  {text_raw}...")
    print(f"  PROC: {training}...")

# Check toxic keywords
print(f"\n🎯 TOXIC KEYWORD PRESERVATION:")
toxic_kw = ['vcl', 'vl', 'đm', 'cc', 'dcm']
for kw in toxic_kw:
    count = df['training_text'].astype(str).str.contains(kw, case=False, na=False).sum()
    if count > 0:
        print(f"   '{kw}': {count} samples ✅")

# Save
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_csv = f'STRATEGIC_SAMPLES_PROCESSED_FINAL_{timestamp}.csv'
output_xlsx = f'STRATEGIC_SAMPLES_PROCESSED_FINAL_{timestamp}.xlsx'

# Select columns
columns = ['training_text', 'text_raw', 'label', 'confidence', 'matched_groups', 
          'note', 'source_file', 'labeler', 'has_teencode', 'sampling_strategy']
df_out = df[[c for c in columns if c in df.columns]]

df_out.to_csv(output_csv, index=False, encoding='utf-8-sig')
df_out.to_excel(output_xlsx, index=False)

print(f"\n💾 Saved:")
print(f"   {output_csv}")
print(f"   {output_xlsx}")

print("\n✅ DONE! Please review the file to confirm preprocessing is correct.")
