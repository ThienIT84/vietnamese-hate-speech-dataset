"""
🔍 KIỂM TRA DỮ LIỆU THEO GUIDELINE V7.2
Tìm các câu gán nhãn ngược với guideline

Author: Thanh Thien
Date: 29/12/2025
"""

import pandas as pd
import re

print("="*80)
print("🔍 KIỂM TRA DỮ LIỆU THEO GUIDELINE V7.2")
print("="*80)

# Load data
df = pd.read_csv('final_train_data_v3_AUGMENTED_20251229_112040.csv', encoding='utf-8')
print(f"✅ Loaded: {len(df)} rows")

violations = []

# ============================================================
# RULE 1: "VÃI LỒN" NGUYÊN BẢN PHẢI LÀ LABEL 1
# ============================================================

print("\n🔍 Rule 1: 'vãi lồn' nguyên bản phải là Label 1...")

pattern_vl_full = r'\b(vãi\s*lồn|vãi\s*cả\s*lồn|địt\s*mẹ|địt\s*cụ)\b'

for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    if re.search(pattern_vl_full, text):
        if label == 0:
            violations.append({
                'index': idx,
                'text': row['training_text'][:150],
                'label': label,
                'expected': 1,
                'rule': 'RULE 1: Từ nguyên bản (vãi lồn, địt mẹ) phải Label 1',
                'severity': 'HIGH'
            })

print(f"   Found: {len([v for v in violations if v['rule'].startswith('RULE 1')])} violations")

# ============================================================
# RULE 2: PHI NHÂN HÓA PHẢI LÀ LABEL 2
# ============================================================

print("\n🔍 Rule 2: Phi nhân hóa (súc vật hóa) phải là Label 2...")

dehumanize_patterns = [
    r'\b(béo|gầy|xấu|mặt)\s+(như|giống)\s+(lợn|chó|ngựa|khỉ|bò|heo)\b',
    r'\b(con|đồ|thằng|mụ)\s+(lợn|chó|ngựa|khỉ|bò|heo)\b',
    r'\bóc\s+(c|chó|lợn)\b',
    r'\b(sủa|kêu)\s+(như|giống)\s+(chó|lợn)\b'
]

for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    for pattern in dehumanize_patterns:
        if re.search(pattern, text):
            if label != 2:
                violations.append({
                    'index': idx,
                    'text': row['training_text'][:150],
                    'label': label,
                    'expected': 2,
                    'rule': 'RULE 2: Phi nhân hóa (súc vật hóa) phải Label 2',
                    'severity': 'CRITICAL'
                })
                break

print(f"   Found: {len([v for v in violations if v['rule'].startswith('RULE 2')])} violations")

# ============================================================
# RULE 3: TẤN CÔNG GIA ĐÌNH PHẢI LÀ LABEL 2
# ============================================================

print("\n🔍 Rule 3: Tấn công gia đình phải là Label 2...")

family_attack_patterns = [
    r'\b(ba|mẹ|bố|má|cha|mẹ)\s+(mày|mi|nó|chúng\s*mày)\b',
    r'\b(ba\s*mẹ|bố\s*mẹ)\s+(mày|mi|nó)\s+(dạy|nuôi|sinh)\b',
    r'\bdòng\s+họ\s+(mày|mi|nó)\b'
]

for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    # Loại trừ trường hợp tường thuật
    is_narrative = bool(re.search(r'\b(nó\s+chửi|họ\s+nói|nghe\s+nói|hình\s+như)\b', text))
    
    if not is_narrative:
        for pattern in family_attack_patterns:
            if re.search(pattern, text):
                if label != 2:
                    violations.append({
                        'index': idx,
                        'text': row['training_text'][:150],
                        'label': label,
                        'expected': 2,
                        'rule': 'RULE 3: Tấn công gia đình phải Label 2',
                        'severity': 'CRITICAL'
                    })
                    break

print(f"   Found: {len([v for v in violations if v['rule'].startswith('RULE 3')])} violations")

# ============================================================
# RULE 4: PRONOUN TRIGGER + PHẠT PHẢI LÀ LABEL 1
# ============================================================

print("\n🔍 Rule 4: Đại từ hạ thấp + đòi phạt phải là Label 1...")

pronoun_trigger_patterns = [
    r'\b(thằng|con|mụ|lão|mày|mi)\s+.{0,30}(nên|phải|cho)\s+(đi|vào)\s+tù\b',
    r'\b(thằng|con|mụ|lão|mày|mi)\s+.{0,30}(bắt|phạt|xử)\b'
]

for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    for pattern in pronoun_trigger_patterns:
        if re.search(pattern, text):
            if label == 0:
                violations.append({
                    'index': idx,
                    'text': row['training_text'][:150],
                    'label': label,
                    'expected': 1,
                    'rule': 'RULE 4: Pronoun Trigger + phạt phải Label 1',
                    'severity': 'MEDIUM'
                })
                break

print(f"   Found: {len([v for v in violations if v['rule'].startswith('RULE 4')])} violations")

# ============================================================
# RULE 5: KÊU GỌI BẠO LỰC PHẢI LÀ LABEL 2
# ============================================================

print("\n🔍 Rule 5: Kêu gọi bạo lực phải là Label 2...")

incitement_patterns = [
    r'\b(nên|phải|cho)\s+(chết|giết|xiên|chém|đánh|tử\s*hình)\b',
    r'\b(đáng|xứng)\s+(chết|đời)\b',
    r'\b(ai|mày|nó)\s+(đánh|giết|chém|xiên)\b'
]

for idx, row in df.iterrows():
    text = str(row['training_text']).lower()
    label = row['label']
    
    # Loại trừ tường thuật
    is_narrative = bool(re.search(r'\b(hình\s+như|nghe\s+nói|theo\s+luật|đã\s+bị)\b', text))
    
    if not is_narrative:
        for pattern in incitement_patterns:
            if re.search(pattern, text):
                if label != 2:
                    violations.append({
                        'index': idx,
                        'text': row['training_text'][:150],
                        'label': label,
                        'expected': 2,
                        'rule': 'RULE 5: Kêu gọi bạo lực phải Label 2',
                        'severity': 'CRITICAL'
                    })
                    break

print(f"   Found: {len([v for v in violations if v['rule'].startswith('RULE 5')])} violations")

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "="*80)
print("📊 KẾT QUẢ KIỂM TRA")
print("="*80)

if len(violations) == 0:
    print("\n✅ HOÀN HẢO! Không tìm thấy vi phạm guideline.")
else:
    print(f"\n⚠️ Tìm thấy {len(violations)} vi phạm guideline:")
    
    # Group by severity
    critical = [v for v in violations if v['severity'] == 'CRITICAL']
    high = [v for v in violations if v['severity'] == 'HIGH']
    medium = [v for v in violations if v['severity'] == 'MEDIUM']
    
    print(f"  - CRITICAL: {len(critical)}")
    print(f"  - HIGH: {len(high)}")
    print(f"  - MEDIUM: {len(medium)}")
    
    # Show top 20 violations
    print("\n📋 TOP 20 VI PHẠM:")
    print("-" * 80)
    
    for i, v in enumerate(violations[:20], 1):
        print(f"\n[{i}] Index: {v['index']}")
        print(f"    Label: {v['label']} → Expected: {v['expected']}")
        print(f"    Rule: {v['rule']}")
        print(f"    Severity: {v['severity']}")
        print(f"    Text: {v['text']}...")
    
    if len(violations) > 20:
        print(f"\n... và {len(violations) - 20} vi phạm khác")
    
    # Save violations
    df_violations = pd.DataFrame(violations)
    output_file = "GUIDELINE_VIOLATIONS.xlsx"
    df_violations.to_excel(output_file, index=False, engine='openpyxl')
    print(f"\n💾 Saved violations to: {output_file}")

print("\n" + "="*80)
print("✅ KIỂM TRA HOÀN TẤT!")
print("="*80)
