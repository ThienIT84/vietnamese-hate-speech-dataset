"""
Test teencode tool với sample data
"""
import pandas as pd

# Tạo sample data
sample_data = {
    'training_text': [
        'nguoi ta ko biet gi ca',
        'dm game nay hay vcl',
        'Boy pho moi nhu </s> Te nan xa hoi'
    ],
    'label': [0, 0, 1]
}

df = pd.DataFrame(sample_data)
df.to_excel('test_sample.xlsx', index=False)

print("✓ Đã tạo file test: test_sample.xlsx")
print("\nNội dung:")
print(df)

print("\n" + "="*60)
print("Bây giờ chạy:")
print("  python teencode_tool.py 1 test_sample.xlsx test_output.xlsx")
print("="*60)
