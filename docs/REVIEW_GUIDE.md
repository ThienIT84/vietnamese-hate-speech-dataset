
# 🎯 HƯỚNG DẪN REVIEW VÀ GÁN NHÃN

## Tổng quan
- Tổng số samples auto-labeled: 5835
- Từ unlabeled data: 33814 rows

## Phân loại theo confidence

### HIGH CONFIDENCE (1404 samples)
- MV Description removed: 1375
- Technical "nặng": 29
- **Khuyến nghị**: Có thể thêm trực tiếp vào training data

### MEDIUM CONFIDENCE (4428 samples)
- Justice call: 681
- Neutral comment: 3747
- **Khuyến nghị**: Review nhanh trước khi thêm

### LOW CONFIDENCE (3 samples)
- Sarcasm/light criticism: 3
- **Khuyến nghị**: Review kỹ, có thể cần relabel

## Cách review

1. Mở file `AUTO_LABELED_HIGH_*.csv`
2. Đọc qua 20-30 samples đầu
3. Nếu đúng > 90% → Thêm toàn bộ vào training data
4. Nếu sai > 20% → Review từng sample

5. Lặp lại với MEDIUM và LOW confidence

## Sau khi review

Merge vào training data:
```python
df_train = pd.read_csv('final_train_data_v2.csv')
df_high = pd.read_csv('AUTO_LABELED_HIGH_*.csv')
df_medium = pd.read_csv('AUTO_LABELED_MEDIUM_*.csv')  # Sau khi review

df_merged = pd.concat([df_train, df_high, df_medium], ignore_index=True)
df_merged.to_csv('final_train_data_v3_AUGMENTED.csv', index=False)
```

## Kỳ vọng

- Tăng training data: +5835 samples
- Giảm False Positive (Label 0 → Predicted 1)
- Cải thiện F1: 0.68 → 0.72-0.75
