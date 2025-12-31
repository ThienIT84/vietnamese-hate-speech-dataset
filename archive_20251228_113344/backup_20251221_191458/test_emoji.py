# -*- coding: utf-8 -*-
from src.preprocessing.advanced_text_cleaning import advanced_clean_text

test_cases = [
    "xấu quá 😢😭",
    "đẹp 😍❤️",
    "stupid vl",
    "t yêu m nhiều lắm",
]

for text in test_cases:
    result = advanced_clean_text(text)
    print(f"Input:  {text}")
    print(f"Output: {result}")
    print(f"Repr:   {repr(result)}")
    print()
