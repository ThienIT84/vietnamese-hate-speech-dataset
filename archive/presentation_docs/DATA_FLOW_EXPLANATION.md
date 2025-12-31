# 📊 Data Flow Explanation - SafeSense-VI

## ✅ QUY TRÌNH XỬ LÝ DỮ LIỆU ĐÚNG

### Bước 1: Thu thập dữ liệu RAW (Crawling)

**Nguồn:**
- Facebook Comments
- YouTube Comments

**Dữ liệu thu được:**
```python
{
    "id": "Y29tbWVudDoxMjIxNDA4...",
    "raw_title": "Boy phố \"gãy cánh\" ngay trước mặt 😂😂",
    "raw_comment": "Dm sao ko đạp cho mấy đạp nhỉ,",
    "source_platform": "Facebook",
    "timestamp": "2025-10-08 15:53:06+00:00",
    ...
}
```

**Lưu ý:**
- ❌ KHÔNG có separator `</s>` trong raw data
- ✅ Title và comment là 2 trường riêng biệt

---

### Bước 2: Gộp Title + Comment với Separator

**Code:**
```python
def prepare_input_text(title, comment):
    """
    Gộp title và comment với separator </s>
    Separator giúp model phân biệt context (title) vs content (comment)
    """
    if pd.notna(title) and title.strip():
        return f"{title.strip()} </s> {comment.strip()}"
    else:
        return comment.strip()

# Ví dụ:
title = "Boy phố \"gãy cánh\" ngay trước mặt 😂😂"
comment = "Dm sao ko đạp cho mấy đạp nhỉ,"

input_text = prepare_input_text(title, comment)
# → "Boy phố \"gãy cánh\" ngay trước mặt 😂😂 </s> Dm sao ko đạp cho mấy đạp nhỉ,"
```

**Tại sao dùng `</s>`?**
1. **Separator token chuẩn:** PhoBERT/BERT sử dụng `[SEP]`, nhưng `</s>` dễ đọc hơn
2. **Context signal:** Model học được title cung cấp context cho comment
3. **Proven approach:** Sử dụng trong nhiều NLP tasks (QA, NLI, etc.)

---

### Bước 3: Áp dụng 18-Step Cleaning Pipeline

**Input:** `"Boy phố \"gãy cánh\" ngay trước mặt 😂😂 </s> Dm sao ko đạp cho mấy đạp nhỉ,"`

**Pipeline processing:**

```python
# BƯỚC 1: Unicode Normalize
# → Chuẩn hóa dấu tiếng Việt

# BƯỚC 2: HTML/URL Removal
# → Xóa HTML tags, URLs
# ⚠️ BẢO TOÀN: </s>, <person>, <user>, <emo_pos>, <emo_neg>

# BƯỚC 3: Hashtag Removal
# → Xóa #giaothong, #xuhuong, etc.

# BƯỚC 4: Teencode Normalization
# → "ko" → "không", NHƯNG giữ "đm", "vcl" (intensity-sensitive)

# BƯỚC 5: Named Entity Masking
# → Mask tên người, username

# BƯỚC 6-8: Lowercase + Protect Tags
# → "Boy phố" → "boy phố"
# → </s> vẫn giữ nguyên

# BƯỚC 9: Emoji → Sentiment Tags
# → 😂😂 → <emo_pos>

# BƯỚC 10-18: Các bước tiếp theo
# → Emoticons, English insults, Unicode tricks, etc.
```

**Output:** `"boy phố gãy cánh ngay trước mặt <emo_pos> </s> địt mẹ sao không đạp cho mấy đạp nhỉ"`

**Lưu ý:**
- ✅ Separator `</s>` được BẢO TOÀN qua toàn bộ pipeline
- ✅ Special tokens (`<person>`, `<user>`, `<emo_pos>`, `<emo_neg>`) được bảo vệ
- ✅ Title và comment được xử lý riêng biệt nhưng vẫn giữ separator

---

### Bước 4: Word Segmentation (Cho PhoBERT)

**Input:** `"boy phố gãy cánh ngay trước mặt <emo_pos> </s> địt mẹ sao không đạp cho mấy đạp nhỉ"`

**Word segmentation:**
```python
from vncorenlp import VnCoreNLP

def word_segment(text):
    """
    PhoBERT yêu cầu word segmentation
    Bảo vệ special tokens khỏi bị segment
    """
    # Protect special tokens
    text = text.replace("</s>", "___SEP___")
    text = text.replace("<emo_pos>", "___EMO_POS___")
    text = text.replace("<emo_neg>", "___EMO_NEG___")
    text = text.replace("<person>", "___PERSON___")
    text = text.replace("<user>", "___USER___")
    
    # Segment
    segmented = rdrsegmenter.word_segment(text)
    
    # Restore special tokens
    segmented = segmented.replace("___SEP___", "</s>")
    segmented = segmented.replace("___EMO_POS___", "<emo_pos>")
    # ... restore others
    
    return segmented

output = word_segment(input_text)
# → "boy_phố gãy_cánh ngay trước_mặt <emo_pos> </s> địt_mẹ sao không đạp cho mấy đạp nhỉ"
```

**Output:** `"boy_phố gãy_cánh ngay trước_mặt <emo_pos> </s> địt_mẹ sao không đạp cho mấy đạp nhỉ"`

---

### Bước 5: Lưu vào Final Dataset

**File:** `data/final/final_train_data_v3_READY.xlsx`

**Columns:**
```
id | input_text | raw_comment | raw_title | cleaned_comment | cleaned_title | label | ...
```

**Example row:**
```python
{
    "id": "Y29tbWVudDoxMjIxNDA4...",
    "raw_title": "Boy phố \"gãy cánh\" ngay trước mặt 😂😂",
    "raw_comment": "Dm sao ko đạp cho mấy đạp nhỉ,",
    "cleaned_title": "boy phố gãy cánh ngay trước mặt <emo_pos>",
    "cleaned_comment": "địt mẹ sao không đạp cho mấy đạp nhỉ",
    "input_text": "boy_phố gãy_cánh ngay trước_mặt <emo_pos> </s> địt_mẹ sao không đạp cho mấy đạp nhỉ",
    "label": 1.0,  # Toxic
    ...
}
```

---

## 🎯 TÓM TẮT DATA FLOW

```
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 1: CRAWLING                                            │
│ Facebook/YouTube → raw_title, raw_comment (riêng biệt)     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 2: MERGE WITH SEPARATOR                                │
│ input_text = f"{title} </s> {comment}"                     │
│ ⭐ Separator </s> được THÊM VÀO ở đây                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 3: 18-STEP CLEANING PIPELINE                          │
│ - Unicode normalize                                         │
│ - HTML/URL removal (BẢO TOÀN </s>)                         │
│ - Teencode normalization (PRESERVE intensity)              │
│ - NER masking                                               │
│ - Lowercase                                                 │
│ - Emoji → sentiment tags                                    │
│ - ... 12 bước khác                                          │
│ ⭐ Separator </s> được BẢO TOÀN qua toàn bộ pipeline        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 4: WORD SEGMENTATION (PhoBERT)                        │
│ "boy phố" → "boy_phố"                                       │
│ ⭐ Bảo vệ </s> khỏi bị segment                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ BƯỚC 5: FINAL DATASET                                       │
│ final_train_data_v3_READY.xlsx (6,285 samples)             │
│ - input_text: "title_segmented </s> comment_segmented"     │
│ - label: 0/1/2                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ❌ NHẦM LẪN THƯỜNG GẶP

### Nhầm lẫn 1: "</s> có sẵn trong raw data"
**SAI:**
```python
raw_comment = "Video hay </s> comment"  # ❌ KHÔNG có </s> trong raw
```

**ĐÚNG:**
```python
raw_title = "Video hay"
raw_comment = "comment"
input_text = f"{raw_title} </s> {raw_comment}"  # ✅ Thêm </s> khi gộp
```

### Nhầm lẫn 2: "Pipeline bảo toàn </s>"
**SAI:** "Pipeline bảo toàn separator </s> từ raw data"

**ĐÚNG:** 
1. Separator `</s>` được THÊM VÀO khi gộp title + comment
2. Pipeline BẢO TOÀN separator này (không xóa) qua 18 bước

### Nhầm lẫn 3: "Cleaning trước, merge sau"
**SAI:**
```python
cleaned_title = clean(raw_title)
cleaned_comment = clean(raw_comment)
input_text = f"{cleaned_title} </s> {cleaned_comment}"  # ❌ SAI thứ tự
```

**ĐÚNG:**
```python
input_text = f"{raw_title} </s> {raw_comment}"  # Merge trước
cleaned_text = clean(input_text)  # Clean sau
```

---

## 📝 CÁCH TRÌNH BÀY TRONG PRESENTATION

### Khi nói về Data Processing:

**Script:**
> "Dữ liệu raw từ Facebook/YouTube có title và comment riêng biệt. Chúng em gộp chúng lại với separator `</s>` để model hiểu được context:
> 
> **Ví dụ:**
> - Title: 'Confession FTU'
> - Comment: 'boy phố mới nhú...'
> - Input: 'Confession FTU </s> boy phố mới nhú...'
> 
> Sau đó áp dụng 18-step cleaning pipeline, trong đó separator `</s>` được bảo toàn để model học được mối quan hệ giữa title và comment."

### Nếu BGK hỏi: "Tại sao dùng </s>?"

**Trả lời:**
> "Separator `</s>` giúp model phân biệt context (title) và content (comment). Đây là approach chuẩn trong NLP, tương tự như BERT dùng [SEP] token. 
> 
> Ví dụ: 'Confession FTU </s> boy phố...' → Model biết đây là confession post về boy phố, giúp classify chính xác hơn."

---

## ✅ CHECKLIST

Trước khi trình bày:

- [ ] Hiểu rõ: Separator `</s>` được THÊM VÀO khi gộp, không có sẵn trong raw
- [ ] Hiểu rõ: Pipeline BẢO TOÀN separator, không xóa nó
- [ ] Hiểu rõ: Thứ tự: Merge → Clean → Segment
- [ ] Có thể giải thích: Tại sao dùng `</s>`? (Context signal)
- [ ] Có thể demo: Show example với title + comment

---

**Bạn đã hiểu rõ data flow! 🎯**
