"""
Test tất cả các fix: NER whitelist + spacing
"""
import sys
sys.path.insert(0, 'src')
from preprocessing.advanced_text_cleaning import advanced_clean_text

print("="*70)
print("TEST ALL FIXES - Guideline V7.2 + Spacing")
print("="*70)

# Test 1: NER Whitelist - Compound relations
print("\n1️⃣ TEST NER WHITELIST (Compound Relations):")
tests_ner = [
    ('ông nội đi chợ', False, 'ông nội'),
    ('bà ngoại nấu cơm', False, 'bà ngoại'),
    ('ba mẹ đi làm', False, 'ba mẹ'),
    ('anh em đi chơi', False, 'anh em'),
    ('chú bác đến nhà', False, 'chú bác'),
    ('tụi nó đi đâu', False, 'tụi nó'),
    ('bọn nó làm gì', False, 'bọn nó'),
    ('chủ quán nói gì', False, 'chủ quán'),
    ('khách hàng đến', False, 'khách hàng'),
    ('Trần Ngọc đi học', True, 'Trần Ngọc'),
]

for text, should_mask, target in tests_ner:
    result = advanced_clean_text(text)
    has_person = '<person>' in result
    status = '✅' if has_person == should_mask else '❌'
    print(f'{status} {text:25} -> {result:35} | Target: {target}')

# Test 2: Spacing around tags
print("\n2️⃣ TEST SPACING AROUND TAGS:")
tests_spacing = [
    'Trần Ngọc đi học',
    '@user123 nói gì',
    'Thật tuyệt 😂😂',
    'Buồn quá 😭',
    'nguuuuu vl',
]

for text in tests_spacing:
    result = advanced_clean_text(text)
    
    # Check for spacing issues (tag dính chữ)
    issues = []
    if '<person>' in result:
        # Check if <person> has space around it
        if '<person>đ' in result or 'c<person>' in result:
            issues.append('❌ <person> dính chữ')
        else:
            issues.append('✅ <person> có space')
    
    if '<user>' in result:
        if '<user>n' in result or 'i<user>' in result:
            issues.append('❌ <user> dính chữ')
        else:
            issues.append('✅ <user> có space')
    
    if '<emo_pos>' in result or '<emo_neg>' in result:
        if 't<emo' in result or 'pos>v' in result:
            issues.append('❌ emoji tag dính chữ')
        else:
            issues.append('✅ emoji tag có space')
    
    if '<intense>' in result or '<very_intense>' in result:
        if 'u<intense>' in result or 'intense>v' in result:
            issues.append('❌ intensity tag dính chữ')
        else:
            issues.append('✅ intensity tag có space')
    
    status = '✅' if not any('❌' in i for i in issues) else '❌'
    print(f'{status} {text:25} -> {result:40}')
    if issues:
        for issue in issues:
            print(f'     {issue}')

# Test 3: Intensity Preservation
print("\n3️⃣ TEST INTENSITY PRESERVATION:")
tests_intensity = [
    ('dm game hay vcl', ['dm', 'vcl']),
    ('dcm cách nói', ['dcm']),
    ('vl thật', ['vl']),
]

for text, expected_words in tests_intensity:
    result = advanced_clean_text(text)
    found = [w for w in expected_words if w in result]
    status = '✅' if len(found) == len(expected_words) else '❌'
    print(f'{status} {text:25} -> {result:35} | Found: {found}')

print("\n" + "="*70)
