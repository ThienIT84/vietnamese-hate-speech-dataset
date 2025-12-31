# apify_to_csv.py
# CẬP NHẬT: Tạo dataset với context (title </s> comment) theo guideline gán nhãn V4.0
# Format output: input_text với cấu trúc "title </s> comment"
# Sử dụng advanced_text_cleaning và emoji mapping
# Project root path
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


import json
import pandas as pd
import hashlib
import os
import re
from datetime import datetime
from tqdm import tqdm
from collections import Counter
from transformers import AutoTokenizer

# Import advanced text cleaning module
from src.preprocessing.advanced_text_cleaning import advanced_clean_text, TEENCODE_DICT

# Load PhoBERT tokenizer để truncate đúng
try:
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
except:
    print("⚠️ Không load được PhoBERT tokenizer, sử dụng word split thay thế")
    tokenizer = None

# ===================== EMOJI MAPPING =====================
EMOJI_MAP = {
    '🏳️‍🌈': ' đồng tính ',
    '🏳️‍⚧️': ' chuyển giới ',
    '🌈': ' lgbt ',
    '👨‍❤️‍💋‍👨': ' nam yêu nam ',
    '👩‍❤️‍💋‍👩': ' nữ yêu nữ ',
    '👬': ' nam yêu nam ',
    '👭': ' nữ yêu nữ ',
    '❤️': ' yêu ',
    '💕': ' thương ',
    '💖': ' tình yêu ',
    '😘': ' hôn ',
    '😍': ' thích ',
    '🥰': ' yêu thương ',
    '💔': ' chia tay ',
}

# ===================== UTILS =====================
def clean_text_with_emoji(text):
    """
    Bước 1: Thay emoji thành text TRƯỚC khi clean
    Bước 2: Xóa hashtags spam
    Bước 3: Apply advanced_clean_text (bao gồm teencode normalization)
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # 1. Thay emoji TRƯỚC
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    
    # 2. Xóa TOÀN BỘ hashtags (spam + thông thường)
    text = re.sub(r'#[a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+', ' ', text)
    
    # 3. Apply advanced cleaning (teencode + tất cả)
    text = advanced_clean_text(text)
    
    return text


def build_input_text(title, comment, max_total_length=256):
    """
    Format: title </s> comment
    Truncate hierarchical: title tối đa 50 tokens, tổng ≤256 tokens
    Theo guideline: ngữ cảnh (title/post) + </s> + comment
    """
    if not title or not title.strip():
        title = ''
    if not comment or not comment.strip():
        comment = ''
    
    title = str(title).strip()
    comment = str(comment).strip()
    
    # Nếu không có title, chỉ trả về comment
    if not title:
        if tokenizer:
            comment_tokens = tokenizer.tokenize(comment)
            if len(comment_tokens) > max_total_length:
                comment_tokens = comment_tokens[:max_total_length]
                comment = tokenizer.convert_tokens_to_string(comment_tokens)
        return comment
    
    # Có title: tokenize và truncate
    if tokenizer:
        title_tokens = tokenizer.tokenize(title)
        comment_tokens = tokenizer.tokenize(comment)
        
        # Truncate title nếu > 50 tokens
        max_title_len = 50
        if len(title_tokens) > max_title_len:
            title_tokens = title_tokens[:max_title_len]
            title = tokenizer.convert_tokens_to_string(title_tokens)
        
        # Separator: </s>
        sep = ' </s> '
        sep_tokens = tokenizer.tokenize(sep)
        
        # Tính comment max length
        available_for_comment = max_total_length - len(title_tokens) - len(sep_tokens)
        
        # Truncate comment nếu cần
        if len(comment_tokens) > available_for_comment and available_for_comment > 0:
            comment_tokens = comment_tokens[:available_for_comment]
            comment = tokenizer.convert_tokens_to_string(comment_tokens)
        
        # Combine
        input_text = f"{title}{sep}{comment}"
    else:
        # Fallback: dùng word count
        title_words = title.split()
        if len(title_words) > 50:
            title = ' '.join(title_words[:50])
        
        input_text = f"{title} </s> {comment}"
        
        # Simple truncate by words
        words = input_text.split()
        if len(words) > max_total_length:
            input_text = ' '.join(words[:max_total_length])
    
    return input_text

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
                # Lấy raw text (comment)
                raw_text = (item.get('text') or item.get('comment') or 
                           item.get('message') or item.get('content') or '')
                if len(raw_text.strip()) < 5: continue
                
                # Skip nested replies
                if item.get('parentId'): continue
                
                # Lấy post title/context
                post_title = (item.get('postTitle') or item.get('title') or 
                             item.get('videoTitle') or '')
                
                # Clean comment và title với emoji mapping
                clean_comment = clean_text_with_emoji(raw_text)
                clean_title = clean_text_with_emoji(post_title)
                
                # Skip nếu cleaned text rỗng
                if len(clean_comment.strip()) < 3: continue
                
                # Build input_text với context: title </s> comment
                input_text = build_input_text(clean_title, clean_comment)
                
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
                    topic = auto_topic(clean_comment, meta_text)
                
                topic_counter[topic] += 1
                
                records.append({
                    # ID & Text - FORMAT MỚI cho training
                    'id': make_id(item.get('id'), raw_text),
                    'input_text': input_text,  # ⭐ CỘT CHÍNH để gán nhãn và train
                    
                    # Raw data (để tham khảo)
                    'raw_comment': raw_text.strip(),
                    'raw_title': post_title.strip() if post_title else '',
                    
                    # Cleaned data (để phân tích)
                    'cleaned_comment': clean_comment,
                    'cleaned_title': clean_title,
                    
                    # Platform & Source
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
                    'char_length': len(clean_comment),
                    'word_count': len(clean_comment.split()),
                    'has_emoji': bool(EMOJI_PATTERN.search(raw_text)),
                    
                    # Topic
                    'topic': topic,
                    
                    # Labeling (để gán nhãn)
                    'label': None,
                    'note': '',  # Ghi chú khi gán nhãn
                })
        except Exception as e:
            print(f"[!] Lỗi {file}: {e}")
    
    if not records:
        print(f"[!] Không có dữ liệu {platform}")
        return None
    
    df = pd.DataFrame(records)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    
    # Kiểm tra file master đã tồn tại chưa
    output_dir = os.path.join(os.path.dirname(input_dir), 'processed')
    os.makedirs(output_dir, exist_ok=True)
    master_file = os.path.join(output_dir, f"{platform.lower()}_master.csv")
    
    if os.path.exists(master_file):
        print(f"[+] Tìm thấy file master hiện có: {master_file}")
        df_existing = pd.read_csv(master_file)
        df_existing['timestamp'] = pd.to_datetime(df_existing['timestamp'], errors='coerce')
        print(f"[+] Dữ liệu cũ: {len(df_existing):,} bình luận")
        
        # Merge với data mới
        df = pd.concat([df_existing, df], ignore_index=True)
        print(f"[+] Sau khi gộp: {len(df):,} bình luận")
    
    # Remove duplicates theo input_text (vì đây là cột chính để train)
    before = len(df)
    df.drop_duplicates(subset=['input_text'], inplace=True)
    after_text = len(df)
    df.drop_duplicates(subset=['id'], inplace=True)
    after = len(df)
    print(f"[+] Loại bỏ {before-after:,} trùng → còn {after:,} bình luận UNIQUE")
    
    # Sort by timestamp
    df = df.sort_values('timestamp', ascending=False).reset_index(drop=True)
    
    # Save
    df.to_csv(master_file, index=False, encoding='utf-8-sig')
    
    # Backup với timestamp
    backup_file = os.path.join(output_dir, f"{platform.lower()}_backup_{datetime.now():%Y%m%d_%H%M%S}.csv")
    df.to_csv(backup_file, index=False, encoding='utf-8-sig')
    
    # Save parquet (nén tốt hơn)
    parquet_file = master_file.replace('.csv', '.parquet')
    df.to_parquet(parquet_file, index=False, compression='gzip')
    
    print(f"\nHOÀN TẤT {platform.upper()}!")
    print(f"   → Master: {master_file} ({len(df):,} bình luận)")
    print(f"   → Format: input_text = 'title </s> comment'")
    print(f"   → Topic distribution:")
    for t, c in topic_counter.most_common(8):
        print(f"      • {t}: {c:,}")
    
    # Hiển thị mẫu
    print(f"\n   → Mẫu input_text đầu tiên:")
    for idx in range(min(3, len(df))):
        print(f"      [{idx+1}] {df.iloc[idx]['input_text'][:100]}...")
    
    return df

# ===================== RUN =====================
if __name__ == "__main__":
    print("="*80)
    print("APIFY → DATASET VỚI CONTEXT (title </s> comment)")
    print("Phiên bản: V4.0 - Theo guideline gán nhãn")
    print("="*80)
    print(f"📋 Using advanced_text_cleaning with {len(TEENCODE_DICT)} teencode words")
    print(f"🔧 Emoji mapping: {len(EMOJI_MAP)} emojis")
    print(f"📝 Output format: input_text = 'title </s> comment'")
    print("="*80)
    
    # Đường dẫn tương đối từ src/preprocessing
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', '..', 'data')
    
    facebook_dir = os.path.join(data_dir, 'raw', 'facebook')
    youtube_dir = os.path.join(data_dir, 'raw', 'youtube')
    
    # Xử lý Facebook
    if os.path.exists(facebook_dir):
        df_fb = convert_apify_to_master(facebook_dir, 'Facebook')
    else:
        print(f"⚠️ Không tìm thấy: {facebook_dir}")
        df_fb = None
    
    # Xử lý YouTube
    if os.path.exists(youtube_dir):
        df_yt = convert_apify_to_master(youtube_dir, 'YouTube')
    else:
        print(f"⚠️ Không tìm thấy: {youtube_dir}")
        df_yt = None
    
    # Gộp cả 2 nền tảng
    if df_fb is not None and df_yt is not None:
        master = pd.concat([df_fb, df_yt], ignore_index=True)
        
        # Remove duplicate toàn bộ dataset
        before = len(master)
        master.drop_duplicates(subset=['input_text'], inplace=True)
        master.drop_duplicates(subset=['id'], inplace=True)
        after = len(master)
        
        combined_file = os.path.join(data_dir, 'processed', 'master_combined.csv')
        master.to_csv(combined_file, index=False, encoding='utf-8-sig')
        master.to_parquet(combined_file.replace('.csv','.parquet'), compression='gzip')
        
        print(f"\n{'='*80}")
        print(f"🎉 MASTER DATASET HOÀN CHỈNH")
        print(f"   → File: {combined_file}")
        print(f"   → Tổng: {len(master):,} bình luận unique")
        print(f"   → Facebook: {len(df_fb):,} | YouTube: {len(df_yt):,}")
        print(f"   → Loại bỏ {before-after:,} trùng lặp cross-platform")
        print(f"   → Format: input_text, label, note")
        print(f"   → Sẵn sàng để gán nhãn theo guideline V4.0")
        print(f"{'='*80}")
        
        # Mẫu cuối
        print(f"\n📌 Mẫu dữ liệu cuối cùng (3 dòng):")
        for idx in range(min(3, len(master))):
            row = master.iloc[idx]
            print(f"\n[{idx+1}] Topic: {row['topic']}")
            print(f"    Input: {row['input_text'][:150]}...")
            
    elif df_fb is not None:
        print(f"\n⚠️  Chỉ có Facebook data: {len(df_fb):,} bình luận")
    elif df_yt is not None:
        print(f"\n⚠️  Chỉ có YouTube data: {len(df_yt):,} bình luận")
    else:
        print(f"\n❌ Không tìm thấy dữ liệu nào!")
