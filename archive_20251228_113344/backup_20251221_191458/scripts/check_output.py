import pandas as pd

df = pd.read_csv(r'c:\Học sâu\Dataset\TOXIC_COMMENT\unlabeled_with_context_phobert.csv')

print(f'Tổng: {len(df):,} mẫu')
print(f'Có title: {df["post_title"].notna().sum():,} ({100*df["post_title"].notna().sum()/len(df):.1f}%)')
print(f'Không có title: {df["post_title"].isna().sum():,} ({100*df["post_title"].isna().sum()/len(df):.1f}%)')
print(f'\nToken length stats:')
print(df['token_length'].describe())

print(f'\n5 mẫu có title đầu tiên:')
with_title = df[df['post_title'].notna()].head(5)
for i, row in with_title.iterrows():
    print(f'\n[{i+1}] Token: {row["token_length"]}')
    print(f'Title: {row["cleaned_title"][:80]}...')
    print(f'Comment: {row["cleaned_text"][:80]}...')
    print(f'Input: {row["input_text"][:150]}...')
