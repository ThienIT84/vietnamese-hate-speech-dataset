"""
🔥 FIX TRAINING DATA - GIẢI PHÁP THỰC TẾ VÀ THƯƠNG MẠI

Nguyên tắc:
1. VCL/VL vẫn là TOXIC dù context tích cực (Label 1)
2. CHỈ fix những lỗi THỰC SỰ SAI:
   - "Nặng" kỹ thuật (video/render)
   - Kêu gọi công lý (ủng hộ pháp luật)
   - Noise từ mô tả MV dài

Author: Thanh Thien
Date: 29/12/2025
"""

import pandas as pd
import re
from datetime import datetime

print("="*80)
print("🔥 FIXING TRAINING DATA - PROPER SOLUTION")
print("="*80)

# ============================================================
# 1. LOAD DATA
# ============================================================

print("\n📂 Loading data...")
df = pd.read_csv('final_train_data_v2.csv', encoding='utf-8')
print(f"✅ Loaded: {len(df)} rows")

# Backup
backup_path = f"backup_proper_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(backup_path, index=False, encoding='utf-8')
print(f"💾 Backup saved: {backup_path}")

# ============================================================
# 2. FIX 1: "NẶNG" KỸ THUẬT (ĐÚNG)
# ============================================================

print("\n🔧 FIX 1: 'Nặng' kỹ thuật (video/render)...")

technical_heavy_patterns = [
    r'\b(video|mv|clip|render|khung\s*hình|file|dung\s*lượng)\s+.{0,20}nặng\b',
    r'\bnặng\s+(khung\s*hình|video|mv|quá|lắm|vcl|vl)\b',
    r'\b(lag|giật|load|tải)\s+.{0,20}(nặng|do\s+nặng)\b',
    r'\bnhìn\s+nặng\b',
    r'\bmv\s+.{0,30}nặng\b',
    r'\bnặng\s+.{0,20}(fps|khung|giây)\b'
]

fixed_heavy = 0
for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    # CHỈ fix nếu đang là toxic NHƯNG nói về kỹ thuật
    if label == 1:
        # Kiểm tra KHÔNG có từ chửi thề khác
        has_other_toxic = bool(re.search(r'\b(đm|dm|dcm|cc|lồn|cặc|đéo|địt)\b', text))
        
        # Nếu có "nặng" kỹ thuật VÀ không có từ toxic khác
        if not has_other_toxic:
            for pattern in technical_heavy_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    df.at[idx, 'label'] = 0
                    df.at[idx, 'note'] = 'Fixed: Technical "nặng" only'
                    fixed_heavy += 1
                    break

print(f"✅ Fixed {fixed_heavy} rows ('nặng' kỹ thuật thuần túy)")

# ============================================================
# 3. FIX 2: KÊU GỌI CÔNG LÝ (ĐÚNG)
# ============================================================

print("\n🔧 FIX 2: Kêu gọi công lý (ủng hộ pháp luật)...")

justice_patterns = [
    r'\b(pháp\s*luật|luật\s*pháp|công\s*an|cảnh\s*sát)\s+.{0,30}(xử\s*lý|dạy\s*dỗ|bắt|phạt)\b',
    r'\b(đi|vào|cho\s+vào)\s+(tù|nhà\s*tù|trại|giam)\b',
    r'\b(bắt|phạt|xử|trừng\s*phạt)\s+.{0,30}(kẻ|thằng|con|đứa)\s+(xấu|tội|phạm)\b',
    r'\b(ủng\s*hộ|đúng|nên)\s+.{0,20}(pháp\s*luật|xử\s*lý|trừng\s*phạt)\b',
    r'\bđi\s+bóc\s+\d+\s+cuốn\b',
    r'\b(luật|pháp\s*luật)\s+(dạy|xử|phạt)\b'
]

# Patterns cho chửi trực tiếp (KHÔNG fix)
direct_insult_patterns = [
    r'\b(mày|mi|bây)\s+(đi|vào)\s+tù\b',
    r'\b(mày|mi|bây)\s+.{0,20}(chó|lợn|súc\s*vật)\b',
    r'\bcho\s+(mày|mi)\s+vào\s+tù\b'
]

fixed_justice = 0
for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    if label in [1, 2]:
        # Kiểm tra KHÔNG phải chửi trực tiếp
        is_direct_insult = any(re.search(p, text) for p in direct_insult_patterns)
        
        if not is_direct_insult:
            # Kiểm tra có kêu gọi công lý
            for pattern in justice_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    df.at[idx, 'label'] = 0
                    df.at[idx, 'note'] = 'Fixed: Justice call (support law)'
                    fixed_justice += 1
                    break

print(f"✅ Fixed {fixed_justice} rows (kêu gọi công lý)")

# ============================================================
# 4. FIX 3: CẮT MÔ TẢ MV DÀI (ĐÚNG)
# ============================================================

print("\n🔧 FIX 3: Cắt bỏ mô tả MV quá dài (noise)...")

mv_description_pattern = r'^(official\s+poster|visualizer\s+mv|body\s+shaming).{100,}?</s>'

fixed_noise = 0
for idx, row in df.iterrows():
    text = str(row['training_text'])
    
    if re.search(mv_description_pattern, text, re.IGNORECASE):
        parts = text.split('</s>')
        if len(parts) >= 2:
            comment_part = parts[-1].strip()
            
            # CHỈ cắt nếu comment ngắn và không có toxic words
            if len(comment_part) < 200:
                # Kiểm tra comment có toxic không
                has_toxic = bool(re.search(r'\b(đm|dm|dcm|cc|lồn|cặc|đéo|địt|vl|vcl)\b', comment_part.lower()))
                
                # Nếu comment không toxic, cắt bỏ mô tả
                if not has_toxic:
                    df.at[idx, 'training_text'] = comment_part
                    df.at[idx, 'note'] = 'Fixed: Removed long MV description'
                    fixed_noise += 1

print(f"✅ Fixed {fixed_noise} rows (cắt mô tả MV dài)")

# ============================================================
# 5. KHÔNG FIX VCL/VL - GIỮ NGUYÊN TOXIC
# ============================================================

print("\n⚠️  VCL/VL: KHÔNG FIX - Giữ nguyên Label 1 (Toxic)")
print("    Lý do: Vẫn là từ tục, không phù hợp thương mại")

# ============================================================
# 6. THÊM AUGMENTATION CHO EDGE CASES
# ============================================================

print("\n🔧 AUGMENTATION: Thêm ví dụ edge cases...")

augmented_examples = [
    # "Nặng" kỹ thuật thuần túy
    ("video này nặng quá, máy tôi không tải nổi", 0, "Augmented: Technical heavy"),
    ("mv render nặng, lag fps thấp", 0, "Augmented: Technical heavy"),
    ("file nặng 2gb, tải lâu quá", 0, "Augmented: Technical heavy"),
    
    # Kêu gọi công lý
    ("pháp luật cần xử lý nghiêm khắc kẻ xấu này", 0, "Augmented: Justice call"),
    ("ủng hộ công an bắt giữ tội phạm", 0, "Augmented: Justice call"),
    ("nên cho vào tù để răn đe", 0, "Augmented: Justice call"),
    
    # VCL/VL vẫn là toxic (để model học rõ)
    ("sản phẩm này vãi lồn", 1, "Augmented: VCL still toxic"),
    ("hay vl nhưng vẫn là từ tục", 1, "Augmented: VL still toxic"),
]

augmented_rows = []
for text, label, note in augmented_examples:
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

output_path = f"final_train_data_v2_PROPER_FIX_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"✅ Saved to: {output_path}")

# ============================================================
# 8. STATISTICS
# ============================================================

print("\n" + "="*80)
print("📊 FIX SUMMARY (PROPER SOLUTION)")
print("="*80)
print(f"Total fixes applied:           {fixed_heavy + fixed_justice + fixed_noise}")
print(f"  - 'Nặng' kỹ thuật thuần:     {fixed_heavy}")
print(f"  - Kêu gọi công lý:           {fixed_justice}")
print(f"  - Cắt mô tả MV dài:          {fixed_noise}")
print(f"  - Augmented examples:        {len(augmented_rows)}")
print(f"\n⚠️  VCL/VL: KHÔNG FIX (giữ Label 1)")
print(f"\nOriginal dataset:              {len(df) - len(augmented_rows)}")
print(f"Fixed dataset:                 {len(df)}")

# Label distribution
print(f"\n📊 Label distribution after proper fix:")
for label, count in df['label'].value_counts().sort_index().items():
    print(f"   Label {label}: {count} ({count/len(df)*100:.1f}%)")

print("\n" + "="*80)
print("✅ PROPER FIXES COMPLETE!")
print("="*80)
print(f"\n🎯 Nguyên tắc:")
print(f"1. VCL/VL vẫn là TOXIC (Label 1) - Không thương mại")
print(f"2. CHỈ fix lỗi thực sự: 'nặng' kỹ thuật, công lý, noise MV")
print(f"3. Giữ tính nhất quán và uy tín hệ thống")
