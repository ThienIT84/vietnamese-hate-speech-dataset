import sys
sys.stdout.reconfigure(encoding='utf-8')

from advanced_text_cleaning import advanced_clean_text

# Test cases from V2.2
test_cases = [
    # Hashtag removal (quotes should also be removed)
    ('boy phố "gãy cánh" ngay trước mặt #giaothong #tainan #xuhuong #lantruyền', 
     'boy phố gãy cánh ngay trước mặt truyền'),
    
    # Surname guardrail - preserve non-name capitalized phrases  
    ("Thạch Trang my20s: Bộ Mặt Thật Của Nàng Thơ", 
     "<person> my20s: bộ mặt thật của nàng thơ"),
    
    # DJ should not be converted (music term) - CORRECTED: Mie is not Vietnamese surname
    ("DJ Mie nghe nhạc", "dj mie nghe nhạc"),
    
    # Vietnamese name should be masked
    ("Nguyễn Văn A đi học", "<person> đi học"),
    
    # Length limit - don't mask 5+ word phrases
    ("Đại Hội Giới Trẻ Việt Nam", "đại hội giới trẻ việt nam"),
]

print("="*100)
print("🔥 V2.2 NEW FEATURES TEST")
print("="*100)
print()

passed = 0
for i, (input_text, expected) in enumerate(test_cases, 1):
    output = advanced_clean_text(input_text)
    
    # Normalize whitespace for comparison
    output_normalized = ' '.join(output.split())
    expected_normalized = ' '.join(expected.split())
    
    status = "✅ PASS" if output_normalized == expected_normalized else "❌ FAIL"
    if output_normalized == expected_normalized:
        passed += 1
    
    print(f"Test {i}: {status}")
    print(f"  Input:    {input_text}")
    print(f"  Expected: {expected_normalized}")
    print(f"  Output:   {output_normalized}")
    if output_normalized != expected_normalized:
        print(f"  ❌ MISMATCH!")
    print()

print("="*100)
print(f"📊 RESULTS: {passed}/{len(test_cases)} tests passed ({passed/len(test_cases)*100:.1f}%)")
print("="*100)
