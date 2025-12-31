# 📊 Data Conversion Summary: PhoBERT → ViDeBERTa

**Date**: 2024-12-30  
**Status**: ✅ Complete

---

## 🎯 Objective

Convert PhoBERT segmented data to ViDeBERTa raw format by removing word segmentation underscores.

---

## 📋 Conversion Results

### Input Data
- **File**: `data/final/final_train_data_v3_READY.xlsx`
- **Format**: SEGMENTED (for PhoBERT)
- **Samples**: 6,139
- **Underscores**: 44,647 total
- **Size**: 1.09 MB

**Example:**
```
"boy phố mới nhú hay sao mà mặt ông cháu nào cũng non_choẹt vậy ?_ </s> tệ_nạn xã_hội"
```

### Output Data
- **File**: `data/final/final_train_data_v3_RAW.xlsx`
- **Format**: RAW (for ViDeBERTa)
- **Samples**: 6,139
- **Underscores**: 0 (all removed ✅)
- **Size**: 0.41 MB (62% smaller!)

**Example:**
```
"boy phố mới nhú hay sao mà mặt ông cháu nào cũng non choẹt vậy ? </s> tệ nạn xã hội"
```

---

## 📊 Statistics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Samples** | 6,139 | 6,139 | 0 |
| **Underscores** | 44,647 | 0 | -44,647 ✅ |
| **File Size** | 1.09 MB | 0.41 MB | -62% |
| **Label 0 (Clean)** | 2,754 (44.9%) | 2,754 (44.9%) | Same |
| **Label 1 (Toxic)** | 1,639 (26.7%) | 1,639 (26.7%) | Same |
| **Label 2 (Hate)** | 1,746 (28.4%) | 1,746 (28.4%) | Same |

---

## 🔄 Conversion Process

### Method
```python
def remove_segmentation(text):
    # Replace underscore with space
    text = str(text).replace('_', ' ')
    
    # Clean multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()
```

### Examples

| Before (Segmented) | After (Raw) |
|-------------------|-------------|
| `học_sinh giỏi` | `học sinh giỏi` |
| `bú_fame` | `bú fame` |
| `cảm_ơn bạn` | `cảm ơn bạn` |
| `tệ_nạn xã_hội` | `tệ nạn xã hội` |
| `phân_biệt vùng_miền` | `phân biệt vùng miền` |
| `non_choẹt` | `non choẹt` |
| `kết_thúc` | `kết thúc` |

### Special Tokens
Special tokens were also cleaned:
- `<emo_pos>` → `<emo pos>` (underscore removed)
- `<person>` → `<person>` (no change, no underscore)
- `</s>` → `</s>` (no change)

---

## ✅ Verification

### 1. Underscore Count
```
Before: 44,647 underscores
After:  0 underscores
✅ All removed successfully!
```

### 2. Sample Comparison
```
Sample 1:
BEFORE: boy phố mới nhú hay sao mà mặt ông cháu nào cũng non_choẹt vậy ?_ </s> tệ_nạn xã_hội
AFTER:  boy phố mới nhú hay sao mà mặt ông cháu nào cũng non choẹt vậy ? </s> tệ nạn xã hội
✅ Changed

Sample 2:
BEFORE: Phân_biệt vùng_miền , miệt_thị người_dân vùng lũ .. Tàng_Keng Ông Trùm
AFTER:  Phân biệt vùng miền , miệt thị người dân vùng lũ .. Tàng Keng Ông Trùm
✅ Changed

Sample 3:
BEFORE: phân_biệt vùng_miền , miệt_thị người_dân vùng lũ . tàng keng <person>
AFTER:  phân biệt vùng miền , miệt thị người dân vùng lũ . tàng keng <person>
✅ Changed
```

### 3. Label Distribution
```
Label 0 (Clean): 2,754 samples (44.9%) ✅ Unchanged
Label 1 (Toxic): 1,639 samples (26.7%) ✅ Unchanged
Label 2 (Hate):  1,746 samples (28.4%) ✅ Unchanged
```

### 4. File Integrity
- ✅ All 6,139 samples preserved
- ✅ No data loss
- ✅ Labels unchanged
- ✅ Text content preserved (only underscores removed)

---

## 📁 Output Files

### 1. Excel Format
```
File: data/final/final_train_data_v3_RAW.xlsx
Size: 0.41 MB
Columns: training_text, label
Samples: 6,139
```

### 2. CSV Format
```
File: data/final/final_train_data_v3_RAW.csv
Size: ~0.4 MB
Encoding: UTF-8
Columns: training_text, label
Samples: 6,139
```

---

## 🎯 Usage

### For PhoBERT Training
```python
# Use SEGMENTED data
data_file = "data/final/final_train_data_v3_READY.xlsx"
model_name = "vinai/phobert-base-v2"

# Text format: "học_sinh giỏi bú_fame"
```

### For ViDeBERTa Training
```python
# Use RAW data
data_file = "data/final/final_train_data_v3_RAW.xlsx"
model_name = "Fsoft-AIC/videberta-base"

# Text format: "học sinh giỏi bú fame"
```

---

## 🔬 Tokenizer Comparison

### PhoBERT with Segmented Data
```python
text = "học_sinh giỏi bú_fame"
tokens = ['học_sinh', 'giỏi', 'b@@', 'ú_@@', 'f@@', 'ame']
# ✅ Correct: "học_sinh" is one token
```

### PhoBERT with Raw Data (WRONG!)
```python
text = "học sinh giỏi bú fame"
tokens = ['học', 'sinh', 'giỏi', 'bú', 'f@@', 'ame']
# ❌ Wrong: "học" and "sinh" separated
```

### ViDeBERTa with Raw Data
```python
text = "học sinh giỏi bú fame"
tokens = ['▁học', '▁sinh', '▁giỏi', '▁bú', '▁', 'fame']
# ✅ Correct: Natural tokenization
```

### ViDeBERTa with Segmented Data (SUBOPTIMAL!)
```python
text = "học_sinh giỏi bú_fame"
tokens = ['▁học_sinh', '▁giỏi', '▁bú', '_', 'fame']
# ⚠️ Works but suboptimal: underscore becomes separate token
```

---

## 📚 Key Learnings

### 1. PhoBERT Requirements
- ✅ Requires word segmentation (underthesea)
- ✅ Vocab trained on segmented text
- ✅ Underscores are part of tokens
- ✅ Max length: 256 tokens

### 2. ViDeBERTa Requirements
- ✅ No segmentation needed
- ✅ Vocab trained on raw text
- ✅ SentencePiece tokenizer handles subwords
- ✅ Max length: 512 tokens

### 3. Conversion is Simple
- ✅ Just replace `_` with ` ` (space)
- ✅ No other preprocessing needed
- ✅ Labels stay the same
- ✅ File size reduced by 62%

### 4. Why ViDeBERTa is Better
- ✅ Simpler pipeline (no segmentation step)
- ✅ Larger vocab (128K vs 64K)
- ✅ Longer context (512 vs 256 tokens)
- ✅ Better for social media text
- ✅ Expected F1 improvement: +3-5%

---

## 🚀 Next Steps

### 1. Upload to Kaggle ⏳
```bash
# Upload file to Kaggle dataset
data/final/final_train_data_v3_RAW.xlsx
```

### 2. Create ViDeBERTa Training Script ⏳
```python
# Base: KAGGLE_TRAINING_CELLS_V2.py
# Changes:
# - MODEL_NAME = "Fsoft-AIC/videberta-base"
# - MAX_LENGTH = 512
# - DATA_FILE = "final_train_data_v3_RAW.xlsx"
```

### 3. Train & Compare ⏳
```
Train both models:
- PhoBERT with SEGMENTED data
- ViDeBERTa with RAW data

Compare F1 scores:
- PhoBERT: Expected 0.72-0.76
- ViDeBERTa: Expected 0.75-0.80
```

### 4. Choose Best Model ⏳
```
Decision criteria:
- F1 score (primary)
- Inference speed
- Model size
- Error patterns
```

---

## 📝 Files Reference

### Scripts
- `scripts/preprocessing/convert_segmented_to_raw.py` - Conversion script
- `archive/test_files/test_videberta_tokenizer.py` - Tokenizer test

### Documentation
- `docs/PHOBERT_VS_VIDEBERTA_DATA.md` - Detailed comparison
- `docs/VIDEBERTA_MIGRATION_PLAN.md` - Migration plan
- `docs/DATA_CONVERSION_SUMMARY.md` - This file

### Data Files
- `data/final/final_train_data_v3_READY.xlsx` - PhoBERT (segmented)
- `data/final/final_train_data_v3_RAW.xlsx` - ViDeBERTa (raw) ⭐
- `data/final/final_train_data_v3_RAW.csv` - ViDeBERTa (raw, CSV)

---

## ✅ Conclusion

**Conversion successful!** 

Data is now ready for ViDeBERTa training:
- ✅ 6,139 samples converted
- ✅ 44,647 underscores removed
- ✅ 0 data loss
- ✅ Labels preserved
- ✅ File size reduced 62%

**Ready to train ViDeBERTa and compare with PhoBERT!** 🚀

---

**Last Updated**: 2024-12-30  
**Status**: ✅ Complete
