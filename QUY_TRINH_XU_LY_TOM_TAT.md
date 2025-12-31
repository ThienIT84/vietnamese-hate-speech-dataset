# 🎯 QUY TRÌNH XỬ LÝ DỮ LIỆU - TÓM TẮT

## 📊 Tổng Quan

```
RAW DATA → CLEANING (5 nhóm) → WORD SEGMENT → 2 VERSIONS
```

---

## 🔄 Quy Trình Chi Tiết

### **BƯỚC 1: Thu thập & Gán nhãn**
```
Facebook/YouTube → 50,000+ comments
↓
Gán nhãn thủ công (Guideline V7.2)
↓
6,285 samples (Clean: 44%, Toxic: 26%, Hate: 29%)
```

---

### **BƯỚC 2: Gộp Title + Comment**
```python
title = "Confession FTU"
comment = "boy phố mới nhú"
↓
input = "Confession FTU </s> boy phố mới nhú"
```
⭐ Thêm separator `</s>` để model hiểu context

---

### **BƯỚC 3: Cleaning Pipeline (5 Nhóm)**

#### **Nhóm 1: Chuẩn hóa cơ bản**
```
"Video <b>hay</b> https://..." → "Video hay"
```
- Xóa: HTML, URLs, hashtags
- Giữ: Special tokens

#### **Nhóm 2: Teencode & Smart NER**
```
"ko biết, đẹp đm, @user Trần Ngọc ở Hà Nội"
→ "không biết, đẹp đm, <user> <person> ở hà nội"
```
- Chuẩn hóa: "ko" → "không"
- **BẢO TOÀN:** "đm", "vcl" (intensity-sensitive)
- Mask: Tên người → `<person>`
- Bảo vệ: 50+ họ, 63 địa danh

#### **Nhóm 3: Emoji & Emoticons**
```
"Béo như 🐷🐷🐷 😡 :))) stupid vl"
→ "Béo như lợn <intense> <emo_neg> <eng_insult> vãi lồn"
```
- Nhiều emoji → `<intense>`
- Sentiment → `<emo_pos>` / `<emo_neg>`
- English insults → `<eng_insult>` / `<eng_vulgar>`

#### **Nhóm 4: Pattern Detection**
```
"n.g.u, ch3t, nguuuuu" → "ngu, chết, ngu <very_intense>"
```
- Bypass: "n.g.u" → "ngu"
- Leetspeak: "ch3t" → "chết"
- Lặp 5+ lần → `<very_intense>`

#### **Nhóm 5: Context-Aware & Finalization**
```
"t yêu m" → "tôi yêu em"  (positive context)
"m ngu vcl" → "mày ngu vcl"  (toxic context)
```
- Context-aware "m" mapping
- Lowercase tên riêng trong comment
- Clean punctuation & spaces

---

### **BƯỚC 4: Word Segmentation (PhoBERT)**
```
"học sinh giỏi bú fame" → "học_sinh giỏi bú_fame"
```
⭐ Thêm underscore để đánh dấu compound words

---

### **BƯỚC 5: Tạo 2 Versions**

#### **Version 1: PhoBERT (READY)**
```
File: final_train_data_v3_READY.xlsx
Format: "học_sinh giỏi </s> comment"
- Có underscore
- Separator: </s>
```

#### **Version 2: ViDeBERTa (SEMANTIC)**
```
File: final_train_data_v3_SEMANTIC.xlsx
Format: "học sinh giỏi <sep> comment"
- KHÔNG underscore
- Separator: <sep>
```

---

## 🎯 Kết Quả

```
INPUT (raw):
"Confession FTU </s> Đ.m nguuuu vcl 😡 @user123 Trần Ngọc béo như 🐷🐷🐷"

↓ [5 nhóm xử lý]

OUTPUT (PhoBERT):
"confession ftu </s> đm ngu <very_intense> vcl <emo_neg> <user> <person> béo như lợn <intense>"

OUTPUT (ViDeBERTa):
"confession ftu <sep> đm ngu <very_intense> vcl <emo_neg> <user> <person> béo như lợn <intense>"
```

---

## 💡 Điểm Nổi Bật

### **1. Intensity Preservation**
```
"đm" ≠ "địt mẹ"  → Giữ nguyên để model học gradient
"nguuuu" → "ngu <very_intense>"  → Model học mức độ cảm xúc
```

### **2. Context-Aware**
```
"t yêu m" → "em"  (có "yêu" → positive)
"m ngu vcl" → "mày"  (có "ngu", "vcl" → toxic)
```

### **3. Smart NER**
```
"Trần Ngọc" → <person>  (mask tên)
"Hà Nội" → "hà nội"  (giữ địa danh - whitelist)
```

### **4. Special Tokens**
```
<person>, <user> → Privacy
<emo_pos>, <emo_neg> → Sentiment
<eng_insult>, <eng_vulgar> → English insults
</s> hoặc <sep> → Separator
<intense>, <very_intense> → Intensity
```

---

## 📝 Script Trình Bày (30 giây)

> "Quy trình xử lý của chúng em gồm 5 bước:
> 
> **1. Thu thập & gán nhãn:** 6,285 samples theo Guideline V7.2
> 
> **2. Gộp title + comment** với separator `</s>`
> 
> **3. Cleaning pipeline 5 nhóm:**
> - Chuẩn hóa cơ bản (HTML, URLs)
> - Teencode & Smart NER (50+ họ, 63 địa danh)
> - Emoji → sentiment tags + English insults
> - Pattern detection (bypass, repeated chars)
> - Context-aware mapping
> 
> **Điểm đặc biệt:** Chúng em **bảo toàn intensity** - giữ nguyên "đm", "vcl" thay vì chuẩn hóa hết, giúp model học được gradient từ nhẹ đến nặng.
> 
> **4. Word segmentation** cho PhoBERT
> 
> **5. Tạo 2 versions:** PhoBERT (có underscore) và ViDeBERTa (không underscore)
> 
> Kết quả: 6,285 samples chất lượng cao, F1-Score đạt 0.80!"

---

## ✅ Key Messages

1. **5 nhóm xử lý** thay vì 18 bước → Dễ hiểu
2. **Intensity Preservation** → Innovation chính
3. **Context-aware** → Thông minh
4. **2 versions** → Optimize cho từng model
5. **Quality over quantity** → 6,285 samples chất lượng cao

---

**Thời gian trình bày: 30 giây - 1 phút tùy chi tiết! 🎯**
