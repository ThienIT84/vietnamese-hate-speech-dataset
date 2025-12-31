# 📋 HƯỚNG DẪN PHÂN TÍCH LỖI MODEL TRÊN GOOGLE COLAB

## 🎯 Mục đích
Sau khi train model xong, phân tích các mẫu dự đoán sai để tìm hướng cải thiện.

---

## 🚀 CÁCH 1: Copy Script Ngắn Gọn (KHUYẾN NGHỊ)

### Bước 1: Mở file `COLAB_ERROR_ANALYSIS_CELL.py`

### Bước 2: Copy toàn bộ code trong file đó

### Bước 3: Paste vào 1 cell mới trong Colab (sau cell training)

### Bước 4: Chạy lệnh này trong cell tiếp theo:

```python
# Phân tích lỗi
errors_df, summary = analyze_errors(val_texts, val_labels, val_preds)
```

### Bước 5: Xem kết quả

```python
# Xem tóm tắt
print(summary)

# Xem chi tiết lỗi 0→1 (model đoán Clean nhưng thực tế là Toxic)
errors_0_to_1 = errors_df[errors_df['error_type'] == '0→1']
print(f"\nLỗi 0→1: {len(errors_0_to_1)} cases")
print(errors_0_to_1[['title', 'comment']].head(10))

# Xem chi tiết lỗi 1→0 (model đoán Toxic nhưng thực tế là Clean)
errors_1_to_0 = errors_df[errors_df['error_type'] == '1→0']
print(f"\nLỗi 1→0: {len(errors_1_to_0)} cases")
print(errors_1_to_0[['title', 'comment']].head(10))
```

---

## 🚀 CÁCH 2: Dùng Script Training Tích Hợp Sẵn

### Bước 1: Upload file `colab_phobert_v2_with_error_analysis.py` lên Colab

### Bước 2: Chạy file đó thay vì script training cũ

```python
!python colab_phobert_v2_with_error_analysis.py
```

Script này sẽ tự động phân tích lỗi sau khi train xong.

---

## 📊 KẾT QUẢ NHẬN ĐƯỢC

Sau khi chạy, bạn sẽ có các file trong Google Drive:

### 1. `MODEL_ERRORS_ALL.xlsx`
- Tất cả các mẫu dự đoán sai
- Columns: error_type, true_label, pred_label, title, comment, text

### 2. `MODEL_ERRORS_[type].xlsx` 
Các file riêng cho từng loại lỗi:
- `MODEL_ERRORS_0_to_1.xlsx` - Model đoán Clean → Toxic
- `MODEL_ERRORS_0_to_2.xlsx` - Model đoán Clean → Hate
- `MODEL_ERRORS_1_to_0.xlsx` - Model đoán Toxic → Clean
- `MODEL_ERRORS_1_to_2.xlsx` - Model đoán Toxic → Hate
- `MODEL_ERRORS_2_to_0.xlsx` - Model đoán Hate → Clean
- `MODEL_ERRORS_2_to_1.xlsx` - Model đoán Hate → Toxic

### 3. `MODEL_ERRORS_SUMMARY.xlsx`
- Tóm tắt số lượng lỗi theo từng loại
- Top patterns phát hiện được

---

## 🔍 PATTERNS ĐƯỢC PHÁT HIỆN

Script tự động phát hiện các patterns phổ biến:

1. **vcl/vl positive** - "chất vcl", "hay vl", "đẹp vl"
2. **technical nặng** - "nặng khung hình", "mv nặng", "lag"
3. **justice call** - "pháp luật xử lý", "bắt đi tù"
4. **mv description** - Mô tả MV dài
5. **family attack** - "chết mẹ", "đụ mẹ", "địt mẹ"
6. **animal words** - "con chó", "thằng lợn"
7. **violence call** - "đánh nó", "giết nó"

---

## 💡 VÍ DỤ OUTPUT

```
================================================================================
🔍 PHÂN TÍCH LỖI MODEL
================================================================================

📊 Total: 853 | ✅ Correct: 785 (92.0%) | ❌ Errors: 68 (8.0%)

📊 PHÂN LOẠI LỖI:
   0→1: 38 (55.9%)
   1→0: 18 (26.5%)
   1→2: 7 (10.3%)
   0→2: 5 (7.4%)

🔍 PATTERNS:

   0→1 (38 cases):
      • vcl/vl: 14 (37%)
      • nặng: 5 (13%)
      • justice: 8 (21%)

   1→0 (18 cases):
      • vcl/vl: 12 (67%)
      • nặng: 3 (17%)

💾 SAVING TO: /content/drive/MyDrive/
   ✅ MODEL_ERRORS_ALL.xlsx
   ✅ MODEL_ERRORS_0_to_1.xlsx
   ✅ MODEL_ERRORS_1_to_0.xlsx
   ✅ MODEL_ERRORS_1_to_2.xlsx
   ✅ MODEL_ERRORS_0_to_2.xlsx
   ✅ MODEL_ERRORS_SUMMARY.xlsx

📋 SAMPLE ERRORS (first 5):

0→1 | True: 0 → Pred: 1
chất vl, video này hay quá đi </s> peak vcl luôn...

1→0 | True: 1 → Pred: 0
phân biệt vùng miền </s> thằng ngu vcl...

✅ DONE!
```

---

## 🎯 SAU KHI CÓ KẾT QUẢ

1. **Download các file Excel về máy**
2. **Phân tích từng loại lỗi**:
   - Lỗi nào nhiều nhất?
   - Pattern nào chiếm đa số?
   - Có cần fix guideline không?
   - Có cần thêm data không?

3. **Quyết định hướng cải thiện**:
   - Fix guideline labeling
   - Thêm augmented data cho pattern thiếu
   - Điều chỉnh preprocessing
   - Thay đổi model architecture

---

## ⚠️ LƯU Ý

- Script cần có 3 biến từ training: `val_texts`, `val_labels`, `val_preds`
- Nếu không có, cần load model và predict lại:

```python
# Load model
model, tokenizer = load_model("/content/drive/MyDrive/phobert_toxic_model")

# Load data
df = pd.read_excel("/content/final_train_data_v3_TRUNCATED_20251229.xlsx")
texts = df['training_text'].tolist()
labels = df['label'].tolist()

# Predict
preds, probs = predict(texts, model, tokenizer)

# Analyze
errors_df, summary = analyze_errors(texts, labels, preds)
```

---

## 📞 HỖ TRỢ

Nếu gặp lỗi, check:
1. Đã mount Google Drive chưa?
2. Đã có `val_texts`, `val_labels`, `val_preds` chưa?
3. Path lưu file đúng chưa?
