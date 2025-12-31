import pandas as pd
import sys
sys.path.insert(0, 'src/preprocessing')
from advanced_text_cleaning import advanced_clean_text

# Load
df = pd.read_csv('STRATEGIC_SAMPLES_FOR_REVIEW_20251229_173539.csv', nrows=5)

print("Testing first 5 rows:")
for i in range(5):
    row = df.iloc[i]
    
    raw_title = row.get('raw_title', '')
    raw_comment = row.get('raw_comment', '')
    
    print(f"\n[{i+1}]")
    print(f"raw_title: '{raw_title[:80]}'")
    print(f"raw_comment: '{raw_comment[:80]}'")
    print(f"raw_title type: {type(raw_title)}, is NaN: {pd.isna(raw_title)}")
    print(f"raw_comment type: {type(raw_comment)}, is NaN: {pd.isna(raw_comment)}")
    
    # Test clean
    if pd.notna(raw_comment) and str(raw_comment).strip():
        result = advanced_clean_text(str(raw_comment))
        print(f"Cleaned comment: '{result[:80]}'")
        print(f"Result type: {type(result)}, length: {len(str(result))}")
    else:
        print("Comment is NaN or empty!")
