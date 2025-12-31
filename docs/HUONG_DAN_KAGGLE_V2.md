# 📚 HƯỚNG DẪN TRAIN MODEL TRÊN KAGGLE - VERSION 2

## 🎯 Mục tiêu
- Train PhoBERT-v2 cho bài toán phân loại bình luận độc hại tiếng Việt
- **Dataset: `final_train_data_v3_READY.xlsx`** (ĐÃ SEGMENT SẴN!)
- Target F1: > 0.72

---

## ✨ Điểm Mới - Version 2

**QUAN TRỌNG**: File data `final_train_data_v3_READY.xlsx` đã được:
- ✅ Word segmentation với underthesea
- ✅ Xóa orphan underscores
- ✅ Bảo vệ special tokens (<person>, <emo_pos>, </s>...)
- ✅ Làm sạch null, duplicates, long texts

**→ KHÔNG CẦN segment trong quá trình training!**

---

## 📦 Files Cần Có

1. **`KAGGLE_TRAINING_CELLS_V2.py`** - Script training mới
2. **`final_train_data_v3_READY.xlsx`** - Dataset đã segment sẵn

---

## 🚀 Các Bước Thực Hiện

### Bước 1: Upload Dataset lên Kaggle

1. Truy cập: https://www.kaggle.com/datasets
2. Click **"+ New Dataset"**
3. Đặt tên: `safesense-training-data`
4. Upload file: `final_train_data_v3_READY.xlsx`
5. Click **"Create"**

### Bước 2: Tạo Notebook Mới

1. Truy cập: https://www.kaggle.com/code
2. Click **"+ New Notebook"**
3. Settings:
   - **Accelerator**: GPU T4 x2 hoặc P100
   - **Internet**: ON
   - **Persistence**: ON

### Bước 3: Add Dataset

1. Click **"+ Add data"** (bên phải)
2. Tìm dataset `safesense-training-data`
3. Click **"Add"**

### Bước 4: Copy & Run Cells

Mở file `KAGGLE_TRAINING_CELLS_V2.py` và copy từng CELL vào notebook:

| Cell | Nội dung | Thời gian |
|------|----------|-----------|
| 1 | Install dependencies | ~2 phút |
| 2 | Import libraries | ~5 giây |
| 3 | Configuration | ~1 giây |
| 4 | Find data file | ~1 giây |
| 5 | Load & explore data | ~5 giây |
| 6 | Visualize data | ~5 giây |
| 7 | Prepare data | ~2 giây |
| 8 | Create dataset | ~10 giây |
| 9 | Create dataloaders | ~2 giây |
| 10 | Load model | ~30 giây |
| 11 | Training functions | ~1 giây |
| 12 | **Training loop** | ~15-20 phút |
| 13 | Plot history | ~5 giây |
| 14 | Final evaluation | ~30 giây |
| 15 | Error analysis | ~10 giây |
| 16 | Save model | ~30 giây |
| 17 | Test inference | ~5 giây |
| 18 | Summary | ~1 giây |

---

## ⚠️ Lưu Ý Quan Trọng

### 1. Warnings Có Thể Bỏ Qua:
- `libcugraph-cu12` dependency conflicts → **BỎ QUA**
- `Some weights were not initialized` → **BÌNH THƯỜNG** (fine-tuning)
- `Exception ignored in DataLoader` → **BỎ QUA** (không ảnh hưởng)

### 2. Khi Inference Với Text MỚI:
```python
from underthesea import word_tokenize

# Text mới cần segment trước khi predict
new_text = "học sinh giỏi bú fame"
segmented = word_tokenize(new_text, format="text")
# → "học_sinh giỏi bú_fame"

pred, probs = predict(segmented, model, tokenizer, device)
```

### 3. Nếu Hết GPU Quota:
- Chờ 12 giờ để reset
- Hoặc dùng CPU (chậm hơn ~10x)

---

## 📊 Kỳ Vọng Kết Quả

| Metric | Target | Kỳ vọng |
|--------|--------|---------|
| F1 (macro) | > 0.72 | 0.72-0.76 |
| Accuracy | > 0.75 | 0.75-0.80 |
| Errors | < 20% | 15-20% |

---

## 📁 Output Files

Sau khi train xong, bạn sẽ có:
- `phobert_toxic_model/` - Model đã train
- `training_history.png` - Biểu đồ training
- `confusion_matrix.png` - Ma trận nhầm lẫn
- `model_errors.xlsx` - Các câu model đoán sai

---

## 🎯 Quick Start

```
1. Upload final_train_data_v3_READY.xlsx lên Kaggle
2. Tạo notebook mới với GPU
3. Copy từng cell từ KAGGLE_TRAINING_CELLS_V2.py
4. Chạy và chờ ~20 phút
5. Download model từ Output tab
```

**Chúc may mắn với IT GotTalent! 🏆**
