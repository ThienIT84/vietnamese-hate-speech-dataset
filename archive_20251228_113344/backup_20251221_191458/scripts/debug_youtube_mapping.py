import pandas as pd
import json
import hashlib
from glob import glob

print("="*80)
print("KIỂM TRA YOUTUBE MAPPING")
print("="*80)

# Load unlabeled data
unlabeled_df = pd.read_csv(r'c:\Học sâu\Dataset\data\processed\unlabeled_data.csv')
print(f"Tổng unlabeled: {len(unlabeled_df):,}")

# Load output file
output_df = pd.read_csv(r'c:\Học sâu\Dataset\TOXIC_COMMENT\unlabeled_with_context_phobert.csv')
no_title_df = output_df[output_df['post_title'].isna()]
print(f"Không có title: {len(no_title_df):,}")

# Load 1 file YouTube JSON để check format
youtube_json = r'c:\Học sâu\Dataset\data\raw\youtube\body-shaming_MVca_nhac.json'

print("\n" + "="*80)
print("CHECK FORMAT YOUTUBE JSON:")
print("="*80)

with open(youtube_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, list):
    items = data[:3]
else:
    items = [data]

for i, item in enumerate(items, 1):
    print(f"\nMẫu {i}:")
    print(f"  Keys: {list(item.keys())[:10]}")
    if 'cid' in item:
        print(f"  cid: {item['cid']}")
    if 'comment' in item:
        comment = item['comment']
        print(f"  comment: {comment[:80]}...")
        # Tạo hash
        hashed = hashlib.md5(comment.encode('utf-8')).hexdigest()[:12]
        print(f"  hash(comment): {hashed}")
    if 'title' in item:
        print(f"  title: {item['title'][:80]}...")

# Kiểm tra mapping YouTube
print("\n" + "="*80)
print("TẠO YOUTUBE MAPPING VÀ KIỂM TRA:")
print("="*80)

youtube_jsons = glob(r'c:\Học sâu\Dataset\data\raw\youtube\*.json')
print(f"Tìm thấy {len(youtube_jsons)} file YouTube JSON")

hashed_to_title = {}
for json_file in youtube_jsons:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        items = data
    else:
        items = [data]
    
    for item in items:
        comment = item.get('comment', '')
        title = item.get('title')
        
        if comment and title:
            hashed_id = hashlib.md5(comment.encode('utf-8')).hexdigest()[:12]
            hashed_to_title[hashed_id] = title

print(f"✓ YouTube mappings: {len(hashed_to_title):,}")

# Kiểm tra mẫu không có title
print("\n" + "="*80)
print("KIỂM TRA 10 MẪU KHÔNG CÓ TITLE:")
print("="*80)

for i in range(min(10, len(no_title_df))):
    row = no_title_df.iloc[i]
    text = row['text']
    
    # Thử hash text gốc (chưa clean)
    if pd.notna(text):
        hashed = hashlib.md5(str(text).encode('utf-8')).hexdigest()[:12]
        matched = hashed in hashed_to_title
        
        print(f"\n{i+1}. ID: {row['id']}")
        print(f"   Text: {str(text)[:80]}...")
        print(f"   Hash: {hashed}")
        print(f"   Matched: {'✓ YES' if matched else '✗ NO'}")
        if matched:
            print(f"   Title: {hashed_to_title[hashed][:80]}...")

# Thống kê tổng quan
print("\n" + "="*80)
print("KIỂM TRA NGƯỢC LẠI - MẪU CÓ TITLE:")
print("="*80)

with_title_df = output_df[output_df['post_title'].notna()]
print(f"Có title: {len(with_title_df):,}")

# Đếm bao nhiêu mẫu có title từ YouTube
youtube_title_count = 0
for i in range(min(100, len(with_title_df))):
    row = with_title_df.iloc[i]
    text = row['text']
    
    if pd.notna(text):
        hashed = hashlib.md5(str(text).encode('utf-8')).hexdigest()[:12]
        if hashed in hashed_to_title:
            youtube_title_count += 1

print(f"✓ Trong 100 mẫu đầu có title, {youtube_title_count} mẫu từ YouTube")
