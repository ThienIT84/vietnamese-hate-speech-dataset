import pandas as pd

print("Đang đọc file...")
df = pd.read_csv(r'c:\Học sâu\Dataset\TOXIC_COMMENT\unlabeled_with_context_phobert.csv')

print(f"Tổng: {len(df):,} rows")

# Lưu lại với UTF-8 BOM để Excel đọc đúng
output_path = r'c:\Học sâu\Dataset\TOXIC_COMMENT\unlabeled_with_context_phobert.csv'
print(f"\nĐang lưu file với UTF-8-BOM encoding...")

df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"✓ Đã lưu: {output_path}")
print(f"\nFile này sẽ hiển thị đúng tiếng Việt khi mở bằng Excel!")

# Kiểm tra lại
df_test = pd.read_csv(output_path, encoding='utf-8-sig')
print(f"\n✓ Kiểm tra: {len(df_test):,} rows")
print(f"✓ Sample text: {df_test.iloc[0]['cleaned_text'][:100]}...")
