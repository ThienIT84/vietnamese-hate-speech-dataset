"""
Match raw data (có emoji) với label từ Label Studio
Flow:
1. Load label từ 3 file Label Studio export
2. Load raw data từ source có emoji
3. Match bằng comment similarity
4. Clean text nhưng GIỮ emoji
5. Output final dataset
"""

import pandas as pd
import json
import re
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher

# Import advanced_text_cleaning nhưng tắt emoji removal
import sys
sys.path.append(r'c:\Học sâu\Dataset\src\preprocessing')

def clean_text_keep_emoji(text):
    """
    Clean text minimal - CHỈ normalize teencode, GIỮ emoji và tất cả tags
    """
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

def normalize_for_matching(text):
    """
    Normalize text để match (remove emoji, tags, special chars)
    """
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
    
    # Remove tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove punctuation and extra spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a, b).ratio()

def load_labelstudio_json(json_path):
    """Load JSON từ Label Studio"""
    print(f"\nĐọc Label Studio JSON: {json_path.name}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for task in data:
        # Lấy comment
        comment = task.get('data', {}).get('comment', '')
        context = task.get('data', {}).get('context', '')
        
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
                            note = ' '.join(text_list)
        
        if label is not None:
            # Normalize để match
            norm_comment = normalize_for_matching(comment)
            norm_context = normalize_for_matching(context)
            
            records.append({
                'comment_normalized': norm_comment,
                'context_normalized': norm_context,
                'label': label,
                'note': note,
                'source_file': json_path.name
            })
    
    print(f"  Loaded: {len(records)} labeled samples")
    return pd.DataFrame(records)

def load_labelstudio_csv(csv_path):
    """Load CSV từ Label Studio export"""
    print(f"\nĐọc Label Studio CSV: {csv_path.name}")
    
    df = pd.read_csv(csv_path, encoding='utf-8')
    df_labeled = df[df['label'].notna()].copy()
    
    records = []
    for _, row in df_labeled.iterrows():
        # Parse input_text để lấy context và comment
        input_text = str(row['input_text'])
        if '</s>' in input_text:
            parts = input_text.split('</s>')
            context = parts[0].strip()
            comment = parts[1].strip() if len(parts) > 1 else ''
        else:
            context = ''
            comment = input_text
        
        # Normalize
        norm_comment = normalize_for_matching(comment)
        norm_context = normalize_for_matching(context)
        
        records.append({
            'comment_normalized': norm_comment,
            'context_normalized': norm_context,
            'label': int(row['label']),
            'note': str(row.get('note', '')) if pd.notna(row.get('note')) else '',
            'source_file': csv_path.name
        })
    
    print(f"  Loaded: {len(records)} labeled samples")
    return pd.DataFrame(records)

def load_raw_data_csv(csv_path):
    """Load raw data CSV (có emoji)"""
    print(f"\nĐọc raw data: {csv_path.name}")
    
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    records = []
    for _, row in df.iterrows():
        raw_comment = str(row.get('raw_comment', '')) if pd.notna(row.get('raw_comment')) else ''
        raw_title = str(row.get('raw_title', '')) if pd.notna(row.get('raw_title')) else ''
        
        # Normalize để match
        norm_comment = normalize_for_matching(raw_comment)
        norm_title = normalize_for_matching(raw_title)
        
        records.append({
            'raw_comment': raw_comment,
            'raw_title': raw_title,
            'comment_normalized': norm_comment,
            'title_normalized': norm_title,
            'row_id': row.get('id', '')
        })
    
    print(f"  Loaded: {len(records)} raw samples")
    return pd.DataFrame(records)

def match_and_merge(labels_df, raw_df, threshold=0.85):
    """
    Match labels với raw data dựa trên similarity - OPTIMIZED
    """
    print("\n" + "="*60)
    print("MATCHING LABELS VỚI RAW DATA")
    print("="*60)
    
    matched = []
    unmatched_labels = []
    
    # Create index dict cho nhanh
    raw_index = {}
    for idx, raw_row in raw_df.iterrows():
        key = raw_row['comment_normalized'][:50]  # First 50 chars as key
        if key not in raw_index:
            raw_index[key] = []
        raw_index[key].append(raw_row)
    
    print(f"Created index with {len(raw_index)} buckets")
    
    total = len(labels_df)
    processed = 0
    
    for idx, label_row in labels_df.iterrows():
        processed += 1
        if processed % 500 == 0:
            print(f"  Processed {processed}/{total} ({100*processed/total:.1f}%)")
        label_comment_norm = label_row['comment_normalized']
        label_context_norm = label_row['context_normalized']
        
        # Tìm raw data tương tự nhất
        best_match = None
        best_score = 0
        
        # Fast lookup: chỉ so sánh với candidates có prefix giống
        candidates = []
        key_prefix = label_comment_norm[:50]
        
        # Tìm exact match trước
        if key_prefix in raw_index:
            candidates.extend(raw_index[key_prefix])
        
        # Nếu không tìm thấy exact, expand search (chậm hơn)
        if not candidates:
            # Chỉ so sánh với subset ngẫu nhiên để tăng tốc
            import random
            candidates = random.sample(list(raw_df.itertuples(index=False)), min(100, len(raw_df)))
        
        for raw_row in candidates:
            if hasattr(raw_row, 'comment_normalized'):  # From itertuples
                raw_comment_norm = raw_row.comment_normalized
                raw_title_norm = raw_row.title_normalized
                raw_comment = raw_row.raw_comment
                raw_title = raw_row.raw_title
            else:  # From dict
                raw_comment_norm = raw_row['comment_normalized']
                raw_title_norm = raw_row['title_normalized']
                raw_comment = raw_row['raw_comment']
                raw_title = raw_row['raw_title']
            
            # Quick check: length difference
            len_diff = abs(len(label_comment_norm) - len(raw_comment_norm))
            if len_diff > max(len(label_comment_norm), len(raw_comment_norm)) * 0.5:
                continue
            
            # Match comment (simple approach)
            if label_comment_norm == raw_comment_norm:
                score_comment = 1.0
            else:
                # Count common words
                label_words = set(label_comment_norm.split())
                raw_words = set(raw_comment_norm.split())
                if not label_words or not raw_words:
                    score_comment = 0
                else:
                    common = label_words & raw_words
                    score_comment = len(common) / max(len(label_words), len(raw_words))
            
            # Match context
            if label_context_norm == raw_title_norm:
                score_context = 1.0
            else:
                label_ctx_words = set(label_context_norm.split())
                raw_ctx_words = set(raw_title_norm.split())
                if not label_ctx_words or not raw_ctx_words:
                    score_context = 0
                else:
                    common_ctx = label_ctx_words & raw_ctx_words
                    score_context = len(common_ctx) / max(len(label_ctx_words), len(raw_ctx_words))
            
            # Combined score
            total_score = (score_comment * 0.7 + score_context * 0.3)
            
            if total_score > best_score:
                best_score = total_score
                best_match = {
                    'raw_comment': raw_comment,
                    'raw_title': raw_title
                }
        
        if best_score >= threshold and best_match is not None:
            # Match thành công!
            # Merge context và comment từ raw
            cleaned_comment = clean_text_keep_emoji(best_match['raw_comment'])
            cleaned_context = clean_text_keep_emoji(best_match['raw_title'])
            
            if cleaned_context and len(cleaned_context.strip()) > 0:
                full_text = f"{cleaned_context} </s> {cleaned_comment}"
            else:
                full_text = cleaned_comment
            
            matched.append({
                'text': full_text,
                'label': label_row['label'],
                'note': label_row['note'],
                'raw_comment': best_match['raw_comment'],
                'raw_title': best_match['raw_title'],
                'match_score': best_score,
                'source': label_row['source_file']
            })
        else:
            unmatched_labels.append({
                'comment': label_comment_norm[:50],
                'label': label_row['label'],
                'best_score': best_score
            })
    
    print(f"\n✓ Matched: {len(matched)}")
    print(f"⚠ Unmatched: {len(unmatched_labels)}")
    
    if unmatched_labels and len(unmatched_labels) <= 10:
        print("\nUnmatched samples:")
        for um in unmatched_labels[:5]:
            print(f"  - {um['comment']}... (score: {um['best_score']:.2f})")
    
    return pd.DataFrame(matched), unmatched_labels

def main():
    print("="*60)
    print("MATCH RAW DATA (CÓ EMOJI) VỚI LABELS TỪ LABEL STUDIO")
    print("="*60)
    
    base_dir = Path(r"c:\Học sâu\Dataset\TOXIC_COMMENT\datasets\final")
    
    # 1. Load labels từ Label Studio
    labels_dfs = []
    
    # JSON 1
    json1 = base_dir / "final_1k_thien_gold_sample.json"
    if json1.exists():
        df1 = load_labelstudio_json(json1)
        labels_dfs.append(df1)
    
    # JSON 2  
    json2 = base_dir / "final_thien_gold_sample.json"
    if json2.exists():
        df2 = load_labelstudio_json(json2)
        labels_dfs.append(df2)
    
    # CSV Quang (labels)
    csv_quang = base_dir / "labeling_task_Quang.csv"
    if csv_quang.exists():
        df3 = load_labelstudio_csv(csv_quang)
        labels_dfs.append(df3)
    
    # Merge all labels
    all_labels = pd.concat(labels_dfs, ignore_index=True)
    print(f"\nTổng labels: {len(all_labels)}")
    
    # Remove duplicates
    all_labels = all_labels.drop_duplicates(subset=['comment_normalized'], keep='first')
    print(f"Sau khi xóa duplicates: {len(all_labels)}")
    
    # 2. Load raw data (có emoji)
    raw_df = load_raw_data_csv(csv_quang)
    
    # 3. Match
    matched_df, unmatched = match_and_merge(all_labels, raw_df, threshold=0.80)
    
    if len(matched_df) == 0:
        print("\n❌ Không match được sample nào!")
        return
    
    # 4. Check emoji
    print("\n" + "="*60)
    print("KIỂM TRA EMOJI")
    print("="*60)
    
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    has_emoji = matched_df['raw_comment'].str.contains(emoji_pattern, na=False).sum()
    print(f"\n✓ Samples có emoji: {has_emoji}/{len(matched_df)}")
    
    # Show samples
    emoji_samples = matched_df[matched_df['raw_comment'].str.contains(emoji_pattern, na=False)]
    if len(emoji_samples) > 0:
        print("\nVí dụ có emoji:")
        for _, row in emoji_samples.head(3).iterrows():
            print(f"  Raw: {row['raw_comment'][:80]}")
            print(f"  Label: {row['label']}\n")
    
    # 5. Save
    print("="*60)
    print("LƯU FILE")
    print("="*60)
    
    output_dir = Path(r"c:\Học sâu\Dataset\data\processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Final dataset (text + label)
    final_df = matched_df[['text', 'label', 'note']].copy()
    
    # CSV
    csv_path = output_dir / f"final_with_emoji_{timestamp}.csv"
    final_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"\n✓ CSV: {csv_path}")
    
    # JSON
    json_path = output_dir / f"final_with_emoji_{timestamp}.json"
    json_data = final_df.to_dict(orient='records')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"✓ JSON: {json_path}")
    
    # Stats
    print(f"\n{'='*60}")
    print("KẾT QUẢ")
    print(f"{'='*60}")
    print(f"Tổng samples: {len(final_df)}")
    print(f"Có emoji: {has_emoji} samples")
    print(f"\nPhân bố label:")
    print(final_df['label'].value_counts().sort_index())

if __name__ == "__main__":
    main()
