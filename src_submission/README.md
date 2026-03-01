# Source Code - SafeSense-VI

## Cấu trúc

```
src/
├── preprocessing/           # Tiền xử lý dữ liệu
│   ├── advanced_text_cleaning.py      # Pipeline 18 bước
│   ├── prepare_phobert_training.py    # Chuẩn bị data cho PhoBERT
│   └── apply_word_segmentation.py     # Word segmentation
│
├── training/               # Training scripts
│   ├── KAGGLE_PHOBERT_V5_FINAL.py    # Script chính (80/10/10 split)
│   └── COLAB_PHOBERT_V5_FINAL.py     # Colab version
│
└── utils/                  # Utilities (placeholder)
```

## Preprocessing

### advanced_text_cleaning.py
Pipeline 18 bước xử lý text:
- Unicode normalization
- Teencode normalization (1,000+ variants)
- Smart NER (50+ họ, 63 tỉnh thành)
- Emoji mapping
- Context-aware "m" mapping
- Intensity preservation

### prepare_phobert_training.py
Chuẩn bị data cho PhoBERT:
- Lowercase
- Remove duplicates
- Shuffle
- Save to CSV

### apply_word_segmentation.py
Word segmentation cho PhoBERT:
- Sử dụng pyvi
- Format: "học_sinh giỏi"

## Training

### KAGGLE_PHOBERT_V5_FINAL.py
Script training chính:
- Data split: 80% Train / 10% Val / 10% Test
- Model: PhoBERT-base-v2
- Class weights: [0.7195, 1.3093, 1.1816]
- Early stopping: patience=2
- Output: Model + Results + Visualizations

### COLAB_PHOBERT_V5_FINAL.py
Version cho Google Colab (tương tự Kaggle)

## Usage

### 1. Preprocessing (nếu cần)
```python
# Data đã được preprocess sẵn trong dataset/
# Nếu muốn reproduce:
python src/preprocessing/prepare_phobert_training.py
python src/preprocessing/apply_word_segmentation.py
```

### 2. Training
```bash
# Kaggle: Copy code từ KAGGLE_PHOBERT_V5_FINAL.py vào notebook
# Colab: Copy code từ COLAB_PHOBERT_V5_FINAL.py vào notebook
```

## Dependencies

```bash
pip install -r requirements.txt
```

Xem file `requirements.txt` ở root folder.
