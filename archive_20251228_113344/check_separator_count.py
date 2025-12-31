import pandas as pd

file = "FINAL_TRAINING_SMART_REBUILT_20251228_111413.xlsx"
df = pd.read_excel(file)

has_sep = df['training_text'].str.contains('</s>', na=False).sum()
total = len(df)

print(f"Total rows: {total}")
print(f"Rows with </s>: {has_sep} ({has_sep/total*100:.1f}%)")
print(f"Rows WITHOUT </s>: {total - has_sep} ({(total-has_sep)/total*100:.1f}%)")

print("\n=== Samples WITH </s> ===")
with_sep = df[df['training_text'].str.contains('</s>', na=False)]
for idx, row in with_sep.head(3).iterrows():
    print(f"\n[{idx}] Label {row['label']}:")
    print(f"  {row['training_text'][:120]}")

print("\n=== Samples WITHOUT </s> ===")
no_sep = df[~df['training_text'].str.contains('</s>', na=False)]
if len(no_sep) > 0:
    for idx, row in no_sep.head(3).iterrows():
        print(f"\n[{idx}] Label {row['label']}:")
        print(f"  {row['training_text'][:120]}")
else:
    print("  (Không có dòng nào thiếu </s>!)")
