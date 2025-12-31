"""
Fix guideline violations in training data
"""
import pandas as pd
import re

# Load data
df = pd.read_csv('final_train_data_v3_AUGMENTED_20251229_112040.csv')
print(f"✅ Loaded: {len(df)} rows")

# Backup
backup_file = 'backup_before_guideline_fix_20251229.csv'
df.to_csv(backup_file, index=False, encoding='utf-8-sig')
print(f"💾 Backup saved: {backup_file}")

fixes = []

# RULE 1: "vãi lồn" nguyên bản phải là Label 1
print("\n🔧 Fixing Rule 1: 'vãi lồn' nguyên bản phải Label 1...")
pattern1 = r'\b(vãi\s*lồn|địt\s*mẹ)\b'
mask1 = df['text'].str.contains(pattern1, case=False, regex=True, na=False)
violations1 = df[mask1 & (df['label'] == 0)]
print(f"   Found {len(violations1)} violations")
for idx in violations1.index:
    old_label = df.at[idx, 'label']
    df.at[idx, 'label'] = 1
    fixes.append({
        'index': idx,
        'rule': 'RULE 1: vãi lồn/địt mẹ → Label 1',
        'old_label': old_label,
        'new_label': 1,
        'text': df.at[idx, 'text'][:100]
    })

# RULE 2: Phi nhân hóa (súc vật hóa) phải là Label 2
print("\n🔧 Fixing Rule 2: Phi nhân hóa phải Label 2...")
animal_words = r'\b(con\s*(chó|lợn|heo|bò|trâu|khỉ|vượn|dê|cừu|gà|vịt)|thằng\s*chó|con\s*súc\s*vật|bò\s*2\s*chân)\b'
mask2 = df['text'].str.contains(animal_words, case=False, regex=True, na=False)
violations2 = df[mask2 & (df['label'] != 2)]
print(f"   Found {len(violations2)} violations")
for idx in violations2.index:
    old_label = df.at[idx, 'label']
    df.at[idx, 'label'] = 2
    fixes.append({
        'index': idx,
        'rule': 'RULE 2: Phi nhân hóa → Label 2',
        'old_label': old_label,
        'new_label': 2,
        'text': df.at[idx, 'text'][:100]
    })

# RULE 3: Tấn công gia đình phải là Label 2
print("\n🔧 Fixing Rule 3: Tấn công gia đình phải Label 2...")
family_attack = r'\b(chết\s*mẹ|dẹp\s*mẹ|bỏ\s*mẹ|con\s*mẹ|im\s*mẹ|đụ\s*mẹ|địt\s*mẹ|đéo\s*mẹ|phạt.*mẹ|phạt.*ba|phạt.*cha|chết\s*cha|chết\s*ba)\b'
mask3 = df['text'].str.contains(family_attack, case=False, regex=True, na=False)
violations3 = df[mask3 & (df['label'] != 2)]
print(f"   Found {len(violations3)} violations")
for idx in violations3.index:
    old_label = df.at[idx, 'label']
    df.at[idx, 'label'] = 2
    fixes.append({
        'index': idx,
        'rule': 'RULE 3: Tấn công gia đình → Label 2',
        'old_label': old_label,
        'new_label': 2,
        'text': df.at[idx, 'text'][:100]
    })

# RULE 4: Đại từ hạ thấp + đòi phạt phải là Label 1
print("\n🔧 Fixing Rule 4: Đại từ + phạt phải Label 1...")
pronoun_punish = r'\b(mày|mi|tao|tau|thằng|con|đứa|bọn).{0,50}(phạt|tù|giam|bắt|bỏ\s*tù|vào\s*tù|nhốt)\b'
mask4 = df['text'].str.contains(pronoun_punish, case=False, regex=True, na=False)
# Exclude if already Label 2 (family attack takes priority)
violations4 = df[mask4 & (df['label'] == 0)]
print(f"   Found {len(violations4)} violations")
for idx in violations4.index:
    old_label = df.at[idx, 'label']
    df.at[idx, 'label'] = 1
    fixes.append({
        'index': idx,
        'rule': 'RULE 4: Đại từ + phạt → Label 1',
        'old_label': old_label,
        'new_label': 1,
        'text': df.at[idx, 'text'][:100]
    })

# RULE 5: Kêu gọi bạo lực phải là Label 2
print("\n🔧 Fixing Rule 5: Kêu gọi bạo lực phải Label 2...")
violence_call = r'\b(đánh|đập|giết|chém|chết|tát|때리|때려|죽여|살해|폭행|bạo\s*hành|hành\s*hung|tra\s*tấn).{0,30}(nó|mày|mi|thằng|con|đứa|bọn|họ|chúng)\b'
mask5 = df['text'].str.contains(violence_call, case=False, regex=True, na=False)
violations5 = df[mask5 & (df['label'] != 2)]
print(f"   Found {len(violations5)} violations")
for idx in violations5.index:
    old_label = df.at[idx, 'label']
    df.at[idx, 'label'] = 2
    fixes.append({
        'index': idx,
        'rule': 'RULE 5: Kêu gọi bạo lực → Label 2',
        'old_label': old_label,
        'new_label': 2,
        'text': df.at[idx, 'text'][:100]
    })

# Save fixed data
output_file = 'final_train_data_v3_FIXED_20251229.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n💾 Fixed data saved: {output_file}")

# Save fix report
if fixes:
    fixes_df = pd.DataFrame(fixes)
    fixes_df.to_excel('GUIDELINE_FIXES_REPORT.xlsx', index=False)
    print(f"📋 Fix report saved: GUIDELINE_FIXES_REPORT.xlsx")

# Summary
print("\n" + "="*80)
print("📊 FIX SUMMARY")
print("="*80)
print(f"Total fixes: {len(fixes)}")
print(f"\nLabel distribution BEFORE:")
print(pd.read_csv(backup_file)['label'].value_counts().sort_index())
print(f"\nLabel distribution AFTER:")
print(df['label'].value_counts().sort_index())
print("\n✅ DONE!")
