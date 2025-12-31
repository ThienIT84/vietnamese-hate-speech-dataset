"""
🎯 DEMO: Cách sử dụng advanced_text_cleaning.py
Chạy file này để xem ví dụ cụ thể
"""

from src.preprocessing.advanced_text_cleaning import advanced_clean_text, replace_person_names
import pandas as pd

print("="*100)
print("🔥 DEMO: ADVANCED TEXT CLEANING")
print("="*100)

# ===== VÍ DỤ 1: Làm sạch 1 câu đơn =====
print("\n📝 VÍ DỤ 1: Làm sạch 1 câu đơn")
print("-"*100)

test_texts = [
    "Mày ngu vl 😡😡😡",
    "Ko hiểu sao thg này lại ngu thế",
    "Bắc kỳ rau muống 🐕🐕",
    "Bạn rất đẹp ❤️❤️❤️",
    "Nguyễn Văn A nói rằng anh Tuấn rất giỏi",
    "Đmmmmm nguuuuu vãi lồnnnn",
]

for text in test_texts:
    cleaned = advanced_clean_text(text)
    print(f"\nGốc:   {text}")
    print(f"Clean: {cleaned}")

# ===== VÍ DỤ 2: Mask tên người =====
print("\n\n📝 VÍ DỤ 2: Mask tên người")
print("-"*100)

name_texts = [
    "Nguyễn Văn A nói rằng Hoàng Sa là của Việt Nam",
    "Anh Tuấn và chị Hoa đi chợ mua hoa tươi",
    "Trần Thị Bích Ngọc gặp anh Minh ở Đà Nẵng",
]

for text in name_texts:
    masked = replace_person_names(text)
    print(f"\nGốc:   {text}")
    print(f"Masked: {masked}")

# ===== VÍ DỤ 3: Xử lý DataFrame =====
print("\n\n📝 VÍ DỤ 3: Xử lý DataFrame (giống như xử lý CSV)")
print("-"*100)

# Tạo DataFrame mẫu
data = {
    'id': [1, 2, 3, 4, 5],
    'text': [
        "Mày ngu vl 😡",
        "Ko biết sao thg này lại toxic thế",
        "Bắc kỳ rau muống",
        "Video hay quá bạn ơi 😍",
        "Nguyễn Văn A nói chuyện với anh Tuấn"
    ],
    'label': [1, 1, 1, 0, 0]
}

df = pd.DataFrame(data)

print("\n📊 DataFrame gốc:")
print(df)

# Áp dụng cleaning
print("\n🔧 Đang làm sạch...")
df['text_cleaned'] = df['text'].apply(lambda x: advanced_clean_text(str(x)))

print("\n✅ DataFrame sau khi clean:")
print(df[['id', 'text', 'text_cleaned', 'label']])

# Lưu ra CSV để demo
output_file = 'demo_cleaned.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n💾 Đã lưu kết quả vào: {output_file}")

# ===== VÍ DỤ 4: So sánh trước/sau =====
print("\n\n📝 VÍ DỤ 4: So sánh chi tiết trước/sau")
print("-"*100)

complex_text = """
Nguyễn Văn A nói: "Mày ngu vãi lồnnnn 😡😡😡, ko hiểu sao thg này 
lại toxic thế. Bắc kỳ rau muống đéo chịu đc 🐕🐕"
"""

print(f"\n📄 Text gốc:")
print(complex_text)

cleaned = advanced_clean_text(complex_text)
print(f"\n✨ Text sau khi clean:")
print(cleaned)

print("\n" + "="*100)
print("🎉 DEMO HOÀN THÀNH!")
print("="*100)
print("\n📖 Xem thêm hướng dẫn chi tiết tại: HUONG_DAN_CLEAN_CSV.md")
print("\n💡 Để làm sạch file CSV của bạn, chạy:")
print("   python clean_csv.py <file.csv> -c <tên_cột> -o <output.csv>")
print("="*100)
