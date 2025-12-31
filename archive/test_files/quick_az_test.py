import sys
sys.path.insert(0, 'src')
from preprocessing.advanced_text_cleaning import advanced_clean_text

tests = [
    'makeup từ a-z',
    'từ A-Z',
    'đ-m game',
    'n-g-u vl',
]

for t in tests:
    print(f'{t:20} -> {advanced_clean_text(t)}')
