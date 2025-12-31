# 🚀 ViDeBERTa Migration Plan

**Date**: 2024-12-30  
**Goal**: Switch from PhoBERT to ViDeBERTa for better toxic comment classification

---

## 🎯 Why ViDeBERTa?

### Performance Advantages
- ✅ **Better for social media**: Pre-trained on 138GB diverse Vietnamese text (including social media)
- ✅ **Lighter model**: 86M params vs PhoBERT-base 135M (36% smaller)
- ✅ **Longer context**: 512 tokens vs PhoBERT 256 tokens
- ✅ **No segmentation**: Works with raw text (simpler pipeline)
- ✅ **Modern architecture**: DeBERTaV3 > BERT (disentangled attention)

### Expected Improvements
- 📊 F1 Score: +3-5% improvement (0.75-0.80 vs 0.72-0.76)
- ⚡ Training: Faster (smaller model)
- 💾 Memory: Less GPU memory needed
- 🎯 Accuracy: Better understanding of toxic/slang/teencode

---

## 📋 Migration Steps

### Step 1: Prepare Raw Text Data ✅

**Current**: `final_train_data_v3_READY.xlsx` (segmented)
```
"học_sinh giỏi bú_fame"  # PhoBERT format
```

**Need**: Raw text version (no segmentation)
```
"học sinh giỏi bú fame"  # ViDeBERTa format
```

**Action**:
```python
# Create script: prepare_raw_text_data.py
import pandas as pd

# Load segmented data
df = pd.read_excel('data/final/final_train_data_v3_READY.xlsx')

# Remove underscores (unsegment)
df['training_text_raw'] = df['training_text'].str.replace('_', ' ')

# Save
df[['training_text_raw', 'label']].to_excel(
    'data/final/final_train_data_v3_RAW.xlsx', 
    index=False
)
```

### Step 2: Create ViDeBERTa Training Script ⏳

**Base**: `scripts/training/KAGGLE_TRAINING_CELLS_V2.py`

**Changes needed**:

1. **Model & Tokenizer**
```python
# OLD (PhoBERT)
MODEL_NAME = "vinai/phobert-base-v2"
MAX_LENGTH = 256

# NEW (ViDeBERTa)
MODEL_NAME = "Fsoft-AIC/videberta-base"
MAX_LENGTH = 512  # Can handle longer text!
```

2. **Tokenizer Import**
```python
# OLD
from transformers import AutoTokenizer, RobertaForSequenceClassification

# NEW
from transformers import AutoTokenizer, DebertaV2ForSequenceClassification
```

3. **Dataset Class** (no changes needed!)
```python
# ViDeBERTa tokenizer works the same way
class ToxicDataset(Dataset):
    def __getitem__(self, idx):
        text = str(self.texts[idx])  # Raw text, no segmentation!
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }
```

4. **Model Loading**
```python
# OLD
model = AutoModelForSequenceClassification.from_pretrained(
    "vinai/phobert-base-v2",
    num_labels=3
)

# NEW
model = DebertaV2ForSequenceClassification.from_pretrained(
    "Fsoft-AIC/videberta-base",
    num_labels=3
)
```

### Step 3: Train on Kaggle ⏳

**Setup**:
1. Upload `final_train_data_v3_RAW.xlsx` to Kaggle
2. Create new notebook: "SafeSense-ViDeBERTa-Training"
3. Settings: GPU T4 x2, Internet ON
4. Copy cells from new script

**Expected time**: ~15-20 minutes (same as PhoBERT)

### Step 4: Compare Results ⏳

| Metric | PhoBERT | ViDeBERTa | Improvement |
|--------|---------|-----------|-------------|
| F1 (macro) | 0.72-0.76 | 0.75-0.80 | +3-5% |
| Accuracy | 0.75-0.80 | 0.78-0.83 | +3% |
| Training time | ~20 min | ~15 min | -25% |
| GPU memory | ~8 GB | ~6 GB | -25% |

### Step 5: Choose Best Model ⏳

**Decision criteria**:
- F1 score (primary)
- Inference speed
- Model size
- Error patterns

---

## 📝 Implementation Checklist

### Data Preparation
- [ ] Create `prepare_raw_text_data.py`
- [ ] Generate `final_train_data_v3_RAW.xlsx`
- [ ] Verify data quality (no segmentation artifacts)
- [ ] Upload to Kaggle dataset

### Script Creation
- [ ] Copy `KAGGLE_TRAINING_CELLS_V2.py` → `KAGGLE_VIDEBERTA_TRAINING.py`
- [ ] Update model name to `Fsoft-AIC/videberta-base`
- [ ] Update max_length to 512
- [ ] Update tokenizer/model imports
- [ ] Test locally (if possible)

### Training
- [ ] Create Kaggle notebook
- [ ] Upload raw data
- [ ] Run training (5 epochs)
- [ ] Monitor F1 score
- [ ] Export error analysis

### Evaluation
- [ ] Compare F1: PhoBERT vs ViDeBERTa
- [ ] Analyze error patterns
- [ ] Check inference speed
- [ ] Document results

### Deployment
- [ ] Choose best model
- [ ] Save final model
- [ ] Create inference script
- [ ] Prepare for competition submission

---

## 🔧 Code Templates

### 1. Prepare Raw Text Data
```python
"""
prepare_raw_text_data.py
Convert segmented data to raw text for ViDeBERTa
"""

import pandas as pd
import re

def unsegment_text(text):
    """Remove word segmentation underscores"""
    # Simple: replace _ with space
    text = str(text).replace('_', ' ')
    
    # Clean multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# Load segmented data
df = pd.read_excel('data/final/final_train_data_v3_READY.xlsx')

print(f"Loaded: {len(df)} samples")
print(f"Columns: {df.columns.tolist()}")

# Unsegment
df['training_text_raw'] = df['training_text'].apply(unsegment_text)

# Verify
print("\nSample comparison:")
for i in range(3):
    print(f"\nSegmented: {df['training_text'].iloc[i][:80]}")
    print(f"Raw:       {df['training_text_raw'].iloc[i][:80]}")

# Save
output_file = 'data/final/final_train_data_v3_RAW.xlsx'
df[['training_text_raw', 'label']].rename(
    columns={'training_text_raw': 'training_text'}
).to_excel(output_file, index=False)

print(f"\n✅ Saved: {output_file}")
print(f"   Samples: {len(df)}")
```

### 2. ViDeBERTa Config
```python
class Config:
    # Model
    MODEL_NAME = "Fsoft-AIC/videberta-base"
    NUM_LABELS = 3
    MAX_LENGTH = 512  # ViDeBERTa supports longer context!
    
    # Training
    BATCH_SIZE = 16  # Can use 16 or 32 (smaller model)
    GRADIENT_ACCUMULATION_STEPS = 2
    EPOCHS = 5
    LEARNING_RATE = 2e-5
    WEIGHT_DECAY = 0.01
    WARMUP_RATIO = 0.1
    
    # Optimization
    USE_CLASS_WEIGHTS = True
    LABEL_SMOOTHING = 0.1
    
    # Paths
    DATA_PATH = "/kaggle/input/safesense-raw-data/final_train_data_v3_RAW.xlsx"
    MODEL_SAVE_PATH = "/kaggle/working/videberta_toxic_model"
```

### 3. Model Loading
```python
from transformers import AutoTokenizer, DebertaV2ForSequenceClassification

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
print(f"✅ Tokenizer: {Config.MODEL_NAME}")
print(f"   Vocab size: {tokenizer.vocab_size}")

# Load model
model = DebertaV2ForSequenceClassification.from_pretrained(
    Config.MODEL_NAME,
    num_labels=Config.NUM_LABELS
)
model.to(Config.DEVICE)

total_params = sum(p.numel() for p in model.parameters())
print(f"✅ Model: {total_params:,} parameters")
```

---

## 📊 Expected Results

### PhoBERT (Baseline)
```
F1 (macro):  0.72-0.76
Accuracy:    0.75-0.80
Precision:   0.73-0.78
Recall:      0.71-0.76
```

### ViDeBERTa (Target)
```
F1 (macro):  0.75-0.80  ⬆️ +3-5%
Accuracy:    0.78-0.83  ⬆️ +3%
Precision:   0.76-0.81  ⬆️ +3%
Recall:      0.74-0.79  ⬆️ +3%
```

### Why Better?
1. **Better pre-training**: 138GB diverse text (vs 20GB formal text)
2. **Social media understanding**: Trained on informal Vietnamese
3. **Longer context**: 512 tokens captures more context
4. **Modern architecture**: DeBERTaV3 attention mechanism

---

## 🎯 Success Criteria

### Minimum (Accept ViDeBERTa)
- F1 > 0.75 (better than PhoBERT 0.72-0.76)
- No significant error pattern changes
- Inference speed acceptable

### Target (Strong Accept)
- F1 > 0.78 (competition competitive)
- Better handling of toxic/slang/teencode
- Faster training & inference

### Stretch (Excellent)
- F1 > 0.80 (top 3 competition)
- Ensemble with PhoBERT for 0.82+

---

## 🚨 Risks & Mitigation

### Risk 1: ViDeBERTa performs worse
**Mitigation**: Keep PhoBERT as backup, can ensemble both

### Risk 2: Kaggle compatibility issues
**Mitigation**: Test locally first, check transformers version

### Risk 3: Longer training time (512 tokens)
**Mitigation**: Use gradient accumulation, reduce batch size if needed

### Risk 4: Data quality after unsegmentation
**Mitigation**: Verify samples manually, check for artifacts

---

## 📅 Timeline

| Day | Task | Duration |
|-----|------|----------|
| Day 1 | Prepare raw text data | 1 hour |
| Day 1 | Create ViDeBERTa script | 2 hours |
| Day 2 | Train on Kaggle | 30 min |
| Day 2 | Evaluate & compare | 1 hour |
| Day 3 | Choose model & optimize | 2 hours |

**Total**: ~2-3 days

---

## 📚 References

- [ViDeBERTa Paper](https://arxiv.org/abs/2301.10439)
- [ViDeBERTa HuggingFace](https://huggingface.co/Fsoft-AIC/videberta-base)
- [DeBERTaV3 Paper](https://arxiv.org/abs/2111.09543)

---

**Ready to start migration! 🚀**
