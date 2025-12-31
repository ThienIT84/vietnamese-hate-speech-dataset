# 🔥 SafeSense-VI: Vietnamese Toxic Comment Classification

Hệ thống phân loại bình luận độc hại tiếng Việt sử dụng Deep Learning (PhoBERT/ViDeBERTa).

## 📊 Project Overview

- **Task**: Multi-class classification (Clean / Toxic / Hate)
- **Dataset**: 6,139 labeled Vietnamese comments
- **Models**: PhoBERT-v2, ViDeBERTa (planned)
- **Target**: F1 > 0.72 (Competition: IT GotTalent)

## 🚀 Quick Start

### 1. Training với PhoBERT (Current)

```bash
# Xem hướng dẫn
cat docs/HUONG_DAN_KAGGLE_V2.md

# Training data
data/final/final_train_data_v3_READY.xlsx  # 6,139 samples, pre-segmented

# Training script
scripts/training/KAGGLE_TRAINING_CELLS_V2.py
```

### 2. Chuyển sang ViDeBERTa (Recommended)

ViDeBERTa tốt hơn PhoBERT cho toxic comments:
- ✅ Hiểu social media text tốt hơn
- ✅ Không cần word segmentation
- ✅ Max length 512 (vs 256)
- ✅ Kỳ vọng F1 tăng 3-5%

## 📁 Project Structure

```
project/
├── scripts/
│   ├── preprocessing/       # Data preprocessing scripts
│   ├── training/           # Training scripts (PhoBERT V2)
│   └── analysis/           # Analysis & evaluation
├── data/
│   ├── final/             # Final training data (READY files)
│   └── review/            # Data for manual review
├── docs/                  # Documentation & guides
├── src/                   # Source code (preprocessing modules)
├── archive/               # Old files (can delete)
│   ├── backups/          # Old data versions
│   ├── old_scripts/      # Deprecated scripts
│   ├── test_files/       # Test scripts
│   ├── intermediate_data/# Intermediate processing data
│   └── old_training/     # Old training scripts (V1, Colab)
├── models/               # Saved models
└── configs/              # Configuration files
```

## 📦 Key Files

### Training Data
- `data/final/final_train_data_v3_READY.xlsx` - **MAIN TRAINING DATA** (pre-segmented)
- `data/final/final_train_data_v3_CLEANED.xlsx` - Cleaned version

### Training Scripts
- `scripts/training/KAGGLE_TRAINING_CELLS_V2.py` - PhoBERT training (18 cells)

### Documentation
- `docs/HUONG_DAN_KAGGLE_V2.md` - Kaggle training guide
- `docs/WORD_SEGMENTATION_GUIDE.md` - Word segmentation guide
- `docs/PREPROCESSING_DOCUMENTATION.md` - Preprocessing docs
- `docs/TRAINING_IMPROVEMENT_GUIDE.md` - Tips to improve F1

### Preprocessing
- `scripts/preprocessing/teencode_tool.py` - Teencode normalization
- `scripts/preprocessing/check_and_clean_final_data.py` - Data cleaning
- `scripts/preprocessing/analyze_model_errors.py` - Error analysis

## 🎯 Training Pipeline

1. **Data Preparation** ✅
   - Cleaned, deduplicated, segmented
   - 6,139 samples ready

2. **Training** (Current)
   - Model: PhoBERT-v2
   - Platform: Kaggle (GPU T4 x2)
   - Expected F1: 0.72-0.76

3. **Next Steps**
   - [ ] Switch to ViDeBERTa
   - [ ] Data augmentation
   - [ ] Ensemble models
   - [ ] Hyperparameter tuning

## 📊 Dataset Statistics

```
Total: 6,139 samples
- Label 0 (Clean): ~40%
- Label 1 (Toxic): ~35%
- Label 2 (Hate): ~25%

Features:
- Word segmentation: Applied ✅
- Special tokens: Protected (<person>, <emo_pos>, </s>)
- Teencode: Normalized with intensity preservation
- Max length: 256 tokens (PhoBERT) / 512 (ViDeBERTa)
```

## 🛠️ Setup

```bash
# Install dependencies
pip install -r requirements.txt

# For training
pip install transformers accelerate torch

# For preprocessing
pip install underthesea pandas openpyxl
```

## 📝 Notes

### PhoBERT
- Requires word segmentation (underthesea)
- Max length: 256 tokens
- Model: `vinai/phobert-base-v2`

### ViDeBERTa (Recommended)
- No word segmentation needed
- Max length: 512 tokens
- Model: `Fsoft-AIC/videberta-base`
- Better for social media text

## 🏆 Competition

- **Event**: IT GotTalent
- **Target**: F1 > 0.72 (competitive: > 0.78)
- **Deadline**: TBD

## 📚 References

- [PhoBERT Paper](https://arxiv.org/abs/2003.00744)
- [ViDeBERTa Paper](https://arxiv.org/abs/2301.10439)
- [Underthesea](https://github.com/undertheseanlp/underthesea)

## 🧹 Maintenance

Archive folder chứa 132 files cũ có thể xóa sau khi confirm training ổn định:
```bash
# Xóa archive (optional, sau khi backup)
rm -rf archive/
```

## 📧 Contact

Project for IT GotTalent Competition - Vietnamese Toxic Comment Classification

---

**Last Updated**: 2024-12-30
**Status**: Ready for ViDeBERTa training
