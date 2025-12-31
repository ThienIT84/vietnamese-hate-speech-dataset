"""
Match labeled data với facebook_master.csv để lấy lại emoji
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import re

def normalize_text(text):
    """Normalize text để matching"""
    if pd.isna(text) or not text:
        return ''
    text = str(text).lower()
    # Remove emoji
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    # Remove tags and special chars
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def fix_encoding(text):
    """Fix encoding Latin1 -> UTF-8"""
    if not text or pd.isna(text):
        return ''
    try:
        return text.encode('latin1').decode('utf-8')
    except:
        return text

def load_master():
    """Load facebook_master.csv"""
    print("\nLoading facebook_master.csv...")
    df = pd.read_csv('data/processed/facebook_master.csv', encoding='utf-8')
    
    # Create normalized text for matching
    df['comment_norm'] = df['raw_comment'].apply(normalize_text)
    df['title_norm'] = df['raw_title'].apply(normalize_text)
    df['full_norm'] = df['title_norm'] + ' ' + df['comment_norm']
    
    print(f"  Loaded: {len(df)} rows")
    
    # Check emoji
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE)
    
    has_emoji = df['raw_comment'].str.contains(emoji_pattern, na=False).sum()
    print(f"  Rows with emoji: {has_emoji}")
    
    return df

def load_json_labels(json_path):
    """Load labels from Label Studio JSON"""
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
                    if item.get('from_name') == 'label' and item.get('type') == 'choices':
                        choices = item.get('value', {}).get('choices', [])
                        if choices:
                            label_str = choices[0]
                            if '0' in label_str:
                                label = 0
                            elif '1' in label_str:
                                label = 1
                            elif '2' in label_str:
                                label = 2
                    
                    if item.get('from_name') == 'note' and item.get('type') == 'textarea':
                        text_list = item.get('value', {}).get('text', [])
                        if text_list:
                            note = ' '.join(text_list)
                            note = fix_encoding(note)
        
        if label is not None:
            # Normalize for matching
            comment_norm = normalize_text(comment)
            context_norm = normalize_text(context)
            full_norm = context_norm + ' ' + comment_norm
            
            records.append({
                'comment_norm': comment_norm,
                'context_norm': context_norm,
                'full_norm': full_norm,
                'label': label,
                'note': note
            })
    
    print(f"  Loaded: {len(records)} labeled samples")
    return pd.DataFrame(records)

def match_and_merge(labels_df, master_df):
    """Match labels với master để lấy raw data có emoji"""
    print("\n" + "="*60)
    print("MATCHING LABELS WITH MASTER DATA")
    print("="*60)
    
    # Create dict for fast lookup
    master_dict = {}
    for idx, row in master_df.iterrows():
        key = row['full_norm']
        if key and len(key) > 10:  # Skip very short texts
            master_dict[key] = {
                'raw_comment': row['raw_comment'],
                'raw_title': row['raw_title'],
                'id': row['id']
            }
    
    print(f"\nMaster dict size: {len(master_dict)}")
    
    matched = []
    unmatched = 0
    
    for idx, label_row in labels_df.iterrows():
        key = label_row['full_norm']
        
        if key in master_dict:
            # Exact match!
            master_row = master_dict[key]
            
            # Create full text with raw data (có emoji)
            if master_row['raw_title'] and pd.notna(master_row['raw_title']):
                full_text = f"{master_row['raw_title']} </s> {master_row['raw_comment']}"
            else:
                full_text = master_row['raw_comment']
            
            matched.append({
                'text': full_text,
                'label': label_row['label'],
                'note': label_row['note'],
                'master_id': master_row['id']
            })
        else:
            unmatched += 1
    
    print(f"\nMatched: {len(matched)}")
    print(f"Unmatched: {unmatched}")
    
    return pd.DataFrame(matched)

def main():
    print("="*60)
    print("RECOVER EMOJI FROM FACEBOOK_MASTER.CSV")
    print("="*60)
    
    # Load master
    master_df = load_master()
    
    # Load labels from JSON files
    base_dir = Path(r"c:\Học sâu\Dataset\TOXIC_COMMENT\datasets\final")
    
    labels_dfs = []
    
    json1 = base_dir / "final_1k_thien_gold_sample.json"
    if json1.exists():
        df1 = load_json_labels(json1)
        labels_dfs.append(df1)
    
    json2 = base_dir / "final_thien_gold_sample.json"
    if json2.exists():
        df2 = load_json_labels(json2)
        labels_dfs.append(df2)
    
    # Merge all labels
    all_labels = pd.concat(labels_dfs, ignore_index=True)
    print(f"\nTotal labels: {len(all_labels)}")
    
    # Remove duplicates
    all_labels = all_labels.drop_duplicates(subset=['full_norm'], keep='first')
    print(f"After dedup: {len(all_labels)}")
    
    # Match
    matched_df = match_and_merge(all_labels, master_df)
    
    if len(matched_df) == 0:
        print("\nNo matches found!")
        return
    
    # Check emoji
    print("\n" + "="*60)
    print("EMOJI CHECK")
    print("="*60)
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+", flags=re.UNICODE)
    
    has_emoji = matched_df['text'].str.contains(emoji_pattern, na=False).sum()
    print(f"\nSamples with emoji: {has_emoji}/{len(matched_df)} ({100*has_emoji/len(matched_df):.1f}%)")
    
    # Show examples
    emoji_samples = matched_df[matched_df['text'].str.contains(emoji_pattern, na=False)]
    if len(emoji_samples) > 0:
        print("\nExamples with emoji:")
        for i, row in emoji_samples.head(5).iterrows():
            print(f"\n{i+1}. {row['text'][:120]}")
            print(f"   Label: {row['label']}")
    
    # Save
    output_dir = Path(r"c:\Học sâu\Dataset\data\processed")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    final_df = matched_df[['text', 'label', 'note']].copy()
    
    csv_path = output_dir / f"RECOVERED_emoji_from_master_{timestamp}.csv"
    final_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\n✓ Saved: {csv_path}")
    
    # Stats
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Total samples: {len(final_df)}")
    print(f"With emoji: {has_emoji} ({100*has_emoji/len(final_df):.1f}%)")
    print(f"\nLabel distribution:")
    print(final_df['label'].value_counts().sort_index())

if __name__ == "__main__":
    main()
