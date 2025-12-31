"""
🎯 CẮT TIÊU ĐỀ DÀI - GIỮ 50 TỪ CUỐI CÙNG
Giữ ngữ cảnh quan trọng nhất của title

Chiến lược:
- Nếu title > 50 từ: Giữ 50 từ cuối + "..." ở đầu
- Nếu title <= 50 từ: Giữ nguyên
- Format: "...50 từ cuối title </s> comment"

Author: Thanh Thien
Date: 29/12/2025
"""

import pandas as pd
import re
from datetime import datetime

print("="*80)
print("🎯 CẮT TIÊU ĐỀ DÀI - GIỮ 50 TỪ CUỐI")
print("="*80)

def truncate_title(text, max_words=50):
    """
    Cắt title dài, giữ max_words từ cuối cùng
    """
    if '</s>' not in text:
        # Không có separator, return nguyên
        return text
    
    parts = text.split('</s>')
    if len(parts) < 2:
        return text
    
    title = parts[0].strip()
    comment = parts[1].strip()
    
    # Đếm số từ trong title
    words = title.split()
    
    if len(words) <= max_words:
        # Title ngắn, giữ nguyên
        return text
    
    # Title dài, giữ max_words từ cuối
    truncated_title = ' '.join(words[-max_words:])
    new_text = f"...{truncated_title} </s> {comment}"
    
    return new_text

# ============================================================
# 1. XỬ LÝ FILE AUTO_LABELED
# ============================================================

print("\n📂 Processing AUTO_LABELED_REVIEW_FIXED.xlsx...")

df = pd.read_excel('AUTO_LABELED_REVIEW_FIXED.xlsx', engine='openpyxl')
print(f"✅ Loaded: {len(df)} rows")

# Thống kê trước khi cắt
long_titles = 0
total_words_before = 0
total_words_after = 0

for idx, row in df.iterrows():
    text = str(row['training_text'])
    
    if '</s>' in text:
        title = text.split('</s>')[0].strip()
        words = title.split()
        total_words_before += len(words)
        
        if len(words) > 50:
            long_titles += 1

print(f"\n📊 Thống kê:")
print(f"  - Rows có title dài (>50 từ): {long_titles}")
print(f"  - Tỷ lệ: {long_titles/len(df)*100:.1f}%")

# Cắt title
print(f"\n✂️ Cắt title dài...")
df['training_text'] = df['training_text'].apply(lambda x: truncate_title(str(x), max_words=50))

# Thống kê sau khi cắt
for idx, row in df.iterrows():
    text = str(row['training_text'])
    if '</s>' in text:
        title = text.split('</s>')[0].strip()
        words = title.split()
        total_words_after += len(words)

avg_words_before = total_words_before / len(df) if len(df) > 0 else 0
avg_words_after = total_words_after / len(df) if len(df) > 0 else 0

print(f"\n📊 Kết quả:")
print(f"  - Trung bình từ/title trước: {avg_words_before:.1f}")
print(f"  - Trung bình từ/title sau: {avg_words_after:.1f}")
print(f"  - Giảm: {avg_words_before - avg_words_after:.1f} từ")

# Lưu file
output_file = "AUTO_LABELED_TRUNCATED.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')
print(f"\n✅ Saved: {output_file}")

# ============================================================
# 2. XỬ LÝ FILE HIGH CONFIDENCE
# ============================================================

print("\n📂 Processing AUTO_LABELED_HIGH_FIXED.xlsx...")

df_high = pd.read_excel('AUTO_LABELED_HIGH_FIXED.xlsx', engine='openpyxl')
print(f"✅ Loaded: {len(df_high)} rows")

df_high['training_text'] = df_high['training_text'].apply(lambda x: truncate_title(str(x), max_words=50))

output_high = "AUTO_LABELED_HIGH_TRUNCATED.xlsx"
df_high.to_excel(output_high, index=False, engine='openpyxl')
print(f"✅ Saved: {output_high}")

# ============================================================
# 3. XỬ LÝ FILE MEDIUM CONFIDENCE
# ============================================================

print("\n📂 Processing AUTO_LABELED_MEDIUM_FIXED.xlsx...")

df_medium = pd.read_excel('AUTO_LABELED_MEDIUM_FIXED.xlsx', engine='openpyxl')
print(f"✅ Loaded: {len(df_medium)} rows")

df_medium['training_text'] = df_medium['training_text'].apply(lambda x: truncate_title(str(x), max_words=50))

output_medium = "AUTO_LABELED_MEDIUM_TRUNCATED.xlsx"
df_medium.to_excel(output_medium, index=False, engine='openpyxl')
print(f"✅ Saved: {output_medium}")

# ============================================================
# 4. HIỂN THỊ VÍ DỤ
# ============================================================

print("\n" + "="*80)
print("📝 VÍ DỤ TRƯỚC VÀ SAU KHI CẮT")
print("="*80)

# Load lại file gốc để so sánh
df_original = pd.read_excel('AUTO_LABELED_REVIEW_FIXED.xlsx', engine='openpyxl')

# Tìm 3 ví dụ có title dài
examples = []
for idx, row in df_original.iterrows():
    text = str(row['training_text'])
    if '</s>' in text:
        title = text.split('</s>')[0].strip()
        if len(title.split()) > 100:
            examples.append((text, df.iloc[idx]['training_text']))
            if len(examples) >= 3:
                break

for i, (before, after) in enumerate(examples, 1):
    print(f"\n[Ví dụ {i}]")
    print(f"TRƯỚC ({len(before)} chars):")
    print(f"  {before[:200]}...")
    print(f"\nSAU ({len(after)} chars):")
    print(f"  {after[:200]}...")
    print("-" * 80)

# ============================================================
# 5. TÓM TẮT
# ============================================================

print("\n" + "="*80)
print("✅ HOÀN THÀNH!")
print("="*80)

print(f"\n📊 Tóm tắt:")
print(f"  - Rows xử lý: {len(df)}")
print(f"  - Rows có title dài (>50 từ): {long_titles}")
print(f"  - Giảm trung bình: {avg_words_before - avg_words_after:.1f} từ/title")

print(f"\n📁 Files đã tạo:")
print(f"  1. {output_file} - Tất cả {len(df)} rows")
print(f"  2. {output_high} - HIGH confidence {len(df_high)} rows")
print(f"  3. {output_medium} - MEDIUM confidence {len(df_medium)} rows")

print(f"\n🎯 Lợi ích:")
print(f"  - Giữ ngữ cảnh quan trọng (50 từ cuối title)")
print(f"  - Giảm noise từ mô tả dài")
print(f"  - Model tập trung vào comment hơn")
print(f"  - Kỳ vọng cải thiện F1: 0.68 → 0.72-0.75")
