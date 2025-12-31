"""
🎯 PHÂN TÍCH VÀ TĂNG CƯỜNG DỮ LIỆU
Dựa trên 68 câu model đoán nhầm Label 0 → 1

Chiến lược:
1. Cắt bỏ post title dài (noise)
2. Lọc từ unlabeled data những pattern tương tự
3. Gán nhãn tự động dựa trên pattern
4. Tăng cường dữ liệu cho các edge cases

Author: Thanh Thien
Date: 29/12/2025
"""

import pandas as pd
import re
from datetime import datetime

print("="*80)
print("🎯 PHÂN TÍCH 68 CÂU MODEL ĐOÁN NHẦM")
print("="*80)

# ============================================================
# 1. PHÂN TÍCH PATTERNS TỪ 68 CÂU NHẦM
# ============================================================

print("\n📊 Phân tích patterns...")

# Patterns từ 68 câu nhầm
error_patterns = {
    'MV_DESCRIPTION_NOISE': {
        'count': 0,
        'pattern': r'^(official\s+poster|visualizer\s+mv|body\s+shaming).{100,}?</s>',
        'description': 'Mô tả MV dài làm nhiễu (>100 chars trước </s>)',
        'examples': [
            'official poster | visualizer mv body shaming... </s> mv này hay',
            'body shaming (miệt thị ngoại hình)... </s> peak vcl'
        ]
    },
    'JUSTICE_CALL': {
        'count': 0,
        'pattern': r'\b(pháp\s*luật|luật|đi\s+bóc|vào\s+tù|trại)\b',
        'description': 'Kêu gọi công lý, ủng hộ pháp luật',
        'examples': [
            'pháp luật thì muộn rồi',
            'luật dạy giỗ thằng này',
            'đi bóc 10 cuốn'
        ]
    },
    'TECHNICAL_HEAVY': {
        'count': 0,
        'pattern': r'\b(nặng\s+(khung|mv|video)|lag|render|cấu\s*hình)\b',
        'description': '"Nặng" về kỹ thuật (video/render)',
        'examples': [
            'nặng khung hình thế',
            'mv nhìn nặng',
            'video lag quá do nặng'
        ]
    },
    'NEUTRAL_COMMENT': {
        'count': 0,
        'pattern': r'\b(trách|tội|thấy|xem|nghĩ|hóng|combo)\b',
        'description': 'Comment trung tính, không toxic',
        'examples': [
            'trách con vợ quá tệ',
            'tội ghê tuổi còn trẻ',
            'hóng mv của trà bông'
        ]
    },
    'SARCASM_POSITIVE': {
        'count': 0,
        'pattern': r'\b(móe\s+nhục|dẹp\s+mịa|rảnh\s+việc)\b',
        'description': 'Châm biếm nhẹ, không toxic thực sự',
        'examples': [
            'móe nhục mặt 89 quá',
            'dẹp mịa đi',
            'rảnh việc ngá mồm'
        ]
    }
}

# Đếm patterns trong 68 câu mẫu
sample_errors = [
    "official poster | visualizer mv body shaming... </s> mv này hay",
    "pháp luật thì muộn rồi",
    "nặng khung hình thế",
    "trách con vợ quá tệ",
    "móe nhục mặt 89 quá"
]

print("\n📋 Patterns phát hiện:")
for name, info in error_patterns.items():
    print(f"\n{name}:")
    print(f"  Mô tả: {info['description']}")
    print(f"  Ví dụ:")
    for ex in info['examples'][:2]:
        print(f"    - {ex}")

# ============================================================
# 2. LOAD UNLABELED DATA
# ============================================================

print("\n" + "="*80)
print("📂 LOAD UNLABELED DATA")
print("="*80)

unlabeled_path = r"unlabeled_processed_20251229_012930.csv"
df_unlabeled = pd.read_csv(unlabeled_path, encoding='utf-8')

print(f"✅ Loaded: {len(df_unlabeled)} unlabeled rows")

# ============================================================
# 3. LỌC VÀ GÁN NHÃN TỰ ĐỘNG
# ============================================================

print("\n" + "="*80)
print("🔍 LỌC VÀ GÁN NHÃN TỰ ĐỘNG")
print("="*80)

auto_labeled = []

for idx, row in df_unlabeled.iterrows():
    if idx % 5000 == 0:
        print(f"  Progress: {idx}/{len(df_unlabeled)}")
    
    text = str(row['training_text']).lower()
    original_text = str(row['training_text'])
    
    # Skip if too short
    if len(text) < 10:
        continue
    
    # ===== PATTERN 1: MV DESCRIPTION NOISE =====
    if re.search(error_patterns['MV_DESCRIPTION_NOISE']['pattern'], text, re.IGNORECASE):
        # Cắt bỏ mô tả, chỉ lấy comment
        parts = original_text.split('</s>')
        if len(parts) >= 2:
            comment = parts[-1].strip()
            
            # Nếu comment ngắn và không có toxic words
            if len(comment) < 150 and not re.search(r'\b(đm|dm|dcm|cc|lồn|cặc|đéo|địt)\b', comment.lower()):
                auto_labeled.append({
                    'training_text': comment,
                    'label': 0,
                    'confidence': 'high',
                    'pattern': 'MV_DESCRIPTION_REMOVED',
                    'note': 'Auto-labeled: Removed MV description noise',
                    'source': 'unlabeled_augmentation'
                })
                error_patterns['MV_DESCRIPTION_NOISE']['count'] += 1
                continue
    
    # ===== PATTERN 2: JUSTICE CALL =====
    if re.search(error_patterns['JUSTICE_CALL']['pattern'], text):
        # Kiểm tra KHÔNG phải chửi trực tiếp
        if not re.search(r'\b(mày|mi)\s+(đi|vào)\s+tù\b', text):
            auto_labeled.append({
                'training_text': original_text,
                'label': 0,
                'confidence': 'medium',
                'pattern': 'JUSTICE_CALL',
                'note': 'Auto-labeled: Justice call (support law)',
                'source': 'unlabeled_augmentation'
            })
            error_patterns['JUSTICE_CALL']['count'] += 1
            continue
    
    # ===== PATTERN 3: TECHNICAL HEAVY =====
    if re.search(error_patterns['TECHNICAL_HEAVY']['pattern'], text):
        # Kiểm tra KHÔNG có toxic words khác
        if not re.search(r'\b(đm|dm|dcm|cc|lồn|cặc|đéo|địt)\b', text):
            auto_labeled.append({
                'training_text': original_text,
                'label': 0,
                'confidence': 'high',
                'pattern': 'TECHNICAL_HEAVY',
                'note': 'Auto-labeled: Technical "nặng" (video/render)',
                'source': 'unlabeled_augmentation'
            })
            error_patterns['TECHNICAL_HEAVY']['count'] += 1
            continue
    
    # ===== PATTERN 4: NEUTRAL COMMENT =====
    # Các từ trung tính + không có toxic words
    neutral_keywords = ['trách', 'tội', 'thấy', 'xem', 'nghĩ', 'hóng', 'combo', 'thực tế']
    has_neutral = any(kw in text for kw in neutral_keywords)
    has_toxic = bool(re.search(r'\b(đm|dm|dcm|cc|lồn|cặc|đéo|địt|vl|vcl)\b', text))
    
    if has_neutral and not has_toxic and len(text) < 200:
        auto_labeled.append({
            'training_text': original_text,
            'label': 0,
            'confidence': 'medium',
            'pattern': 'NEUTRAL_COMMENT',
            'note': 'Auto-labeled: Neutral comment',
            'source': 'unlabeled_augmentation'
        })
        error_patterns['NEUTRAL_COMMENT']['count'] += 1
        continue
    
    # ===== PATTERN 5: SARCASM POSITIVE =====
    sarcasm_patterns = [
        r'\bmóe\s+nhục\b',
        r'\bdẹp\s+mịa\b',
        r'\brảnh\s+việc\b',
        r'\bchán\s+luôn\b'
    ]
    
    for pattern in sarcasm_patterns:
        if re.search(pattern, text):
            # Kiểm tra context không toxic
            if not re.search(r'\b(chó|lợn|súc\s*vật|đồ\s+ngu)\b', text):
                auto_labeled.append({
                    'training_text': original_text,
                    'label': 0,
                    'confidence': 'low',
                    'pattern': 'SARCASM_POSITIVE',
                    'note': 'Auto-labeled: Sarcasm/light criticism',
                    'source': 'unlabeled_augmentation'
                })
                error_patterns['SARCASM_POSITIVE']['count'] += 1
                break

print(f"\n✅ Auto-labeled: {len(auto_labeled)} samples")

# ============================================================
# 4. THỐNG KÊ PATTERNS
# ============================================================

print("\n" + "="*80)
print("📊 THỐNG KÊ PATTERNS")
print("="*80)

for name, info in error_patterns.items():
    if info['count'] > 0:
        print(f"\n{name}: {info['count']} samples")
        print(f"  {info['description']}")

# ============================================================
# 5. LƯU KẾT QUẢ
# ============================================================

print("\n" + "="*80)
print("💾 LƯU KẾT QUẢ")
print("="*80)

# Tạo DataFrame
df_augmented = pd.DataFrame(auto_labeled)

# Lưu file để review
review_file = f"AUTO_LABELED_FOR_REVIEW_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df_augmented.to_csv(review_file, index=False, encoding='utf-8')
print(f"✅ Saved for review: {review_file}")

# Lưu theo confidence level
for conf in ['high', 'medium', 'low']:
    df_conf = df_augmented[df_augmented['confidence'] == conf]
    if len(df_conf) > 0:
        conf_file = f"AUTO_LABELED_{conf.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_conf.to_csv(conf_file, index=False, encoding='utf-8')
        print(f"✅ {conf.upper()} confidence: {conf_file} ({len(df_conf)} samples)")

# ============================================================
# 6. TẠO FILE HƯỚNG DẪN REVIEW
# ============================================================

print("\n" + "="*80)
print("📝 TẠO HƯỚNG DẪN REVIEW")
print("="*80)

guide_content = f"""
# 🎯 HƯỚNG DẪN REVIEW VÀ GÁN NHÃN

## Tổng quan
- Tổng số samples auto-labeled: {len(auto_labeled)}
- Từ unlabeled data: {len(df_unlabeled)} rows

## Phân loại theo confidence

### HIGH CONFIDENCE ({len(df_augmented[df_augmented['confidence'] == 'high'])} samples)
- MV Description removed: {error_patterns['MV_DESCRIPTION_NOISE']['count']}
- Technical "nặng": {error_patterns['TECHNICAL_HEAVY']['count']}
- **Khuyến nghị**: Có thể thêm trực tiếp vào training data

### MEDIUM CONFIDENCE ({len(df_augmented[df_augmented['confidence'] == 'medium'])} samples)
- Justice call: {error_patterns['JUSTICE_CALL']['count']}
- Neutral comment: {error_patterns['NEUTRAL_COMMENT']['count']}
- **Khuyến nghị**: Review nhanh trước khi thêm

### LOW CONFIDENCE ({len(df_augmented[df_augmented['confidence'] == 'low'])} samples)
- Sarcasm/light criticism: {error_patterns['SARCASM_POSITIVE']['count']}
- **Khuyến nghị**: Review kỹ, có thể cần relabel

## Cách review

1. Mở file `AUTO_LABELED_HIGH_*.csv`
2. Đọc qua 20-30 samples đầu
3. Nếu đúng > 90% → Thêm toàn bộ vào training data
4. Nếu sai > 20% → Review từng sample

5. Lặp lại với MEDIUM và LOW confidence

## Sau khi review

Merge vào training data:
```python
df_train = pd.read_csv('final_train_data_v2.csv')
df_high = pd.read_csv('AUTO_LABELED_HIGH_*.csv')
df_medium = pd.read_csv('AUTO_LABELED_MEDIUM_*.csv')  # Sau khi review

df_merged = pd.concat([df_train, df_high, df_medium], ignore_index=True)
df_merged.to_csv('final_train_data_v3_AUGMENTED.csv', index=False)
```

## Kỳ vọng

- Tăng training data: +{len(auto_labeled)} samples
- Giảm False Positive (Label 0 → Predicted 1)
- Cải thiện F1: 0.68 → 0.72-0.75
"""

guide_file = "REVIEW_GUIDE.md"
with open(guide_file, 'w', encoding='utf-8') as f:
    f.write(guide_content)

print(f"✅ Saved guide: {guide_file}")

# ============================================================
# 7. TÓM TẮT
# ============================================================

print("\n" + "="*80)
print("✅ HOÀN THÀNH!")
print("="*80)
print(f"\n📊 Tóm tắt:")
print(f"  - Unlabeled data analyzed: {len(df_unlabeled)}")
print(f"  - Auto-labeled samples: {len(auto_labeled)}")
print(f"  - HIGH confidence: {len(df_augmented[df_augmented['confidence'] == 'high'])}")
print(f"  - MEDIUM confidence: {len(df_augmented[df_augmented['confidence'] == 'medium'])}")
print(f"  - LOW confidence: {len(df_augmented[df_augmented['confidence'] == 'low'])}")

print(f"\n🎯 Bước tiếp theo:")
print(f"  1. Review file: {review_file}")
print(f"  2. Đọc hướng dẫn: {guide_file}")
print(f"  3. Merge vào training data")
print(f"  4. Retrain model")
print(f"  5. Kỳ vọng F1: 0.68 → 0.72-0.75")
