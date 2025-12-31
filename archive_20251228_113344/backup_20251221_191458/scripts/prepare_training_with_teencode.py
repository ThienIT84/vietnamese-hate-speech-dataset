import pandas as pd
import json
import os
import re
import sys
import hashlib
from glob import glob
from transformers import AutoTokenizer

# Import advanced cleaning từ src
sys.path.append(r'c:\Học sâu\Dataset\src\preprocessing')
from advanced_text_cleaning import advanced_clean_text

# Load PhoBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# Emoji mapping
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

def clean_text_with_emoji(text):
    """
    Bước 1: Thay emoji thành text TRƯỚC khi clean
    Bước 2: Xóa hashtags (cả spam và thông thường)
    Bước 3: Apply advanced_clean_text (bao gồm teencode normalization)
    """
    if not text or pd.isna(text):
        return ''
    
    text = str(text)
    
    # 1. Thay emoji TRƯỚC
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    
    # 2. Xóa TOÀN BỘ hashtags (spam + thông thường)
    # Pattern: # + chữ/số liên tiếp
    text = re.sub(r'#[a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+', ' ', text)
    
    # 3. Apply advanced cleaning (teencode + tất cả)
    text = advanced_clean_text(text)
    
    return text

print("="*80)
print("BƯỚC 1: LOAD POST_TITLE TỪ JSON GỐC")
print("="*80)

# Tìm tất cả file JSON
facebook_jsons = glob(r'c:\Học sâu\Dataset\data\raw\facebook\*.json')
youtube_jsons = glob(r'c:\Học sâu\Dataset\data\raw\youtube\*.json')

all_jsons = facebook_jsons + youtube_jsons
print(f"Tìm thấy {len(all_jsons)} file JSON")

# Tạo mapping id → postTitle
# Facebook: id trực tiếp
# YouTube: cid → hash(text) → cần tạo cả 2 mappings
id_to_posttitle = {}
hashed_to_title = {}  # Cho YouTube

for json_file in all_jsons:
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # JSON có thể là list hoặc dict
        if isinstance(data, list):
            items = data
        else:
            items = [data]
        
        is_youtube = 'youtube' in json_file.lower()
        
        for item in items:
            if is_youtube:
                # YouTube: cid → hash MD5(comment text)
                cid = item.get('cid')
                comment = item.get('comment', '')
                title = item.get('title')
                
                if comment and title:
                    # Tạo hashed ID giống như apify_to_csv.py
                    hashed_id = hashlib.md5(comment.encode('utf-8')).hexdigest()[:12]
                    hashed_to_title[hashed_id] = title
                    if cid:
                        id_to_posttitle[cid] = title
            else:
                # Facebook: id và postTitle
                comment_id = item.get('id')
                post_title = item.get('postTitle')
                
                if comment_id and post_title:
                    id_to_posttitle[comment_id] = post_title
        
        print(f"  ✅ {os.path.basename(json_file)}: +{len(items)} comments")
    
    except Exception as e:
        print(f"  ⚠️ Error loading {json_file}: {e}")

# Merge cả 2 dictionaries
id_to_posttitle.update(hashed_to_title)

print(f"\n✅ Tổng: {len(id_to_posttitle)} comments có post_title")

print("\n"+"="*80)
print("BƯỚC 2: GỘP DỮ LIỆU LABELED")
print("="*80)

# File 1: majority_vote_labels.csv
df_majority = pd.read_csv(r'c:\Học sâu\Dataset\data\labeled\majority_vote_labels.csv')
df1 = df_majority[['id', 'text_to_label', 'label_majority']].copy()
df1.columns = ['id', 'text', 'label']
print(f"✅ File 1: {len(df1)} samples")

# File 2: auto_labeled_500_samples_master_fixed.csv
df2 = pd.read_csv(r'c:\Học sâu\Dataset\TOXIC_COMMENT\auto_labeled_500_samples_master_fixed.csv')
df2 = df2[['id', 'text', 'label']].copy()
print(f"✅ File 2: {len(df2)} samples")

# Gộp
df_combined = pd.concat([df1, df2], ignore_index=True)
df_combined = df_combined.drop_duplicates(subset=['id'])

print(f"✅ Tổng: {len(df_combined)} samples")
print("\n📊 Phân bố nhãn:")
print(df_combined['label'].value_counts().sort_index())

print("\n"+"="*80)
print("BƯỚC 3: XỬ LÝ TEENCODE + EMOJI CHO POST_TITLE & COMMENT")
print("="*80)

def build_input_text(row, max_length=256):
    """
    Format: [post_title_clean (max 50 tokens)] </s> [comment_clean]
    Total: <= 256 tokens
    
    ✅ Xử lý teencode cho CẢ 2: post_title và comment
    ✅ Sử dụng </s> thay vì [SEP] (PhoBERT separator token)
    """
    row_id = row['id']
    text = row['text']
    
    # Lấy post_title theo ID
    post_title = id_to_posttitle.get(row_id, '')
    
    # ✅ CLEAN CẢ 2 (emoji + teencode + advanced cleaning)
    post_title_clean = clean_text_with_emoji(post_title)
    text_clean = clean_text_with_emoji(text)
    
    if not post_title_clean or post_title_clean.strip() == '':
        return text_clean
    
    # Truncate title về 50 tokens
    title_tokens = tokenizer.encode(post_title_clean, add_special_tokens=False)[:50]
    title_truncated = tokenizer.decode(title_tokens, skip_special_tokens=True)
    
    # Build full text với </s> (PhoBERT separator)
    full_text = f"{title_truncated} </s> {text_clean}"
    
    # Kiểm tra tổng tokens
    total_tokens = tokenizer.encode(full_text, add_special_tokens=True)
    
    if len(total_tokens) <= max_length:
        return full_text
    
    # Quá dài → Cắt comment, giữ title
    available = max_length - len(title_tokens) - 10
    comment_tokens = tokenizer.encode(text_clean, add_special_tokens=False)[:available]
    comment_truncated = tokenizer.decode(comment_tokens, skip_special_tokens=True)
    
    return f"{title_truncated} </s> {comment_truncated}"

# Apply
print("🔧 Đang xử lý teencode cho post_title & comment...")
df_combined['input_text'] = df_combined.apply(build_input_text, axis=1)

# Thống kê
has_title = df_combined['input_text'].str.contains('</s>', na=False).sum()
print(f"✅ Hoàn thành:")
print(f"   - Có post_title: {has_title}/{len(df_combined)} ({has_title/len(df_combined)*100:.1f}%)")
print(f"   - Chỉ comment: {len(df_combined) - has_title}")

# Kiểm tra token length
token_lengths = []
for text in df_combined['input_text'].head(100):
    tokens = tokenizer.encode(text, add_special_tokens=True)
    token_lengths.append(len(tokens))

print(f"\n📏 Token length stats (100 samples):")
print(f"   - Mean: {sum(token_lengths)/len(token_lengths):.1f}")
print(f"   - Max: {max(token_lengths)}")
print(f"   - Min: {min(token_lengths)}")

print("\n"+"="*80)
print("BƯỚC 4: LƯU FILE")
print("="*80)

df_final = df_combined[['input_text', 'label']].copy()
df_final = df_final.drop_duplicates(subset=['input_text'])

output_path = r'c:\Học sâu\Dataset\TOXIC_COMMENT\training_data_with_context_phobert_clean.csv'
df_final.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"✅ Saved: {output_path}")
print(f"\n📊 Final stats:")
print(f"   Total: {len(df_final)} samples")
for label in sorted(df_final['label'].unique()):
    count = (df_final['label'] == label).sum()
    print(f"   Label {label}: {count} ({count/len(df_final)*100:.1f}%)")

# Examples
print("\n"+"="*80)
print("VÍ DỤ (SAU KHI CLEAN TEENCODE):")
print("="*80)

for label in [0, 1, 2]:
    samples = df_final[df_final['label'] == label].head(2)
    if len(samples) > 0:
        print(f"\n🏷️ Label {label}:")
        for _, row in samples.iterrows():
            text = row['input_text']
            if '</s>' in text:
                parts = text.split('</s>')
                print(f"   📰 Title: {parts[0][:70]}...")
                print(f"   💬 Comment: {parts[1].strip()[:70]}...")
            else:
                print(f"   💬 {text[:80]}...")

print("\n✅ DONE!")
