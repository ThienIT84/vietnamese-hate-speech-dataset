import pandas as pd
import re

import os

# Define paths relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

print("="*80)
print("TÌM 150 COMMENT TIỀM NĂNG LABEL 1 (OFFENSIVE)")
print("="*80)

# Load labeled data để phân tích pattern
labeled_path = os.path.join(PROCESSED_DIR, 'training_data_with_context_phobert_clean.csv')
labeled_df = pd.read_csv(labeled_path)
print(f"\n📊 Phân bố hiện tại:")
print(labeled_df['label'].value_counts().sort_index())

label1_df = labeled_df[labeled_df['label'] == 1]
print(f"\n📌 Có {len(label1_df)} mẫu Label 1")

# Phân tích keywords phổ biến trong Label 1
print("\n⏳ Phân tích keywords Label 1...")

# Keywords đặc trưng cho Label 1 (Offensive nhưng không phải Hate Speech)
# Dựa trên phân tích labeled data
OFFENSIVE_KEYWORDS = [
    # Chửi thề nhẹ/vừa (không kèm kỳ thị)
    r'\blồn\b', r'\bcặc\b', r'\bđéo\b', r'\bđm\b', r'\bcc\b', r'\bcl\b',
    r'\bvãi\b.*\blồn\b', r'\bđịt\b.*\bmẹ\b', r'\bcon\b.*\bmẹ\b',
    r'\bngu\b', r'\bkhùng\b', r'\bđần\b', r'\bngáo\b', r'\btrâu\b', r'\bbò\b',
    r'\bchó\b(?!.*chết)', r'\blợn\b(?!.*chết)', # chó/lợn đơn thuần, không kết hợp "chết"
    
    # Chê bai chung chung (không target nhóm yếu thế)
    r'\bngu\b.*\bvãi\b', r'\bnhư\b.*\blồn\b', r'\bnhư\b.*\bcứt\b',
    r'\bxạo\b', r'\bphông\b', r'\bnổ\b', r'\blừa\b.*\bđảo\b',
    r'\bmất\b.*\bdạy\b', r'\bvô\b.*\bhọc\b', r'\bthiếu\b.*\bdạy\b',
    
    # Châm biếm/mỉa mai
    r'\bđéo\b.*\bgì\b', r'\bcái\b.*\blồn\b.*\bgì\b', r'\bcái\b.*\bthể\b.*\blồn\b',
    r'\bđồ\b.*\bngu\b', r'\bthằng\b.*\bngu\b', r'\bcon\b.*\bngu\b',
    
    # Phản ứng cáu gắt
    r'\bcay\b.*\bhả\b', r'\bcay\b.*\bquá\b', r'\bgiận\b.*\bquá\b',
    r'\bchửi\b', r'\bmắng\b', r'\blăng\b.*\bmạ\b',
    
    # Từ tục tĩu nhẹ
    r'\bđjt\b', r'\bdkm\b', r'\bvcl\b', r'\bvcc\b', r'\blol\b',
    r'\bđmm\b', r'\bdmm\b', r'\bclgt\b',
]

# Keywords TRÁNH (thuộc Label 2 - Hate Speech)
HATE_SPEECH_KEYWORDS = [
    r'bắc\s*kỳ', r'nam\s*kỳ', r'miền\s*bắc.*\bchó\b', r'miền\s*nam.*\bchó\b',
    r'đồng\s*tính.*\bchết\b', r'lgbt.*\bchết\b', r'béo.*\bchết\b',
    r'\bchết\b.*\bđi\b', r'\btử\b.*\bhình\b', r'\bgiết\b',
    r'người\s*béo.*\bngu\b', r'người\s*gầy.*\nngu\b',
    r'đàn\s*bà.*\bngu\b', r'con\s*gái.*\bngu\b',
]

# Load unlabeled data
unlabeled_path = os.path.join(PROCESSED_DIR, 'unlabeled_with_context_phobert.csv')
unlabeled_df = pd.read_csv(unlabeled_path)
print(f"\n📦 Unlabeled: {len(unlabeled_df):,} mẫu")

# Score từng comment
scores = []
for idx, row in unlabeled_df.iterrows():
    text = str(row['cleaned_text']).lower()
    
    # Tính điểm offensive
    offensive_score = 0
    for pattern in OFFENSIVE_KEYWORDS:
        if re.search(pattern, text):
            offensive_score += 1
    
    # Loại trừ hate speech
    hate_score = 0
    for pattern in HATE_SPEECH_KEYWORDS:
        if re.search(pattern, text):
            hate_score += 1
    
    # Chỉ lấy nếu có offensive keywords nhưng KHÔNG có hate keywords
    if offensive_score > 0 and hate_score == 0:
        scores.append({
            'index': idx,
            'id': row['id'],
            'text': row['cleaned_text'],
            'input_text': row['input_text'],
            'offensive_score': offensive_score,
            'token_length': row['token_length']
        })

scores_df = pd.DataFrame(scores)
print(f"\n✓ Tìm thấy {len(scores_df):,} candidates")

# Sắp xếp theo offensive_score giảm dần
scores_df = scores_df.sort_values('offensive_score', ascending=False)

# Lấy top 150
top150 = scores_df.head(150).copy()

print(f"\n📌 Top 150 candidates:")
print(f"  Offensive score range: {top150['offensive_score'].min()} - {top150['offensive_score'].max()}")
print(f"  Token length: mean={top150['token_length'].mean():.1f}, max={top150['token_length'].max()}")

# Tạo file output để review
output_df = pd.DataFrame({
    'input_text': top150['input_text'],
    'label': '',  # Để trống cho user điền thủ công
    'note': ''
})

output_path = os.path.join(PROCESSED_DIR, 'label1_candidates_150samples.csv')
output_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ Đã lưu: {output_path}")
print(f"\n📝 Hướng dẫn:")
print(f"  1. Mở file {output_path}")
print(f"  2. Review từng mẫu và điền nhãn (0/1/2) vào cột 'label'")
print(f"  3. Có thể thêm note nếu cần")
print(f"  4. Sau khi xong, gộp vào training data")

# Hiển thị 10 mẫu đầu
print(f"\n" + "="*80)
print("10 MẪU ĐẦU TIÊN (SCORE CAO NHẤT):")
print("="*80)

for i in range(min(10, len(top150))):
    row = top150.iloc[i]
    print(f"\n[{i+1}] Score: {row['offensive_score']}, Tokens: {row['token_length']}")
    print(f"Text: {row['text'][:150]}...")
