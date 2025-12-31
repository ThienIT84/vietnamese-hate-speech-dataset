# 🔍 Nhóm 5 - Clarification

## ❌ Nhầm lẫn trước đây

**SAI:**
```python
Input:  "đm m ngu vcl"
Output: "địt mẹ mày ngu vcl"
```

**Vấn đề:**
- "đm" đã được GIỮ NGUYÊN ở Nhóm 2 (intensity-sensitive)
- Không thể expand "đm" → "địt mẹ" ở Nhóm 5
- Mâu thuẫn với triết lý "Intensity Preservation"

---

## ✅ Sửa lại đúng

### Nhóm 5: Finalization & Smart Mapping

**Bao gồm:**
1. Xử lý tên riêng trong comment (không phải NER)
2. Context-aware "m" mapping
3. Punctuation normalization
4. Whitespace normalization

---

### 1. Xử lý tên riêng trong comment

**Khác với NER masking (Nhóm 2):**

**NER masking (Nhóm 2):**
```python
# Mask tên người KHÔNG có đại từ xúc phạm:
Input:  "Trần Ngọc đẹp vcl"
Output: "<person> đẹp vcl"
```

**Tên riêng trong comment (Nhóm 5):**
```python
# KHÔNG mask tên người CÓ đại từ xúc phạm (theo Guideline V7.2):
Input:  "Thằng Tuấn ngu vcl, con Hoa béo"
Output: "thằng tuấn ngu vcl, con hoa béo"

# Lý do: "Thằng Tuấn", "con Hoa" là công kích cá nhân
# → Cần giữ tên để model học pattern này
# → Nhưng lowercase để chuẩn hóa
```

**Quy tắc:**
- Có đại từ xúc phạm ("thằng", "con", "lũ", "bọn") + tên → KHÔNG mask, chỉ lowercase
- Không có đại từ xúc phạm + tên → Mask thành `<person>` (đã xử lý ở Nhóm 2)

---

### 2. Context-aware "m" mapping

**Positive context:**
```python
Input:  "t yêu m"
Output: "tôi yêu em"

Input:  "m đẹp quá"
Output: "em đẹp quá"
```

**Toxic context:**
```python
Input:  "m ngu vcl"
Output: "mày ngu vcl"

Input:  "m đi chết đi"
Output: "mày đi chết đi"
```

**Neutral context:**
```python
Input:  "m đi đâu"
Output: "mình đi đâu"
```

**⚠️ Lưu ý quan trọng:**
- "đm" đã được giữ nguyên ở Nhóm 2
- Nhóm 5 CHỈ xử lý "m" đứng riêng, KHÔNG xử lý "đm"

**Ví dụ:**
```python
# Case 1: "đm" + "m" riêng
Input:  "đm, m ngu vcl"
Output: "đm, mày ngu vcl"
# → "đm" giữ nguyên (Nhóm 2)
# → "m" → "mày" (Nhóm 5, toxic context)

# Case 2: Chỉ có "m"
Input:  "m ngu vcl"
Output: "mày ngu vcl"
# → "m" → "mày" (Nhóm 5, toxic context)
```

---

### 3. Punctuation & Whitespace

**Punctuation:**
```python
Input:  "Video hay.Cảm ơn,bạn!"
Output: "Video hay. Cảm ơn, bạn!"
```

**Whitespace:**
```python
Input:  "Video   hay    vcl"
Output: "Video hay vcl"
```

---

## 📊 Ví dụ tổng hợp Nhóm 5

```python
# INPUT (sau Nhóm 1-4):
"confession ftu </s> đm ngu <very_intense> vcl <emo_neg> <user> Thằng Tuấn béo, t yêu m"

# ===== NHÓM 5: FINALIZATION =====

# Bước 1: Xử lý tên riêng trong comment
# → "Thằng Tuấn" → "thằng tuấn" (lowercase, không mask vì có "thằng")

# Bước 2: Context-aware "m" mapping
# → "t yêu m" → "tôi yêu em" (positive context)

# Bước 3: Punctuation
# → Thêm space sau dấu phẩy nếu cần

# Bước 4: Whitespace
# → Normalize multiple spaces

# OUTPUT CUỐI CÙNG:
"confession ftu </s> đm ngu <very_intense> vcl <emo_neg> <user> thằng tuấn béo, tôi yêu em"
```

---

## 🎯 Key Points

### 1. "đm" được xử lý ở đâu?
- **Nhóm 2:** Giữ nguyên "đm" (intensity-sensitive)
- **Nhóm 5:** KHÔNG xử lý "đm"

### 2. Tên riêng được xử lý như thế nào?
- **Nhóm 2 (NER):** Mask tên KHÔNG có đại từ xúc phạm → `<person>`
- **Nhóm 5:** Lowercase tên CÓ đại từ xúc phạm (không mask)

### 3. "m" được xử lý như thế nào?
- **Nhóm 5:** Context-aware mapping
  - Positive → "em"
  - Toxic → "mày"
  - Neutral → "mình"

---

## 📝 Cách trình bày đúng

**Khi nói về Nhóm 5:**

> "**Nhóm 5: Finalization & Smart Mapping**
> 
> Xử lý các bước cuối cùng:
> 
> 1. **Tên riêng trong comment:** Theo Guideline V7.2, nếu có đại từ xúc phạm như 'thằng Tuấn', chúng em giữ tên nhưng lowercase để model học pattern công kích cá nhân.
> 
> 2. **Context-aware 'm' mapping:** Phân biệt 'm' là 'em' (positive) hay 'mày' (toxic) dựa vào context.
> 
> 3. **Finalization:** Chuẩn hóa punctuation và whitespace."

**KHÔNG nói:**
- ❌ "đm m ngu" → "địt mẹ mày ngu" (SAI! "đm" đã giữ nguyên ở Nhóm 2)

---

## ✅ Checklist

Trước khi trình bày:

- [ ] Nhớ: "đm" được giữ nguyên ở Nhóm 2, KHÔNG xử lý ở Nhóm 5
- [ ] Nhớ: Nhóm 5 xử lý tên riêng CÓ đại từ xúc phạm
- [ ] Nhớ: "m" → "em"/"mày"/"mình" theo context
- [ ] Nhớ: Finalization = punctuation + whitespace
- [ ] KHÔNG nhầm lẫn giữa NER masking (Nhóm 2) và tên riêng trong comment (Nhóm 5)

---

**Đã sửa lại đúng! 🎯**
