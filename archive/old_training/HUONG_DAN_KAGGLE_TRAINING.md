# 📚 HƯỚNG DẪN TRAIN MODEL TRÊN KAGGLE (WITH WORD SEGMENTATION)

## 🎯 Mục tiêu
- Train PhoBERT-v2 cho bài toán phân loại bình luận độc hại tiếng Việt
- Dataset: `final_train_data_v3_CLEANED.xlsx` (đã làm sạch + segment)
- Target F1: > 0.72
- **MỚI**: Có word segmentation để tăng F1 score 2-5%

---

## ✨ Điểm Mới - Word Segmentation

**QUAN TRỌNG**: Phiên bản này sử dụng **underthesea** để segment text trước khi train:
- "học sinh" → "học_sinh"
- "bú fame" → "bú_fame"  
- "body shaming" → "body_shaming"

PhoBERT được train với word segmentation, nên cần segment để đạt hiệu quả tốt nhất!

---

## 📦 Chuẩn bị

### Files cần có:
1. **`KAGGLE_TRAINING_CELLS.py`** - Script training (đã có word segmentation)
2. **`final_train_data_v3_CLEANED.xlsx`** - Dataset đã làm sạch

---

## 🚀 Các bước thực hiện

### Bước 1: Upload Dataset lên Kaggle

1. Truy cập: https://www.kaggle.com/datasets
2. Click **"+ New Dataset"**
3. Đặt tên: `safesense-training-data`
4. Upload file: `final_train_data_v3_TRUNCATED_20251229.xlsx`
5. Click **"Create"**
6. Chờ upload hoàn tất

### Bước 2: Tạo Notebook mới

1. Truy cập: https://www.kaggle.com/code
2. Click **"+ New Notebook"**
3. Đặt tên: `SafeSense-PhoBERT-Training`

### Bước 3: Cấu hình Notebook

1. Click **Settings** (biểu tượng bánh răng bên phải)
2. **Accelerator**: Chọn **GPU T4 x2** hoặc **P100**
3. **Internet**: Bật **ON** (để download model từ HuggingFace)
4. **Persistence**: Bật **ON** (để lưu output)

### Bước 4: Add Dataset

1. Click **"+ Add data"** (bên phải)
2. Tìm dataset: `safesense-training-data`
3. Click **"Add"**
4. Dataset sẽ xuất hiện ở `/kaggle/input/safesense-training-data/`

### Bước 5: Copy code vào Notebook

1. Mở file `KAGGLE_TRAINING_CELLS.py`
2. Copy từng CELL (đánh dấu `# ═══ CELL X ═══`)
3. Paste vào từng cell trong Kaggle notebook
4. Chạy từng cell theo thứ tự

### Bước 6: Chạy Training

- Click **"Run All"** hoặc chạy từng cell
- Training mất khoảng **20-40 phút** (Kaggle GPU nhanh hơn Colab)

### Bước 7: Download kết quả

1. Sau khi training xong, click tab **"Output"**
2. Download các files:
   - `phobert_toxic_model/` - Model đã train
   - `training_history.png` - Biểu đồ training
   - `confusion_matrix.png` - Ma trận nhầm lẫn
   - `model_errors.csv` - Các mẫu dự đoán sai

---

## 📋 Danh sách CELL

| Cell | Nội dung | Thời gian |
|------|----------|-----------|
| 1 | Install Dependencies | 30 giây |
| 2 | Import Libraries | 5 giây |
| 3 | Configuration | 5 giây |
| 4 | Check Input Data | 5 giây |
| 5 | Load & Explore Data | 10 giây |
| 6 | Visualize Distribution | 10 giây |
| 7 | Prepare Data | 5 giây |
| 8 | Load Tokenizer & Dataset | 1 phút |
| 9 | Create DataLoaders | 5 giây |
| 10 | Load Model & Setup | 1-2 phút |
| 11 | Training Functions | 5 giây |
| 12 | **Training Loop** | **20-40 phút** |
| 13 | Plot History | 10 giây |
| 14 | Final Evaluation | 1 phút |
| 15 | Error Analysis | 30 giây |
| 16 | Save Model | 1 phút |
| 17 | Test Inference | 10 giây |
| 18 | Summary | 5 giây |

---

## ⚙️ Cấu hình có thể điều chỉnh

Trong CELL 3, bạn có thể thay đổi:

```python
class Config:
    MAX_LENGTH = 256        # Tăng lên 384 nếu text dài
    BATCH_SIZE = 16         # Kaggle GPU mạnh, có thể tăng lên 32
    EPOCHS = 5              # Tăng lên 10 nếu cần
    LEARNING_RATE = 2e-5    # Giảm xuống 1e-5 nếu loss không giảm
    PATIENCE = 2            # Tăng lên 3 nếu muốn train lâu hơn
```

---

## 🔧 Kaggle vs Colab - Khác biệt

| Feature | Kaggle | Colab |
|---------|--------|-------|
| GPU | T4 x2 / P100 | T4 |
| RAM | 16GB | 12GB |
| Disk | 20GB | 100GB |
| Session | 12 hours | 12 hours |
| Internet | Cần bật | Mặc định ON |
| Data path | `/kaggle/input/` | Upload trực tiếp |
| Output | `/kaggle/working/` | `/content/` |

---

## 🎯 Kết quả mong đợi

### Metrics tốt:
- F1 (macro): > 0.72
- Accuracy: > 0.80
- Training time: 20-40 phút

### Nếu F1 < 0.72:
1. Tăng EPOCHS lên 10
2. Giảm LEARNING_RATE xuống 1e-5
3. Tăng BATCH_SIZE lên 32 (Kaggle GPU mạnh)

---

## 💾 Output files

Sau khi train xong, trong tab **Output**:

```
/kaggle/working/
├── phobert_toxic_model/
│   ├── pytorch_model.bin
│   ├── config.json
│   ├── tokenizer_config.json
│   ├── vocab.txt
│   ├── training_config.json
│   └── training_history.csv
├── training_history.png
├── confusion_matrix.png
├── data_distribution.png
└── model_errors.csv
```

---

## ❓ Troubleshooting

### Lỗi "No GPU available"
- Settings → Accelerator → GPU T4 x2

### Lỗi "Internet disabled"
- Settings → Internet → ON

### Lỗi "Dataset not found"
- Kiểm tra đã Add dataset chưa
- Kiểm tra tên dataset trong Config.DATA_PATH

### Lỗi "Out of memory"
- Giảm BATCH_SIZE xuống 8
- Giảm MAX_LENGTH xuống 128

### Training quá chậm
- Kiểm tra GPU đã được enable
- Kaggle T4 x2 nhanh hơn Colab T4

---

## 📥 Download Model

Sau khi training xong:

1. Click tab **"Output"** (bên phải)
2. Click **"Download All"** hoặc download từng file
3. Model nằm trong folder `phobert_toxic_model/`

---

## 🔄 Sử dụng Model đã train

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load model
model_path = "path/to/phobert_toxic_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Predict
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=256, truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()
    return ["Clean", "Toxic", "Hate"][pred]

# Test
print(predict("video hay quá"))  # Clean
print(predict("thằng ngu"))      # Toxic
```

---

**Good luck! 🚀**
