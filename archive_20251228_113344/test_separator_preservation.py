import sys
sys.path.insert(0, 'src')

from preprocessing.advanced_text_cleaning import advanced_clean_text

# Test if </s> is preserved
test_cases = [
    "Title here </s> Comment here",
    "Boy phố mới nhú </s> Tệ nạn xã hội",
    "Phân biệt vùng miền </s> Loại này nên cắt lưỡi",
]

print("Testing </s> preservation in advanced_clean_text():\n")

for test in test_cases:
    result = advanced_clean_text(test)
    has_sep = "</s>" in result
    
    print(f"Input:  {test}")
    print(f"Output: {result}")
    print(f"Has </s>: {has_sep}")
    print()
