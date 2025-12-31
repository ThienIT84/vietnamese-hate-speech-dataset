import pandas as pd

df = pd.read_csv(r'c:\Học sâu\Dataset\TOXIC_COMMENT\unlabeled_with_context_phobert.csv')

print("="*80)
print("PHÂN TÍCH CHI TIẾT POST_TITLE COVERAGE")
print("="*80)

# Thống kê tổng
total = len(df)
with_title = df['post_title'].notna().sum()
no_title = df['post_title'].isna().sum()

print(f"\n📊 Tổng quan:")
print(f"  Tổng mẫu: {total:,}")
print(f"  Có title: {with_title:,} ({100*with_title/total:.1f}%)")
print(f"  Không có title: {no_title:,} ({100*no_title/total:.1f}%)")

# Phân biệt Facebook vs YouTube title
# YouTube title thường có keywords đặc trưng
youtube_keywords = ['youtube', 'mv', 'visualizer', 'official', 'awai', 'win', 'body shaming']

def is_youtube_title(title):
    if pd.isna(title):
        return False
    title_lower = str(title).lower()
    return any(keyword in title_lower for keyword in youtube_keywords)

df['is_youtube'] = df['post_title'].apply(is_youtube_title)

youtube_count = df['is_youtube'].sum()
facebook_count = with_title - youtube_count

print(f"\n📌 Phân loại nguồn:")
print(f"  Facebook: {facebook_count:,} ({100*facebook_count/total:.1f}%)")
print(f"  YouTube: {youtube_count:,} ({100*youtube_count/total:.1f}%)")
print(f"  Không rõ: {no_title:,} ({100*no_title/total:.1f}%)")

# Token length stats
print(f"\n📏 Token length:")
print(f"  Mean: {df['token_length'].mean():.1f}")
print(f"  Median: {df['token_length'].median():.1f}")
print(f"  Max: {df['token_length'].max()}")
print(f"  >200 tokens: {(df['token_length'] > 200).sum():,} mẫu")
print(f"  >250 tokens: {(df['token_length'] > 250).sum():,} mẫu")

# Mẫu YouTube
print(f"\n🎬 10 mẫu YouTube đầu tiên:")
youtube_samples = df[df['is_youtube']].head(10)
for i, row in youtube_samples.iterrows():
    print(f"\n{i+1}. Token: {row['token_length']}")
    print(f"   Title: {row['cleaned_title'][:80]}...")
    print(f"   Comment: {row['cleaned_text'][:80]}...")

# Mẫu không có title
print(f"\n❓ 5 mẫu KHÔNG có title:")
no_title_samples = df[df['post_title'].isna()].head(5)
for i, row in no_title_samples.iterrows():
    print(f"\n{i+1}. ID: {row['id']}")
    print(f"   Comment: {row['cleaned_text'][:100]}...")
