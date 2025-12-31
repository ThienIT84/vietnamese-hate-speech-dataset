"""Test NER with new pipeline"""
import sys
sys.path.insert(0, 'src')

from preprocessing.advanced_text_cleaning import advanced_clean_text

test_cases = [
    "Trần Ngọc chắc e k phải đắp chiếu nữa chị ak mộ xanh cỏ luôn rồi đó 😂",
    "Cay đắng cảnh anh chồng bắt quả tang vợ lén lút ngoại tình. Mặc cho quỳ gối van xin hết lời nhưng chị vợ nhất quyết không về #reels #viral #xuhuong #MultiTV </s> Trần Ngọc chắc e k phải đắp chiếu nữa chị ak mộ xanh cỏ luôn rồi đó 😂",
]

for i, text in enumerate(test_cases, 1):
    print(f"\n{'='*70}")
    print(f"TEST {i}:")
    print(f"{'='*70}")
    print(f"INPUT:\n{text}")
    
    result = advanced_clean_text(text)
    
    print(f"\nOUTPUT:\n{result}")
    
    # Check
    checks = []
    if '<person>' in result:
        checks.append("✅ Has <person> tag")
    else:
        checks.append("❌ Missing <person> tag")
    
    if 'trần ngọc' in result.lower() and '<person>' not in result:
        checks.append("❌ 'Trần Ngọc' not masked!")
    
    if 'đắp chiếu' in result:
        checks.append("✅ 'đắp chiếu' preserved")
    
    if 'xanh cỏ' in result:
        checks.append("✅ 'xanh cỏ' preserved")
    
    if 'chị ạ' in result:
        checks.append("✅ 'chị ak' → 'chị ạ' (correct)")
    elif 'chị ak' in result:
        checks.append("❌ 'chị ak' not normalized")
    
    print(f"\nCHECKS:")
    for check in checks:
        print(f"  {check}")
