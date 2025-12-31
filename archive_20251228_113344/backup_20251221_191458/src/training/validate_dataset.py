import pandas as pd

df = pd.read_csv('final_dataset/facebook_master.csv')

print('='*70)
print('KIỂM TRA VẤN ĐỀ DATASET MỚI IMPORT')
print('='*70)

# 1. Duplicates
print(f'\n1️⃣  DUPLICATES CHECK:')
dup_id = df['id'].duplicated().sum()
dup_text = df['text'].duplicated().sum()
dup_norm = df['cleaned_text_norm'].duplicated().sum()
print(f'   • Duplicate IDs: {dup_id}')
print(f'   • Duplicate text: {dup_text}')
print(f'   • Duplicate cleaned_text_norm: {dup_norm}')
if dup_id > 0 or dup_text > 0 or dup_norm > 0:
    print('   ⚠️  CÓ DUPLICATE - CẦN XÓA!')
else:
    print('   ✅ Không có duplicate')

# 2. Missing values
print(f'\n2️⃣  MISSING VALUES:')
null_cols = df.isnull().sum()
null_cols = null_cols[null_cols > 0]
expected_nulls = ['source_url', 'video_id', 'label', 'annotator_id', 'confidence', 'prediction', 'pred_prob_toxic']
unexpected = [c for c in null_cols.index if c not in expected_nulls]
if unexpected:
    print(f'   ⚠️  UNEXPECTED NULL: {unexpected}')
    for col in unexpected:
        print(f'      - {col}: {null_cols[col]} nulls')
else:
    print(f'   ✅ Chỉ có NULL ở các trường dự kiến')

# 3. Data types
print(f'\n3️⃣  DATA TYPES:')
# Parse timestamp từ CSV (luôn là object/string khi load từ CSV)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

wrong_types = []
if df['timestamp'].dtype not in ['datetime64[ns]', 'datetime64[ns, UTC]']:
    wrong_types.append(f'timestamp ({df["timestamp"].dtype})')
if df['has_emoji'].dtype != 'bool':
    wrong_types.append(f'has_emoji ({df["has_emoji"].dtype})')
if df['is_crosscheck'].dtype != 'bool':
    wrong_types.append(f'is_crosscheck ({df["is_crosscheck"].dtype})')
if wrong_types:
    print(f'   ⚠️  WRONG TYPES: {wrong_types}')
else:
    print(f'   ✅ Data types đúng')

# 4. Text length
print(f'\n4️⃣  TEXT QUALITY:')
short = df[df['char_length'] < 10]
very_short = df[df['char_length'] < 5]
print(f'   • Comments < 10 ký tự: {len(short)} ({len(short)/len(df)*100:.1f}%)')
print(f'   • Comments < 5 ký tự: {len(very_short)} ({len(very_short)/len(df)*100:.1f}%)')
if len(very_short) > 0:
    print(f'   ⚠️  Sample quá ngắn:')
    for i, row in very_short.head(3).iterrows():
        print(f'      "{row["text"]}" ({row["char_length"]} chars)')

# 5. Topic distribution
print(f'\n5️⃣  TOPIC DISTRIBUTION:')
print(f'   • Topics unique: {df["topic"].nunique()}')
topic_counts = df['topic'].value_counts()
for topic, count in topic_counts.items():
    pct = count/len(df)*100
    print(f'   • {topic}: {count} ({pct:.1f}%)')
other_count = df[df['topic'].str.lower() == 'other'].shape[0]
if other_count > len(df) * 0.5:
    print(f'   ⚠️  Topic "Other" quá cao: {other_count/len(df)*100:.1f}%')

# 6. Teencode normalization check
print(f'\n6️⃣  TEENCODE NORMALIZATION:')
sample_with_teencode = df[df['text'].str.contains(r'\b(ko|lun|bả|j|cj|nta|nha|thiệt)\b', case=False, na=False)].head(3)
if len(sample_with_teencode) > 0:
    for idx, row in sample_with_teencode.iterrows():
        orig = row["text"][:70]
        norm = row["cleaned_text_norm"][:70]
        print(f'   Original: {orig}')
        print(f'   Normalized: {norm}')
        print()
else:
    print('   ℹ️  Không tìm thấy teencode trong sample')

# 7. Toxic rate
print(f'\n7️⃣  TOXIC CONTENT:')
toxic_keywords = df['cleaned_text_norm'].str.contains(
    'vãi|địt|cặc|lồn|đéo|đụ|ngáo|ngu|điên|óc chó|ghen tị', 
    case=False, na=False
)
toxic_count = toxic_keywords.sum()
toxic_pct = toxic_count/len(df)*100
print(f'   • Comments có toxic keywords: {toxic_count}/{len(df)} ({toxic_pct:.1f}%)')
if toxic_pct < 5:
    print(f'   ⚠️  Toxic rate quá thấp! Cần >30% để train tốt')
elif toxic_pct < 15:
    print(f'   ⚠️  Toxic rate thấp. Nên >30%')
elif toxic_pct < 30:
    print(f'   ✅ Toxic rate ổn nhưng có thể tốt hơn')
else:
    print(f'   ✅ Toxic rate tốt!')

# 8. Username hashed
print(f'\n8️⃣  PRIVACY:')
anon_count = df[df['username'] == 'user_anonymous'].shape[0]
hashed_count = df[df['username'].str.startswith('user_', na=False)].shape[0]
print(f'   • Username anonymous: {anon_count}')
print(f'   • Username hashed: {hashed_count - anon_count}')
if anon_count == len(df):
    print(f'   ⚠️  TẤT CẢ username đều anonymous - metadata bị mất?')
elif hashed_count == len(df):
    print(f'   ✅ Username được hash đúng')

# Summary
print('\n' + '='*70)
print('📊 TỔNG KẾT:')
print('='*70)
issues = []
if dup_id > 0 or dup_text > 0 or dup_norm > 0:
    issues.append('Có duplicate')
if unexpected:
    issues.append('Có unexpected NULL values')
if wrong_types:
    issues.append('Data types sai')
if len(very_short) > 10:
    issues.append(f'{len(very_short)} comments quá ngắn')
if toxic_pct < 15:
    issues.append('Toxic rate quá thấp')
if anon_count == len(df):
    issues.append('Tất cả username anonymous')

if issues:
    print('⚠️  CÓ VẤN ĐỀ:')
    for issue in issues:
        print(f'   • {issue}')
else:
    print('✅ DATASET HOÀN HẢO - KHÔNG CÓ VẤN ĐỀ!')

print(f'\n📌 Dataset: {len(df):,} comments từ {df["username"].nunique():,} users')
print('='*70)
