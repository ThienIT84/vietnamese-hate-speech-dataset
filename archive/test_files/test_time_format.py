"""
Test xử lý format thời gian (12:30, 14:00...)
"""
import sys
sys.path.insert(0, 'src')

from preprocessing.advanced_text_cleaning import advanced_clean_text

# Test cases
test_cases = [
    "Video lúc 12:30 rất hay",
    "Họp lúc 14:00 nhé",
    "Từ 9:00 đến 17:30",
    "12:19 lói móc nghe đã vcl",
    "0:27 mr. bitch",
    "Thời gian: 15:45",
]

print("=" * 60)
print("🧪 TEST TIME FORMAT PRESERVATION")
print("=" * 60)

for test in test_cases:
    result = advanced_clean_text(test)
    has_colon = ':' in result
    
    print(f"\nInput:  {test}")
    print(f"Output: {result}")
    print(f"Has ':' {has_colon} {'✅' if has_colon else '❌'}")
    
    # Check if time is preserved
    import re
    time_pattern = r'\d+:\d+'
    input_times = re.findall(time_pattern, test)
    output_times = re.findall(time_pattern, result)
    
    if input_times:
        print(f"Times: {input_times} → {output_times}")
        if input_times != output_times:
            print(f"⚠️  TIME LOST!")

print("\n" + "=" * 60)
