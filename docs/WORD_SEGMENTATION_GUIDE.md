# 🚀 WORD SEGMENTATION CHO PHOBERT - HƯỚNG DẪN NHANH

## 🎯 Tại Sao Cần Word Segmentation?

PhoBERT được train với **VnCoreNLP word segmentation**, nên cần segment text trước khi tokenize để:
- ✅ Model hiểu ngữ nghĩa đúng: "học_sinh" (1 concept) ≠ "học" + "sinh" (2 concepts)
- ✅ Tăng F1 score **2-5%**
- ✅ Đặc biệt quan trọng với slang: "bú_fame", "body_shaming"

## 📊 So Sánh

### ❌ KHÔNG Segment (Cũ):
```
Input: "học sinh giỏi bú fame"
Tokens: ["học", "sinh", "giỏi", "bú", "fame"]
→ Model hiểu sai: 5 từ riêng lẻ
```

### ✅ CÓ Segment (Mới):
```
Input: "học sinh giỏi bú fame"
Segmented: "học_sinh giỏi bú_fame"
Tokens: ["học_sinh", "giỏi", "bú_fame"]
→ Model hiểu đúng: 3 concepts
```

---

## 🔧 Cách Sử Dụng

### Option 1: Segment Data Trước (KHUYẾN NGHỊ cho IT GotTalent)

**Bước 1:** Chạy script segment data
```bash
python apply_word_segmentation.py
```

**Output:** `final_train_data_v3_SEGMENTED.xlsx`

**Bước 2:** Upload file đã segment lên Kaggle và train bình thường

**Ưu điểm:**
- ✅ Segment 1 lần, train nhiều lần (nhanh hơn)
- ✅ Không cần install underthesea trên Kaggle
- ✅ Ổn định hơn

---

### Option 2: Segment Trong Quá Trình Train

**Bước 1:** Dùng `KAGGLE_TRAINING_CELLS.py` (đã có word segmentation)

**Bước 2:** CELL 1 sẽ install underthesea:
```python
!pip install transformers accelerate underthesea -q
```

**Bước 3:** CELL 8 sẽ tự động segment khi load data:
```python
from underthesea import word_tokenize

def segment_text(text):
    return word_tokenize(str(text), format="text")
```

**Ưu điểm:**
- ✅ Linh hoạt, có thể bật/tắt segmentation
- ✅ Không cần pre-process data

**Nhược điểm:**
- ⚠️ Chậm hơn (segment mỗi epoch)
- ⚠️ Cần install underthesea trên Kaggle

---

## 📁 Files Đã Cập Nhật

### 1. `apply_word_segmentation.py`
- Script để segment data trước khi train
- Input: `final_train_data_v3_CLEANED.xlsx`
- Output: `final_train_data_v3_SEGMENTED.xlsx`

### 2. `KAGGLE_TRAINING_CELLS.py`
- Đã thêm word segmentation trong Dataset class
- CELL 1: Install underthesea
- CELL 8: Segment text trước khi tokenize
- CELL 17: Segment text khi inference

### 3. `HUONG_DAN_KAGGLE_TRAINING.md`
- Cập nhật hướng dẫn với word segmentation

---

## 🎯 Khuyến Nghị Cho IT GotTalent

**Dùng Option 1** (segment data trước):
1. Chạy `apply_word_segmentation.py` để tạo `final_train_data_v3_SEGMENTED.xlsx`
2. Upload file segmented lên Kaggle
3. Train với `KAGGLE_TRAINING_CELLS.py` (bỏ qua phần segment trong code)

**Lý do:**
- ⚡ Nhanh hơn (segment 1 lần)
- 🎯 Ổn định hơn cho thi đấu
- 💪 Tập trung vào tuning hyperparameters

---

## 📈 Kỳ Vọng Kết Quả

**Trước (không segment):**
- F1 macro: ~0.68-0.70

**Sau (có segment):**
- F1 macro: ~0.70-0.75 ✅
- **Tăng 2-5%** nhờ model hiểu ngữ nghĩa đúng hơn

---

## 🔍 Kiểm Tra Segmentation

Chạy test nhanh:
```python
from underthesea import word_tokenize

test_cases = [
    "học sinh giỏi",
    "bú fame",
    "body shaming",
    "bọn bắc kỳ",
    "sản phẩm chất vcl"
]

for text in test_cases:
    segmented = word_tokenize(text, format="text")
    print(f"{text:30} → {segmented}")
```

**Expected output:**
```
học sinh giỏi                  → học_sinh giỏi
bú fame                        → bú_fame
body shaming                   → body_shaming
bọn bắc kỳ                     → bọn bắc_kỳ
sản phẩm chất vcl              → sản_phẩm chất vcl
```

---

## ⚠️ Lưu Ý

1. **Underthesea không hoàn hảo**: Một số từ có thể segment sai
2. **Tốc độ**: Segment ~100 texts/giây (6000 texts = ~1 phút)
3. **Memory**: Cần ~500MB RAM cho underthesea model
4. **Kaggle**: Có thể bị timeout nếu dataset quá lớn (>50k rows)

---

## 🚀 Quick Start

```bash
# Segment data
python apply_word_segmentation.py

# Upload lên Kaggle
# → final_train_data_v3_SEGMENTED.xlsx

# Train với KAGGLE_TRAINING_CELLS.py
# → F1 score tăng 2-5%!
```

**Chúc may mắn với IT GotTalent! 🏆**
