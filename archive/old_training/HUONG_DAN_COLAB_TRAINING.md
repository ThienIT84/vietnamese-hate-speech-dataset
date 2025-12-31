# 📚 HƯỚNG DẪN TRAIN MODEL TRÊN GOOGLE COLAB

## 🎯 Mục tiêu
- Train PhoBERT-v2 cho bài toán phân loại bình luận độc hại tiếng Việt
- Dataset: `final_train_data_v3_TRUNCATED_20251229.xlsx`
- Target F1: > 0.72

---

## 📦 Files cần chuẩn bị

1. **`COLAB_TRAINING_CELLS.py`** - Script chứa tất cả code
2. **`final_train_data_v3_TRUNCATED_20251229.xlsx`** - Dataset

---

## 🚀 Các bước thực hiện

### Bước 1: Mở Google Colab
1. Truy cập: https://colab.research.google.com
2. Tạo notebook mới: File → New notebook
3. Đổi runtime sang GPU: Runtime → Change runtime type → GPU (T4)

### Bước 2: Copy code vào Colab
1. Mở file `COLAB_TRAINING_CELLS.py`
2. Copy từng CELL (được đánh dấu bằng `# ═══ CELL X: Title ═══`)
3. Paste vào từng cell trong Colab
4. Chạy từng cell theo thứ tự

### Bước 3: Upload dataset
- Khi chạy CELL 4, Colab sẽ yêu cầu upload file
- Chọn file `final_train_data_v3_TRUNCATED_20251229.xlsx`

### Bước 4: Chờ training
- Training mất khoảng 30-60 phút (tùy GPU)
- Theo dõi metrics sau mỗi epoch

### Bước 5: Kiểm tra kết quả
- Xem F1 score, accuracy, confusion matrix
- Download model từ Google Drive

---

## 📋 Danh sách các CELL

| Cell | Nội dung | Thời gian |
|------|----------|-----------|
| 1 | Mount Drive & Install | 1-2 phút |
| 2 | Import Libraries | 10 giây |
| 3 | Configuration | 5 giây |
| 4 | Upload Data | 30 giây |
| 5 | Load & Explore Data | 10 giây |
| 6 | Visualize Distribution | 10 giây |
| 7 | Prepare Data | 10 giây |
| 8 | Load Tokenizer | 30 giây |
| 9 | Create Dataset Class | 5 giây |
| 10 | Create DataLoaders | 5 giây |
| 11 | Calculate Class Weights | 5 giây |
| 12 | Load Model | 1-2 phút |
| 13 | Setup Optimizer | 5 giây |
| 14 | Training Functions | 5 giây |
| 15 | **Training Loop** | **30-60 phút** |
| 16 | Plot History | 10 giây |
| 17 | Final Evaluation | 1 phút |
| 18 | Error Analysis | 30 giây |
| 19 | Save Model | 1 phút |
| 20 | Test Inference | 10 giây |
| 21 | Summary | 5 giây |

---

## ⚙️ Cấu hình có thể điều chỉnh

Trong CELL 3 (Configuration), bạn có thể thay đổi:

```python
class Config:
    MAX_LENGTH = 256        # Tăng lên 384 nếu text dài
    BATCH_SIZE = 16         # Giảm xuống 8 nếu hết RAM
    EPOCHS = 5              # Tăng lên 10 nếu muốn train lâu hơn
    LEARNING_RATE = 2e-5    # Giảm xuống 1e-5 nếu loss không giảm
    PATIENCE = 2            # Tăng lên 3 nếu muốn train lâu hơn
```

---

## 🎯 Kết quả mong đợi

### Metrics tốt:
- F1 (macro): > 0.72
- Accuracy: > 0.80
- Precision: > 0.70
- Recall: > 0.70

### Nếu F1 < 0.72:
1. Tăng EPOCHS lên 10
2. Giảm LEARNING_RATE xuống 1e-5
3. Thử Focal Loss (thay CrossEntropyLoss)
4. Thêm data augmentation

---

## 💾 Output files

Sau khi train xong, bạn sẽ có:

1. **Model** (trong Google Drive):
   - `/content/drive/MyDrive/phobert_toxic_model/`
   - Chứa: pytorch_model.bin, config.json, tokenizer files

2. **Errors** (trong Colab):
   - `/content/model_errors.xlsx`
   - Chứa: các mẫu model dự đoán sai

3. **Plots** (trong Colab):
   - `/content/training_history.png`
   - `/content/confusion_matrix.png`

---

## ❓ Troubleshooting

### Lỗi "CUDA out of memory"
- Giảm BATCH_SIZE xuống 8
- Giảm MAX_LENGTH xuống 128

### Lỗi "File not found"
- Kiểm tra đường dẫn DATA_PATH
- Upload lại file dataset

### F1 không tăng
- Kiểm tra class balance
- Thử focal loss
- Tăng epochs

### Training quá chậm
- Kiểm tra GPU đã được enable chưa
- Runtime → Change runtime type → GPU

---

## 📞 Liên hệ

Nếu gặp vấn đề, kiểm tra:
1. GPU đã được enable
2. File dataset đúng format
3. Đủ RAM (>12GB)
4. Đủ disk space (>5GB)

---

**Good luck! 🚀**
