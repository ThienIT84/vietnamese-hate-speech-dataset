"""Debug NER pattern"""
import re

surnames = {'Trần', 'Nguyễn', 'Lê'}
surnames_regex = '|'.join(re.escape(s) for s in surnames)

# Pattern hiện tại
pattern = re.compile(
    rf'\b({surnames_regex})(?:\s+[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]*)'
    r'{1,3}\b',
    re.UNICODE
)

test_texts = [
    "Trần Ngọc chắc em",
    "Nguyễn Văn A đi học",
    "Lê Thị Bích Ngọc",
]

print("Pattern:", pattern.pattern)
print()

for text in test_texts:
    matches = list(pattern.finditer(text))
    print(f"Text: {text}")
    print(f"Matches: {len(matches)}")
    for m in matches:
        print(f"  - '{m.group(0)}' at {m.span()}")
    print()
