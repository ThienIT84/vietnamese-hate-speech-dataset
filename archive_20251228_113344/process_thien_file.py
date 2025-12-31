"""
Apply advanced_text_cleaning with teencode to labeling_task_Thien_assigned.csv
Process raw_comment and raw_title, merge with </s> separator
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent / 'src'))
from preprocessing.advanced_text_cleaning import clean_text

def clean_text_preserve_separator(text):
    """Clean text but preserve </s> separator"""
    if not text or pd.isna(text):
        return text
    
    if ' </s> ' in text:
        parts = text.split(' </s> ')
        cleaned_parts = [clean_text(p.strip()) for p in parts if p.strip()]
        return ' </s> '.join(cleaned_parts) if cleaned_parts else ''
    return clean_text(text)

print("="*60)
print("APPLY TEENCODE TO labeling_task_Thien_assigned.csv")
print("="*60)

# Load file from backup
input_file = Path(r"backup_20251221_191458\data\labeled\Quang_final.csv")

if not input_file.exists():
    print(f"\nError: File not found at {input_file}")
    print("Searching for file...")
    # Try to find the file
    import glob
    files = glob.glob("**/labeling_task_Thien_assigned.csv", recursive=True)
    if files:
        input_file = Path(files[0])
        print(f"Found at: {input_file}")
    else:
        print("File not found anywhere!")
        exit(1)

print(f"\n[1/3] Loading {input_file.name}...")
df = pd.read_csv(input_file, encoding='utf-8')
print(f"  Loaded: {len(df)} rows")
print(f"  Columns: {list(df.columns)}")

# Check for raw_comment and raw_title columns
if 'raw_comment' not in df.columns:
    print("\n  Warning: 'raw_comment' column not found")
    print(f"  Available columns: {list(df.columns)}")
    # Try alternative column names
    if 'comment' in df.columns:
        df['raw_comment'] = df['comment']
        print("  Using 'comment' as 'raw_comment'")
    elif 'Comment' in df.columns:
        df['raw_comment'] = df['Comment']
        print("  Using 'Comment' as 'raw_comment'")

if 'raw_title' not in df.columns:
    if 'title' in df.columns:
        df['raw_title'] = df['title']
        print("  Using 'title' as 'raw_title'")
    elif 'Title' in df.columns:
        df['raw_title'] = df['Title']
        print("  Using 'Title' as 'raw_title'")
    elif 'context' in df.columns:
        df['raw_title'] = df['context']
        print("  Using 'context' as 'raw_title'")

# Build text_raw column
print("\n[2/3] Building text with </s> separator...")
text_raw_list = []
for idx, row in df.iterrows():
    raw_comment = row.get('raw_comment', '')
    raw_title = row.get('raw_title', '')
    
    # Build full text
    if pd.notna(raw_title) and len(str(raw_title).strip()) > 0:
        text_raw = f"{raw_title} </s> {raw_comment}"
    else:
        text_raw = raw_comment
    
    text_raw_list.append(text_raw)

df['text_raw'] = text_raw_list
print(f"  Built {len(text_raw_list)} text entries")

# Show example
if len(df) > 0:
    print("\n  Example BEFORE cleaning:")
    example = df.iloc[0]
    print(f"  Title: {example.get('raw_title', '')[:100]}")
    print(f"  Comment: {example.get('raw_comment', '')[:100]}")
    print(f"  Combined: {example['text_raw'][:150]}")

# Apply cleaning
print("\n[3/3] Applying advanced_text_cleaning...")
cleaned_texts = []
for i, text_raw in enumerate(df['text_raw'], 1):
    if i % 100 == 0:
        print(f"  Processing {i}/{len(df)}...")
    
    cleaned = clean_text_preserve_separator(text_raw)
    cleaned_texts.append(cleaned)

df['text'] = cleaned_texts
print(f"  Cleaned: {len(cleaned_texts)} texts")

# Show example after cleaning
if len(df) > 0:
    print("\n  Example AFTER cleaning:")
    example = df.iloc[0]
    print(f"  BEFORE: {example['text_raw'][:150]}")
    print(f"  AFTER:  {example['text'][:150]}")

# Check emoji conversion
import re
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    "]+", flags=re.UNICODE)

had_emoji = df['text_raw'].str.contains(emoji_pattern, na=False).sum()
has_emo_tag = df['text'].str.contains('<emo_', na=False).sum()
has_person_tag = df['text'].str.contains('<person>', na=False).sum()

print(f"\n  Emoji in raw: {had_emoji}")
print(f"  <emo_*> tags: {has_emo_tag}")
print(f"  <person> tags: {has_person_tag}")

# Save
output_dir = Path(r"data\processed")
output_dir.mkdir(exist_ok=True, parents=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

csv_path = output_dir / f"labeling_task_Quang_CLEANED_{timestamp}.csv"
df.to_csv(csv_path, index=False, encoding='utf-8-sig')

print("\n" + "="*60)
print("RESULTS")
print("="*60)
print(f"Saved: {csv_path.name}")
print(f"\nTotal rows: {len(df)}")
print(f"Emoji converted: {has_emo_tag} (<emo_pos>, <emo_neg>)")
print(f"Person names: {has_person_tag} (<person>)")
print(f"\nColumns: {list(df.columns)}")

print("\n" + "="*60)
print("DONE!")
print("="*60)
