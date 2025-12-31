"""
Kiểm tra sâu hơn - tìm TẤT CẢ các trường hợp token bị nối
"""

import pandas as pd
import re

print("="*80)
print("🔍 DEEP CHECK FOR TOKEN CONCATENATION")
print("="*80)

# Load data
df = pd.read_excel("final_train_data_v3_READY.xlsx")
print(f"\n📊 Dataset: {len(df)} rows")

# Tìm TẤT CẢ các pattern có underscore liên quan đến special tokens
print(f"\n🔍 SEARCHING FOR ALL UNDERSCORE PATTERNS...")

issues = []

for idx, row in df.iterrows():
    text = str(row['training_text'])
    
    # Tìm tất cả các pattern có underscore gần special tokens
    # Pattern 1: </s> + underscore + word
    if re.search(r'</s>\s*_\w+', text):
        issues.append({
            'row': idx,
            'type': '</s>_word (space before underscore)',
            'text': text[:150]
        })
    
    # Pattern 2: word + underscore + </s>
    if re.search(r'\w+_\s*</s>', text):
        issues.append({
            'row': idx,
            'type': 'word_</s> (space after underscore)',
            'text': text[:150]
        })
    
    # Pattern 3: <token> + underscore + word
    if re.search(r'<\w+>\s*_\w+', text):
        issues.append({
            'row': idx,
            'type': '<token>_word (space before underscore)',
            'text': text[:150]
        })
    
    # Pattern 4: word + underscore + <token>
    if re.search(r'\w+_\s*<\w+>', text):
        issues.append({
            'row': idx,
            'type': 'word_<token> (space after underscore)',
            'text': text[:150]
        })

if issues:
    print(f"\n⚠️ FOUND {len(issues)} ISSUES!")
    print("\n📋 FIRST 20 EXAMPLES:")
    
    for i, issue in enumerate(issues[:20]):
        print(f"\n{i+1}. Row {issue['row']} - {issue['type']}:")
        print(f"   {issue['text']}...")
else:
    print(f"\n✅ NO ISSUES FOUND!")

# Count by type
if issues:
    print(f"\n📊 ISSUE BREAKDOWN:")
    from collections import Counter
    type_counts = Counter([issue['type'] for issue in issues])
    for issue_type, count in type_counts.items():
        print(f"   {issue_type}: {count}")

print("\n" + "="*80)
