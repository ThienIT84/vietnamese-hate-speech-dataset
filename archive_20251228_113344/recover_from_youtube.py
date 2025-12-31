"""
Match unmatched samples với youtube_master.csv
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re

def normalize_for_match(text):
    """Normalize để match"""
    if pd.isna(text) or not text:
        return ''
    text = str(text).lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def fix_encoding(text):
    """Fix encoding"""
    if not text or pd.isna(text):
        return ''
    try:
        return text.encode('latin1').decode('utf-8')
    except:
        return text

print("="*60)
print("RECOVER FROM YOUTUBE_MASTER")
print("="*60)

# Load youtube_master
print("\n[1/3] Loading youtube_master.csv...")
youtube = pd.read_csv('data/processed/youtube_master.csv', encoding='utf-8')
youtube['cleaned_comment_norm'] = youtube['cleaned_comment'].apply(normalize_for_match)
print(f"  ✓ Loaded: {len(youtube)} rows")

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    "]+", flags=re.UNICODE)

has_emoji = youtube['raw_comment'].str.contains(emoji_pattern, na=False).sum()
print(f"  ✓ Rows with emoji: {has_emoji}")

# Load labels from JSON
print("\n[2/3] Loading labels...")
base_dir = Path(r"TOXIC_COMMENT\datasets\final")

all_labels = []
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
                all_labels.append({
                    'comment_norm': normalize_for_match(comment),
                    'context_norm': normalize_for_match(context),
                    'label': label,
                    'note': note
                })

labels_df = pd.DataFrame(all_labels).drop_duplicates(subset=['comment_norm'], keep='first')
print(f"  ✓ Total labels: {len(labels_df)}")

# Match với youtube
print("\n[3/3] Matching with youtube_master...")

youtube_lookup = {}
for idx, row in youtube.iterrows():
    key = row['cleaned_comment_norm']
    if key and len(key) > 5:
        youtube_lookup[key] = {
            'raw_comment': row['raw_comment'],
            'raw_title': row['raw_title'],
            'id': row['id']
        }

print(f"  Created lookup: {len(youtube_lookup)} entries")

matched_youtube = []
for idx, label_row in labels_df.iterrows():
    comment_key = label_row['comment_norm']
    
    if comment_key in youtube_lookup:
        yt_row = youtube_lookup[comment_key]
        
        raw_title = yt_row['raw_title']
        raw_comment = yt_row['raw_comment']
        
        if raw_title and pd.notna(raw_title) and len(str(raw_title).strip()) > 0:
            full_text = f"{raw_title} </s> {raw_comment}"
        else:
            full_text = raw_comment
        
        matched_youtube.append({
            'text': full_text,
            'label': label_row['label'],
            'note': label_row['note'],
            'source': 'youtube'
        })

print(f"  ✓ Matched: {len(matched_youtube)}")

if len(matched_youtube) > 0:
    youtube_df = pd.DataFrame(matched_youtube)
    
    # Check emoji
    has_emoji_yt = youtube_df['text'].str.contains(emoji_pattern, na=False).sum()
    print(f"  ✓ With emoji: {has_emoji_yt} ({100*has_emoji_yt/len(youtube_df):.1f}%)")
    
    # Show examples
    if has_emoji_yt > 0:
        emoji_samples = youtube_df[youtube_df['text'].str.contains(emoji_pattern, na=False)]
        print("\n" + "="*60)
        print("EXAMPLES FROM YOUTUBE")
        print("="*60)
        for i, (idx, row) in enumerate(emoji_samples.head(3).iterrows(), 1):
            print(f"\n{i}. {row['text'][:120]}")
            print(f"   Label: {row['label']}")
    
    # Load previous facebook results
    print("\n" + "="*60)
    print("COMBINING WITH FACEBOOK RESULTS")
    print("="*60)
    
    fb_df = pd.read_csv('data/processed/RECOVERED_from_master_20251224_142151.csv', encoding='utf-8-sig')
    print(f"\nFacebook: {len(fb_df)} samples")
    print(f"Youtube:  {len(youtube_df)} samples")
    
    # Combine
    combined = pd.concat([fb_df, youtube_df[['text', 'label', 'note']]], ignore_index=True)
    combined = combined.drop_duplicates(subset=['text'], keep='first')
    
    print(f"Combined: {len(combined)} samples (after dedup)")
    
    # Final emoji count
    has_emoji_final = combined['text'].str.contains(emoji_pattern, na=False).sum()
    print(f"\n✓ TOTAL WITH EMOJI: {has_emoji_final}/{len(combined)} ({100*has_emoji_final/len(combined):.1f}%)")
    
    # Save
    output_dir = Path(r"data\processed")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    csv_path = output_dir / f"FINAL_RECOVERED_FB_YT_{timestamp}.csv"
    combined.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    json_path = output_dir / f"FINAL_RECOVERED_FB_YT_{timestamp}.json"
    json_data = combined.to_dict(orient='records')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(f"✓ Saved: {csv_path.name}")
    print(f"✓ Saved: {json_path.name}")
    print(f"\nTotal samples: {len(combined)}")
    print(f"With emoji: {has_emoji_final} ({100*has_emoji_final/len(combined):.1f}%)")
    print(f"\nLabel distribution:")
    for label, count in combined['label'].value_counts().sort_index().items():
        pct = 100 * count / len(combined)
        print(f"  Label {label}: {count:,} ({pct:.1f}%)")
    
    print("\n" + "="*60)
    print("✓ SUCCESS!")
    print("="*60)
else:
    print("\n✗ No matches found in youtube_master")
