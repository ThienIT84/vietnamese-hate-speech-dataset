import pandas as pd
import sys
import re
from datetime import datetime

# Import TEENCODE_DICT từ advanced_text_cleaning
sys.path.append('src/preprocessing')
from advanced_text_cleaning import TEENCODE_DICT

def replace_teencode_only(text):
    """
    Chỉ thay thế teencode (từ viết tắt/sai chính tả) mà KHÔNG động vào:
    - Emoji
    - Tags đã có (<emo_pos>, <person>, v.v.)
    - Ngữ cảnh (</s>)
    - Bất kỳ xử lý nào khác
    """
    if not isinstance(text, str) or not text.strip():
        return text
    
    # Tạo pattern từ TEENCODE_DICT, sắp xếp theo độ dài giảm dần để match từ dài trước
    sorted_teencode = sorted(TEENCODE_DICT.items(), key=lambda x: len(x[0]), reverse=True)
    
    result = text
    
    for teencode, replacement in sorted_teencode:
        # Tạo pattern với word boundary để tránh thay thế nhầm
        # Ví dụ: "ko" không thay thế trong "không"
        pattern = r'\b' + re.escape(teencode) + r'\b'
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    return result

# Đọc file training dataset
input_path = r'data\processed\FINAL_TRAINING_DATASET_20251225_110326.csv'
df = pd.read_csv(input_path)

print(f"File shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# Kiểm tra xem có cột training_text không
if 'training_text' not in df.columns:
    print(f"\n❌ Lỗi: Không tìm thấy cột 'training_text'")
    print(f"Các cột có sẵn: {df.columns.tolist()}")
    sys.exit(1)

print(f"\n📊 Sample training_text TRƯỚC khi xử lý teencode:")
for i in range(min(3, len(df))):
    print(f"  [{i+1}] {df['training_text'].iloc[i][:150]}")

# Áp dụng teencode replacement
print(f"\n🔄 Đang xử lý teencode cho {len(df):,} dòng...")
df['training_text'] = df['training_text'].apply(replace_teencode_only)

print(f"\n✅ Hoàn thành!")
print(f"\n📊 Sample training_text SAU khi xử lý teencode:")
for i in range(min(3, len(df))):
    print(f"  [{i+1}] {df['training_text'].iloc[i][:150]}")

# So sánh một số ví dụ có thay đổi
print(f"\n📝 Một số ví dụ có thay đổi:")
original_df = pd.read_csv(input_path)
changed_count = 0
for i in range(len(df)):
    if df['training_text'].iloc[i] != original_df['training_text'].iloc[i]:
        changed_count += 1
        if changed_count <= 5:  # Chỉ hiển thị 5 ví dụ đầu
            print(f"\n--- Ví dụ {changed_count} ---")
            print(f"Trước: {original_df['training_text'].iloc[i][:200]}")
            print(f"Sau:  {df['training_text'].iloc[i][:200]}")

print(f"\n📊 Tổng số dòng có thay đổi: {changed_count}/{len(df)} ({changed_count/len(df)*100:.1f}%)")

# Lưu file kết quả
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f'data/processed/FINAL_TRAINING_DATASET_TEENCODE_{timestamp}.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"\n✅ Đã lưu file kết quả tại: {output_path}")
print(f"Tổng số dòng: {len(df):,}")
print(f"Tổng số cột: {len(df.columns)}")
print(f"\n🎯 File này đã được xử lý teencode và sẵn sàng để train!")
