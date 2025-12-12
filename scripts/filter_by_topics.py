import pandas as pd
import re

# Load unlabeled data
df = pd.read_csv(r'c:\Học sâu\Dataset\data\processed\unlabeled_data.csv')

# Define keywords cho 6 topics (từ GUIDELINE_GAN_NHAN_V3.md)
keywords = {
    'Region': ['bắc kỳ', 'nam kỳ', '3 que', 'ba que', 'dân miền', 'miền bắc', 'miền nam', 'miền trung', 'hưng yên', 'đồng nai'],
    'Body': ['béo', 'mập', 'heo', 'lợn', 'xấu xí', 'body shaming', 'ngoại hình xấu', 'mặt xấu', 'thân hình'],
    'Gender': ['đĩ', 'chó đẻ', 'bê đê', 'bóng kín', 'lẩu gà', 'gay', 'les', 'lgbt', 'đồng tính', 'con đĩ'],
    'Family': ['mẹ mày', 'ba mày', 'cả lò', 'gia đình mày', 'nhà mày', 'bố mày', 'con mẹ', 'đéo mẹ', 'địt mẹ', 'vô phúc'],
    'Disability': ['thiểu năng', 'khuyết tật', 'tàn tật', 'người khuyết', 'bệnh hoạn', 'não cá vàng'],
    'Violence': ['chết đi', 'giết', 'xiên', 'đánh chết', 'cho chết', 'sống thực vật', 'đập chết', 'bọn này chết', 'mày chết']
}

# Tìm các câu chứa keywords
def contains_keyword(text, keyword_list):
    text_lower = str(text).lower()
    return any(kw.lower() in text_lower for kw in keyword_list)

df['topic'] = None
for topic, kw_list in keywords.items():
    mask = df['text'].apply(lambda x: contains_keyword(x, kw_list))
    df.loc[mask, 'topic'] = topic

# Lọc ra các câu có topic
df_filtered = df[df['topic'].notna()].copy()

print(f'Tìm thấy {len(df_filtered)} câu chứa keywords')
print('\nPhân bố theo topic:')
print(df_filtered['topic'].value_counts())

# Lấy mẫu cân bằng từ mỗi topic (tổng ~500 mẫu)
samples_per_topic = min(100, len(df_filtered) // 6)  # Chia đều cho 6 topics

df_sampled = pd.DataFrame()
for topic in keywords.keys():
    topic_df = df_filtered[df_filtered['topic'] == topic]
    if len(topic_df) > 0:
        n_samples = min(samples_per_topic, len(topic_df))
        df_sampled = pd.concat([df_sampled, topic_df.sample(n=n_samples, random_state=42)])

print(f'\nĐã lấy mẫu: {len(df_sampled)} câu')
print('\nPhân bố mẫu theo topic:')
print(df_sampled['topic'].value_counts())

# Lưu file để gán nhãn thủ công
df_sampled[['id', 'text', 'topic']].to_csv(
    r'c:\Học sâu\Dataset\TOXIC_COMMENT\to_label_500_samples.csv', 
    index=False, 
    encoding='utf-8-sig'
)

# Lưu cả file filtered đầy đủ để tham khảo
df_filtered.to_csv(
    r'c:\Học sâu\Dataset\TOXIC_COMMENT\filtered_by_topics_full.csv', 
    index=False, 
    encoding='utf-8-sig'
)

print('\nSaved files:')
print('- to_label_500_samples.csv (để gán nhãn)')
print('- filtered_by_topics_full.csv (tham khảo)')
