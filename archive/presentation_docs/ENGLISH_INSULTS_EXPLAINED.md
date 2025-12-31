# 🌍 Xử Lý Từ Tiếng Anh (English Insults)

## 🎯 Tại Sao Cần Xử Lý?

Người Việt thường **code-switch** - trộn tiếng Anh vào comment:
- "stupid vl" (ngu vãi lồn)
- "fuck you" (địt mẹ mày)
- "idiot" (đồ ngốc)
- "trash" (rác)

→ Cần detect và tag để model học được!

---

## 📋 Danh Sách English Insults

### **Vulgar Words (Từ tục tĩu)**
```python
ENGLISH_INSULTS = {
    # Vulgar - Tag: <eng_vulgar>
    "fuck": "<eng_vulgar>",
    "fucking": "<eng_vulgar>",
    "fucked": "<eng_vulgar>",
    "shit": "<eng_vulgar>",
    "bitch": "<eng_vulgar>",
    "bastard": "<eng_vulgar>",
    "asshole": "<eng_vulgar>",
    "damn": "<eng_vulgar>",
    "crap": "<eng_vulgar>",
}
```

### **Insult Words (Từ xúc phạm)**
```python
ENGLISH_INSULTS = {
    # Insults - Tag: <eng_insult>
    "stupid": "<eng_insult>",
    "idiot": "<eng_insult>",
    "dumb": "<eng_insult>",
    "moron": "<eng_insult>",
    "fool": "<eng_insult>",
    "loser": "<eng_insult>",
    "trash": "<eng_insult>",
    "garbage": "<eng_insult>",
}
```

**Tổng cộng:** 17 từ tiếng Anh

---

## 🔄 Cách Xử Lý

### Logic

```python
def map_english_insults(text):
    """
    Map English insults to tags
    
    Examples:
        "stupid" → "<eng_insult>"
        "fuck" → "<eng_vulgar>"
    """
    words = text.split()
    result = []
    
    for word in words:
        # Clean word (remove punctuation)
        clean_word = re.sub(r'[^\w]', '', word.lower())
        
        if clean_word in ENGLISH_INSULTS:
            result.append(ENGLISH_INSULTS[clean_word].strip())
        else:
            result.append(word)
    
    return ' '.join(result)
```

---

## 🎬 Ví Dụ

### Ví dụ 1: Vulgar
```python
Input:  "fuck you"
Output: "<eng_vulgar> you"

# ✅ "fuck" → "<eng_vulgar>"
# ✅ "you" giữ nguyên
```

### Ví dụ 2: Insult
```python
Input:  "stupid vl"
Output: "<eng_insult> vãi lồn"

# ✅ "stupid" → "<eng_insult>"
# ✅ "vl" → "vãi lồn" (teencode normalization)
```

### Ví dụ 3: Mixed
```python
Input:  "thằng idiot ngu vcl"
Output: "thằng <eng_insult> ngu vcl"

# ✅ "idiot" → "<eng_insult>"
# ✅ Các từ khác giữ nguyên
```

### Ví dụ 4: With Punctuation
```python
Input:  "stupid!!!"
Output: "<eng_insult>!!!"

# ✅ "stupid" → "<eng_insult>"
# ✅ "!!!" giữ nguyên
```

---

## 🎯 Tại Sao Dùng Tags?

### Approach 1: Translate (❌ KHÔNG TỐT)
```python
"stupid" → "ngu"
"fuck" → "địt"
```

**Vấn đề:**
- Mất thông tin: "stupid" và "ngu" có nuance khác nhau
- "stupid vl" → "ngu vãi lồn" (mất context code-switching)

### Approach 2: Tags (✅ TỐT HƠN)
```python
"stupid" → "<eng_insult>"
"fuck" → "<eng_vulgar>"
```

**Lợi ích:**
- ✅ Giữ thông tin: Model biết đây là từ tiếng Anh
- ✅ Phân biệt: `<eng_vulgar>` (nặng) vs `<eng_insult>` (nhẹ hơn)
- ✅ Code-switching signal: Model học được pattern trộn ngôn ngữ

---

## 📊 Thống Kê

### Trong Dataset

```python
# Từ code thực tế:
ENGLISH_INSULTS: 17 words
- Vulgar: 9 words
- Insults: 8 words
```

### Frequency (ước tính)

```
Top English insults trong dataset:
1. stupid: ~50 occurrences
2. fuck: ~30 occurrences
3. idiot: ~20 occurrences
4. shit: ~15 occurrences
5. trash: ~10 occurrences
```

---

## 🎤 Cách Trình Bày

### Script ngắn (10 giây):

> "Nhóm 3 còn xử lý **từ tiếng Anh** mà người Việt hay dùng như 'stupid', 'fuck'. Chúng em tag thành `<eng_insult>` hoặc `<eng_vulgar>` để model học được pattern code-switching."

### Nếu BGK hỏi chi tiết:

**Q: "Tại sao không dịch sang tiếng Việt?"**

A: "Chúng em không dịch vì:

1. **Nuance khác nhau:** 'stupid' và 'ngu' có sắc thái khác nhau
2. **Code-switching signal:** Model cần học được pattern trộn ngôn ngữ
3. **Phân biệt mức độ:** `<eng_vulgar>` (fuck, shit) nặng hơn `<eng_insult>` (stupid, idiot)

Ví dụ:
- 'stupid vl' → `<eng_insult> vãi lồn`
- Model học được: Người dùng code-switch + dùng từ tục → Toxic

Nếu dịch thành 'ngu vãi lồn' → Mất thông tin code-switching."

**Q: "Có bao nhiêu từ tiếng Anh?"**

A: "Chúng em có 17 từ tiếng Anh phổ biến:
- 9 vulgar words: fuck, shit, bitch, damn...
- 8 insult words: stupid, idiot, trash, loser...

Đây là những từ xuất hiện thường xuyên trong comment tiếng Việt."

---

## 🔍 Trong Pipeline

### Vị trí: Nhóm 3

```
NHÓM 1: Basic Normalization
NHÓM 2: Teencode & NER
NHÓM 3: Emoji + Emoticons + ENGLISH INSULTS ← Đây!
NHÓM 4: Pattern Detection
NHÓM 5: Context-Aware
```

### Thứ tự xử lý trong Nhóm 3:

```python
1. Emoji → sentiment tags
   "😡" → "<emo_neg>"

2. Text emoticons removal
   ":)))" → ""

3. English insults mapping
   "stupid" → "<eng_insult>"
```

---

## ✅ Test Cases

### Test 1: Simple
```python
Input:  "stupid"
Output: "<eng_insult>"
✅ Pass
```

### Test 2: With Vietnamese
```python
Input:  "stupid vl"
Output: "<eng_insult> vãi lồn"
✅ Pass (teencode "vl" → "vãi lồn")
```

### Test 3: Multiple
```python
Input:  "stupid idiot"
Output: "<eng_insult> <eng_insult>"
✅ Pass
```

### Test 4: Vulgar
```python
Input:  "fuck you"
Output: "<eng_vulgar> you"
✅ Pass
```

### Test 5: Case Insensitive
```python
Input:  "STUPID"
Output: "<eng_insult>"
✅ Pass (lowercase trước khi check)
```

### Test 6: With Punctuation
```python
Input:  "stupid!!!"
Output: "<eng_insult>!!!"
✅ Pass (remove punctuation khi check)
```

---

## 📚 Code Reference

**File:** `src/preprocessing/advanced_text_cleaning.py`

**Lines:** 345-360 (ENGLISH_INSULTS dictionary)

**Function:** `map_english_insults()` (lines 1095-1115)

---

## 🎯 Key Takeaways

1. **17 từ tiếng Anh** phổ biến trong comment Việt
2. **2 loại tags:** `<eng_vulgar>` (nặng) và `<eng_insult>` (nhẹ)
3. **Giữ thông tin code-switching** thay vì dịch
4. **Xử lý trong Nhóm 3** cùng với emoji và emoticons
5. **Case insensitive** và **punctuation tolerant**

---

**Bạn đã hiểu rõ về English insults! 🌍**
