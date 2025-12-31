import sys
sys.path.insert(0, 'src')
from preprocessing.advanced_text_cleaning import advanced_clean_text

tests = [
    ('Trần Ngọc đi học', True),
    ('anh chồng đi làm', False),
    ('chị Lan nói gì', True),
    ('chị vợ nấu cơm', False),
    ('ông cháu đi chơi', False),
]

print('NER TESTS:')
for text, should_mask in tests:
    result = advanced_clean_text(text)
    has_person = '<person>' in result
    status = '✅' if has_person == should_mask else '❌'
    print(f'{status} {text:25} -> {result:35} | Mask: {has_person}')
