"""
FINAL SOLUTION: Match cleaned text from JSON with cleaned_comment in master
Then get raw_comment (with emoji)
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re

def normalize_for_match(text):
    """Normalize để match chính xác"""
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

def load_master():
    """Load facebook_master"""
    print("\n[1/4] Loading facebook_master.csv...")
    df = pd.read_csv('data/processed/facebook_master.csv', encoding='utf-8')
    
    # Normalize cleaned fields for matching
    df['cleaned_comment_norm'] = df['cleaned_comment'].apply(normalize_for_match)
    df['cleaned_title_norm'] = df['cleaned_title'].apply(normalize_for_match)
    
    print(f"  ✓ Loaded: {len(df)} rows")
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        "]+", flags=re.UNICODE)
    
    has_emoji = df['raw_comment'].str.contains(emoji_pattern, na=False).sum()
    print(f"  ✓ Rows with emoji in raw_comment: {has_emoji}")
    
    return df

def load_json_labels(json_path):
    """Load labels from JSON"""
    print(f"\nLoading {json_path.name}...")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for task in data:
        comment = task.get('data', {}).get('comment', '')
        context = task.get('data', {}).get('context', '')
        
        # Fix encoding
        comment = fix_encoding(comment)
        context = fix_encoding(context)
        
        # Get label
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
            # Normalize
            comment_norm = normalize_for_match(comment)
            context_norm = normalize_for_match(context)
            
            records.append({
                'comment_norm': comment_norm,
                'context_norm': context_norm,
                'label': label,
                'note': note
            })
    
    print(f"  ✓ Loaded: {len(records)} labeled samples")
    return pd.DataFrame(records)

def match_with_master(labels_df, master_df):
    """Match labels với master"""
    print("\n[3/4] Matching labels with master...")
    
    # Create lookup dict: cleaned_comment -> master row
    master_lookup = {}
    for idx, row in master_df.iterrows():
        key_comment = row['cleaned_comment_norm']
        key_title = row['cleaned_title_norm']
        
        if key_comment and len(key_comment) > 5:
            master_lookup[key_comment] = {
                'raw_comment': row['raw_comment'],
                'raw_title': row['raw_title'],
                'id': row['id']
            }
    
    print(f"  Created lookup dict: {len(master_lookup)} entries")
    
    matched = []
    unmatched = 0
    
    for idx, label_row in labels_df.iterrows():
        comment_key = label_row['comment_norm']
        
        if comment_key in master_lookup:
            master_row = master_lookup[comment_key]
            
            # Build full text with raw data (HAS EMOJI!)
            raw_title = master_row['raw_title']
            raw_comment = master_row['raw_comment']
            
            if raw_title and pd.notna(raw_title) and len(str(raw_title).strip()) > 0:
                full_text = f"{raw_title} </s> {raw_comment}"
            else:
                full_text = raw_comment
            
            matched.append({
                'text': full_text,
                'label': label_row['label'],
                'note': label_row['note'],
                'master_id': master_row['id']
            })
        else:
            unmatched += 1
    
    print(f"  ✓ Matched: {len(matched)}")
    print(f"  ✗ Unmatched: {unmatched}")
    
    return pd.DataFrame(matched)

def main():
    print("="*60)
    print("RECOVER EMOJI FROM FACEBOOK_MASTER")
    print("="*60)
    
    # Load master
    master_df = load_master()
    
    # Load labels
    print("\n[2/4] Loading labeled data...")
    base_dir = Path(r"TOXIC_COMMENT\datasets\final")
    
    labels_dfs = []
    
    for json_file in ['final_1k_thien_gold_sample.json', 'final_thien_gold_sample.json']:
        json_path = base_dir / json_file
        if json_path.exists():
            df = load_json_labels(json_path)
            labels_dfs.append(df)
    
    all_labels = pd.concat(labels_dfs, ignore_index=True)
    print(f"\n  ✓ Total labels: {len(all_labels)}")
    
    # Remove duplicates
    all_labels = all_labels.drop_duplicates(subset=['comment_norm'], keep='first')
    print(f"  ✓ After dedup: {len(all_labels)}")
    
    # Match
    matched_df = match_with_master(all_labels, master_df)
    
    if len(matched_df) == 0:
        print("\n✗ No matches found!")
        return
    
    # Check emoji
    print("\n[4/4] Checking emoji...")
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        "]+", flags=re.UNICODE)
    
    has_emoji = matched_df['text'].str.contains(emoji_pattern, na=False).sum()
    print(f"  ✓ Samples with emoji: {has_emoji}/{len(matched_df)} ({100*has_emoji/len(matched_df):.1f}%)")
    
    # Show examples
    emoji_samples = matched_df[matched_df['text'].str.contains(emoji_pattern, na=False)]
    if len(emoji_samples) > 0:
        print("\n" + "="*60)
        print("EXAMPLES WITH EMOJI")
        print("="*60)
        for i, (idx, row) in enumerate(emoji_samples.head(5).iterrows(), 1):
            print(f"\n{i}. {row['text'][:120]}")
            print(f"   Label: {row['label']}")
    
    # Save
    print("\n" + "="*60)
    print("SAVING RESULTS")
    print("="*60)
    
    output_dir = Path(r"data\processed")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    final_df = matched_df[['text', 'label', 'note']].copy()
    
    csv_path = output_dir / f"RECOVERED_from_master_{timestamp}.csv"
    final_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\n✓ CSV saved: {csv_path.name}")
    
    # JSON
    json_path = output_dir / f"RECOVERED_from_master_{timestamp}.json"
    json_data = final_df.to_dict(orient='records')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON saved: {json_path.name}")
    
    # Final stats
    print("\n" + "="*60)
    print("FINAL STATISTICS")
    print("="*60)
    print(f"Total samples: {len(final_df)}")
    print(f"With emoji: {has_emoji} ({100*has_emoji/len(final_df):.1f}%)")
    print(f"\nLabel distribution:")
    for label, count in final_df['label'].value_counts().sort_index().items():
        pct = 100 * count / len(final_df)
        print(f"  Label {label}: {count:,} ({pct:.1f}%)")
    
    print("\n" + "="*60)
    print("✓ DONE!")
    print("="*60)

if __name__ == "__main__":
    main()
