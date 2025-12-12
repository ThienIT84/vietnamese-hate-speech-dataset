import pandas as pd
import json
import os
import re
import sys
import hashlib
import base64
from glob import glob
from transformers import AutoTokenizer

# Import advanced cleaning từ src
sys.path.append(r'c:\Học sâu\Dataset\src\preprocessing')
from advanced_text_cleaning import advanced_clean_text

# Load PhoBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# Emoji mapping (giống prepare_training_with_teencode.py)
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
    text = re.sub(r'#[a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+', ' ', text)
    
    # 3. Apply advanced cleaning (teencode + tất cả)
    text = advanced_clean_text(text)
    
    return text

def build_input_text(title, comment, max_total_length=256):
    """
    Format: title </s> comment
    Truncate hierarchical: title tối đa 50 tokens, tổng ≤256 tokens
    """
    if pd.isna(title) or not title:
        title = ''
    if pd.isna(comment) or not comment:
        comment = ''
    
    title = str(title).strip()
    comment = str(comment).strip()
    
    # Tokenize
    title_tokens = tokenizer.tokenize(title)
    comment_tokens = tokenizer.tokenize(comment)
    
    # Truncate title nếu > 50 tokens
    max_title_len = 50
    if len(title_tokens) > max_title_len:
        title_tokens = title_tokens[:max_title_len]
        title = tokenizer.convert_tokens_to_string(title_tokens)
    
    # Separator: </s>
    sep = ' </s> '
    
    # Tính comment max length
    sep_tokens = tokenizer.tokenize(sep)
    available_for_comment = max_total_length - len(title_tokens) - len(sep_tokens)
    
    # Truncate comment nếu cần
    if len(comment_tokens) > available_for_comment:
        comment_tokens = comment_tokens[:available_for_comment]
        comment = tokenizer.convert_tokens_to_string(comment_tokens)
    
    # Combine
    input_text = f"{title}{sep}{comment}"
    
    return input_text

print("="*80)
print("BƯỚC 1: LOAD POST_TITLE TỪ JSON GỐC")
print("="*80)

# Tìm tất cả file JSON
facebook_jsons = glob(r'c:\Học sâu\Dataset\data\raw\facebook\*.json')
youtube_jsons = glob(r'c:\Học sâu\Dataset\data\raw\youtube\*.json')

all_jsons = facebook_jsons + youtube_jsons
print(f"Tìm thấy {len(all_jsons)} file JSON")

# Tạo mapping id → postTitle
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
                comment = item.get('comment', '')
                title = item.get('title')
                
                if comment and title:
                    # Tạo hashed ID giống như apify_to_csv.py
                    hashed_id = hashlib.md5(comment.encode('utf-8')).hexdigest()[:12]
                    hashed_to_title[hashed_id] = title
            else:
                # Facebook: ID đã được encode base64 trong JSON
                # Cần decode để match với unlabeled data
                comment_id_encoded = item.get('id')  # Base64 encoded
                post_title = item.get('postTitle')
                
                if comment_id_encoded and post_title:
                    # Decode base64 để lấy dạng "comment:postId_commentId"
                    try:
                        decoded_id = base64.b64decode(comment_id_encoded).decode('utf-8')
                        # Bỏ prefix "comment:" để lấy postId_commentId
                        if ':' in decoded_id:
                            plain_id = decoded_id.split(':', 1)[1]
                        else:
                            plain_id = decoded_id
                        
                        # Lưu mapping với plain ID
                        id_to_posttitle[plain_id] = post_title
                    except:
                        pass
                    
    except Exception as e:
        print(f"⚠ Lỗi đọc {json_file}: {e}")

print(f"✓ Facebook mappings: {len(id_to_posttitle):,}")
print(f"✓ YouTube mappings: {len(hashed_to_title):,}")
print(f"✓ Tổng mappings: {len(id_to_posttitle) + len(hashed_to_title):,}")

print("\n" + "="*80)
print("BƯỚC 2: LOAD UNLABELED DATA")
print("="*80)

unlabeled_df = pd.read_csv(r'c:\Học sâu\Dataset\data\processed\unlabeled_data.csv')
print(f"Unlabeled data: {len(unlabeled_df):,} mẫu")

print("\n" + "="*80)
print("BƯỚC 3: LOAD LABELED DATA ĐỂ LỌC TRÙNG")
print("="*80)

labeled_df = pd.read_csv(r'c:\Học sâu\Dataset\TOXIC_COMMENT\training_data_with_context_phobert_clean.csv')
print(f"Labeled data (đang train): {len(labeled_df):,} mẫu")

# Lấy danh sách comment text từ labeled data để lọc
# Cần extract comment từ input_text (phần sau </s>)
labeled_comments = set()
for idx, row in labeled_df.iterrows():
    input_text = row['input_text']
    if pd.notna(input_text) and '</s>' in str(input_text):
        # Tách lấy comment (phần sau </s>)
        comment_part = str(input_text).split('</s>')[-1].strip()
        labeled_comments.add(comment_part)

print(f"✓ Tìm thấy {len(labeled_comments):,} comment unique trong labeled data")

print("\n" + "="*80)
print("BƯỚC 4: LỌC UNLABELED DATA (KHÔNG TRÙNG VỚI LABELED)")
print("="*80)

# Decode base64 ID để lấy original ID
import base64

def decode_base64_id(encoded_id):
    """Decode base64 ID thành dạng comment:postId_commentId"""
    try:
        decoded = base64.b64decode(encoded_id).decode('utf-8')
        return decoded
    except:
        return None

unlabeled_df['decoded_id'] = unlabeled_df['id'].apply(decode_base64_id)

# Extract original ID từ decoded
def extract_original_id(decoded_str):
    """Extract commentId từ 'comment:postId_commentId'
    
    Format: comment:1272561691569054_856950340247180
    → Trả về: 856950340247180 (comment ID)
    
    Nhưng JSON Facebook lưu full postId_commentId như: 1272561691569054_856950340247180
    """
    if not decoded_str:
        return None
    
    # Bỏ prefix 'comment:'
    if ':' in decoded_str:
        id_part = decoded_str.split(':', 1)[1]  # Lấy phần sau 'comment:'
    else:
        id_part = decoded_str
    
    # id_part bây giờ có dạng: postId_commentId
    # JSON Facebook lưu full postId_commentId nên trả về luôn
    return id_part

unlabeled_df['original_id'] = unlabeled_df['decoded_id'].apply(extract_original_id)

print(f"✓ Decoded {unlabeled_df['original_id'].notna().sum():,} IDs")

# Áp dụng advanced cleaning cho unlabeled text
print("\n⏳ Cleaning unlabeled text...")
unlabeled_df['cleaned_text'] = unlabeled_df['text'].apply(clean_text_with_emoji)

# Lọc ra các comment KHÔNG có trong labeled data
unlabeled_df['is_duplicate'] = unlabeled_df['cleaned_text'].isin(labeled_comments)
filtered_unlabeled_df = unlabeled_df[~unlabeled_df['is_duplicate']].copy()

print(f"✓ Loại bỏ {unlabeled_df['is_duplicate'].sum():,} mẫu trùng")
print(f"✓ Còn lại {len(filtered_unlabeled_df):,} mẫu unique")

print("\n" + "="*80)
print("BƯỚC 5: TẠO MAPPING YOUTUBE TỪNG TEXT GỐC")
print("="*80)

# Tạo mapping text → title cho YouTube từ JSON
# Vì unlabeled_data.csv đã clean nên không match được với hash
# Cần tạo mapping bằng cách so sánh text sau khi clean
youtube_text_to_title = {}

print("⏳ Đang tạo YouTube text mapping...")
for json_file in youtube_jsons:
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            items = data
        else:
            items = [data]
        
        for item in items:
            comment_raw = item.get('comment', '')
            title = item.get('title')
            
            if comment_raw and title:
                # Clean comment giống như unlabeled_data
                comment_cleaned = clean_text_with_emoji(comment_raw)
                # Lưu mapping cleaned text → title
                youtube_text_to_title[comment_cleaned] = title
    except Exception as e:
        print(f"⚠ Lỗi đọc {json_file}: {e}")

print(f"✓ YouTube text mappings: {len(youtube_text_to_title):,}")

print("\n" + "="*80)
print("BƯỚC 6: THÊM POST_TITLE CHO UNLABELED DATA")
print("="*80)

# Thêm post_title
def get_post_title(row):
    """Lấy post_title từ mappings"""
    original_id = row['original_id']
    
    # Thử Facebook mapping trước (dùng ID)
    if pd.notna(original_id) and original_id in id_to_posttitle:
        return id_to_posttitle[original_id]
    
    # Thử YouTube mapping (dùng cleaned text)
    cleaned_text = row['cleaned_text']
    if pd.notna(cleaned_text) and cleaned_text in youtube_text_to_title:
        return youtube_text_to_title[cleaned_text]
    
    return None

print("⏳ Mapping post_title...")
filtered_unlabeled_df['post_title'] = filtered_unlabeled_df.apply(get_post_title, axis=1)

# Clean post_title
print("⏳ Cleaning post_title...")
filtered_unlabeled_df['cleaned_title'] = filtered_unlabeled_df['post_title'].apply(clean_text_with_emoji)

# Thống kê
title_found = filtered_unlabeled_df['post_title'].notna().sum()
print(f"✓ Tìm thấy title cho {title_found:,}/{len(filtered_unlabeled_df):,} mẫu ({100*title_found/len(filtered_unlabeled_df):.1f}%)")

print("\n" + "="*80)
print("BƯỚC 7: BUILD INPUT_TEXT (TITLE </s> COMMENT)")
print("="*80)

print("⏳ Building input_text...")
filtered_unlabeled_df['input_text'] = filtered_unlabeled_df.apply(
    lambda row: build_input_text(row['cleaned_title'], row['cleaned_text']),
    axis=1
)

# Thống kê token length
print("\n⏳ Analyzing token lengths...")
token_lengths = []
for text in filtered_unlabeled_df['input_text']:
    if pd.notna(text):
        tokens = tokenizer.tokenize(str(text))
        token_lengths.append(len(tokens))
    else:
        token_lengths.append(0)

filtered_unlabeled_df['token_length'] = token_lengths

print(f"\nToken length statistics:")
print(f"  Mean: {filtered_unlabeled_df['token_length'].mean():.1f}")
print(f"  Median: {filtered_unlabeled_df['token_length'].median():.1f}")
print(f"  Max: {filtered_unlabeled_df['token_length'].max()}")
print(f"  Min: {filtered_unlabeled_df['token_length'].min()}")

print("\n" + "="*80)
print("BƯỚC 8: LƯU FILE OUTPUT")
print("="*80)

# Chọn các cột cần thiết
output_df = filtered_unlabeled_df[['id', 'input_text', 'text', 'cleaned_text', 'post_title', 'cleaned_title', 'token_length']].copy()

# Sắp xếp theo token_length giảm dần
output_df = output_df.sort_values('token_length', ascending=False)

output_path = r'c:\Học sâu\Dataset\TOXIC_COMMENT\unlabeled_with_context_phobert.csv'
output_df.to_csv(output_path, index=False, encoding='utf-8')

print(f"✓ Đã lưu {len(output_df):,} mẫu vào: {output_path}")

# Thống kê chi tiết
print("\n" + "="*80)
print("THỐNG KÊ CUỐI CÙNG")
print("="*80)
print(f"Unlabeled data gốc: {len(unlabeled_df):,}")
print(f"Loại bỏ trùng với labeled: -{unlabeled_df['is_duplicate'].sum():,}")
print(f"Còn lại unique: {len(filtered_unlabeled_df):,}")
print(f"Có post_title: {title_found:,} ({100*title_found/len(filtered_unlabeled_df):.1f}%)")
print(f"Không có post_title: {len(filtered_unlabeled_df) - title_found:,} ({100*(len(filtered_unlabeled_df) - title_found)/len(filtered_unlabeled_df):.1f}%)")
print(f"\nFile output: unlabeled_with_context_phobert.csv")
print(f"  - Tổng: {len(output_df):,} mẫu")
print(f"  - Format: title </s> comment")
print(f"  - Token length: mean={output_df['token_length'].mean():.1f}, max={output_df['token_length'].max()}")

# Hiển thị 5 mẫu đầu
print("\n" + "="*80)
print("MẪU INPUT_TEXT ĐẦU TIÊN (5 DÒNG)")
print("="*80)
for idx in range(min(5, len(output_df))):
    row = output_df.iloc[idx]
    print(f"\n[{idx+1}] Token length: {row['token_length']}")
    print(f"Input: {row['input_text'][:200]}...")

print("\n✅ HOÀN TẤT!")
