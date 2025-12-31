import sys
sys.path.insert(0, 'src')
from preprocessing.advanced_text_cleaning import advanced_clean_text

print("="*70)
print("TEST FINAL UPDATES")
print("="*70)

tests = [
    ('bh tôi đi học', 'Test bh → bây giờ'),
    ('t yêu em', 'Test t → tôi'),
    ('vs t thì ok', 'Test t → tôi'),
    ('óc c gì vậy', 'Test óc c preserved'),
    ('makeup từ a-z', 'Test a-z still works'),
]

print("\nRESULTS:")
for text, desc in tests:
    result = advanced_clean_text(text)
    print(f'\n{desc}')
    print(f'  Input:  {text}')
    print(f'  Output: {result}')

print("\n" + "="*70)
