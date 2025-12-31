"""
Script xem chi tiết những comment đã fix
So sánh trước và sau khi fix
"""

import pandas as pd

print("="*100)
print("🔍 REVIEW FIXED DATA - CHI TIẾT NHỮNG COMMENT ĐÃ FIX")
print("="*100)

# Load data
df_original = pd.read_csv('backup_before_fix_20251229_013655.csv', encoding='utf-8')
df_fixed = pd.read_csv('final_train_data_v2_FIXED_20251229_013656.csv', encoding='utf-8')

print(f"\n📊 Original: {len(df_original)} rows")
print(f"📊 Fixed: {len(df_fixed)} rows")

# Tìm những rows đã bị thay đổi label
changed_rows = []

for idx in range(len(df_original)):
    if idx < len(df_original):
        orig_label = df_original.iloc[idx]['label']
        fixed_label = df_fixed.iloc[idx]['label']
        
        if orig_label != fixed_label:
            changed_rows.append({
                'index': idx,
                'text': df_fixed.iloc[idx]['training_text'],
                'old_label': orig_label,
                'new_label': fixed_label,
                'note': df_fixed.iloc[idx].get('note', ''),
                'text_length': len(str(df_fixed.iloc[idx]['training_text']))
            })

print(f"\n✅ Tìm thấy {len(changed_rows)} rows đã thay đổi label")

# Phân loại theo loại fix
fix_categories = {
    'VCL/VL positive': [],
    'Technical nặng': [],
    'Justice call': [],
    'MV description': [],
    'Other': []
}

for row in changed_rows:
    note = str(row['note']).lower()
    if 'vcl' in note or 'vl' in note:
        fix_categories['VCL/VL positive'].append(row)
    elif 'nặng' in note or 'technical' in note:
        fix_categories['Technical nặng'].append(row)
    elif 'justice' in note or 'law' in note:
        fix_categories['Justice call'].append(row)
    elif 'mv' in note or 'description' in note:
        fix_categories['MV description'].append(row)
    else:
        fix_categories['Other'].append(row)

# In chi tiết từng nhóm
print("\n" + "="*100)
print("📋 CHI TIẾT TỪNG NHÓM FIX")
print("="*100)

for category, rows in fix_categories.items():
    if len(rows) > 0:
        print(f"\n{'='*100}")
        print(f"🔧 {category.upper()}: {len(rows)} rows")
        print(f"{'='*100}")
        
        for i, row in enumerate(rows[:20], 1):  # Hiển thị tối đa 20 rows mỗi nhóm
            print(f"\n[{i}] Index: {row['index']}")
            print(f"    Label: {row['old_label']} → {row['new_label']}")
            print(f"    Note: {row['note']}")
            print(f"    Text ({row['text_length']} chars):")
            
            # Hiển thị text, cắt nếu quá dài
            text = str(row['text'])
            if len(text) > 200:
                print(f"    \"{text[:200]}...\"")
            else:
                print(f"    \"{text}\"")
            print(f"    {'-'*96}")
        
        if len(rows) > 20:
            print(f"\n    ... và {len(rows) - 20} rows khác")

# Thống kê chi tiết
print("\n" + "="*100)
print("📊 THỐNG KÊ CHI TIẾT")
print("="*100)

for category, rows in fix_categories.items():
    if len(rows) > 0:
        print(f"\n{category}:")
        print(f"  Tổng số: {len(rows)}")
        
        # Đếm label changes
        label_changes = {}
        for row in rows:
            change = f"{row['old_label']} → {row['new_label']}"
            label_changes[change] = label_changes.get(change, 0) + 1
        
        print(f"  Label changes:")
        for change, count in sorted(label_changes.items()):
            print(f"    {change}: {count} rows")

# Xuất ra file Excel để review dễ hơn
print("\n" + "="*100)
print("💾 XUẤT FILE REVIEW")
print("="*100)

df_review = pd.DataFrame(changed_rows)
review_file = 'REVIEW_FIXED_DATA_20251229.xlsx'
df_review.to_excel(review_file, index=False, engine='openpyxl')
print(f"✅ Đã xuất file review: {review_file}")
print(f"   Mở file này để xem chi tiết tất cả {len(changed_rows)} rows đã fix")

# Tạo file CSV cho từng nhóm
for category, rows in fix_categories.items():
    if len(rows) > 0:
        df_cat = pd.DataFrame(rows)
        cat_file = f'REVIEW_{category.replace("/", "_").replace(" ", "_")}.csv'
        df_cat.to_csv(cat_file, index=False, encoding='utf-8')
        print(f"✅ {category}: {cat_file}")

print("\n" + "="*100)
print("✅ REVIEW COMPLETE!")
print("="*100)
