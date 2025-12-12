import pandas as pd
import json
import base64
from glob import glob

# Load 1 file JSON Facebook để kiểm tra format
facebook_json = r'c:\Học sâu\Dataset\data\raw\facebook\body_shaming.json'

print("Kiểm tra format JSON Facebook:")
print("="*80)
with open(facebook_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, list):
    items = data[:3]
else:
    items = [data]

for i, item in enumerate(items, 1):
    print(f"\nMẫu {i}:")
    print(f"  Keys: {list(item.keys())}")
    print(f"  id: {item.get('id')}")
    print(f"  postTitle: {item.get('postTitle', 'N/A')[:100] if item.get('postTitle') else 'N/A'}...")

# Load unlabeled data và decode ID
print("\n" + "="*80)
print("Kiểm tra unlabeled IDs:")
print("="*80)

unlabeled_df = pd.read_csv(r'c:\Học sâu\Dataset\data\processed\unlabeled_data.csv', nrows=10)

for i, row in unlabeled_df.iterrows():
    decoded = base64.b64decode(row['id']).decode('utf-8')
    # Bỏ prefix 'comment:'
    if ':' in decoded:
        id_part = decoded.split(':', 1)[1]
    else:
        id_part = decoded
    
    print(f"\n{i+1}.")
    print(f"  Encoded: {row['id']}")
    print(f"  Decoded: {decoded}")
    print(f"  Extracted ID: {id_part}")
    print(f"  Text: {row['text'][:80]}...")

# Tạo mapping từ JSON
print("\n" + "="*80)
print("Tạo mapping từ JSON và kiểm tra match:")
print("="*80)

facebook_jsons = glob(r'c:\Học sâu\Dataset\data\raw\facebook\*.json')
id_to_posttitle = {}

for json_file in facebook_jsons:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        items = data
    else:
        items = [data]
    
    for item in items:
        comment_id = item.get('id')
        post_title = item.get('postTitle')
        
        if comment_id and post_title:
            id_to_posttitle[comment_id] = post_title

print(f"✓ Tổng số Facebook mappings: {len(id_to_posttitle):,}")
print(f"\nMẫu 5 key đầu tiên:")
for i, key in enumerate(list(id_to_posttitle.keys())[:5], 1):
    print(f"{i}. {key}")

# Kiểm tra match
print("\n" + "="*80)
print("Kiểm tra match giữa unlabeled và JSON:")
print("="*80)

for i, row in unlabeled_df.iterrows():
    decoded = base64.b64decode(row['id']).decode('utf-8')
    if ':' in decoded:
        id_part = decoded.split(':', 1)[1]
    else:
        id_part = decoded
    
    matched = id_part in id_to_posttitle
    print(f"\n{i+1}. ID: {id_part}")
    print(f"   Matched: {'✓ YES' if matched else '✗ NO'}")
    if matched:
        print(f"   Title: {id_to_posttitle[id_part][:80]}...")
