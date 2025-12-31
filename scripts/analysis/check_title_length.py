import pandas as pd

df = pd.read_csv('final_train_data_v3_AUGMENTED_20251229_112040.csv')
titles = df['training_text'].str.split('</s>').str[0]
word_counts = titles.str.split().str.len()

print(f'Total rows: {len(df)}')
print(f'Titles > 50 words: {(word_counts > 50).sum()}')
print(f'Max words: {word_counts.max()}')
print(f'Mean words: {word_counts.mean():.1f}')
print(f'\nTop 10 longest titles:')
for idx in word_counts.nlargest(10).index:
    print(f'  [{idx}] {word_counts[idx]} words: {titles[idx][:150]}...')
