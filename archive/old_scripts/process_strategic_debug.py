"""
Debug version - process strategic samples
"""
import pandas as pd
import sys
sys.path.insert(0, 'src/preprocessing')
from advanced_text_cleaning import advanced_clean_text

print("Loading...")
df = pd.read_excel('STRATEGIC_SAMPLES_FOR_REVIEW_20251229_162052.xlsx')
print(f"Loaded: {len(df)} rows")
print(f"Columns: {df.columns.tolist()}")

# Test first row
print("\n" + "="*80)
print("TEST FIRST ROW:")
print("="*80)
row = df.iloc[0]
print(f"raw_title: {row.get('raw_title', 'N/A')[:100]}")
print(f"raw_comment: {row.get('raw_comment', 'N/A')[:100]}")

raw_title = str(row.get('raw_title', '')) if pd.notna(row.get('raw_title')) else ''
raw_comment = str(row.get('raw_comment', '')) if pd.notna(row.get('raw_comment')) else ''

print(f"\nAfter str conversion:")
print(f"raw_title: '{raw_title[:100]}'")
print(f"raw_comment: '{raw_comment[:100]}'")

if raw_title and raw_comment:
    print("\nProcessing title...")
    title_clean = advanced_clean_text(raw_title)
    print(f"Title clean: '{title_clean[:100]}'")
    
    print("\nProcessing comment...")
    comment_clean = advanced_clean_text(raw_comment)
    print(f"Comment clean: '{comment_clean[:100]}'")
    
    training_text = f"{title_clean} </s> {comment_clean}"
    print(f"\nFinal training_text: '{training_text[:150]}'")
    print(f"Length: {len(training_text)}")
else:
    print("\nNo title or comment!")

# Now process all
print("\n" + "="*80)
print("PROCESSING ALL ROWS:")
print("="*80)

processed_texts = []
for idx in range(min(10, len(df))):  # Test first 10
    row = df.iloc[idx]
    
    raw_title = str(row.get('raw_title', '')) if pd.notna(row.get('raw_title')) else ''
    raw_comment = str(row.get('raw_comment', '')) if pd.notna(row.get('raw_comment')) else ''
    
    if raw_title and raw_comment:
        title_clean = advanced_clean_text(raw_title)
        comment_clean = advanced_clean_text(raw_comment)
        training_text = f"{title_clean} </s> {comment_clean}"
    elif raw_comment:
        training_text = advanced_clean_text(raw_comment)
    elif raw_title:
        training_text = advanced_clean_text(raw_title)
    else:
        training_text = ""
    
    processed_texts.append(training_text)
    print(f"{idx+1}. [{len(training_text)} chars] {training_text[:80]}")

print(f"\nProcessed {len(processed_texts)} texts")
print(f"Empty: {sum(1 for t in processed_texts if not t)}")
