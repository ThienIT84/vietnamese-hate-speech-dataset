# 📊 PhoBERT vs ViDeBERTa: Data Processing Comparison

**Date**: 2024-12-30  
**Question**: Có thể dùng data của PhoBERT cho ViDeBERTa không?

---

## 🎯 TL;DR - Câu Trả Lời Nhanh

**❌ KHÔNG thể dùng trực tiếp!**

Data hiện tại của bạn:
```
"học_sinh giỏi bú_fame"  ← Có underscores (segmented)
```

Cần convert thành:
```
"học sinh giỏi bú fame"  ← Không có underscores (raw)
```

**✅ Giải pháp**: Chỉ cần **XÓA underscores** là xong!

---

## 🔬 Test Results - Kết Quả Thực Nghiệm

### Test Setup
```python
# Test với 2 formats:
raw_text = "học sinh giỏi bú fame"       # Raw (no underscore)
segmented_text = "học_sinh giỏi bú_fame" # Segmented (with underscore)
```

### PhoBERT Tokenization

**With RAW text:**
```python
['học', 'sinh', 'giỏi', 'bú', 'f@@', 'ame']  # 6 tokens
# ❌ Tách riêng "học" và "sinh" → mất nghĩa compound word
```

**With SEGMENTED text:**
```python
['học_sinh', 'giỏi', 'b@@', 'ú_@@', 'f@@', 'ame']  # 6 tokens
# ✅ Giữ nguyên "học_sinh" → đúng nghĩa
```

### ViDeBERTa Tokenization

**With RAW text:**
```python
['▁học', '▁sinh', '▁giỏi', '▁bú', '▁', 'fame']  # 6 tokens
# ✅ Tokenizer tự hiểu "học sinh" là 2 từ riêng biệt
```

**With SEGMENTED text:**
```python
['▁học_sinh', '▁giỏi', '▁bú', '_', 'fame']  # 5 tokens
# ⚠️ Coi "học_sinh" là 1 token lạ, underscore thành token riêng
```

---

## 📋 Chi Tiết So Sánh

### PhoBERT (vinai/phobert-base-v2)

| Aspect | Details |
|--------|---------|
| **Tokenizer** | PhobertTokenizer (RobertaTokenizer) |
| **Algorithm** | BPE (Byte-Pair Encoding) |
| **Vocab Size** | 64,000 tokens |
| **Pre-training** | 20GB Vietnamese text (Wikipedia, News) |
| **Segmentation** | ✅ **REQUIRED** - Trained on segmented text |
| **Input Format** | `"học_sinh giỏi"` (with underscores) |
| **Why?** | Vocab được build từ text đã segment |

**Example:**
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")

# ✅ CORRECT for PhoBERT
text = "học_sinh giỏi bú_fame"
tokens = tokenizer.tokenize(text)
# → ['học_sinh', 'giỏi', 'b@@', 'ú_@@', 'f@@', 'ame']

# ❌ WRONG for PhoBERT
text = "học sinh giỏi bú fame"
tokens = tokenizer.tokenize(text)
# → ['học', 'sinh', 'giỏi', 'bú', 'f@@', 'ame']
# Problem: "học" và "sinh" tách rời → mất nghĩa compound
```

### ViDeBERTa (Fsoft-AIC/videberta-base)

| Aspect | Details |
|--------|---------|
| **Tokenizer** | DebertaV2TokenizerFast |
| **Algorithm** | SentencePiece (Unigram) |
| **Vocab Size** | 128,000 tokens (2x PhoBERT!) |
| **Pre-training** | 138GB Vietnamese text (diverse sources) |
| **Segmentation** | ❌ **NOT NEEDED** - Trained on raw text |
| **Input Format** | `"học sinh giỏi"` (no underscores) |
| **Why?** | Vocab được build từ raw text, tự học subwords |

**Example:**
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")

# ✅ CORRECT for ViDeBERTa
text = "học sinh giỏi bú fame"
tokens = tokenizer.tokenize(text)
# → ['▁học', '▁sinh', '▁giỏi', '▁bú', '▁', 'fame']

# ⚠️ WORKS but SUBOPTIMAL
text = "học_sinh giỏi bú_fame"
tokens = tokenizer.tokenize(text)
# → ['▁học_sinh', '▁giỏi', '▁bú', '_', 'fame']
# Problem: Underscore thành token riêng, không tự nhiên
```

---

## 🔄 Conversion Process

### Your Current Data
```
File: final_train_data_v3_READY.xlsx
Format: SEGMENTED (for PhoBERT)

training_text                                    label
học_sinh giỏi bú_fame                           1
thằng ngu vcl đm                                2
video hay quá cảm_ơn bạn                        0
```

### Need for ViDeBERTa
```
File: final_train_data_v3_RAW.xlsx (NEW)
Format: RAW (for ViDeBERTa)

training_text                                    label
học sinh giỏi bú fame                           1
thằng ngu vcl đm                                2
video hay quá cảm ơn bạn                        0
```

### Conversion Script

```python
"""
convert_segmented_to_raw.py
Convert PhoBERT segmented data to ViDeBERTa raw format
"""

import pandas as pd
import re

def remove_segmentation(text):
    """
    Remove word segmentation underscores
    
    Examples:
        "học_sinh giỏi" → "học sinh giỏi"
        "bú_fame" → "bú fame"
        "cảm_ơn" → "cảm ơn"
    """
    # Replace underscore with space
    text = str(text).replace('_', ' ')
    
    # Clean multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# Load segmented data
input_file = 'data/final/final_train_data_v3_READY.xlsx'
df = pd.read_excel(input_file)

print(f"📂 Loaded: {len(df)} samples")
print(f"📂 Columns: {df.columns.tolist()}")

# Check if data is segmented
sample = df['training_text'].iloc[0]
underscore_count = str(sample).count('_')
print(f"\n🔍 Sample text: {sample[:80]}")
print(f"🔍 Underscores: {underscore_count}")

if underscore_count > 0:
    print("✅ Data is SEGMENTED → Converting to RAW...")
    
    # Convert
    df['training_text_raw'] = df['training_text'].apply(remove_segmentation)
    
    # Verify
    print("\n📊 BEFORE vs AFTER:")
    for i in range(5):
        print(f"\n{i+1}. BEFORE: {df['training_text'].iloc[i][:60]}")
        print(f"   AFTER:  {df['training_text_raw'].iloc[i][:60]}")
    
    # Save
    output_file = 'data/final/final_train_data_v3_RAW.xlsx'
    df_output = df[['training_text_raw', 'label']].copy()
    df_output.columns = ['training_text', 'label']
    df_output.to_excel(output_file, index=False)
    
    print(f"\n✅ Saved: {output_file}")
    print(f"   Samples: {len(df_output)}")
    
    # Also save CSV
    csv_file = output_file.replace('.xlsx', '.csv')
    df_output.to_csv(csv_file, index=False)
    print(f"✅ Saved: {csv_file}")
    
else:
    print("⚠️ Data is already RAW (no underscores)")

print("\n" + "="*80)
print("✅ CONVERSION COMPLETE!")
print("="*80)
```

---

## 🎯 Summary Table

| Feature | PhoBERT | ViDeBERTa |
|---------|---------|-----------|
| **Input Format** | Segmented (`học_sinh`) | Raw (`học sinh`) |
| **Tokenizer** | RobertaTokenizer (BPE) | DebertaV2 (SentencePiece) |
| **Vocab Size** | 64K | 128K |
| **Max Length** | 256 tokens | 512 tokens |
| **Pre-training** | 20GB formal text | 138GB diverse text |
| **Segmentation Tool** | underthesea required | Not needed |
| **Your Data** | ✅ Ready (SEGMENTED) | ⚠️ Need convert (remove `_`) |

---

## ✅ Action Plan

### Step 1: Convert Data (5 minutes)
```bash
python convert_segmented_to_raw.py
```

**Output:**
- `data/final/final_train_data_v3_RAW.xlsx` (for ViDeBERTa)
- `data/final/final_train_data_v3_RAW.csv`

### Step 2: Verify Conversion
```python
import pandas as pd

# Load both
segmented = pd.read_excel('data/final/final_train_data_v3_READY.xlsx')
raw = pd.read_excel('data/final/final_train_data_v3_RAW.xlsx')

# Compare
print("Segmented:", segmented['training_text'].iloc[0])
print("Raw:      ", raw['training_text'].iloc[0])

# Check no underscores in raw
assert '_' not in raw['training_text'].iloc[0], "Still has underscores!"
print("✅ Conversion successful!")
```

### Step 3: Train with ViDeBERTa
```python
# In training script, just change:

# OLD (PhoBERT)
MODEL_NAME = "vinai/phobert-base-v2"
DATA_FILE = "final_train_data_v3_READY.xlsx"  # Segmented

# NEW (ViDeBERTa)
MODEL_NAME = "Fsoft-AIC/videberta-base"
DATA_FILE = "final_train_data_v3_RAW.xlsx"  # Raw (no underscores)
```

---

## 🚨 Common Mistakes

### ❌ Mistake 1: Use segmented data for ViDeBERTa
```python
# WRONG!
text = "học_sinh giỏi bú_fame"  # Has underscores
model = ViDeBERTa(...)
# → Underscores become separate tokens, suboptimal
```

### ❌ Mistake 2: Use raw data for PhoBERT
```python
# WRONG!
text = "học sinh giỏi bú fame"  # No underscores
model = PhoBERT(...)
# → "học" and "sinh" separated, loses compound meaning
```

### ✅ Correct Usage
```python
# PhoBERT
text = "học_sinh giỏi bú_fame"  # Segmented
model = PhoBERT(...)

# ViDeBERTa
text = "học sinh giỏi bú fame"  # Raw
model = ViDeBERTa(...)
```

---

## 💡 Key Insights

1. **PhoBERT = Segmented Input**
   - Vocab trained on `học_sinh`, `cảm_ơn`, etc.
   - Underscore is part of the token
   - Must use underthesea for segmentation

2. **ViDeBERTa = Raw Input**
   - Vocab trained on `học sinh`, `cảm ơn`, etc.
   - Tokenizer learns subwords naturally
   - No preprocessing needed

3. **Conversion is Simple**
   - Just replace `_` with ` ` (space)
   - No other changes needed
   - Labels stay the same

4. **Why ViDeBERTa is Better**
   - Simpler pipeline (no segmentation)
   - Larger vocab (128K vs 64K)
   - Longer context (512 vs 256)
   - Better for social media text

---

## 📚 References

- [PhoBERT Paper](https://arxiv.org/abs/2003.00744)
- [ViDeBERTa Paper](https://arxiv.org/abs/2301.10439)
- [Underthesea](https://github.com/undertheseanlp/underthesea)

---

**Kết luận**: Cần convert data từ segmented → raw (xóa underscores) trước khi train ViDeBERTa!
