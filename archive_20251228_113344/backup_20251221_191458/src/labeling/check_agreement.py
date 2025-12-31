"""
Đánh giá độ tương đồng (Inter-Annotator Agreement) giữa 2 người gán nhãn
Sử dụng Cohen's Kappa và các metrics khác
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

# Đọc 2 file
print("📖 Đọc file gán nhãn...")
df1 = pd.read_csv('labeled/Gán chung-Thiện.csv')

# File xlsx cần đọc bằng read_excel
df2 = pd.read_excel('labeled/Gán-chung-Kiệt.xlsx')

print(f"   Thiện: {len(df1)} mẫu")
print(f"   Kiệt:  {len(df2)} mẫu")

# Kiểm tra cột
print(f"\n📋 Cột trong file Thiện: {list(df1.columns)}")
print(f"📋 Cột trong file Kiệt:  {list(df2.columns)}")

# Tìm cột label
label_col1 = 'label' if 'label' in df1.columns else None
label_col2 = 'label' if 'label' in df2.columns else None

if not label_col1 or not label_col2:
    print("❌ Không tìm thấy cột 'label' trong file!")
    exit()

# Merge theo ID hoặc text
print("\n🔗 Merge 2 file theo ID...")

# Tìm cột ID
id_col = 'id' if 'id' in df1.columns else df1.columns[0]

# Merge
merged = df1[[id_col, label_col1]].merge(
    df2[[id_col, label_col2]], 
    on=id_col, 
    suffixes=('_thien', '_kiet')
)

print(f"   Số mẫu chung: {len(merged)}")

# Lọc các mẫu đã gán nhãn (không rỗng)
merged = merged.dropna(subset=[f'{label_col1}_thien', f'{label_col1}_kiet'])
merged = merged[merged[f'{label_col1}_thien'] != '']
merged = merged[merged[f'{label_col1}_kiet'] != '']

# Chuyển về số
merged[f'{label_col1}_thien'] = pd.to_numeric(merged[f'{label_col1}_thien'], errors='coerce')
merged[f'{label_col1}_kiet'] = pd.to_numeric(merged[f'{label_col1}_kiet'], errors='coerce')
merged = merged.dropna()

print(f"   Số mẫu đã gán nhãn: {len(merged)}")

if len(merged) == 0:
    print("❌ Không có mẫu nào được gán nhãn!")
    exit()

# Lấy nhãn
labels_thien = merged[f'{label_col1}_thien'].astype(int).values
labels_kiet = merged[f'{label_col1}_kiet'].astype(int).values

print("\n" + "="*70)
print("📊 KẾT QUẢ ĐÁNH GIÁ ĐỘ TƯƠNG ĐỒNG")
print("="*70)

# 1. Cohen's Kappa
kappa = cohen_kappa_score(labels_thien, labels_kiet)
print(f"\n🎯 Cohen's Kappa: {kappa:.4f}")

if kappa >= 0.8:
    print("   → Excellent agreement (Tuyệt vời)")
elif kappa >= 0.6:
    print("   → Substantial agreement (Tốt)")
elif kappa >= 0.4:
    print("   → Moderate agreement (Trung bình)")
elif kappa >= 0.2:
    print("   → Fair agreement (Khá)")
else:
    print("   → Slight/Poor agreement (Kém)")

# 2. Agreement percentage
agree = (labels_thien == labels_kiet).sum()
agree_pct = agree / len(labels_thien) * 100
print(f"\n📈 Tỷ lệ đồng ý: {agree}/{len(labels_thien)} = {agree_pct:.1f}%")

# 3. Confusion Matrix
print(f"\n📊 Confusion Matrix (Thiện vs Kiệt):")
cm = confusion_matrix(labels_thien, labels_kiet)
labels_unique = sorted(set(labels_thien) | set(labels_kiet))
print(f"   Labels: {labels_unique}")
print(cm)

# 4. Chi tiết từng label
print(f"\n📋 Phân bố nhãn:")
print(f"   Thiện: {dict(pd.Series(labels_thien).value_counts().sort_index())}")
print(f"   Kiệt:  {dict(pd.Series(labels_kiet).value_counts().sort_index())}")

# 5. Các mẫu bất đồng
print(f"\n❌ Các mẫu KHÔNG đồng ý ({len(merged) - agree} mẫu):")
disagree_mask = labels_thien != labels_kiet
disagree_df = merged[disagree_mask].copy()
disagree_df['label_thien'] = labels_thien[disagree_mask]
disagree_df['label_kiet'] = labels_kiet[disagree_mask]

# Đọc lại text để hiển thị
df1_text = df1[[id_col, 'text_to_label']].drop_duplicates()
disagree_df = disagree_df.merge(df1_text, on=id_col, how='left')

print(f"\n{'ID':<20} | {'Thiện':^6} | {'Kiệt':^6} | Text")
print("-"*100)
for idx, row in disagree_df.head(20).iterrows():
    text = str(row.get('text_to_label', ''))[:60]
    print(f"{str(row[id_col])[:20]:<20} | {int(row['label_thien']):^6} | {int(row['label_kiet']):^6} | {text}")

if len(disagree_df) > 20:
    print(f"... và {len(disagree_df) - 20} mẫu khác")

# 7. Xuất file các mẫu bất đồng
output_file = 'labeled/disagreement_samples.xlsx'
disagree_export = disagree_df[[id_col, 'text_to_label', 'label_thien', 'label_kiet']].copy()
disagree_export.columns = ['id', 'text_to_label', 'label_Thiện', 'label_Kiệt']
disagree_export['label_final'] = ''  # Cột để điền nhãn cuối cùng sau khi thảo luận
disagree_export['note'] = ''  # Ghi chú

disagree_export.to_excel(output_file, index=False)
print(f"\n💾 Đã xuất {len(disagree_export)} mẫu bất đồng ra: {output_file}")

# 6. Phân tích loại bất đồng
print(f"\n📊 Loại bất đồng:")
for t in labels_unique:
    for k in labels_unique:
        if t != k:
            count = ((labels_thien == t) & (labels_kiet == k)).sum()
            if count > 0:
                print(f"   Thiện={t}, Kiệt={k}: {count} mẫu")

print("\n" + "="*70)
print("🎯 MỤC TIÊU: Cohen's Kappa ≥ 0.75")
if kappa >= 0.75:
    print("✅ ĐẠT MỤC TIÊU!")
else:
    print(f"⚠️ CHƯA ĐẠT! Cần thảo luận lại các mẫu bất đồng.")
print("="*70)
