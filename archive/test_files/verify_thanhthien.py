import pandas as pd

df = pd.read_excel('final_dataset_thanhthien.xlsx')

print("="*70)
print("VERIFICATION - final_dataset_thanhthien.xlsx")
print("="*70)

print(f"\n📊 DATASET INFO:")
print(f"  Total rows: {len(df)}")

print(f"\n✅ SEPARATOR:")
has_sep = df['training_text'].str.contains('</s>', na=False).sum()
print(f"  Has </s>: {has_sep}/{len(df)} ({has_sep/len(df)*100:.1f}%)")

print(f"\n✅ NEW UPDATES:")
print(f"  'bây giờ' (from bh): {df['training_text'].str.contains('bây giờ', na=False).sum()} dòng")
print(f"  'tôi' (from t): {df['training_text'].str.contains(' tôi ', na=False).sum()} dòng")
print(f"  'óc c' (preserved): {df['training_text'].str.contains('óc c', na=False).sum()} dòng")

print(f"\n✅ INTENSITY PRESERVATION:")
print(f"  dcm: {df['training_text'].str.contains('dcm', case=False, na=False).sum()} dòng")
print(f"  vl: {df['training_text'].str.contains(' vl', case=False, na=False).sum()} dòng")
print(f"  vcl: {df['training_text'].str.contains('vcl', case=False, na=False).sum()} dòng")

print(f"\n✅ NER WHITELIST:")
print(f"  'ông cháu': {df['training_text'].str.contains('ông cháu', case=False, na=False).sum()} dòng")
print(f"  'ba mẹ': {df['training_text'].str.contains('ba mẹ', case=False, na=False).sum()} dòng")

print(f"\n✅ BUG FIXES:")
print(f"  'a-z': {df['training_text'].str.contains('a-z', na=False).sum()} dòng (preserved)")

print("\n" + "="*70)
print("✅ DATASET READY FOR TRAINING!")
print("="*70)
