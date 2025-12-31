"""
Quick revert: Đổi explicit → abbrev cho Label 0
Chỉ chạy 1 lần để fix 60 dòng
"""
import pandas as pd
from datetime import datetime
import shutil
import re

input_file = "FINAL_TRAINING_DATASET_TEENCODE_20251225_151716.xlsx"

# Backup
backup = f"backup_before_revert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
shutil.copy(input_file, backup)
print(f"✓ Backup: {backup}")

# Load
df = pd.read_excel(input_file)

# Revert map
revert_map = {
    'vãi lồn': 'vcl',
    'vãi cái lồn': 'vcl',
    'địt mẹ': 'đm',
    'địt con mẹ': 'đcm',
    'cái lồn mẹ': 'clm',
    'đụ má': 'duma',
    'con mẹ nó lồn': 'cmnl',
}

changes = 0
for idx, row in df.iterrows():
    if row['label'] == 0:
        text = row['training_text']
        original = text
        
        for explicit, abbrev in revert_map.items():
            text = re.sub(r'\b' + re.escape(explicit) + r'\b', abbrev, text, flags=re.IGNORECASE)
        
        if text != original:
            df.loc[idx, 'training_text'] = text
            changes += 1

print(f"✓ Reverted {changes} dòng")

# Save
output = f"FINAL_TRAINING_REVERTED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(output, index=False)
print(f"✓ Saved: {output}")
print("\n✅ DONE! Bây giờ dataset nhất quán với Intensity Preservation strategy")
