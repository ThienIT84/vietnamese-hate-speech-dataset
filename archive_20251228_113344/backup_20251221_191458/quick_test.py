# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.preprocessing.advanced_text_cleaning import replace_person_names

# Test cases
tests = [
    ("Nguyễn Văn A ngu quá", "Should mask: Nguyen Van A"),
    ("Trần Thị Bích Ngọc đẹp", "Should mask: Tran Thi Bich Ngoc"),
    ("Thạch Trang xinh", "Should mask: Thach Trang"),
    ("Bộ Mặt Thật của người này", "Should NOT mask: Bo Mat That"),
    ("Nàng Thơ Du Học Sinh Đức", "Should NOT mask: Nang Tho..."),
]

print("Test Person Masking:")
print("-" * 60)
for input_text, note in tests:
    output = replace_person_names(input_text)
    has_person = "<person>" in output.lower()
    status = "MASKED" if has_person else "KEPT"
    print(f"{status:6} | {input_text:40} | {note}")

print("-" * 60)
print("Done!")
