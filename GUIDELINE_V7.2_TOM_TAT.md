# 📋 GUIDELINE V7.2 - TÓM TẮT NHANH

## 🎯 Triết Lý Cốt Lõi

**"NGỮ CẢNH QUYẾT ĐỊNH NHÃN"** (Contextual Intelligence)

→ Cùng từ, khác context → Khác label

---

## 📊 3 Nguyên Tắc Chính

### **1. Phân Biệt Ý Định**
```
"Hình như bị tử hình rồi"  → Clean (tường thuật)
"Nên tử hình thằng này"    → Hate (kích động)
```

### **2. Phân Biệt Đối Tượng**
```
"Thằng này ngu"            → Toxic (cá nhân)
"Ba mẹ mày ngu"            → Hate (gia đình)
```

### **3. Positive Slang**
```
"Giỏi vcl"                 → Clean (khen + vcl)
"Ngu vcl"                  → Toxic (chửi + vcl)
```

---

## 🏷️ 3 Labels

### **Label 0: Clean**
- Tường thuật khách quan
- Cảnh báo nguy hiểm
- Phẫn nộ văn minh
- **Positive Slang**

### **Label 1: Toxic**
- Công kích cá nhân
- Chửi thề tiêu cực
- Miệt thị
- **Pronoun Trigger** (thằng, mày)

### **Label 2: Hate**
- **Family Attack**
- **Incitement** (kích động)
- **Identity Hate** (vùng miền, LGBT)
- **Dehumanization** (phi nhân hóa)

---

## 🎯 Quy Tắc Đặc Biệt

### **Positive Slang**
```
Từ khen + vcl/vãi/đm → Clean
Từ chửi + vcl/vãi/đm → Toxic
```

### **Pronoun Trigger**
```
"Nên vào tù"               → Clean
"Thằng này nên vào tù"     → Toxic (có "thằng")
```

### **Narrative vs Incitement**
```
Quá khứ + khách quan       → Clean
Tương lai + chủ quan       → Hate
```

### **Risk Assessment vs Threat**
```
"Coi chừng nó giết"        → Clean (cảnh báo)
"Gặp t là t giết"          → Hate (đe dọa)
```

---

## 📝 Script Trả Lời (30 giây)

> "Chúng em gán nhãn theo **Guideline V7.2** với triết lý **'Ngữ cảnh quyết định Nhãn'**.
> 
> **3 nguyên tắc:**
> 1. Phân biệt ý định: Tường thuật vs Kích động
> 2. Phân biệt đối tượng: Cá nhân vs Gia đình
> 3. Positive Slang: 'Giỏi vcl' (Clean) vs 'Ngu vcl' (Toxic)
> 
> Guideline có **713 dòng, 100+ ví dụ**, xử lý edge cases như Pronoun Trigger và Narrative vs Incitement.
> 
> Kết quả: **70-75% full consensus** từ 3 annotators."

---

## 📚 Thông Tin

- **File:** `TOXIC_COMMENT/guiline/guidline.txt`
- **Độ dài:** 713 dòng
- **Ví dụ:** 100+ cases
- **Annotators:** 3 người
- **Consensus:** 70-75% full agreement

---

## ✅ Key Messages

1. **Khoa học:** 713 dòng, 100+ ví dụ
2. **Context-based:** Ngữ cảnh quyết định nhãn
3. **Edge cases:** Positive Slang, Pronoun Trigger
4. **Quality:** 70-75% consensus

---

**Nhớ 3 ví dụ này là đủ! 🎯**

1. "Hình như bị tử hình" → Clean (narrative)
2. "Nên tử hình thằng này" → Hate (incitement)
3. "Giỏi vcl" → Clean (Positive Slang)
