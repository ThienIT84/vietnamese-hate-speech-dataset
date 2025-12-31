# 🎯 Context-Aware "m" Mapping - Chi tiết Logic

## Câu hỏi: Phân biệt "em" hay "mày" dựa trên gì?

**Trả lời:** Dựa trên **từ xung quanh** (context words) trong cửa sổ 3 từ trước và 3 từ sau "m"

---

## 📊 Logic từ Code

### Bước 1: Kiểm tra Context Window

```python
def context_aware_m_mapping(text):
    words = text.split()
    
    for i, word in enumerate(words):
        if word == 'm':
            # Lấy 3 từ trước và 3 từ sau
            context_start = max(0, i - 3)
            context_end = min(len(words), i + 4)
            context_words = set(words[context_start:i] + words[i+1:context_end])
            
            # Kiểm tra context
            if context_words & TOXIC_CONTEXT:
                → "mày"
            elif context_words & POSITIVE_CONTEXT:
                → "em"
            else:
                → "mình" (neutral)
```

---

## 📚 Danh sách Context Words

### POSITIVE_CONTEXT (15 từ)
```python
{
    'yêu', 'thương', 'nhớ', 'anh', 'em', 'iu', 'thích', 'quý',
    'tình', 'cưng', 'baby', 'honey', 'dear', 'love', 'like',
    'miss', 'care', 'hôn', 'ôm', 'yêu thương', 'quan tâm',
    'vô cùng', 'nhiều lắm', 'lắm',
}
```

**Ý nghĩa:** Từ thể hiện tình cảm tích cực, yêu thương

---

### TOXIC_CONTEXT (25+ từ)
```python
{
    'địt', 'đm', 'dm', 'ngu', 'lồn', 'vcl', 'vl', 'đéo', 'deo',
    'cặc', 'cc', 'đít', 'chết', 'giết', 'mẹ', 'má', 'điên',
    'khùng', 'óc chó', 'óc lợn', 'rác', 'phế', 'xấu', 'chó',
    'lợn', 'heo', 'đần', 'ngáo', 'stupid', 'idiot', 'fuck',
    'vãi lồn', 'vãi', 'ngu lồn',
}
```

**Ý nghĩa:** Từ chửi thề, xúc phạm, công kích

---

## 🎬 Ví dụ Chi tiết

### Ví dụ 1: Positive Context → "em"

```python
Input: "t yêu m vô cùng"

# Phân tích:
# - "m" ở vị trí index 2
# - Context window: ["t", "yêu"] (trước) + ["vô", "cùng"] (sau)
# - Context words: {"t", "yêu", "vô", "cùng"}
# - Check: {"yêu", "vô", "cùng"} ∩ POSITIVE_CONTEXT = {"yêu", "vô cùng"} ✅
# - Kết quả: "m" → "em"

Output: "tôi yêu em vô cùng"
```

---

### Ví dụ 2: Toxic Context → "mày"

```python
Input: "m ngu vcl"

# Phân tích:
# - "m" ở vị trí index 0
# - Context window: [] (trước) + ["ngu", "vcl"] (sau)
# - Context words: {"ngu", "vcl"}
# - Check: {"ngu", "vcl"} ∩ TOXIC_CONTEXT = {"ngu", "vcl"} ✅
# - Kết quả: "m" → "mày"

Output: "mày ngu vcl"
```

---

### Ví dụ 3: Neutral Context → "mình"

```python
Input: "m đi đâu"

# Phân tích:
# - "m" ở vị trí index 0
# - Context window: [] (trước) + ["đi", "đâu"] (sau)
# - Context words: {"đi", "đâu"}
# - Check TOXIC: {"đi", "đâu"} ∩ TOXIC_CONTEXT = {} ❌
# - Check POSITIVE: {"đi", "đâu"} ∩ POSITIVE_CONTEXT = {} ❌
# - Kết quả: "m" → "mình" (default)

Output: "mình đi đâu"
```

---

### Ví dụ 4: Mixed Context (Toxic Priority)

```python
Input: "đm m yêu vcl"

# Phân tích:
# - "m" ở vị trí index 1
# - Context window: ["đm"] (trước) + ["yêu", "vcl"] (sau)
# - Context words: {"đm", "yêu", "vcl"}
# - Check TOXIC: {"đm", "vcl"} ∩ TOXIC_CONTEXT = {"đm", "vcl"} ✅
# - Kết quả: "m" → "mày" (toxic có priority cao hơn)

Output: "đm mày yêu vcl"
```

**⚠️ Lưu ý:** Toxic context có **priority cao hơn** positive context!

---

## 🎯 Tại sao cách này hiệu quả?

### 1. Simple but Effective
- Không cần deep learning model
- Chỉ cần check từ xung quanh
- Nhanh, không tốn tài nguyên

### 2. Context-Aware
- "t yêu m" → "em" (tình cảm)
- "m ngu vcl" → "mày" (xúc phạm)
- Phân biệt chính xác dựa vào ngữ cảnh

### 3. Robust
- Cửa sổ 3 từ trước + 3 từ sau = đủ context
- Toxic priority → tránh false positive
- Default "mình" → an toàn cho trường hợp ambiguous

---

## 📊 Thống kê từ Code

```python
POSITIVE_CONTEXT: 24 từ
TOXIC_CONTEXT: 25+ từ
Context window: 3 từ trước + 3 từ sau = 6 từ
Priority: TOXIC > POSITIVE > NEUTRAL
```

---

## 🎤 Cách trình bày trong Presentation

### Script ngắn gọn (20 giây):

> "**Nhóm 5** có context-aware mapping cho từ 'm'. Chúng em kiểm tra 3 từ trước và 3 từ sau 'm':
> 
> - Nếu có từ toxic như 'ngu', 'vcl' → 'm' thành 'mày'
> - Nếu có từ positive như 'yêu', 'thương' → 'm' thành 'em'
> - Không có gì → 'm' thành 'mình'
> 
> Ví dụ: 't yêu m' → 'tôi yêu em', nhưng 'm ngu vcl' → 'mày ngu vcl'."

### Nếu BGK hỏi chi tiết:

**Q: "Làm sao phân biệt positive và toxic?"**

A: "Chúng em có 2 danh sách:
- **POSITIVE_CONTEXT:** 24 từ như 'yêu', 'thương', 'nhớ', 'thích'...
- **TOXIC_CONTEXT:** 25+ từ như 'ngu', 'vcl', 'lồn', 'đm'...

Kiểm tra 3 từ trước và 3 từ sau 'm', nếu match với danh sách nào thì map theo đó. Toxic có priority cao hơn để tránh false positive."

**Q: "Tại sao không dùng model?"**

A: "Rule-based approach này:
1. **Nhanh hơn:** Không cần load model
2. **Chính xác hơn:** Dựa trên từ điển cụ thể cho tiếng Việt
3. **Dễ debug:** Biết chính xác tại sao map như vậy
4. **Không cần training data:** Chỉ cần define danh sách từ"

---

## ✅ Key Takeaways

1. **Context window:** 3 từ trước + 3 từ sau
2. **2 danh sách:** POSITIVE_CONTEXT (24 từ) + TOXIC_CONTEXT (25+ từ)
3. **Priority:** TOXIC > POSITIVE > NEUTRAL
4. **Default:** "mình" (an toàn)
5. **Simple but effective:** Rule-based, không cần model

---

**Bạn đã hiểu rõ logic! 🎯**
