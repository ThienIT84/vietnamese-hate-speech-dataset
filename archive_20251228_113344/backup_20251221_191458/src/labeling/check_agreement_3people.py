"""
Đánh giá độ tương đồng (Inter-Annotator Agreement) giữa 3 người gán nhãn
Sử dụng Fleiss' Kappa và Cohen's Kappa
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Đọc 3 file
print("📖 Đọc file gán nhãn...")
df_thien = pd.read_csv('labeled/Gán chung-Thiện.csv')
df_kiet = pd.read_excel('labeled/Gán-chung-Kiệt.xlsx')
df_huy = pd.read_csv('labeled/GanChung-Huy.csv')

print(f"   Thiện: {len(df_thien)} mẫu")
print(f"   Kiệt:  {len(df_kiet)} mẫu")
print(f"   Huy:   {len(df_huy)} mẫu")

# Merge theo ID
print("\n🔗 Merge 3 file theo ID...")

merged = df_thien[['id', 'label', 'text_to_label']].merge(
    df_kiet[['id', 'label']], on='id', suffixes=('_thien', '_kiet')
).merge(
    df_huy[['id', 'label']], on='id'
)
merged = merged.rename(columns={'label': 'label_huy'})

print(f"   Số mẫu chung: {len(merged)}")

# Lọc các mẫu đã gán nhãn
merged = merged.dropna(subset=['label_thien', 'label_kiet', 'label_huy'])
for col in ['label_thien', 'label_kiet', 'label_huy']:
    merged = merged[merged[col] != '']
    merged[col] = pd.to_numeric(merged[col], errors='coerce')

merged = merged.dropna()
print(f"   Số mẫu đã gán nhãn cả 3: {len(merged)}")

if len(merged) == 0:
    print("❌ Không có mẫu nào được gán nhãn bởi cả 3!")
    exit()

# Lấy nhãn
t = merged['label_thien'].astype(int).values
k = merged['label_kiet'].astype(int).values
h = merged['label_huy'].astype(int).values

print("\n" + "="*70)
print("📊 KẾT QUẢ ĐÁNH GIÁ ĐỘ TƯƠNG ĐỒNG (3 NGƯỜI)")
print("="*70)

# 1. Cohen's Kappa từng cặp
print("\n🎯 Cohen's Kappa từng cặp:")
kappa_tk = cohen_kappa_score(t, k)
kappa_th = cohen_kappa_score(t, h)
kappa_kh = cohen_kappa_score(k, h)

print(f"   Thiện - Kiệt: {kappa_tk:.4f}")
print(f"   Thiện - Huy:  {kappa_th:.4f}")
print(f"   Kiệt - Huy:   {kappa_kh:.4f}")
print(f"   Trung bình:   {(kappa_tk + kappa_th + kappa_kh) / 3:.4f}")

# 2. Fleiss' Kappa (cho 3+ người)
def fleiss_kappa(data):
    """
    Tính Fleiss' Kappa cho nhiều người gán nhãn
    data: numpy array shape (n_samples, n_categories) - số người chọn mỗi category
    """
    n, k = data.shape
    N = data.sum(axis=1)[0]  # Số người gán nhãn mỗi mẫu
    
    # P_i: tỷ lệ đồng ý cho mỗi mẫu
    P_i = (data.sum(axis=1) ** 2 - N) / (N * (N - 1))
    P_bar = P_i.mean()
    
    # P_e: tỷ lệ đồng ý kỳ vọng
    p_j = data.sum(axis=0) / (n * N)
    P_e = (p_j ** 2).sum()
    
    kappa = (P_bar - P_e) / (1 - P_e) if P_e != 1 else 1
    return kappa

# Tạo matrix cho Fleiss' Kappa
labels_unique = sorted(set(t) | set(k) | set(h))
n_samples = len(merged)
n_categories = len(labels_unique)

fleiss_data = np.zeros((n_samples, n_categories))
for i in range(n_samples):
    for label in [t[i], k[i], h[i]]:
        fleiss_data[i, labels_unique.index(label)] += 1

fk = fleiss_kappa(fleiss_data)
print(f"\n🎯 Fleiss' Kappa (3 người): {fk:.4f}")

if fk >= 0.8:
    print("   → Excellent agreement (Tuyệt vời)")
elif fk >= 0.6:
    print("   → Substantial agreement (Tốt)")
elif fk >= 0.4:
    print("   → Moderate agreement (Trung bình)")
else:
    print("   → Fair/Poor agreement (Khá/Kém)")

# 3. Tỷ lệ đồng ý
agree_all = ((t == k) & (k == h)).sum()
agree_2of3 = ((t == k) | (k == h) | (t == h)).sum()

print(f"\n📈 Tỷ lệ đồng ý:")
print(f"   Cả 3 đồng ý:    {agree_all}/{len(t)} = {agree_all/len(t)*100:.1f}%")
print(f"   Ít nhất 2/3:    {agree_2of3}/{len(t)} = {agree_2of3/len(t)*100:.1f}%")

# 4. Phân bố nhãn
print(f"\n📋 Phân bố nhãn:")
print(f"   Thiện: {dict(pd.Series(t).value_counts().sort_index())}")
print(f"   Kiệt:  {dict(pd.Series(k).value_counts().sort_index())}")
print(f"   Huy:   {dict(pd.Series(h).value_counts().sort_index())}")

# 5. Majority Vote
print(f"\n🗳️ MAJORITY VOTE (2/3 đồng ý):")
majority = []
for i in range(len(t)):
    votes = [t[i], k[i], h[i]]
    # Lấy nhãn có nhiều vote nhất
    from collections import Counter
    counter = Counter(votes)
    maj = counter.most_common(1)[0][0]
    majority.append(maj)

majority = np.array(majority)
print(f"   Phân bố: {dict(pd.Series(majority).value_counts().sort_index())}")

# Tính Kappa của majority vs từng người
kappa_maj_t = cohen_kappa_score(majority, t)
kappa_maj_k = cohen_kappa_score(majority, k)
kappa_maj_h = cohen_kappa_score(majority, h)
print(f"\n   Kappa (Majority vs Thiện): {kappa_maj_t:.4f}")
print(f"   Kappa (Majority vs Kiệt):  {kappa_maj_k:.4f}")
print(f"   Kappa (Majority vs Huy):   {kappa_maj_h:.4f}")

# 6. Các mẫu cả 3 bất đồng
print(f"\n❌ Các mẫu CẢ 3 KHÔNG ĐỒNG Ý:")
disagree_all = (t != k) & (k != h) & (t != h)
disagree_df = merged[disagree_all].copy()
disagree_df['label_thien'] = t[disagree_all]
disagree_df['label_kiet'] = k[disagree_all]
disagree_df['label_huy'] = h[disagree_all]

print(f"   Số mẫu: {len(disagree_df)}")
if len(disagree_df) > 0:
    print(f"\n{'Text':<60} | T | K | H")
    print("-"*80)
    for idx, row in disagree_df.head(10).iterrows():
        text = str(row['text_to_label'])[:55]
        print(f"{text:<60} | {int(row['label_thien'])} | {int(row['label_kiet'])} | {int(row['label_huy'])}")

# 7. Xuất file majority vote
output_file = 'labeled/majority_vote_labels.csv'
merged['label_majority'] = majority
merged[['id', 'text_to_label', 'label_thien', 'label_kiet', 'label_huy', 'label_majority']].to_csv(
    output_file, index=False, encoding='utf-8-sig'
)
print(f"\n💾 Đã xuất majority vote ra: {output_file}")

print("\n" + "="*70)
print("🎯 KẾT LUẬN")
print("="*70)
print(f"   Fleiss' Kappa:     {fk:.4f}")
print(f"   Mục tiêu:          ≥ 0.75")
if fk >= 0.75:
    print("   ✅ ĐẠT MỤC TIÊU!")
else:
    print(f"   ⚠️ CHƯA ĐẠT - Có thể dùng Majority Vote ({agree_2of3/len(t)*100:.1f}% có 2/3 đồng ý)")
print("="*70)
