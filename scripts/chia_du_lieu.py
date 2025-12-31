"""
Script chia dữ liệu theo chiến lược gán nhãn khoa học
- Nhóm 1: 3000 mẫu có khả năng Hate Speech cao (keyword-based)
- Nhóm 2: 3000 mẫu từ topic nhạy cảm (regional discrimination, lgbt, body_shaming...)
- Nhóm 3: 3000 mẫu random
- IAA Set: 500 mẫu overlap để tính Inter-Annotator Agreement
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

# ================================
# PHẦN 1: CẤU HÌNH
# ================================

# Từ khóa nhạy cảm để lọc Hate Speech
HATE_KEYWORDS = [
    r'\bđéo\b', r'\bđ\*\*\b', r'\bđệch\b', r'\bđm\b', r'\bđcm\b', r'\bđụ\b',
    r'\blồn\b', r'\bloz\b', r'\blolz\b', r'\bcặc\b', r'\bcak\b',
    r'\bchó\b', r'\bđĩ\b', r'\bsủa\b', r'\blũ\b', r'\bthằng\b',
    r'\bcon\s+mẹ\b', r'\bđit\s+mẹ\b', r'\bđịt\s+mẹ\b', r'\bđéo\s+mẹ\b',
    r'\bđần\s+độn\b', r'\bngu\s+(như|thế|vãi|vcl)\b', r'\bngáo\b',
    r'\bbệnh\s+hoạn\b', r'\bkhốn\s+nạn\b', r'\bthối\s+nát\b',
    r'\brác\s+rưởi\b', r'\btồi\s+tệ\b', r'\bchết\s+đi\b', r'\bchết\s+mẹ\b',
    r'\bvãi\s+lồn\b', r'\bvcl\b', r'\bvai\s+lon\b',
    r'\bngu\s+đần\b', r'\bngu\s+ngốc\b', r'\bkhùng\b', r'\bđiên\b',
    r'\bque\b', r'\bba\s+que\b', r'\bdm\b', r'\bđm\b',
    r'\bđập\s+chết\b', r'\bgiết\b', r'\btông\s+cho\b', r'\bđánh\s+cho\b'
]

# Topic nhạy cảm
SENSITIVE_TOPICS = [
    'regional discrimination', 'gender-lgbtq', 'body_shaming', 'body-shaming',
    'social issue - pbvm', 'regional discrimination!', 'topiclgbt',
    'lgbtvn', 'gener', 'gender', 'regional discriminationn',
    'drama influencer - chửi bới cự chiến binh  30-4'
]

# ================================
# PHẦN 2: HÀM HỖ TRỢ
# ================================

def contains_hate_keyword(text):
    """Kiểm tra xem text có chứa từ khóa hate speech không"""
    if pd.isna(text):
        return False
    text_lower = str(text).lower()
    for pattern in HATE_KEYWORDS:
        if re.search(pattern, text_lower):
            return True
    return False


def clean_data(df):
    """Loại bỏ các mẫu không đủ chất lượng"""
    print("\n🧹 Làm sạch dữ liệu...")
    before = len(df)
    
    # Loại bỏ mẫu quá ngắn (< 3 từ), trừ khi là từ chửi thề đơn lẻ
    df['is_hate_keyword'] = df['input_text'].apply(contains_hate_keyword)
    df = df[(df['word_count'] >= 3) | (df['is_hate_keyword'] == True)].copy()
    
    # Loại bỏ mẫu trống hoặc null
    df = df[df['input_text'].notna()].copy()
    df = df[df['input_text'].str.strip() != ''].copy()
    
    after = len(df)
    print(f"  - Trước: {before:,} mẫu")
    print(f"  - Sau: {after:,} mẫu")
    print(f"  - Đã loại bỏ: {before-after:,} mẫu ({(before-after)/before*100:.1f}%)")
    
    return df


def stratified_sampling(df, n_hate=3000, n_topic=3000, n_random=3000):
    """
    Chia dữ liệu theo 3 nhóm chiến lược
    """
    print("\n📊 CHIẾN LƯỢC CHỌN MẪU")
    print("=" * 70)
    
    # NHÓM 1: Mẫu có khả năng Hate Speech cao (keyword-based)
    print(f"\n🔴 NHÓM 1: Mẫu có khả năng Hate Speech cao (mục tiêu: {n_hate})")
    df_hate = df[df['is_hate_keyword'] == True].copy()
    print(f"  - Tìm thấy: {len(df_hate):,} mẫu chứa từ khóa nhạy cảm")
    
    if len(df_hate) >= n_hate:
        sample_hate = df_hate.sample(n=n_hate, random_state=42)
    else:
        print(f"  ⚠️ Chỉ đủ {len(df_hate)} mẫu, lấy tất cả")
        sample_hate = df_hate
    print(f"  ✓ Đã chọn: {len(sample_hate):,} mẫu")
    
    # NHÓM 2: Mẫu từ Topic nhạy cảm
    print(f"\n🟡 NHÓM 2: Mẫu từ Topic nhạy cảm (mục tiêu: {n_topic})")
    df_remaining = df.drop(sample_hate.index)
    df_topic = df_remaining[df_remaining['topic'].isin(SENSITIVE_TOPICS)].copy()
    print(f"  - Tìm thấy: {len(df_topic):,} mẫu từ {len(SENSITIVE_TOPICS)} topic nhạy cảm")
    
    topic_dist = df_topic['topic'].value_counts()
    print(f"  - Phân bố topic:")
    for topic, count in topic_dist.head(10).items():
        print(f"    • {topic}: {count:,}")
    
    if len(df_topic) >= n_topic:
        sample_topic = df_topic.sample(n=n_topic, random_state=42)
    else:
        print(f"  ⚠️ Chỉ đủ {len(df_topic)} mẫu, lấy tất cả")
        sample_topic = df_topic
    print(f"  ✓ Đã chọn: {len(sample_topic):,} mẫu")
    
    # NHÓM 3: Mẫu ngẫu nhiên (Random)
    print(f"\n🟢 NHÓM 3: Mẫu ngẫu nhiên (mục tiêu: {n_random})")
    df_remaining2 = df_remaining.drop(sample_topic.index)
    print(f"  - Tổng mẫu còn lại: {len(df_remaining2):,}")
    
    if len(df_remaining2) >= n_random:
        sample_random = df_remaining2.sample(n=n_random, random_state=42)
    else:
        print(f"  ⚠️ Chỉ đủ {len(df_remaining2)} mẫu, lấy tất cả")
        sample_random = df_remaining2
    print(f"  ✓ Đã chọn: {len(sample_random):,} mẫu")
    
    # Gộp 3 nhóm
    final_samples = pd.concat([sample_hate, sample_topic, sample_random])
    
    # Đánh dấu nhóm để báo cáo
    final_samples['sampling_strategy'] = ''
    final_samples.loc[sample_hate.index, 'sampling_strategy'] = 'hate_keyword'
    final_samples.loc[sample_topic.index, 'sampling_strategy'] = 'sensitive_topic'
    final_samples.loc[sample_random.index, 'sampling_strategy'] = 'random'
    
    print(f"\n✅ Tổng mẫu đã chọn: {len(final_samples):,}")
    
    return final_samples


def create_iaa_set(df, n_overlap=500):
    """
    Tạo tập overlap để tính Inter-Annotator Agreement
    """
    print(f"\n📐 TẠO IAA SET ({n_overlap} mẫu)")
    print("=" * 70)
    print("  💡 Mục đích: Cả 3 người cùng gán để đo độ đồng thuận (Fleiss' Kappa)")
    
    # Chọn ngẫu nhiên n_overlap mẫu từ tập đầy đủ
    # Nên chọn đa dạng: một phần từ hate, một phần từ topic, một phần random
    n_per_group = n_overlap // 3
    
    hate_group = df[df['sampling_strategy'] == 'hate_keyword']
    topic_group = df[df['sampling_strategy'] == 'sensitive_topic']
    random_group = df[df['sampling_strategy'] == 'random']
    
    iaa_hate = hate_group.sample(n=min(n_per_group, len(hate_group)), random_state=42)
    iaa_topic = topic_group.sample(n=min(n_per_group, len(topic_group)), random_state=42)
    iaa_random = random_group.sample(n=min(n_overlap - len(iaa_hate) - len(iaa_topic), len(random_group)), random_state=42)
    
    iaa_set = pd.concat([iaa_hate, iaa_topic, iaa_random])
    
    print(f"  - Hate keyword: {len(iaa_hate)}")
    print(f"  - Sensitive topic: {len(iaa_topic)}")
    print(f"  - Random: {len(iaa_random)}")
    print(f"  ✓ Tổng IAA set: {len(iaa_set)} mẫu")
    
    return iaa_set


def split_for_annotators(df, iaa_set, n_members=3):
    """
    Chia dữ liệu cho 3 người gán nhãn
    """
    print(f"\n👥 CHIA DỮ LIỆU CHO {n_members} THÀNH VIÊN")
    print("=" * 70)
    
    # Các mẫu không nằm trong IAA set
    remaining = df.drop(iaa_set.index)
    
    # Shuffle để phân phối đều
    remaining = remaining.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Chia đều cho 3 người
    chunk_size = len(remaining) // n_members
    
    splits = []
    for i in range(n_members):
        if i < n_members - 1:
            member_data = remaining.iloc[i*chunk_size:(i+1)*chunk_size].copy()
        else:
            # Người cuối nhận phần còn lại (có thể nhiều hơn một chút)
            member_data = remaining.iloc[i*chunk_size:].copy()
        
        splits.append(member_data)
        print(f"  - Thành viên {i+1}: {len(member_data):,} mẫu")
    
    print(f"\n  💡 Mỗi người sẽ gán:")
    print(f"     • {len(iaa_set):,} mẫu IAA (chung cả 3 người)")
    print(f"     • ~{chunk_size:,} mẫu riêng")
    print(f"     • Tổng: ~{len(iaa_set) + chunk_size:,} mẫu/người")
    
    return splits


# ================================
# PHẦN 3: MAIN WORKFLOW
# ================================

def main():
    print("=" * 70)
    print("🎯 CHIA DỮ LIỆU GÁN NHÃN THEO CHIẾN LƯỢC KHOA HỌC")
    print("=" * 70)
    
    # Load dữ liệu
    base_dir = Path(__file__).parent.parent
    input_file = base_dir / "data" / "processed" / "unlabeled_data_for_labeling.csv"
    output_dir = base_dir / "data" / "labeled"
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n📂 Đọc dữ liệu: {input_file}")
    df = pd.read_csv(input_file)
    print(f"  ✓ Đã load: {len(df):,} mẫu")
    
    # Làm sạch
    df = clean_data(df)
    
    # Chọn mẫu theo chiến lược
    final_samples = stratified_sampling(df, n_hate=3000, n_topic=3000, n_random=3000)
    
    # Shuffle để tránh bias khi gán
    final_samples = final_samples.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Tạo IAA set
    iaa_set = create_iaa_set(final_samples, n_overlap=500)
    
    # Chia cho 3 người
    member_splits = split_for_annotators(final_samples, iaa_set, n_members=3)
    
    # ================================
    # XUẤT FILE
    # ================================
    print("\n💾 XUẤT FILE")
    print("=" * 70)
    
    # File IAA (cả 3 người cùng gán)
    iaa_file = output_dir / "IAA_set_500_samples.csv"
    iaa_set.to_csv(iaa_file, index=False, encoding='utf-8-sig')
    print(f"  ✓ IAA Set: {iaa_file}")
    print(f"    → Cả 3 thành viên gán {len(iaa_set)} mẫu này để tính Fleiss' Kappa")
    
    # File cho từng thành viên
    member_names = ['Thien', 'Huy', 'Thuy']
    for i, (member_data, name) in enumerate(zip(member_splits, member_names)):
        # Gộp IAA set + phần riêng
        full_data = pd.concat([iaa_set, member_data])
        full_data = full_data.sample(frac=1, random_state=42+i).reset_index(drop=True)
        
        # Thêm cột để gán nhãn
        full_data['label'] = ''
        full_data['note'] = ''
        full_data['labeler'] = name
        
        # Xuất file
        member_file = output_dir / f"labeling_task_{name}.csv"
        full_data.to_csv(member_file, index=False, encoding='utf-8-sig')
        print(f"  ✓ {name}: {member_file}")
        print(f"    → {len(full_data):,} mẫu ({len(iaa_set)} IAA + {len(member_data)} riêng)")
    
    # File thống kê
    stats_file = output_dir / "sampling_statistics.txt"
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("THỐNG KÊ CHIẾN LƯỢC CHỌN MẪU\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Tổng mẫu: {len(final_samples):,}\n\n")
        f.write("Phân bố theo chiến lược:\n")
        strategy_dist = final_samples['sampling_strategy'].value_counts()
        for strategy, count in strategy_dist.items():
            f.write(f"  - {strategy}: {count:,} ({count/len(final_samples)*100:.1f}%)\n")
        f.write(f"\nIAA Set: {len(iaa_set):,} mẫu\n")
        f.write(f"Mỗi thành viên: ~{len(member_splits[0]):,} mẫu riêng\n")
        f.write(f"\n💡 Hướng dẫn tính Fleiss' Kappa:\n")
        f.write("   Sử dụng thư viện: from statsmodels.stats.inter_rater import fleiss_kappa\n")
        f.write("   Kappa > 0.6 = Tốt | Kappa > 0.8 = Rất tốt\n")
    
    print(f"  ✓ Thống kê: {stats_file}")
    
    print("\n" + "=" * 70)
    print("✅ HOÀN TẤT!")
    print("=" * 70)
    print("\n📋 HƯỚNG DẪN SỬ DỤNG:")
    print("  1️⃣ Cả 3 người gán nhãn file IAA_set_500_samples.csv TRƯỚC")
    print("  2️⃣ Tính Fleiss' Kappa để đo độ đồng thuận")
    print("  3️⃣ Nếu Kappa thấp: Thảo luận conflict cases, thống nhất rule")
    print("  4️⃣ Mỗi người gán phần riêng của mình (labeling_task_*.csv)")
    print("  5️⃣ Đưa chỉ số Kappa vào báo cáo/slide → Giảng viên sẽ rất ấn tượng!")
    print("\n💡 Lưu ý: Các file đã shuffle ngẫu nhiên để tránh bias khi gán nhãn")
    print("=" * 70)


if __name__ == "__main__":
    main()
# m1.to_csv('Task_Member_1.csv', index=False)
# m2.to_csv('Task_Member_2.csv', index=False)
# m3.to_csv('Task_Member_3.csv', index=False)

print("Đã chia xong dữ liệu cho 3 thành viên!")