"""
Test fix cho lỗi a-z → anhvậy
"""
import sys
sys.path.insert(0, 'src')
from preprocessing.advanced_text_cleaning import advanced_clean_text

print("="*70)
print("TEST FIX: Ambiguous Single Letters (a-z, A-Z, vitamin A...)")
print("="*70)

tests = [
    # Critical bug: a-z
    ('makeup từ a-z', 'makeup từ a-z', 'Giữ nguyên a-z'),
    ('từ A-Z', 'từ a-z', 'Giữ nguyên A-Z (lowercase)'),
    
    # Vitamin, plan
    ('vitamin A', 'vitamin a', 'Giữ nguyên vitamin A'),
    ('plan B', 'plan b', 'Giữ nguyên plan B'),
    
    # Các từ hợp lệ vẫn phải work
    ('tui đi học', 'tôi đi học', 'tui → tôi'),
    ('mk yêu em', 'mình yêu em', 'mk → mình'),
    ('ae đi chơi', 'anh em đi chơi', 'ae → anh em'),
    
    # Check không bị dính chữ
    ('nữa. tao', 'nữa. tao', 'Không dính: nữatao'),
    ('sao mày', 'sao mày', 'Không dính: saomày'),
]

print("\nTEST CASES:")
for input_text, expected, description in tests:
    result = advanced_clean_text(input_text)
    
    # Check if result matches expected
    passed = result == expected
    status = '✅' if passed else '❌'
    
    print(f'\n{status} {description}')
    print(f'  Input:    {input_text}')
    print(f'  Expected: {expected}')
    print(f'  Got:      {result}')
    
    if not passed:
        print(f'  ⚠️  MISMATCH!')

print("\n" + "="*70)
