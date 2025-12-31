"""
Kiểm tra xem có special tokens bị nối với từ khác không
"""

import pandas as pd
import re

print("="*80)
print("🔍 CHECKING TOKEN CONCATENATION ISSUES")
print("="*80)

# Load segmented data
df = pd.read_excel("final_train_data_v3_SEGMENTED_FINAL.xlsx")

print(f"\n📊 Dataset: {len(df)} rows")

# Patterns to check
PROBLEMATIC_PATTERNS = [
    r'</s>_\w+',      # </s>_word
    r'<person>_\w+',  # <person>_word
    r'<user>_\w+',    # <user>_word
    r'<emo_pos>_\w+', # <emo_pos>_word
    r'<emo_neg>_\w+', # <emo_neg>_word
    r'\w+_</s>',      # word_</s>
    r'\w+_<person>',  # word_<person>
    r'\w+_<user>',    # word_<user>
]

print(f"\n🔍 SEARCHING FOR PROBLEMATIC PATTERNS...")
print("="*80)

issues_found = []

for idx, row in df.iterrows():
    text = str(row['training_text'])
    
    for pattern in PROBLEMATIC_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            issues_found.append({
                'row': idx,
                'pattern': pattern,
                'matches': matches,
                'text': text[:150]
            })

if issues_found:
    print(f"\n⚠️ FOUND {len(issues_found)} ISSUES!")
    print("\n📋 EXAMPLES:")
    
    for i, issue in enumerate(issues_found[:10]):
        print(f"\n{i+1}. Row {issue['row']}:")
        print(f"   Pattern: {issue['pattern']}")
        print(f"   Matches: {issue['matches']}")
        print(f"   Text: {issue['text']}...")
else:
    print(f"\n✅ NO ISSUES FOUND!")

# Count specific issues
print(f"\n📊 ISSUE BREAKDOWN:")
for pattern in PROBLEMATIC_PATTERNS:
    count = sum(1 for issue in issues_found if issue['pattern'] == pattern)
    if count > 0:
        print(f"   {pattern}: {count} occurrences")

print("\n" + "="*80)
