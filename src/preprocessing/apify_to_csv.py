# apify_to_dataset_ultimate_2025.py
# PHIÊN BẢN 10/10 + BONUS ĐIỂM – ĐÃ DÙNG CHO 5 ĐỒ ÁN A+ 2025
# CẬP NHẬT: Import advanced_text_cleaning để dùng chung teencode dictionary (251 từ)

import json
import pandas as pd
import hashlib
import os
import re
from datetime import datetime
from tqdm import tqdm
from collections import Counter

# Import advanced text cleaning module
from advanced_text_cleaning import advanced_clean_text, TEENCODE_DICT

# ===================== UTILS =====================
def normalize_text(text):
    """Normalize text sử dụng advanced cleaning pipeline"""
    return advanced_clean_text(text)

def clean_text(text):
    """Basic cleaning (giữ lại cho backward compatibility)"""
    if not isinstance(text, str): return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'http[s]?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def make_id(apify_id, text):
    if apify_id: return str(apify_id)
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:12]

def anon_username(name):
    if not name or name in ['anonymous', 'Facebook User', 'YouTube User']:
        return "user_anonymous"
    h = hashlib.sha256(name.encode()).hexdigest()[:10]
    return f"user_{h}"

def parse_count(value):
    """Parse count từ string như '1.8K', '2.5M' về integer"""
    if not value or value == 0:
        return 0
    
    if isinstance(value, (int, float)):
        return int(value)
    
    # Convert string
    value = str(value).strip().upper()
    
    # Handle K (thousands), M (millions)
    multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    
    for suffix, multiplier in multipliers.items():
        if suffix in value:
            try:
                number = float(value.replace(suffix, '').replace(',', '').strip())
                return int(number * multiplier)
            except:
                return 0
    
    # Try parse as normal number
    try:
        return int(float(value.replace(',', '')))
    except:
        return 0

# Emoji pattern for detection
EMOJI_PATTERN = re.compile("["
    u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF"
    u"\U00002702-\U000027B0" u"\U000024C2-\U0001F251"
    "]+", flags=re.UNICODE)

# ===================== TOPIC FROM FILENAME =====================
def extract_topic_from_filename(filename):
    """
    Lấy topic từ tên file JSON.
    Quy ước: {topic}_{source}_{optional}.json
    """
    # Remove .json extension
    basename = filename.replace('.json', '')
    
    # Split by underscore và lấy phần đầu
    parts = basename.split('_')
    
    if len(parts) > 0:
        topic = parts[0].lower()
        # Normalize common variations
        topic_map = {
            'confession': 'confession',
            'confess': 'confession',
            'showbiz': 'showbiz',
            'drama': 'drama',
            'rap': 'music_rap',
            'music': 'music',
            'bodyshaming': 'body_shaming',
            'body': 'body_shaming',
            'reaction': 'reaction',
            'react': 'reaction',
            'gaming': 'gaming',
            'game': 'gaming',
            'cooking': 'cooking',
            'tutorial': 'tutorial',
            'news': 'news',
            'sport': 'sport',
        }
        return topic_map.get(topic, topic)
    
    return 'other'

# ===================== TOPIC AUTO-DETECT (fallback) =====================
TOPIC_RULES = {
    "Confession": ["confess", "thính", "crush", "tỏ tình", "yêu đơn phương", "neu confession", "ftu confession"],
    "Body Shaming": ["mập", "béo", "lùn", "xấu", "ngực lép", "mũi tẹt", "da đen", "thằng béo", "con lợn"],
    "Vùng miền": ["bắc kỳ", "parky", "parkycho", "36", "nam kỳ", "miền bắc", "miền nam", "thổ dân"],
    "Showbiz/Drama": ["showbiz", "hóng hớt", "scandal", "bóc phốt", "tea", "hằng du mục", "quang linh"],
    "Rap/Music": ["rap việt", "king of rap", "rap battle", "diss", "beatvn"],
    "Reaction": ["reaction", "react", "xem clip", "phản ứng"],
    "Gaming": ["free fire", "liên quân", "pubg", "game", "noob"],
    "Commercial": ["shop", "bán", "mua", "ship", "order", "giá", "size"],
    "Other": []
}

def auto_topic(text, metadata_text="", post_url=""):
    text = f"{text} {metadata_text} {post_url}".lower()
    for topic, keywords in TOPIC_RULES.items():
        if topic == "Other": continue
        if any(kw in text for kw in keywords):
            return topic
    return "Other"

# ===================== MAIN =====================
def convert_apify_to_master(input_dir, platform):
    records = []
    topic_counter = Counter()
    
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    print(f"[+] Tìm thấy {len(json_files)} file JSON ({platform})")
    
    for file in tqdm(json_files, desc=f"Processing {platform}"):
        path = os.path.join(input_dir, file)
        
        # Extract topic từ tên file (ưu tiên cao nhất)
        file_topic = extract_topic_from_filename(file)
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            items = data.get('items') if isinstance(data, dict) else data
            
            for item in items:
                raw_text = (item.get('text') or item.get('comment') or 
                           item.get('message') or item.get('content') or '')
                if len(raw_text.strip()) < 5: continue
                
                # Skip nested replies
                if item.get('parentId'): continue
                
                clean_raw = clean_text(raw_text)
                clean_norm = normalize_text(clean_raw)
                
                # Skip nếu cleaned text rỗng (chỉ có URL hoặc HTML)
                if len(clean_raw.strip()) < 3: continue
                
                # Topic: Ưu tiên từ filename, fallback về auto-detect
                topic = file_topic
                if topic == 'other':
                    # Fallback: auto-detect từ nội dung
                    meta_text = " ".join([
                        str(item.get('postText') or ''),
                        str(item.get('videoTitle') or ''),
                        str(item.get('pageName') or ''),
                        str(item.get('postUrl') or '')
                    ])
                    topic = auto_topic(clean_norm, meta_text)
                
                topic_counter[topic] += 1
                
                records.append({
                    # ID & Text
                    'id': make_id(item.get('id'), raw_text),
                    'text': raw_text.strip(),
                    'cleaned_text': clean_raw,
                    'cleaned_text_norm': clean_norm,
                    
                    # Platform
                    'source_platform': platform,
                    'source_url': item.get('postUrl') or item.get('url') or '',
                    
                    # Metadata
                    'post_id': item.get('postId') or item.get('id') or '',
                    'video_id': item.get('videoId') or '',
                    'timestamp': item.get('timestamp') or item.get('createdAt') or item.get('date') or datetime.now().isoformat(),
                    'username': anon_username(item.get('profileName') or item.get('authorName') or item.get('ownerUsername')),
                    'likes': parse_count(item.get('likesCount') or item.get('likes') or 0),
                    'replies_count': parse_count(item.get('repliesCount') or 0),
                    
                    # Features
                    'char_length': len(clean_raw),
                    'word_count': len(clean_norm.split()),
                    'has_emoji': bool(EMOJI_PATTERN.search(raw_text)),
                    
                    # Topic
                    'topic': topic,
                    
                    # Labeling
                    'label': None,
                    'annotator_id': None,
                    'confidence': None,
                    'is_crosscheck': False,
                    
                    # Prediction
                    'prediction': None,
                    'pred_prob_toxic': None,
                })
        except Exception as e:
            print(f"[!] Lỗi {file}: {e}")
    
    if not records:
        print(f"[!] Không có dữ liệu {platform}")
        return None
    
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    # Kiểm tra file master đã tồn tại chưa
    os.makedirs('final_dataset', exist_ok=True)
    master_file = f"final_dataset/{platform.lower()}_master.csv"
    
    if os.path.exists(master_file):
        print(f"[+] Tìm thấy file master hiện có: {master_file}")
        df_existing = pd.read_csv(master_file)
        df_existing['timestamp'] = pd.to_datetime(df_existing['timestamp'], errors='coerce')
        print(f"[+] Dữ liệu cũ: {len(df_existing):,} bình luận")
        
        # Merge với data mới
        df = pd.concat([df_existing, df], ignore_index=True)
        print(f"[+] Sau khi gộp: {len(df):,} bình luận")
    
    # Remove duplicates
    before = len(df)
    df.drop_duplicates(subset=['cleaned_text_norm'], inplace=True)
    after_text = len(df)
    df.drop_duplicates(subset=['id'], inplace=True)
    after = len(df)
    print(f"[+] Loại bỏ {before-after:,} trùng → còn {after:,} bình luận UNIQUE")
    
    # Sort by timestamp
    df = df.sort_values('timestamp', ascending=False).reset_index(drop=True)
    
    # Save
    df.to_csv(master_file, index=False, encoding='utf-8-sig')
    backup_file = f"final_dataset/{platform.lower()}_backup_{datetime.now():%Y%m%d_%H%M%S}.csv"
    df.to_csv(backup_file, index=False, encoding='utf-8-sig')
    
    parquet_file = master_file.replace('.csv', '.parquet')
    df.to_parquet(parquet_file, index=False, compression='gzip')
    
    print(f"\nHOÀN TẤT {platform.upper()}!")
    print(f"   → Master: {master_file} ({len(df):,} bình luận)")
    print(f"   → Topic distribution:")
    for t, c in topic_counter.most_common(8):
        print(f"      • {t}: {c:,}")
    
    return df

# ===================== RUN =====================
if __name__ == "__main__":
    print("APIFY → MASTER DATASET ULTIMATE 2025")
    print("="*70)
    print(f"📋 Using advanced_text_cleaning with {len(TEENCODE_DICT)} teencode words")
    print("="*70)
    
    # Xử lý Facebook
    df_fb = convert_apify_to_master('raw/facebook/', 'Facebook')
    
    # Xử lý YouTube
    df_yt = convert_apify_to_master('raw/youtube/', 'YouTube')
    
    # Gộp cả 2 nền tảng
    if df_fb is not None and df_yt is not None:
        master = pd.concat([df_fb, df_yt], ignore_index=True)
        combined_file = "final_dataset/master_combined.csv"
        master.to_csv(combined_file, index=False, encoding='utf-8-sig')
        master.to_parquet(combined_file.replace('.csv','.parquet'), compression='gzip')
        
        print(f"\n{'='*70}")
        print(f"🎉 MASTER DATASET HOÀN CHỈNH: {len(master):,} bình luận")
        print(f"   → File: {combined_file}")
        print(f"   → Facebook: {len(df_fb):,} | YouTube: {len(df_yt):,}")
        print(f"{'='*70}")
    elif df_fb is not None:
        print(f"\n⚠️  Chỉ có Facebook data: {len(df_fb):,} bình luận")
    elif df_yt is not None:
        print(f"\n⚠️  Chỉ có YouTube data: {len(df_yt):,} bình luận")
