# ✅ ViDeBERTa Dataset Ready for Training

**Date**: 2024-12-30  
**Status**: ✅ Production Ready  
**File**: `data/final/final_train_data_v3_SEMANTIC.xlsx`

---

## 📊 Dataset Summary

### Basic Info
```
Samples: 6,285
Columns: training_text, label
Format: Raw Vietnamese text + Semantic tokens
Model: Fsoft-AIC/videberta-base
Max Length: 512 tokens
```

### Label Distribution
```
Label 0 (Clean): 2,795 samples (44.5%)
Label 1 (Toxic): 1,647 samples (26.2%)
Label 2 (Hate):  1,843 samples (29.3%)

Total: 6,285 samples
Balance: Good (no class too dominant)
```

---

## ✅ Data Quality Verification

### Special Tokens (All Preserved)
```
<sep>:     5,862 ✅ (semantic separator)
<emo_pos>: 1,250 ✅ (positive emoji)
<emo_neg>:   246 ✅ (negative emoji)
<person>:  3,270 ✅ (person mention)
<user>:      353 ✅ (user mention)
```

### Removed Tokens (All Clean)
```
</s>: 0 ✅ (BOS/EOS removed)
<s>:  0 ✅ (BOS/EOS removed)
```

### Broken Tokens (None Found)
```
<emo pos>: 0 ✅ (no broken special tokens)
<emo neg>: 0 ✅ (no broken special tokens)
```

---

## 🔧 Changes from PhoBERT Version

### What Changed
1. **Underscores removed**: `học_sinh` → `học sinh`
2. **BOS/EOS removed**: `</s>` → removed completely
3. **Semantic separator added**: `</s>` → `<sep>`
4. **Special tokens preserved**: `<emo_pos>`, `<person>`, etc.
5. **Labels cleaned**: Removed 6 text labels, kept 6,285 numeric labels

### What Stayed the Same
- Label values: 0, 1, 2
- Label meanings: Clean, Toxic, Hate
- Text content: Same toxic/clean examples
- Special token semantics: Same meaning

---

## 📝 Sample Data

### Example 1: Clean (Label 0)
```
boy phố mới nhú hay sao mà mặt ông cháu nào cũng non choẹt vậy ? 
<sep> 
tệ nạn xã hội tương lai đấy có tương lai cố gắng phấn đấu nhé các cháu
```

### Example 2: Hate (Label 2)
```
Phân biệt vùng miền , miệt thị người dân vùng lũ . Tàng Keng Ông Trùm lên tiếng xin lỗi nhưng . QUÁ MUỘN ! 
<sep> 
thang trời đánh
```

### Example 3: Toxic (Label 1)
```
phân biệt vùng miền , miệt thị người dân vùng lũ . tàng keng <person> lên tiếng xin lỗi nhưng . quá muộn ! 
<sep> 
mất dạy hả bây giờ trả giá rồi mới xin lỗi phải không
```

---

## 🚀 Training Setup

### Model Configuration
```python
MODEL_NAME = "Fsoft-AIC/videberta-base"
MAX_LENGTH = 512
BATCH_SIZE = 16
GRADIENT_ACCUMULATION = 2  # Effective batch = 32
EPOCHS = 5
LEARNING_RATE = 2e-5
```

### Special Tokens Setup (CRITICAL!)
```python
# Add special tokens to tokenizer
special_tokens_dict = {
    'additional_special_tokens': [
        '<sep>',      # Semantic separator
        '<emo_pos>',  # Positive emoji
        '<emo_neg>',  # Negative emoji
        '<person>',   # Person mention
        '<user>'      # User mention
    ]
}
tokenizer.add_special_tokens(special_tokens_dict)

# Resize model embeddings (MUST DO!)
model.resize_token_embeddings(len(tokenizer))
```

### Training Script
```
File: scripts/training/KAGGLE_VIDEBERTA_TRAINING.py
Cells: 19 (complete training pipeline)
Platform: Kaggle
GPU: T4 x2 or P100
```

---

## 📈 Expected Performance

### Baseline (PhoBERT)
```
Model: vinai/phobert-base
F1 Score: 0.72-0.76
Max Length: 256 tokens
Data: Segmented text
```

### Target (ViDeBERTa)
```
Model: Fsoft-AIC/videberta-base
F1 Score: 0.76-0.80 (+3-5%)
Max Length: 512 tokens
Data: Raw text + semantic tokens
```

### Why Better?
1. **Longer context**: 512 vs 256 tokens
2. **Better tokenization**: Raw text, no segmentation errors
3. **Semantic understanding**: `<sep>` helps model learn structure
4. **Diverse training**: 138GB vs 20GB training data
5. **Modern architecture**: DeBERTa improvements

---

## 📁 Files

### Training Data
```
Main file:  data/final/final_train_data_v3_SEMANTIC.xlsx
CSV backup: data/final/final_train_data_v3_SEMANTIC.csv
Size:       ~0.5 MB
Encoding:   UTF-8
```

### Training Script
```
Script: scripts/training/KAGGLE_VIDEBERTA_TRAINING.py
Guide:  docs/HUONG_DAN_VIDEBERTA_KAGGLE.md
Cells:  19 (complete pipeline)
```

### Conversion Scripts
```
Main:   scripts/preprocessing/convert_with_semantic_tokens.py
Fix:    fix_videberta_labels.py
Verify: verify_semantic_data.py
```

---

## 🎯 Next Steps

### 1. Upload to Kaggle ✅
```bash
# Upload these files:
- final_train_data_v3_SEMANTIC.xlsx (training data)
- KAGGLE_VIDEBERTA_TRAINING.py (training script)
```

### 2. Setup Kaggle Notebook
```python
# Cell 1: Install dependencies
!pip install transformers datasets accelerate -q

# Cell 2: Load data
import pandas as pd
df = pd.read_excel('/kaggle/input/your-dataset/final_train_data_v3_SEMANTIC.xlsx')
print(f"Loaded {len(df)} samples")
```

### 3. Run Training
```python
# Follow KAGGLE_VIDEBERTA_TRAINING.py
# 19 cells total
# Expected time: 2-3 hours on T4 x2
```

### 4. Evaluate & Compare
```python
# Compare with PhoBERT baseline
# Target: F1 > 0.76
# Competitive: F1 > 0.78
```

---

## ⚠️ Important Notes

### MUST DO
1. ✅ Add special tokens to tokenizer (Cell 8)
2. ✅ Resize model embeddings (Cell 11)
3. ✅ Use MAX_LENGTH = 512 (not 256)
4. ✅ Set num_workers = 0 (Kaggle requirement)

### DO NOT
1. ❌ Remove special tokens from data
2. ❌ Add `</s>` or `<s>` manually (tokenizer does it)
3. ❌ Segment text with underthesau (use raw text)
4. ❌ Use MAX_LENGTH = 256 (too short for ViDeBERTa)

---

## 🔍 Troubleshooting

### Issue: Special tokens not recognized
```python
# Solution: Add to tokenizer
tokenizer.add_special_tokens(special_tokens_dict)
model.resize_token_embeddings(len(tokenizer))
```

### Issue: F1 score lower than expected
```python
# Check:
1. Special tokens added? (Cell 8)
2. Model embeddings resized? (Cell 11)
3. MAX_LENGTH = 512? (not 256)
4. Learning rate = 2e-5? (not too high)
```

### Issue: Training too slow
```python
# Solutions:
1. Use T4 x2 or P100 GPU
2. Reduce batch size to 8 (increase accumulation to 4)
3. Use mixed precision (fp16=True)
```

---

## 📚 Documentation

### Read These First
1. `docs/HUONG_DAN_VIDEBERTA_KAGGLE.md` - Training guide
2. `docs/SEMANTIC_VS_REMOVED_SEPARATOR.md` - Why semantic tokens
3. `docs/PHOBERT_VS_VIDEBERTA_DATA.md` - Model comparison

### Reference
1. `scripts/training/KAGGLE_VIDEBERTA_TRAINING.py` - Complete script
2. `scripts/preprocessing/convert_with_semantic_tokens.py` - Conversion
3. `fix_videberta_labels.py` - Label cleaning

---

## ✅ Final Checklist

Before training, verify:

- [x] Dataset loaded: 6,285 samples
- [x] Labels clean: 0, 1, 2 (no text)
- [x] Special tokens present: `<sep>`, `<emo_pos>`, etc.
- [x] BOS/EOS removed: no `</s>` or `<s>`
- [x] No broken tokens: no `<emo pos>`
- [x] Training script ready: 19 cells
- [x] Special tokens config: Cell 8
- [x] Model resize: Cell 11
- [x] MAX_LENGTH = 512
- [x] Documentation read

**Status**: ✅ ALL CHECKS PASSED - READY TO TRAIN!

---

## 🎯 Success Criteria

### Minimum (Pass)
- F1 Score: > 0.72 (better than baseline)
- Training: No errors
- Inference: Works on new data

### Target (Good)
- F1 Score: > 0.76 (expected improvement)
- Training: Stable convergence
- Inference: Fast and accurate

### Competitive (Excellent)
- F1 Score: > 0.78 (top tier)
- Training: Early stopping at epoch 3-4
- Inference: Production ready

---

**Dataset**: ✅ Ready  
**Script**: ✅ Ready  
**Documentation**: ✅ Complete  
**Status**: 🚀 Ready to Train!

---

**Last Updated**: 2024-12-30  
**Next Action**: Upload to Kaggle and train!
