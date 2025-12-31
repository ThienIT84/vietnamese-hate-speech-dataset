# 📊 Hai Phiên Bản Dữ Liệu: PhoBERT vs ViDeBERTa

## 🎯 Tại Sao Cần 2 Versions?

**PhoBERT** và **ViDeBERTa** có tokenizer khác nhau → Cần format data khác nhau!

---

## 📋 So Sánh 2 Versions

### Version 1: PhoBERT (READY version)

**File:** `data/final/final_train_data_v3_READY.xlsx`

**Đặc điểm:**
- ✅ **Word segmented:** Có underscore để đánh dấu compound words
- ✅ **Separator:** `</s>` giữa title và comment
- ✅ **Special tokens:** `<person>`, `<user>`, `<emo_pos>`, `<emo_neg>`
- ✅ **Intensity markers:** `<intense>`, `<very_intense>`

**Ví dụ:**
```python
"học_sinh giỏi bú_fame </s> thằng này ngu vcl <emo_neg>"
```

**Tại sao cần underscore?**
- PhoBERT được train trên text đã word-segmented
- Vocab của PhoBERT có "học_sinh" (compound word)
- Nếu không có underscore: "học" và "sinh" tách rời → mất nghĩa

**Tokenization:**
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
text = "học_sinh giỏi bú_fame"
tokens = tokenizer.tokenize(text)
# → ['học_sinh', 'giỏi', 'bú_@@', 'fame']
# ✅ "học_sinh" giữ nguyên compound word
```

---

### Version 2: ViDeBERTa (SEMANTIC version)

**File:** `data/final/final_train_data_v3_SEMANTIC.xlsx`

**Đặc điểm:**
- ✅ **Raw text:** KHÔNG có underscore
- ✅ **Semantic separator:** `<sep>` thay vì `</s>`
- ✅ **Special tokens:** Preserved (giống PhoBERT version)
- ✅ **Intensity markers:** Preserved

**Ví dụ:**
```python
"học sinh giỏi bú fame <sep> thằng này ngu vcl <emo_neg>"
```

**Tại sao KHÔNG cần underscore?**
- ViDeBERTa tokenizer tự hiểu word boundaries
- Vocab của ViDeBERTa không có underscore
- Nếu có underscore: Tokenizer coi "_" là token riêng → sai

**Tokenization:**
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")
text = "học sinh giỏi bú fame"
tokens = tokenizer.tokenize(text)
# → ['▁học', '▁sinh', '▁giỏi', '▁bú', '▁fame']
# ✅ Tokenizer tự hiểu "học sinh" là 2 từ riêng
```

**Tại sao dùng `<sep>` thay vì `</s>`?**
- `</s>` là end-of-sequence token trong BERT/RoBERTa
- `<sep>` rõ ràng hơn: Semantic separator giữa title và comment
- Model học được: "Trước `<sep>` là context (title), sau `<sep>` là content (comment)"

---

## 🔄 Quy Trình Chuyển Đổi

### Từ PhoBERT → ViDeBERTa

**Script:** `scripts/preprocessing/convert_with_semantic_tokens.py`

**Các bước:**

1. **Protect special tokens:**
   ```python
   "<emo_pos>" → "XSPECIALTOKENX0X" (temporary)
   ```

2. **Replace separator:**
   ```python
   "</s>" → "<sep>"
   ```

3. **Remove underscores:**
   ```python
   "học_sinh" → "học sinh"
   "bú_fame" → "bú fame"
   ```

4. **Clean punctuation:**
   ```python
   "Video hay.Cảm ơn" → "Video hay. Cảm ơn"
   ```

5. **Restore special tokens:**
   ```python
   "XSPECIALTOKENX0X" → "<emo_pos>"
   ```

6. **Clean spaces:**
   ```python
   "Video   hay" → "Video hay"
   ```

**Ví dụ End-to-End:**

```python
# INPUT (PhoBERT version):
"học_sinh giỏi bú_fame </s> thằng này ngu vcl <emo_neg>"

# ↓ Convert

# OUTPUT (ViDeBERTa version):
"học sinh giỏi bú fame <sep> thằng này ngu vcl <emo_neg>"
```

---

## 📊 Test Cases

### Test 1: Compound Words

**PhoBERT:**
```python
Input:  "học_sinh giỏi"
Tokens: ['học_sinh', 'giỏi']
✅ Compound word preserved
```

**ViDeBERTa:**
```python
Input:  "học sinh giỏi"
Tokens: ['▁học', '▁sinh', '▁giỏi']
✅ Tokenizer tự hiểu boundaries
```

---

### Test 2: Separator

**PhoBERT:**
```python
Input:  "Confession FTU </s> boy phố"
Tokens: ['Confession', 'FTU', '</s>', 'boy', 'phố']
✅ </s> là separator token
```

**ViDeBERTa:**
```python
Input:  "Confession FTU <sep> boy phố"
Tokens: ['▁Confession', '▁FTU', '<sep>', '▁boy', '▁phố']
✅ <sep> là semantic separator (cần add vào special tokens)
```

---

### Test 3: Special Tokens

**PhoBERT:**
```python
Input:  "thằng <person> ngu <emo_neg>"
Tokens: ['thằng', '<person>', 'ngu', '<emo_neg>']
✅ Special tokens preserved
```

**ViDeBERTa:**
```python
Input:  "thằng <person> ngu <emo_neg>"
Tokens: ['▁thằng', '<person>', '▁ngu', '<emo_neg>']
✅ Special tokens preserved (cần add vào tokenizer)
```

---

### Test 4: Intensity Markers

**PhoBERT:**
```python
Input:  "nguuuu vcl"
After:  "ngu <very_intense> vcl"
Tokens: ['ngu', '<very_intense>', 'vcl']
✅ Intensity marker preserved
```

**ViDeBERTa:**
```python
Input:  "nguuuu vcl"
After:  "ngu <very_intense> vcl"
Tokens: ['▁ngu', '<very_intense>', '▁vcl']
✅ Intensity marker preserved
```

---

## 🎯 Khi Nào Dùng Version Nào?

### Dùng PhoBERT Version (READY)

**Khi:**
- ✅ Train PhoBERT model
- ✅ Cần word segmentation
- ✅ Vocab có compound words với underscore

**File:** `data/final/final_train_data_v3_READY.xlsx`

**Format:**
```python
"học_sinh giỏi </s> comment"
```

---

### Dùng ViDeBERTa Version (SEMANTIC)

**Khi:**
- ✅ Train ViDeBERTa model
- ✅ Tokenizer không cần underscore
- ✅ Muốn semantic separator rõ ràng

**File:** `data/final/final_train_data_v3_SEMANTIC.xlsx`

**Format:**
```python
"học sinh giỏi <sep> comment"
```

---

## 📝 Cách Trình Bày Trong Presentation

### Script ngắn gọn (15 giây):

> "Sau khi xử lý, chúng em tạo **2 versions** của data:
> 
> 1. **PhoBERT version:** Có underscore để word segmentation ("học_sinh")
> 2. **ViDeBERTa version:** Raw text không underscore ("học sinh")
> 
> Mỗi version được optimize cho tokenizer của model tương ứng."

### Nếu BGK hỏi chi tiết:

**Q: "Tại sao cần 2 versions?"**

A: "PhoBERT và ViDeBERTa có tokenizer khác nhau:

- **PhoBERT:** Trained trên text đã word-segmented, vocab có "học_sinh" (compound word)
- **ViDeBERTa:** Trained trên raw text, tokenizer tự hiểu word boundaries

Nếu dùng sai format:
- PhoBERT với raw text → "học" và "sinh" tách rời, mất nghĩa compound
- ViDeBERTa với underscore → Tokenizer coi "_" là token riêng, sai

Chúng em convert từ PhoBERT version sang ViDeBERTa version bằng script tự động:
- Xóa underscores
- Thay `</s>` → `<sep>` (semantic separator)
- Preserve special tokens"

---

## ✅ Checklist

Trước khi train:

### PhoBERT
- [ ] Dùng file: `final_train_data_v3_READY.xlsx`
- [ ] Check: Text có underscore ("học_sinh")
- [ ] Check: Separator là `</s>`
- [ ] Check: Special tokens preserved

### ViDeBERTa
- [ ] Dùng file: `final_train_data_v3_SEMANTIC.xlsx`
- [ ] Check: Text KHÔNG có underscore ("học sinh")
- [ ] Check: Separator là `<sep>`
- [ ] Check: Special tokens preserved
- [ ] Add `<sep>` vào tokenizer special tokens

---

## 🔍 Verification

### Kiểm tra PhoBERT version:

```python
import pandas as pd

df = pd.read_excel('data/final/final_train_data_v3_READY.xlsx')

# Check underscores
underscore_count = df['training_text'].str.count('_').sum()
print(f"Underscores: {underscore_count}")  # Should be > 0

# Check separator
sep_count = df['training_text'].str.contains('</s>').sum()
print(f"</s> tokens: {sep_count}")  # Should be > 0

# Sample
print(df['training_text'].iloc[0])
# → "học_sinh giỏi </s> comment"
```

### Kiểm tra ViDeBERTa version:

```python
import pandas as pd

df = pd.read_excel('data/final/final_train_data_v3_SEMANTIC.xlsx')

# Check underscores
underscore_count = df['training_text'].str.count('_').sum()
print(f"Underscores: {underscore_count}")  # Should be 0

# Check separator
sep_count = df['training_text'].str.contains('<sep>').sum()
print(f"<sep> tokens: {sep_count}")  # Should be > 0

old_sep_count = df['training_text'].str.contains('</s>').sum()
print(f"</s> tokens: {old_sep_count}")  # Should be 0

# Sample
print(df['training_text'].iloc[0])
# → "học sinh giỏi <sep> comment"
```

---

## 📚 Tài Liệu Tham Khảo

- `docs/PHOBERT_VS_VIDEBERTA_DATA.md` - So sánh chi tiết
- `docs/SEMANTIC_VS_REMOVED_SEPARATOR.md` - Tại sao dùng `<sep>`
- `scripts/preprocessing/convert_with_semantic_tokens.py` - Script convert

---

**Bạn đã hiểu rõ 2 versions! 🎯**
