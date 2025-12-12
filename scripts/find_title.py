import json
import os

target_id = 'Y29tbWVudDoxODUwMjM4ODYyNDI3MDUyXzU2OTkyNTg2NjEzOTcwNg=='

files = [
    r'c:\Học sâu\Dataset\data\raw\facebook\drama influencer - chửi bới cự chiến binh  30-4 .json',
    r'c:\Học sâu\Dataset\data\raw\facebook\Drama Influencer.json',
    r'c:\Học sâu\Dataset\data\raw\facebook\social_issues.json',
    r'c:\Học sâu\Dataset\data\raw\facebook\Social Issues- tệ nạn giao thông.json',
]

# Thêm file youtube
youtube_files = [
    r'c:\Học sâu\Dataset\data\raw\youtube\social_issues_tai_nan_giao_thong.json',
]

all_files = files + youtube_files

for filepath in all_files:
    if not os.path.exists(filepath):
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = data if isinstance(data, list) else [data]
        
        for item in items:
            item_id = item.get('id')
            if item_id == target_id:
                print(f"✅ Found in: {os.path.basename(filepath)}")
                print(f"📰 Title (original): {item.get('postTitle', 'N/A')}")
                print(f"💬 Comment: {item.get('text', '')[:100]}")
                break
    except Exception as e:
        print(f"⚠️ Error reading {filepath}: {e}")
