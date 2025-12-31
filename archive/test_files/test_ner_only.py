"""Test NER only"""
import sys
sys.path.insert(0, 'src')

from preprocessing.advanced_text_cleaning import PersonNameDetector

detector = PersonNameDetector()

test_cases = [
    "Trần Ngọc chắc em không phải đắp chiếu",
    "chị ạ Trần Ngọc mộ xanh cỏ",
    "Nguyễn Văn A đi học",
    "anh chồng bắt quả tang vợ",
]

for text in test_cases:
    result = detector.mask_person_names(text)
    print(f"INPUT:  {text}")
    print(f"OUTPUT: {result}")
    print()
