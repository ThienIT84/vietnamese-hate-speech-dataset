"""
Script chia dữ liệu cho 3 người gắn nhãn
- Người 1 (Tech Lead): 3,000 mẫu đa dạng nhất
- Người 2: 7,500 mẫu
- Người 3: 7,500 mẫu
- Overlap: 500 mẫu chung (để tính Cohen's Kappa)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime

# =====================================================
# CẤU HÌNH
# =====================================================

INPUT_FILE = "final_dataset/master_combined.csv"
OUTPUT_DIR = "labeling/"

# Số lượng mẫu
TECH_LEAD_SAMPLES = 3000      # Người đã làm crawl + cleaning
PERSON2_SAMPLES = 7500        # Người 2
PERSON3_SAMPLES = 7500        # Người 3
OVERLAP_SAMPLES = 500         # 3 người cùng label để tính Kappa

TOTAL_NEEDED = TECH_LEAD_SAMPLES + PERSON2_SAMPLES + PERSON3_SAMPLES + OVERLAP_SAMPLES
print(f"📊 Tổng mẫu cần: {TOTAL_NEEDED:,}")

# =====================================================
# ĐỌC DỮ LIỆU
# =====================================================

print("\n🔍 Đọc dữ liệu...")
df = pd.read_csv(INPUT_FILE)
print(f"✅ Đọc được {len(df):,} dòng")

# Chỉ lấy các cột cần thiết
# Dùng cleaned_text_norm (đã qua TOÀN BỘ pipeline bao gồm replace_person_names)
df_labeling = df[['id', 'text', 'cleaned_text_norm', 'source_platform', 'topic']].copy()

# Loại bỏ duplicate và missing
print("\n🧹 Làm sạch dữ liệu...")
before = len(df_labeling)
df_labeling = df_labeling.dropna(subset=['cleaned_text_norm'])
df_labeling = df_labeling[df_labeling['cleaned_text_norm'].str.strip() != '']
df_labeling = df_labeling.drop_duplicates(subset=['cleaned_text_norm'])
df_labeling = df_labeling.reset_index(drop=True)
print(f"✅ Còn lại {len(df_labeling):,} mẫu unique ({before - len(df_labeling):,} đã loại bỏ)")

# Kiểm tra đủ mẫu không
if len(df_labeling) < TOTAL_NEEDED:
    print(f"⚠️ CẢNH BÁO: Chỉ có {len(df_labeling):,} mẫu, cần {TOTAL_NEEDED:,}")
    print("→ Sẽ lấy tất cả mẫu có sẵn và chia tỷ lệ")

# =====================================================
# STRATIFIED SAMPLING (Chia theo topic để đa dạng)
# =====================================================

print("\n📊 Phân tích phân bố topic...")
print(df_labeling['topic'].value_counts())

# Thêm các đặc trưng để stratify
df_labeling['text_length_bin'] = pd.cut(df_labeling['cleaned_text_norm'].str.len(), 
                                         bins=[0, 50, 100, 200, 1000], 
                                         labels=['short', 'medium', 'long', 'very_long'])

df_labeling['platform'] = df_labeling['source_platform'].fillna('unknown')

# Tạo stratify key
df_labeling['stratify_key'] = (
    df_labeling['topic'].fillna('unknown').astype(str) + '_' + 
    df_labeling['text_length_bin'].astype(str) + '_' +
    df_labeling['platform'].astype(str)
)

print(f"\n🎯 Có {df_labeling['stratify_key'].nunique()} nhóm stratify khác nhau")

# =====================================================
# CHIA DỮ LIỆU
# =====================================================

print("\n✂️ Chia dữ liệu...")

# Bước 1: Tách 500 mẫu overlap (3 người cùng label)
try:
    df_overlap, df_remaining = train_test_split(
        df_labeling, 
        train_size=min(OVERLAP_SAMPLES, len(df_labeling) // 4),
        stratify=df_labeling['stratify_key'],
        random_state=42
    )
    print(f"✅ Overlap set: {len(df_overlap):,} mẫu")
except:
    # Nếu stratify không được, lấy random
    print("⚠️ Không thể stratify, lấy random...")
    df_overlap = df_labeling.sample(n=min(OVERLAP_SAMPLES, len(df_labeling) // 4), random_state=42)
    df_remaining = df_labeling.drop(df_overlap.index)

# Bước 2: Tách 3,000 mẫu cho Tech Lead (ĐA DẠNG NHẤT)
try:
    df_tech, df_remaining2 = train_test_split(
        df_remaining,
        train_size=min(TECH_LEAD_SAMPLES, len(df_remaining) // 3),
        stratify=df_remaining['stratify_key'],
        random_state=42
    )
    print(f"✅ Tech Lead set: {len(df_tech):,} mẫu (đa dạng)")
except:
    df_tech = df_remaining.sample(n=min(TECH_LEAD_SAMPLES, len(df_remaining) // 3), random_state=42)
    df_remaining2 = df_remaining.drop(df_tech.index)

# Bước 3: Chia đều cho Person 2 và Person 3
remaining_samples = len(df_remaining2)
person2_size = min(PERSON2_SAMPLES, remaining_samples // 2)

df_person2 = df_remaining2.sample(n=person2_size, random_state=42)
df_person3 = df_remaining2.drop(df_person2.index)

print(f"✅ Person 2 set: {len(df_person2):,} mẫu")
print(f"✅ Person 3 set: {len(df_person3):,} mẫu")

# =====================================================
# THÊM CỘT GÁN NHÃN
# =====================================================

def prepare_labeling_file(df, include_overlap=False):
    """Chuẩn bị file cho gắn nhãn"""
    result = df[['id','source_platform', 'topic', 'cleaned_text_norm']].copy()
    
    # Đổi tên cột: text_to_label để gắn nhãn
    result = result.rename(columns={
        'cleaned_text_norm': 'text_to_label'  # Text đã clean HOÀN TOÀN (có <PERSON>, <USER>)
    })
    
    # Thêm các cột cần điền
    result['label'] = ''           # 0 / 1 / 2
    result['topic_hate'] = ''      # Region/Body/Gender/Family/Disability/Violence (nếu label=2)
    result['confidence'] = ''      # 1 / 2 / 3
    result['note'] = ''            # Ghi chú nếu khó
    result['original_text'] = df['text'].values  # Text gốc - đẩy ra cuối để tham khảo
    
    return result

df_tech_final = prepare_labeling_file(df_tech)
df_person2_final = prepare_labeling_file(df_person2)
df_person3_final = prepare_labeling_file(df_person3)
df_overlap_final = prepare_labeling_file(df_overlap)

# =====================================================
# THỐNG KÊ
# =====================================================

print("\n" + "="*80)
print("📊 THỐNG KÊ PHÂN CHIA")
print("="*80)

def print_stats(df, name):
    print(f"\n{name}:")
    print(f"  • Tổng mẫu: {len(df):,}")
    print(f"  • Phân bố topic:")
    for topic, count in df['topic'].value_counts().head(5).items():
        print(f"    - {topic}: {count} ({count/len(df)*100:.1f}%)")
    print(f"  • Độ dài trung bình: {df['text_to_label'].str.len().mean():.0f} ký tự")
    print(f"  • Platform:")
    for platform, count in df['source_platform'].value_counts().items():
        print(f"    - {platform}: {count} ({count/len(df)*100:.1f}%)")

print_stats(df_overlap_final, "📍 OVERLAP (3 người cùng label)")
print_stats(df_tech_final, "👨‍💻 TECH LEAD (Người crawl + cleaning)")
print_stats(df_person2_final, "👤 PERSON 2")
print_stats(df_person3_final, "👤 PERSON 3")

# =====================================================
# LƯU FILE
# =====================================================

timestamp = datetime.now().strftime("%Y%m%d")

files = {
    f"dataset_to_label_OVERLAP_{timestamp}.csv": df_overlap_final,
    f"dataset_to_label_TECH_LEAD_{timestamp}.csv": df_tech_final,
    f"dataset_to_label_PERSON2_{timestamp}.csv": df_person2_final,
    f"dataset_to_label_PERSON3_{timestamp}.csv": df_person3_final,
}

print("\n" + "="*80)
print("💾 LƯU FILE")
print("="*80)

for filename, data in files.items():
    filepath = OUTPUT_DIR + filename
    data.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"✅ {filepath} ({len(data):,} mẫu)")

# =====================================================
# HƯỚNG DẪN
# =====================================================

print("\n" + "="*80)
print("📋 HƯỚNG DẪN SỬ DỤNG")
print("="*80)

print(f"""
1️⃣ GIAI ĐOẠN 1: GẮN NHÃN OVERLAP (500 mẫu)
   • 3 người CÙNG gắn nhãn file: dataset_to_label_OVERLAP_{timestamp}.csv
   • Mục đích: Đánh giá độ thống nhất (Cohen's Kappa)
   • Yêu cầu: Kappa ≥ 0.75 (nếu thấp hơn → thảo luận lại guideline)

2️⃣ GIAI ĐOẠN 2: GẮN NHÃN RIÊNG
   Tech Lead:  dataset_to_label_TECH_LEAD_{timestamp}.csv  ({len(df_tech_final):,} mẫu)
   Person 2:   dataset_to_label_PERSON2_{timestamp}.csv    ({len(df_person2_final):,} mẫu)
   Person 3:   dataset_to_label_PERSON3_{timestamp}.csv    ({len(df_person3_final):,} mẫu)

3️⃣ CÁC CỘT CẦN ĐIỀN:
   • label:      0 (Clean) / 1 (Offensive) / 2 (Hate & Dangerous)
   • topic_hate: Region/Body/Gender/Family/Disability/Violence (CHỈ khi label=2)
   • confidence: 1 (không chắc) / 2 (tương đối) / 3 (rất chắc)
   • note:       Ghi chú nếu khó (tùy chọn)

4️⃣ SAU KHI GẮN XONG:
   • Lưu file với tên: dataset_LABELED_<TÊN>_{timestamp}.csv
   • Chạy script merge để tính Cohen's Kappa
   • Resolve các mẫu có disagreement cao

📖 ĐỌC GUIDELINE: GUIDELINE_GAN_NHAN_V3.md

🎯 MỤC TIÊU: Cohen's Kappa ≥ 0.75
""")

print("\n✅ HOÀN TẤT! Chúc gắn nhãn hiệu quả! 🎯\n")
