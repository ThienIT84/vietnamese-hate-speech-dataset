# 🚀 ViDeBERTa Training - Quick Start

**5 phút để bắt đầu train!**

---

## 📦 Files Cần Upload

```
✅ data/final/final_train_data_v3_SEMANTIC.xlsx  (6,285 samples)
✅ scripts/training/KAGGLE_VIDEBERTA_TRAINING.py  (19 cells)
```

---

## ⚡ 5 Bước Nhanh

### 1️⃣ Upload Dataset (2 phút)
```
Kaggle → Datasets → New Dataset
→ Upload: final_train_data_v3_SEMANTIC.xlsx
→ Name: safesense-videberta-data
→ Create
```

### 2️⃣ Tạo Notebook (1 phút)
```
Kaggle → Code → New Notebook
→ GPU: T4 x2 hoặc P100
→ Internet: ON
→ Add data: safesense-videberta-data
```

### 3️⃣ Copy Script (1 phút)
```
Mở KAGGLE_VIDEBERTA_TRAINING.py
→ Copy tất cả 19 cells vào notebook
```

### 4️⃣ Run Training (20 phút)
```
Run All Cells
→ Chờ ~20 phút
→ Xem F1 score mỗi epoch
```

### 5️⃣ Download Model (1 phút)
```
Output tab → Download videberta_toxic_model/
```

---

## ⚠️ 2 Điều BẮT BUỘC

### Cell 8: Add Special Tokens
```python
special_tokens_dict = {
    'additional_special_tokens': [
        '<sep>', '<emo_pos>', '<emo_neg>', '<person>', '<user>'
    ]
}
tokenizer.add_special_tokens(special_tokens_dict)
```

### Cell 11: Resize Embeddings
```python
model.resize_token_embeddings(len(tokenizer))
```

**⚠️ Không làm 2 bước này = model không hiểu special tokens!**

---

## 📊 Kỳ Vọng

```
Epoch 1: F1 ~0.65-0.70
Epoch 2: F1 ~0.72-0.75
Epoch 3: F1 ~0.75-0.78  ← Best
Epoch 4: F1 ~0.76-0.79
Epoch 5: F1 ~0.76-0.80

Target: F1 > 0.76 (tốt hơn PhoBERT 0.72-0.76)
```

---

## 🎯 Config Quan Trọng

```python
MODEL_NAME = "Fsoft-AIC/videberta-base"  # NOT phobert!
MAX_LENGTH = 512                          # NOT 256!
BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 2e-5
num_workers = 0  # Kaggle requirement
```

---

## 🔍 Kiểm Tra Nhanh

### Data đúng format?
```python
# Cell 5: Check data
print(df['training_text'].iloc[0])
# Phải có: <sep>, <emo_pos>, <person>
# KHÔNG có: </s>, <s>, dấu _
```

### Special tokens đã add?
```python
# Cell 8: Check tokenizer
print(len(tokenizer))  # Phải > 64000
print('<sep>' in tokenizer.get_vocab())  # Phải True
```

### Model đã resize?
```python
# Cell 11: Check embeddings
print(model.get_input_embeddings().weight.shape[0])
# Phải = len(tokenizer)
```

---

## 🚨 Troubleshooting

| Lỗi | Giải pháp |
|-----|-----------|
| Token not in vocabulary | Chạy lại Cell 8 |
| Size mismatch | Chạy lại Cell 11 |
| CUDA out of memory | BATCH_SIZE = 8 |
| F1 < 0.70 | Check data format |

---

## 📁 Output Files

```
videberta_toxic_model/          ← Model đã train
training_history.png            ← Biểu đồ training
confusion_matrix.png            ← Ma trận nhầm lẫn
videberta_errors.xlsx           ← Errors analysis
```

---

## 📚 Docs Đầy Đủ

- **Training guide**: `docs/HUONG_DAN_VIDEBERTA_KAGGLE.md`
- **Dataset info**: `docs/VIDEBERTA_DATASET_READY.md`
- **Full summary**: `VIDEBERTA_TRAINING_SUMMARY.md`

---

## ✅ Checklist

- [ ] Dataset uploaded
- [ ] GPU enabled (T4 x2)
- [ ] Internet ON
- [ ] 19 cells copied
- [ ] Cell 8 run (special tokens)
- [ ] Cell 11 run (resize)
- [ ] Training started

---

**Thời gian**: ~25 phút total  
**Expected F1**: 0.76-0.80  
**Status**: ✅ Ready!

**Chúc may mắn! 🎉**
