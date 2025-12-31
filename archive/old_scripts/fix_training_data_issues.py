"""
🔥 FIX TRAINING DATA ISSUES - Nâng F1 từ 0.68 lên 0.80+

Giải quyết 4 vấn đề chính:
1. VCL/VL trong context tích cực (positive slang)
2. "Nặng" kỹ thuật vs "nặng" toxic
3. Kêu gọi công lý bị nhầm là toxic
4. Noise từ mô tả MV quá dài

Author: Thanh Thien
Date: 29/12/2025
"""

import pandas as pd
import re
from datetime import datetime

print("="*80)
print("🔥 FIXING TRAINING DATA ISSUES")
print("="*80)

# ============================================================
# 1. LOAD DATA
# ============================================================

print("\n📂 Loading data...")
df = pd.read_csv('final_train_data_v2.csv', encoding='utf-8')
print(f"✅ Loaded: {len(df)} rows")

# Backup
backup_path = f"backup_before_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(backup_path, index=False, encoding='utf-8')
print(f"💾 Backup saved: {backup_path}")

# ============================================================
# 2. FIX NHÓM 1: VCL/VL POSITIVE SLANG
# ============================================================

print("\n🔧 FIX 1: VCL/VL trong context tích cực...")

# Patterns cho positive slang với vcl/vl
positive_vcl_patterns = [
    r'\b(chất|đỉnh|peak|vip|hay|đẹp|tuyệt|ngon|xịn|pro|giỏi|khủng)\s+(vcl|vl|vãi\s*lồn)\b',
    r'\b(vcl|vl|vãi\s*lồn)\s+(chất|đỉnh|peak|vip|hay|đẹp|tuyệt|ngon|xịn|pro|giỏi|khủng)\b',
    r'\b(quá|cực|siêu|rất|cực\s*kỳ)\s+(chất|đỉnh|hay|đẹp|tuyệt|ngon)\s+(vcl|vl)\b',
    r'\b(sản\s*phẩm|video|bài\s*hát|mv|nhạc|clip)\s+.{0,30}(chất|đỉnh|hay|đẹp)\s+(vcl|vl)\b',
    r'\b(mua|dùng|xem|nghe)\s+.{0,30}(thích|hay|tốt|ổn)\s+(vcl|vl)\b'
]

fixed_vcl = 0
for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    # Nếu đang là label 1 (toxic) nhưng có positive slang với vcl/vl
    if label == 1:
        for pattern in positive_vcl_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                df.at[idx, 'label'] = 0
                df.at[idx, 'note'] = 'Fixed: VCL/VL positive slang'
                fixed_vcl += 1
                break

print(f"✅ Fixed {fixed_vcl} rows (VCL/VL positive slang)")

# ============================================================
# 3. FIX NHÓM 2: "NẶNG" KỸ THUẬT
# ============================================================

print("\n🔧 FIX 2: 'Nặng' kỹ thuật (video/render)...")

# Patterns cho "nặng" về kỹ thuật
technical_heavy_patterns = [
    r'\b(video|mv|clip|render|khung\s*hình|file|dung\s*lượng)\s+.{0,20}nặng\b',
    r'\bnặng\s+(khung\s*hình|video|mv|quá|lắm|vcl|vl)\b',
    r'\b(lag|giật|load|tải)\s+.{0,20}(nặng|do\s+nặng)\b',
    r'\bnhìn\s+nặng\b',
    r'\bmv\s+.{0,30}nặng\b'
]

fixed_heavy = 0
for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    # Nếu đang là label 1 (toxic) nhưng nói về "nặng" kỹ thuật
    if label == 1:
        for pattern in technical_heavy_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                df.at[idx, 'label'] = 0
                df.at[idx, 'note'] = 'Fixed: Technical "nặng" (video/render)'
                fixed_heavy += 1
                break

print(f"✅ Fixed {fixed_heavy} rows ('nặng' kỹ thuật)")

# ============================================================
# 4. FIX NHÓM 3: KÊU GỌI CÔNG LÝ
# ============================================================

print("\n🔧 FIX 3: Kêu gọi công lý (ủng hộ pháp luật)...")

# Patterns cho kêu gọi công lý
justice_patterns = [
    r'\b(pháp\s*luật|luật\s*pháp|công\s*an|cảnh\s*sát)\s+.{0,30}(xử\s*lý|dạy\s*dỗ|bắt|phạt)\b',
    r'\b(đi|vào|cho\s+vào)\s+(tù|nhà\s*tù|trại|giam)\b',
    r'\b(bắt|phạt|xử|trừng\s*phạt)\s+.{0,30}(kẻ|thằng|con|đứa)\s+(xấu|tội|phạm)\b',
    r'\b(ủng\s*hộ|đúng|nên)\s+.{0,20}(pháp\s*luật|xử\s*lý|trừng\s*phạt)\b',
    r'\bđi\s+bóc\s+\d+\s+cuốn\b',  # "đi bóc 10 cuốn" = đi tù
    r'\b(luật|pháp\s*luật)\s+(dạy|xử|phạt)\b'
]

fixed_justice = 0
for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    # Nếu đang là label 1 hoặc 2 nhưng là kêu gọi công lý
    if label in [1, 2]:
        for pattern in justice_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                # Kiểm tra không phải chửi trực tiếp người khác
                if not re.search(r'\b(mày|mi|bây)\s+(đi|vào)\s+tù\b', text):
                    df.at[idx, 'label'] = 0
                    df.at[idx, 'note'] = 'Fixed: Justice call (support law)'
                    fixed_justice += 1
                    break

print(f"✅ Fixed {fixed_justice} rows (kêu gọi công lý)")

# ============================================================
# 5. FIX NHÓM 4: NOISE TỪ MÔ TẢ MV DÀI
# ============================================================

print("\n🔧 FIX 4: Cắt bỏ mô tả MV quá dài (noise)...")

# Pattern nhận diện mô tả MV
mv_description_pattern = r'^(official\s+poster|visualizer\s+mv|body\s+shaming).{100,}?</s>'

fixed_noise = 0
for idx, row in df.iterrows():
    text = str(row['training_text'])
    
    # Nếu có mô tả MV dài trước </s>
    if re.search(mv_description_pattern, text, re.IGNORECASE):
        # Tách phần sau </s> (comment thực sự)
        parts = text.split('</s>')
        if len(parts) >= 2:
            comment_part = parts[-1].strip()
            
            # Nếu comment ngắn và không toxic, giữ lại comment
            if len(comment_part) < 200:
                df.at[idx, 'training_text'] = comment_part
                df.at[idx, 'note'] = 'Fixed: Removed long MV description noise'
                fixed_noise += 1

print(f"✅ Fixed {fixed_noise} rows (cắt mô tả MV dài)")

# ============================================================
# 6. THÊM AUGMENTATION CHO VCL/VL POSITIVE
# ============================================================

print("\n🔧 AUGMENTATION: Thêm ví dụ VCL/VL positive...")

# Tạo thêm ví dụ positive slang với vcl/vl
positive_vcl_examples = [
    ("sản phẩm chất lượng vcl, mua về dùng thích lắm", 0, "Augmented: VCL positive"),
    ("video này đỉnh vcl, xem đi xem lại không chán", 0, "Augmented: VCL positive"),
    ("bài hát hay vl, nghe mãi không ngán", 0, "Augmented: VCL positive"),
    ("quả đẹp vcl, chơi game sướng quá", 0, "Augmented: VCL positive"),
    ("peak vcl, đội này mạnh thật", 0, "Augmented: VCL positive"),
    ("vip vl, dịch vụ tốt lắm", 0, "Augmented: VCL positive"),
    ("render đẹp vcl nhưng nặng khung hình quá", 0, "Augmented: VCL + technical"),
    ("mv nhìn nặng vcl nhưng chất lượng cao", 0, "Augmented: VCL + technical"),
]

augmented_rows = []
for text, label, note in positive_vcl_examples:
    augmented_rows.append({
        'training_text': text,
        'label': label,
        'note': note,
        'source_file': 'augmentation',
        'labeler': 'auto_fix'
    })

df_augmented = pd.DataFrame(augmented_rows)
df = pd.concat([df, df_augmented], ignore_index=True)

print(f"✅ Added {len(augmented_rows)} augmented examples")

# ============================================================
# 7. SAVE FIXED DATA
# ============================================================

print("\n💾 Saving fixed data...")

output_path = f"final_train_data_v2_FIXED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"✅ Saved to: {output_path}")

# ============================================================
# 8. STATISTICS
# ============================================================

print("\n" + "="*80)
print("📊 FIX SUMMARY")
print("="*80)
print(f"Total fixes applied:           {fixed_vcl + fixed_heavy + fixed_justice + fixed_noise}")
print(f"  - VCL/VL positive slang:     {fixed_vcl}")
print(f"  - 'Nặng' kỹ thuật:           {fixed_heavy}")
print(f"  - Kêu gọi công lý:           {fixed_justice}")
print(f"  - Cắt mô tả MV dài:          {fixed_noise}")
print(f"  - Augmented examples:        {len(augmented_rows)}")
print(f"\nOriginal dataset:              {len(df) - len(augmented_rows)}")
print(f"Fixed dataset:                 {len(df)}")

# Label distribution
print(f"\n📊 Label distribution after fix:")
for label, count in df['label'].value_counts().sort_index().items():
    print(f"   Label {label}: {count} ({count/len(df)*100:.1f}%)")

print("\n" + "="*80)
print("✅ FIXES COMPLETE!")
print("="*80)
print(f"\n🎯 Next steps:")
print(f"1. Review fixed data: {output_path}")
print(f"2. Retrain model with fixed data")
print(f"3. Expected F1 improvement: 0.68 → 0.75-0.80+")
