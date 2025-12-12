import pandas as pd

# Load files
df_auto = pd.read_csv(r'c:\Học sâu\Dataset\TOXIC_COMMENT\auto_labeled_500_samples.csv')
df_unlabeled = pd.read_csv(r'c:\Học sâu\Dataset\data\processed\unlabeled_data.csv')

print('Auto-labeled samples:', len(df_auto))
print('Unlabeled samples:', len(df_unlabeled))

print('\nAuto-labeled IDs sample:')
print(df_auto['id'].head())

print('\nUnlabeled IDs sample:')
print(df_unlabeled['id'].head())

# Check if IDs match
match_count = df_auto['id'].isin(df_unlabeled['id']).sum()
print(f'\nIDs matching: {match_count} / {len(df_auto)}')

if match_count == len(df_auto):
    print('✅ All IDs are valid!')
else:
    print(f'⚠️ {len(df_auto) - match_count} IDs are NOT in unlabeled_data.csv')
