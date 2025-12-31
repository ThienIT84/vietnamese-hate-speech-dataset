# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.preprocessing.advanced_text_cleaning import advanced_clean_text

print("=" * 80)
print("🧪 TEST PERSON MASKING - QUY TẮC HỌ + TÊN")
print("=" * 80)

test_cases = [
    # ✅ PHẢI MASKING (Bắt đầu bằng họ)
    ("Parky Có Nghĩa Là Gì ?", "parky → <person>"),
    ("Trần Thị Bích Ngọc đẹp", "trần thị bích ngọc → <person>"),
    ("Thạch Trang xinh", "thạch trang → <person>"),
    ("Lê Minh Trí thông minh", "lê minh trí → <person>"),
    
    # ❌ KHÔNG MASKING (Không bắt đầu bằng họ)
    ("Bộ Mặt Thật của người này", "bộ mặt thật → GIỮ NGUYÊN"),
    ("Nàng Thơ Du Học Sinh Đức", "nàng thơ du học sinh đức → GIỮ NGUYÊN"),
    ("Người Đẹp Nhân Ái 2023", "người đẹp nhân ái → GIỮ NGUYÊN"),
    ("Vẻ Đẹp Vạn Người Mê", "vẻ đẹp vạn người mê → GIỮ NGUYÊN"),
    
    # ✅ MIXED CASES
    ("Nguyễn Văn A và Bộ Mặt Thật", "nguyễn văn a → <person>, bộ mặt thật → GIỮ"),
    ("Thạch Trang tham gia Nàng Thơ", "thạch trang → <person>, nàng thơ → GIỮ"),
]

print(f"\n{'INPUT':<50} | {'EXPECTED BEHAVIOR':<40}")
print("-" * 92)

for input_text, expected_behavior in test_cases:
    output = advanced_clean_text(input_text)
    print(f"{input_text:<50} | {expected_behavior:<40}")
    print(f"  → Output: {output}")
    print()

print("=" * 80)
print("✅ CHECKLIST:")
print("  [?] Tên người (có họ) được masking → <person>")
print("  [?] Cụm từ tiêu đề (không có họ) được GIỮ NGUYÊN")
print("  [?] Độ dài giới hạn 2-4 từ (họ + tên)")
print("=" * 80)
