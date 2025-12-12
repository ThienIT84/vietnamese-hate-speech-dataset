import pandas as pd

# Load file cần gán nhãn
df = pd.read_csv(r'c:\Học sâu\Dataset\TOXIC_COMMENT\to_label_500_samples.csv')

print(f'Tổng số mẫu: {len(df)}')
print('\nPhân bố theo topic:')
print(df['topic'].value_counts())

# Auto-label dựa trên topic
# Tất cả các mẫu đã lọc theo keywords nhạy cảm → Label 2 (Hate Speech)
df['label'] = 2

# Thêm cột confidence (giả định high confidence vì đã lọc theo keywords)
df['confidence'] = 0.95
df['labeling_method'] = 'auto_by_keyword'

# Đổi tên cột để phù hợp với training_data.csv
df_labeled = df[['id', 'text', 'label', 'topic', 'confidence', 'labeling_method']]

print(f'\n✅ Đã auto-label {len(df_labeled)} mẫu với Label 2 (Hate Speech)')
print('\nPhân bố nhãn:')
print(df_labeled['label'].value_counts())

# Lưu file
df_labeled.to_csv(
    r'c:\Học sâu\Dataset\TOXIC_COMMENT\auto_labeled_500_samples.csv',
    index=False,
    encoding='utf-8-sig'
)

print('\n📁 Saved to: auto_labeled_500_samples.csv')
print('\nCấu trúc file:')
print(df_labeled.head())
print('\n⚠️ LƯU Ý: Hãy mở file để review lại trước khi merge vào training data!')
