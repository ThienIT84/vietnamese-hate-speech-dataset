"""
Fix encoding issue trong Label Studio JSON files
Decode Latin1 -> UTF-8 để recover emoji
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import re

def fix_encoding_text(text):
    """
    Fix text bị encode nhầm Latin1/Windows-1252 thành UTF-8
    """
    if not text or pd.isna(text):
        return ''
    
    try:
        # Text đã bị decode nhầm UTF-8, encode lại Latin1 rồi decode đúng UTF-8
        fixed = text.encode('latin1').decode('utf-8')
        return fixed
    except:
        return text

def load_and_fix_labelstudio_json(json_path):
    """Load and fix encoding JSON from Label Studio"""
    print(f"\nReading and fixing encoding: {json_path.name}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for task in data:
        # Lấy comment và context
        comment = task.get('data', {}).get('comment', '')
        context = task.get('data', {}).get('context', '')
        
        # Fix encoding
        comment_fixed = fix_encoding_text(comment)
        context_fixed = fix_encoding_text(context)
        
        # Lấy label
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
                            note_raw = ' '.join(text_list)
                            note = fix_encoding_text(note_raw)
        
        if label is not None:
            # Create full text
            if context_fixed and len(context_fixed.strip()) > 0:
                full_text = f"{context_fixed} </s> {comment_fixed}"
            else:
                full_text = comment_fixed
            
            records.append({
                'text': full_text,
                'label': label,
                'note': note,
                'comment': comment_fixed,
                'context': context_fixed,
                'source_file': json_path.name
            })
    
    print(f"  Loaded and fixed: {len(records)} samples")
    return pd.DataFrame(records)

def clean_text_keep_emoji(text):
    """Clean text minimal - GIỮ emoji"""
    if pd.isna(text) or not text:
        return ''
    
    text = str(text)
    
    # Teencode cơ bản
    replacements = {
        r'\bko\b': 'không', r'\bk\b': 'không', r'\bkh\b': 'không',
        r'\bdc\b': 'được', r'\bđc\b': 'được',
        r'\bvs\b': 'với', r'\bvj\b': 'vì',
        r'\br\b': 'rồi', r'\bz\b': 'vậy', r'\bv\b': 'vậy',
        r'\bmk\b': 'mình', r'\bt\b': 'tôi',
        r'\bng\b': 'người', r'\bmn\b': 'mọi người',
        r'\bvcl\b': 'vãi cả lồn', r'\bvkl\b': 'vãi cả lồn',
        r'\bloz\b': 'lồn', r'\blol\b': 'lồn',
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def main():
    print("="*60)
    print("FIX ENCODING AND RECOVER EMOJI FROM LABEL STUDIO JSON")
    print("="*60)
    
    base_dir = Path(r"c:\Học sâu\Dataset\TOXIC_COMMENT\datasets\final")
    
    # Load và fix JSON files
    dfs = []
    
    json1 = base_dir / "final_1k_thien_gold_sample.json"
    if json1.exists():
        df1 = load_and_fix_labelstudio_json(json1)
        dfs.append(df1)
    
    json2 = base_dir / "final_thien_gold_sample.json"
    if json2.exists():
        df2 = load_and_fix_labelstudio_json(json2)
        dfs.append(df2)
    
    # Merge
    all_data = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal: {len(all_data)} samples")
    
    # Remove duplicates
    all_data = all_data.drop_duplicates(subset=['text'], keep='first')
    print(f"After removing duplicates: {len(all_data)}")
    
    # Apply text cleaning (GIỮ emoji)
    print("\nApplying text cleaning (keeping emoji)...")
    all_data['text_cleaned'] = all_data['text'].apply(clean_text_keep_emoji)
    
    # Check emoji
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    has_emoji = all_data['text_cleaned'].str.contains(emoji_pattern, na=False).sum()
    print(f"\n✓ Samples có emoji: {has_emoji}/{len(all_data)}")
    
    # Show examples
    emoji_samples = all_data[all_data['text_cleaned'].str.contains(emoji_pattern, na=False)]
    if len(emoji_samples) > 0:
        print("\n" + "="*60)
        print("EXAMPLES WITH EMOJI:")
        print("="*60)
        for i, row in emoji_samples.head(10).iterrows():
            print(f"\n{i+1}. {row['text_cleaned'][:150]}")
            print(f"   Label: {row['label']}")
    
    # Save
    output_dir = Path(r"c:\Học sâu\Dataset\data\processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Final dataset
    final_df = all_data[['text_cleaned', 'label', 'note']].copy()
    final_df.columns = ['text', 'label', 'note']
    
    # CSV
    csv_path = output_dir / f"FIXED_ENCODING_emoji_{timestamp}.csv"
    final_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\n✓ CSV: {csv_path}")
    
    # JSON
    json_path = output_dir / f"FIXED_ENCODING_emoji_{timestamp}.json"
    json_data = final_df.to_dict(orient='records')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON: {json_path}")
    
    # Stats
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    print(f"Total samples: {len(final_df)}")
    print(f"Has emoji: {has_emoji} samples ({100*has_emoji/len(final_df):.1f}%)")
    print(f"\nLabel distribution:")
    print(final_df['label'].value_counts().sort_index())
    
    # Check tags
    has_person = final_df['text'].str.contains('<person>', na=False).sum()
    print(f"\nSamples with <person> tag: {has_person}/{len(final_df)}")

if __name__ == "__main__":
    main()
