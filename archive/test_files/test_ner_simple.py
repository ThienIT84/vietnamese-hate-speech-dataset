"""
Test NER masking với guideline mới
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing.advanced_text_cleaning import advanced_clean_text

print("="*70)
print("TEST NER MASKING - Guideline V7.2")
print("="*70)

test_cases = [
    # Should MASK (tên riêng)
    ("Trần Ngọc đi học", "Should mask 'Trần Ngọc'"),
    ("Nguyễn Văn A rất giỏi", "Should mask 'Nguyễn Văn A'"),
    ("anh Tuấn đến rồi", "Should mask 'anh Tuấn'"),
    ("chị Lan nói gì", "Should mask 'chị Lan'"),
    
    # Should NOT MASK (vai trò/quan hệ)
    ("anh chồng đi làm", "Should NOT mask 'anh chồng'"),
    ("chị vợ nấu cơm", "Should NOT mask 'chị vợ'"),
    ("ông cháu đi chơi", "Should NOT mask 'ông cháu'"),
    ("ba mẹ đi du lịch", "Should NOT mask 'ba mẹ'"),
    ("thằng bạn tôi", "Should NOT mask 'thằng bạn'"),
    ("dòng họ Nguyễn", "Should NOT mask 'dòng họ'"),
]

for i, (text, expected) in enumerate(test_cases, 1):
    result = advanced_clean_text(text)
    
    has_person = '<person>' in result
    
    # Determine if test passed
    should_mask = "Should mask" in expected and "NOT" not in expected
    passed = (should_mask and has_person) or (not should_mask and not has_person)
    
    status = "✅ PASS" if passed else "❌ FAIL"
    
    print(f"\n[{i}] {status}")
    print(f"  Input:    {text}")
    print(f"  Output:   {result}")
    print(f"  Expected: {expected}")
    print(f"  Has <person>: {has_person}")

print("\n" + "="*70)
