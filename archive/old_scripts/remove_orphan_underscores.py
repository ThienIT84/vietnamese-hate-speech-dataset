"""
Xóa các underscore thừa gần special tokens
Pattern: "</s> _word" → "</s> word"
"""

import pandas as pd
import re
from datetime import datetime

print("="*80)
print("🔧 REMOVING ORPHAN UNDERSCORES NEAR SPECIAL TOKENS")
print("="*80)

# Load data
df = pd.read_excel("final_train_data_v3_SEGMENTED_FINAL.xlsx")
print(f"\n📊 Dataset: {len(df)} rows")

# Backup
backup_file = f"backup_before_underscore_removal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(backup_file, index=False)
print(f"💾 Backup saved: {backup_file}")

def remove_orphan_underscores(text):
    """Remove orphan underscores near special tokens"""
    if pd.isna(text) or text == '':
        return text
    
    text = str(text)
    
    # Pattern 1: </s> _word → </s> word
    text = re.sub(r'</s>\s+_(\w+)', r'</s> \1', text)
    
    # Pattern 2: word_ </s> → word </s>
    text = re.sub(r'(\w+)_\s+</s>', r'\1 </s>', text)
    
    # Pattern 3: <token> _word → <token> word
    text = re.sub(r'<(\w+)>\s+_(\w+)', r'<\1> \2', text)
    
    # Pattern 4: word_ <token> → word <token>
    text = re.sub(r'(\w+)_\s+<(\w+)>', r'\1 <\2>', text)
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

print(f"\n🔧 Removing orphan underscores...")

# Apply fix
df['training_text'] = df['training_text'].apply(remove_orphan_underscores)

# Show examples
print(f"\n📊 EXAMPLES AFTER FIX:")
print("="*80)

for i in range(min(5, len(df))):
    text = df.iloc[i]['training_text']
    if any(token in str(text) for token in ['</s>', '<person>', '<emo_pos>']):
        print(f"\n{i+1}. {str(text)[:150]}...")

# Verify no issues remain
print(f"\n🔍 VERIFYING...")

issues_count = 0
patterns = [
    (r'</s>\s+_\w+', '</s> _word'),
    (r'\w+_\s+</s>', 'word_ </s>'),
    (r'<\w+>\s+_\w+', '<token> _word'),
    (r'\w+_\s+<\w+>', 'word_ <token>'),
]

for pattern, name in patterns:
    count = df['training_text'].fillna('').astype(str).str.count(pattern).sum()
    if count > 0:
        print(f"   ❌ {name}: {count} remaining")
        issues_count += count
    else:
        print(f"   ✅ {name}: 0 issues")

if issues_count == 0:
    print(f"\n✅ ALL ORPHAN UNDERSCORES REMOVED!")
else:
    print(f"\n⚠️ {issues_count} issues remaining")

# Save
output_file = "final_train_data_v3_READY.xlsx"
df.to_excel(output_file, index=False)
print(f"\n💾 Saved: {output_file}")

csv_file = "final_train_data_v3_READY.csv"
df.to_csv(csv_file, index=False)
print(f"💾 Saved: {csv_file}")

# Statistics
total_underscores = df['training_text'].fillna('').astype(str).str.count('_').sum()

print("\n" + "="*80)
print("✅ CLEANUP COMPLETE!")
print("="*80)
print(f"\n📊 STATISTICS:")
print(f"   Total compound words: {total_underscores}")
print(f"   Orphan underscores removed: {issues_count == 0}")
print(f"\n📁 OUTPUT FILES:")
print(f"   1. {backup_file} (backup)")
print(f"   2. {output_file} (READY for training)")
print(f"   3. {csv_file} (READY CSV)")
print(f"\n🎯 Use {output_file} for training on Kaggle!")
