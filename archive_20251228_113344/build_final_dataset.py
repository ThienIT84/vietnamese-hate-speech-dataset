"""
CORRECT APPROACH: Start with ALL JSON labels, then replace with emoji version if available
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys
import re

sys.path.insert(0, str(Path(__file__).parent / 'src'))
from preprocessing.advanced_text_cleaning import clean_text

def normalize_for_match(text):
    if pd.isna(text) or not text:
        return ''
    text = str(text).lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def fix_encoding(text):
    if not text or pd.isna(text):
        return ''
    try:
        return text.encode('latin1').decode('utf-8')
    except:
        return text

def clean_text_preserve_separator(text):
    if not text or pd.isna(text):
        return text
    if ' </s> ' in text:
        parts = text.split(' </s> ')
        cleaned_parts = [clean_text(p.strip()) for p in parts if p.strip()]
        return ' </s> '.join(cleaned_parts) if cleaned_parts else ''
    return clean_text(text)

print("="*60)
print("BUILD COMPLETE DATASET")
print("="*60)

# Step 1: Load ALL JSON labels (BASE TRUTH)
print("\n[1/3] Loading ALL JSON labels (base dataset)...")
base_dir = Path(r"TOXIC_COMMENT\datasets\final")

all_json = []
for json_file in ['final_1k_thien_gold_sample.json', 'final_thien_gold_sample.json']:
    json_path = base_dir / json_file
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for task in data:
            comment = fix_encoding(task.get('data', {}).get('comment', ''))
            context = fix_encoding(task.get('data', {}).get('context', ''))
            
            label = None
            note = ''
            
            if 'annotations' in task and len(task['annotations']) > 0:
                annotation = task['annotations'][0]
                if 'result' in annotation:
                    for item in annotation['result']:
                        if item.get('from_name') == 'label':
                            choices = item.get('value', {}).get('choices', [])
                            if choices:
                                label_str = choices[0]
                                if '0' in label_str:
                                    label = 0
                                elif '1' in label_str:
                                    label = 1
                                elif '2' in label_str:
                                    label = 2
                        
                        if item.get('from_name') == 'note':
                            text_list = item.get('value', {}).get('text', [])
                            if text_list:
                                note = fix_encoding(' '.join(text_list))
            
            if label is not None:
                # Build text from JSON
                if context and len(str(context).strip()) > 0:
                    text_raw_json = f"{context} </s> {comment}"
                else:
                    text_raw_json = comment
                
                all_json.append({
                    'comment': comment,
                    'context': context,
                    'text_raw_json': text_raw_json,
                    'label': label,
                    'note': note
                })

json_df = pd.DataFrame(all_json).drop_duplicates(subset=['comment'], keep='first')
print(f"  Total unique labels: {len(json_df)}")

# Step 2: Load recovered data (emoji versions)
print("\n[2/3] Loading recovered data (emoji versions)...")
recovered = pd.read_csv('data/processed/FINAL_TRAINING_FIXED_20251224_143406.csv', encoding='utf-8-sig')
print(f"  Recovered samples: {len(recovered)}")

# Build lookup: normalized_comment -> (text_cleaned, text_raw_with_emoji)
recovered_lookup = {}
for idx, row in recovered.iterrows():
    # Extract comment from text_raw
    if ' </s> ' in str(row['text_raw']):
        comment_part = row['text_raw'].split(' </s> ')[-1]
    else:
        comment_part = row['text_raw']
    
    key = normalize_for_match(comment_part)
    recovered_lookup[key] = {
        'text': row['text'],
        'text_raw': row['text_raw']
    }

print(f"  Lookup entries: {len(recovered_lookup)}")

# Step 3: Build final dataset
print("\n[3/3] Building final dataset...")

final_data = []
matched_count = 0
for idx, row in json_df.iterrows():
    comment_key = normalize_for_match(row['comment'])
    
    # Check if we have emoji version
    if comment_key in recovered_lookup:
        # Use emoji version
        rec = recovered_lookup[comment_key]
        final_data.append({
            'text': rec['text'],
            'label': row['label'],
            'note': row['note'],
            'text_raw': rec['text_raw'],
            'source': 'emoji_recovered'
        })
        matched_count += 1
    else:
        # Use JSON version (no emoji)
        text_cleaned = clean_text_preserve_separator(row['text_raw_json'])
        final_data.append({
            'text': text_cleaned,
            'label': row['label'],
            'note': row['note'],
            'text_raw': row['text_raw_json'],
            'source': 'json_only'
        })

final_df = pd.DataFrame(final_data)
print(f"  Emoji version: {matched_count}")
print(f"  JSON only: {len(final_df) - matched_count}")
print(f"  TOTAL: {len(final_df)}")

# Check emoji
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    "]+", flags=re.UNICODE)

has_emoji = final_df['text_raw'].str.contains(emoji_pattern, na=False).sum()
print(f"  With emoji: {has_emoji} ({100*has_emoji/len(final_df):.1f}%)")

# Save
output_dir = Path(r"data\processed")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

csv_path = output_dir / f"TRAINING_COMPLETE_{timestamp}.csv"
final_df.to_csv(csv_path, index=False, encoding='utf-8-sig')

json_path = output_dir / f"TRAINING_COMPLETE_{timestamp}.json"
json_data = final_df.to_dict(orient='records')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)
print(f"Saved: {csv_path.name}")
print(f"Saved: {json_path.name}")
print(f"\nTotal samples: {len(final_df)}")
print(f"  - With emoji: {has_emoji} ({100*has_emoji/len(final_df):.1f}%)")
print(f"  - No emoji: {len(final_df)-has_emoji} ({100*(len(final_df)-has_emoji)/len(final_df):.1f}%)")

print(f"\nBy source:")
for source, count in final_df['source'].value_counts().items():
    pct = 100 * count / len(final_df)
    print(f"  {source}: {count:,} ({pct:.1f}%)")

print(f"\nLabel distribution:")
for label, count in final_df['label'].value_counts().sort_index().items():
    pct = 100 * count / len(final_df)
    print(f"  Label {label}: {count:,} ({pct:.1f}%)")

print("\n" + "="*60)
print(f"SUCCESS: {len(final_df)} LABELED SAMPLES!")
print("="*60)
