import pandas as pd

df = pd.read_excel('FINAL_TRAINING_COMPLETE_20251228.xlsx')

print("="*70)
print("FINAL VERIFICATION - FINAL_TRAINING_COMPLETE_20251228.xlsx")
print("="*70)

print(f"\n📊 DATASET INFO:")
print(f"  Total rows: {len(df)}")

print(f"\n✅ SEPARATOR:")
has_sep = df['training_text'].str.contains('</s>', na=False).sum()
print(f"  Has </s>: {has_sep}/{len(df)} ({has_sep/len(df)*100:.1f}%)")

print(f"\n✅ INTENSITY PRESERVATION:")
print(f"  dcm: {df['training_text'].str.contains('dcm', case=False, na=False).sum()} dòng")
print(f"  vl: {df['training_text'].str.contains(' vl', case=False, na=False).sum()} dòng")
print(f"  vcl: {df['training_text'].str.contains('vcl', case=False, na=False).sum()} dòng")

print(f"\n✅ FIX a-z:")
has_az = df['training_text'].str.contains('a-z', na=False).sum()
print(f"  Has 'a-z': {has_az} dòng (should be preserved)")

print(f"\n✅ NER WHITELIST:")
print(f"  'ông cháu': {df['training_text'].str.contains('ông cháu', case=False, na=False).sum()} dòng")
print(f"  'ba mẹ': {df['training_text'].str.contains('ba mẹ', case=False, na=False).sum()} dòng")
print(f"  'anh em': {df['training_text'].str.contains('anh em', case=False, na=False).sum()} dòng")

print(f"\n✅ SAMPLE (first 3 rows with 'dcm' or 'vl'):")
sample = df[df['training_text'].str.contains('dcm|vl', case=False, na=False)].head(3)
for idx, row in sample.iterrows():
    print(f"\n[{idx}] Label: {row['label']}")
    print(f"  {row['training_text'][:100]}...")

print("\n" + "="*70)
