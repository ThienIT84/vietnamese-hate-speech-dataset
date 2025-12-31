# 📚 HƯỚNG DẪN TRAIN ViDeBERTa TRÊN KAGGLE

**Date**: 2024-12-30  
**Model**: Fsoft-AIC/videberta-base  
**Data**: final_train_data_v3_SEMANTIC.xlsx

---

## 🎯 Mục Tiêu

Train ViDeBERTa cho bài toán phân loại bình luận độc hại tiếng Việt với:
- ✅ RAW TEXT (không cần word segmentation)
- ✅ SEMANTIC TOKENS (<sep>, <emo_pos>, <person>, etc.)
- ✅ Target F1: > 0.76 (cao hơn PhoBERT 0.72-0.76)

---

## ✨ Điểm Khác Biệt vs PhoBERT

| Feature | PhoBERT | ViDeBERTa |
|---------|---------|-----------|
| **Model** | vinai/phobert-base-v2 | Fsoft-AIC/videberta-base |
| **Parameters** | 135M | 86M (36% nhỏ hơn!) |
| **Max Length** | 256 tokens | 512 tokens (2x!) |
| **Input Format** | Segmented (`học_sinh`) | Raw (`học sinh`) |
| **Segmentation** | Required (underthesea) | Not needed ✅ |
| **Special Tokens** | Basic | Semantic (<sep>, etc.) ✅ |
| **Expected F1** | 0.72-0.76 | 0.76-0.80 |

---

## 📦 Files Cần Có

1. **`KAGGLE_VIDEBERTA_TRAINING.py`** - Script training (19 cells)
2. **`final_train_data_v3_SEMANTIC.xlsx`** - Dataset với semantic tokens

---

## 🚀 Các Bước Thực Hiện

### Bước 1: Upload Dataset lên Kaggle

1. Truy cập: https://www.kaggle.com/datasets
2. Click **"+ New Dataset"**
3. Đặt tên: `safesense-videberta-data`
4. Upload file: `final_train_data_v3_SEMANTIC.xlsx`
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
2. Tìm dataset `safesense-videberta-data`
3. Click **"Add"**

### Bước 4: Copy & Run Cells

Mở file `KAGGLE_VIDEBERTA_TRAINING.py` và copy từng CELL vào notebook:

| Cell | Nội dung | Thời gian | Notes |
|------|----------|-----------|-------|
| 1 | Install dependencies | ~2 phút | |
| 2 | Import libraries | ~5 giây | |
| 3 | Configuration | ~1 giây | Max length 512! |
| 4 | Find data file | ~1 giây | |
| 5 | Load & explore data | ~5 giây | Check semantic tokens |
| 6 | Visualize data | ~5 giây | |
| 7 | Prepare data | ~2 giây | |
| 8 | Load tokenizer & add special tokens | ~10 giây | **IMPORTANT!** |
| 9 | Create dataset | ~10 giây | No segmentation! |
| 10 | Create dataloaders | ~2 giây | |
| 11 | Load model & resize embeddings | ~30 giây | **IMPORTANT!** |
| 12 | Training functions | ~1 giây | |
| 13 | **Training loop** | ~15-20 phút | Main training |
| 14 | Plot history | ~5 giây | |
| 15 | Final evaluation | ~30 giây | |
| 16 | Error analysis | ~10 giây | |
| 17 | Save model | ~30 giây | |
| 18 | Test inference | ~5 giây | |
| 19 | Summary | ~1 giây | |

---

## ⚠️ Lưu Ý Quan Trọng

### 1. Special Tokens (CRITICAL!)

**Cell 8**: Add special tokens to tokenizer
```python
special_tokens_dict = {
    'additional_special_tokens': ['<sep>', '<emo_pos>', '<emo_neg>', '<person>', '<user>']
}
tokenizer.add_special_tokens(special_tokens_dict)
```

**Cell 11**: Resize model embeddings
```python
model.resize_token_embeddings(len(tokenizer))
```

⚠️ **BẮT BUỘC**: Nếu không làm 2 bước này, model sẽ không hiểu special tokens!

### 2. Data Format

**Input format**:
```
"học sinh giỏi <sep> <emo_pos> <person> bú fame"
```

**NOT**:
```
"học_sinh giỏi </s> <emo_pos> <person> bú_fame"  ❌
```

### 3. Warnings Có Thể Bỏ Qua

- `libcugraph-cu12` dependency conflicts → **BỎ QUA**
- `Some weights were not initialized` → **BÌNH THƯỜNG** (fine-tuning)
- `Exception ignored in DataLoader` → **BỎ QUA** (không ảnh hưởng)

### 4. Nếu Hết GPU Quota

- Chờ 12 giờ để reset
- Hoặc dùng CPU (chậm hơn ~10x)
- Hoặc giảm batch size: `BATCH_SIZE = 8`

---

## 📊 Kỳ Vọng Kết Quả

| Metric | PhoBERT | ViDeBERTa Target | Expected |
|--------|---------|------------------|----------|
| F1 (macro) | 0.72-0.76 | > 0.76 | 0.76-0.80 |
| Accuracy | 0.75-0.80 | > 0.78 | 0.78-0.83 |
| Errors | 15-20% | < 15% | 12-18% |
| Training time | ~20 min | ~15 min | Faster! |

---

## 📁 Output Files

Sau khi train xong, bạn sẽ có:
- `videberta_toxic_model/` - Model đã train
- `training_history.png` - Biểu đồ training
- `confusion_matrix.png` - Ma trận nhầm lẫn
- `videberta_errors.xlsx` - Các câu model đoán sai

---

## 🎯 Quick Start

```
1. Upload final_train_data_v3_SEMANTIC.xlsx lên Kaggle
2. Tạo notebook mới với GPU
3. Copy từng cell từ KAGGLE_VIDEBERTA_TRAINING.py
4. Chạy và chờ ~20 phút
5. Download model từ Output tab
```

---

## 🔬 So Sánh với PhoBERT

### PhoBERT
```python
# Cần word segmentation
from underthesea import word_tokenize
text = word_tokenize("học sinh giỏi", format="text")
# → "học_sinh giỏi"

# Max length 256
# Expected F1: 0.72-0.76
```

### ViDeBERTa
```python
# KHÔNG cần word segmentation
text = "học sinh giỏi"  # Raw text!

# Max length 512
# Expected F1: 0.76-0.80
```

---

## 🚨 Troubleshooting

### Lỗi: "Token not in vocabulary"
**Nguyên nhân**: Chưa add special tokens  
**Giải pháp**: Chạy lại Cell 8 (add special tokens)

### Lỗi: "Size mismatch for embeddings"
**Nguyên nhân**: Chưa resize embeddings  
**Giải pháp**: Chạy lại Cell 11 (resize embeddings)

### Lỗi: "CUDA out of memory"
**Giải pháp**: Giảm batch size
```python
BATCH_SIZE = 8  # Thay vì 16
```

### F1 Score thấp (<0.70)
**Kiểm tra**:
1. Data có đúng format không? (có `<sep>` không?)
2. Special tokens đã add chưa?
3. Embeddings đã resize chưa?

---

## 💡 Tips để Tăng F1

1. **Data augmentation**: Thêm data nếu có
2. **Hyperparameter tuning**:
   ```python
   LEARNING_RATE = 3e-5  # Thử tăng
   EPOCHS = 7  # Thử tăng
   ```
3. **Ensemble**: Kết hợp PhoBERT + ViDeBERTa
4. **Post-processing**: Xử lý errors patterns

---

## 📚 References

- [ViDeBERTa Paper](https://arxiv.org/abs/2301.10439)
- [ViDeBERTa HuggingFace](https://huggingface.co/Fsoft-AIC/videberta-base)
- [Transformers Special Tokens](https://huggingface.co/docs/transformers/preprocessing#special-tokens)

---

## ✅ Checklist

Trước khi train, đảm bảo:
- [ ] Dataset uploaded lên Kaggle
- [ ] GPU enabled (T4 x2 hoặc P100)
- [ ] Internet ON
- [ ] Data có `<sep>` và special tokens
- [ ] Cell 8: Add special tokens ✅
- [ ] Cell 11: Resize embeddings ✅

---

**Chúc may mắn với IT GotTalent! 🏆**

**Expected result**: F1 0.76-0.80 (tốt hơn PhoBERT 3-5%)

---

**Last Updated**: 2024-12-30  
**Status**: ✅ Ready to train
