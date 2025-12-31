import pandas as pd

old = pd.read_csv('output.csv')
new = pd.read_csv('output_v2.csv')

print('='*80)
print('COMPARISON: OLD (from input_text) vs NEW (from raw_comment + raw_title)')
print('='*80)

for i in range(5):
    print(f'\n[Row {i+1}]')
    print(f'OLD: {old["input_text"].iloc[i][:120]}...')
    print(f'NEW: {new["input_text"].iloc[i][:120]}...')
    
    # Check if different
    if old["input_text"].iloc[i] != new["input_text"].iloc[i]:
        print('    ⚠️ DIFFERENT!')
    else:
        print('    ✅ Same')

print('\n' + '='*80)
print('STATISTICS')
print('='*80)
print(f'Total rows: {len(new):,}')
print(f'Different rows: {(old["input_text"] != new["input_text"]).sum():,}')
print(f'Match rate: {((old["input_text"] == new["input_text"]).sum() / len(new) * 100):.1f}%')

# Check for emoji tags
print(f'\nEmoji tags in NEW:')
print(f'  <emo_neg>: {new["input_text"].str.contains("<emo_neg>", na=False).sum():,}')
print(f'  <emo_pos>: {new["input_text"].str.contains("<emo_pos>", na=False).sum():,}')
print(f'  <eng_insult>: {new["input_text"].str.contains("<eng_insult>", na=False).sum():,}')
print(f'  <intense>: {new["input_text"].str.contains("<intense>", na=False).sum():,}')
