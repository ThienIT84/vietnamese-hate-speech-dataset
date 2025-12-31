# 🔧 Fix CUDA Out of Memory - ViDeBERTa Training

**Lỗi**: `OutOfMemoryError: CUDA out of memory. Tried to allocate 192.00 MiB`

---

## ✅ GIẢI PHÁP 1: Gradient Checkpointing + Batch 8 (KHUYẾN NGHỊ)

### Bước 1: Sửa Cell 3 (Configuration)

```python
# Cell 3: Configuration
import torch

class Config:
    MODEL_NAME = "Fsoft-AIC/videberta-base"
    MAX_LENGTH = 512  # Giữ nguyên
    BATCH_SIZE = 8  # ← GIẢM từ 16 xuống 8
    GRADIENT_ACCUMULATION_STEPS = 4  # ← TĂNG từ 2 lên 4
    EPOCHS = 5
    LEARNING_RATE = 2e-5
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print("="*60)
print("CONFIGURATION")
print("="*60)
print(f"Model: {Config.MODEL_NAME}")
print(f"Max Length: {Config.MAX_LENGTH}")
print(f"Batch Size: {Config.BATCH_SIZE}")
print(f"Gradient Accumulation: {Config.GRADIENT_ACCUMULATION_STEPS}")
print(f"Effective Batch Size: {Config.BATCH_SIZE * Config.GRADIENT_ACCUMULATION_STEPS}")
print(f"Epochs: {Config.EPOCHS}")
print(f"Learning Rate: {Config.LEARNING_RATE}")
print(f"Device: {Config.DEVICE}")
```

### Bước 2: Sửa Cell 11 (Load Model)

```python
# Cell 11: Load model & resize embeddings
print("="*60)
print("LOADING MODEL")
print("="*60)

model = AutoModelForSequenceClassification.from_pretrained(
    Config.MODEL_NAME,
    num_labels=3,
    ignore_mismatched_sizes=True
)

# Resize embeddings for special tokens
model.resize_token_embeddings(len(tokenizer))

# ✅ THÊM DÒNG NÀY - Enable gradient checkpointing
model.gradient_checkpointing_enable()
print("✅ Gradient checkpointing enabled (saves ~40% memory)")

model = model.to(Config.DEVICE)

print(f"\n✅ Model loaded: {Config.MODEL_NAME}")
print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")
print(f"   Trainable: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
print(f"   Embeddings size: {model.get_input_embeddings().weight.shape}")
print(f"   Device: {next(model.parameters()).device}")
```

### Bước 3: Restart & Run

1. **Restart Kernel**: Session → Restart Session
2. **Clear GPU**: Giải phóng memory cũ
3. **Run All Cells**: Chạy lại từ đầu

**Kết quả kỳ vọng**:
- Memory usage: ~9-10GB (thay vì 14.7GB)
- Training time: +20% (chậm hơn một chút)
- F1 score: Không đổi (vẫn 0.76-0.80)

---

## ✅ GIẢI PHÁP 2: Giảm MAX_LENGTH (nếu vẫn lỗi)

### Sửa Cell 3:

```python
class Config:
    MODEL_NAME = "Fsoft-AIC/videberta-base"
    MAX_LENGTH = 384  # ← GIẢM từ 512 xuống 384
    BATCH_SIZE = 12  # ← Có thể tăng lại
    GRADIENT_ACCUMULATION_STEPS = 3
    EPOCHS = 5
    LEARNING_RATE = 2e-5
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

**Trade-off**:
- ✅ Memory: ~8GB (an toàn)
- ✅ Speed: Nhanh hơn
- ⚠️ F1: Có thể giảm 0.5-1% (vẫn tốt hơn PhoBERT)

---

## ✅ GIẢI PHÁP 3: Extreme (nếu vẫn lỗi)

### Sửa Cell 3:

```python
class Config:
    MODEL_NAME = "Fsoft-AIC/videberta-base"
    MAX_LENGTH = 256  # ← Giống PhoBERT
    BATCH_SIZE = 16
    GRADIENT_ACCUMULATION_STEPS = 2
    EPOCHS = 5
    LEARNING_RATE = 2e-5
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

**Trade-off**:
- ✅ Memory: ~6GB (rất an toàn)
- ✅ Speed: Nhanh nhất
- ⚠️ F1: Có thể giảm 1-2% (vẫn tương đương PhoBERT)

---

## 🎯 Khuyến Nghị

### Thử theo thứ tự:

1. **Giải pháp 1** (Gradient Checkpointing + Batch 8)
   - Giữ MAX_LENGTH=512 (tối ưu nhất)
   - Chỉ chậm hơn 20%
   - F1 không đổi

2. **Giải pháp 2** (MAX_LENGTH=384)
   - Nếu giải pháp 1 vẫn lỗi
   - Vẫn dài hơn PhoBERT (256)
   - F1 giảm nhẹ (~0.5%)

3. **Giải pháp 3** (MAX_LENGTH=256)
   - Nếu GPU quá yếu
   - Giống PhoBERT
   - Vẫn có lợi thế tokenization

---

## 📊 Memory Comparison

| Config | Memory | Time/Epoch | F1 Expected |
|--------|--------|------------|-------------|
| **Original** (Batch 16, Len 512) | 14.7GB ❌ | 15 min | 0.76-0.80 |
| **Fix 1** (Batch 8, Len 512 + Checkpoint) | ~9GB ✅ | 18 min | 0.76-0.80 |
| **Fix 2** (Batch 12, Len 384) | ~8GB ✅ | 12 min | 0.75-0.79 |
| **Fix 3** (Batch 16, Len 256) | ~6GB ✅ | 10 min | 0.74-0.78 |

---

## 🔍 Kiểm Tra Memory

Thêm cell này để monitor memory:

```python
# Check GPU memory
import torch

if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Total memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    print(f"Allocated: {torch.cuda.memory_allocated(0) / 1024**3:.2f} GB")
    print(f"Cached: {torch.cuda.memory_reserved(0) / 1024**3:.2f} GB")
    print(f"Free: {(torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)) / 1024**3:.2f} GB")
```

---

## ⚠️ Lưu Ý

### Sau khi sửa config:

1. **PHẢI restart kernel**: Session → Restart Session
2. **Clear GPU memory**: Giải phóng memory cũ
3. **Run từ đầu**: Chạy lại tất cả cells

### Không restart = vẫn lỗi!

---

## ✅ Expected Results

### Với Giải pháp 1 (Khuyến nghị):

```
Epoch 1: F1 ~0.65-0.70 (18 min)
Epoch 2: F1 ~0.72-0.75 (18 min)
Epoch 3: F1 ~0.75-0.78 (18 min) ← Best
Epoch 4: F1 ~0.76-0.79 (18 min)
Epoch 5: F1 ~0.76-0.80 (18 min)

Total time: ~90 min (thay vì 75 min)
Memory: ~9GB (thay vì 14.7GB)
F1: Không đổi ✅
```

---

## 🚀 Quick Fix

**Copy & paste vào Cell 3**:

```python
class Config:
    MODEL_NAME = "Fsoft-AIC/videberta-base"
    MAX_LENGTH = 512
    BATCH_SIZE = 8  # ← Changed
    GRADIENT_ACCUMULATION_STEPS = 4  # ← Changed
    EPOCHS = 5
    LEARNING_RATE = 2e-5
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
```

**Thêm vào Cell 11** (sau `model.resize_token_embeddings`):

```python
model.gradient_checkpointing_enable()
print("✅ Gradient checkpointing enabled")
```

**Restart kernel → Run all cells**

---

**Chúc may mắn! 🚀**
