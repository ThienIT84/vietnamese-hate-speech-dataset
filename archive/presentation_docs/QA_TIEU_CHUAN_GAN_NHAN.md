# 🎯 Q&A: Tiêu Chuẩn Gán Nhãn

## ❓ Câu Hỏi: "Gán nhãn dựa trên tiêu chuẩn nào?"

---

## ✅ Câu Trả Lời Chuẩn (30 giây)

> "Chúng em gán nhãn dựa trên **Guideline V7.2 - Tiếp cận Khoa học** với triết lý cốt lõi là **'Ngữ cảnh quyết định Nhãn'** (Contextual Intelligence).
> 
> Guideline này có 3 nguyên tắc chính:
> 
> **1. Phân biệt Ý định (Intent):**
> - Tường thuật: 'Hình như bị tử hình rồi' → Clean (narrative fact)
> - Kích động: 'Nên tử hình thằng này' → Hate (incitement)
> 
> **2. Phân biệt Đối tượng (Target):**
> - Cá nhân: 'Thằng này ngu' → Toxic (personal attack)
> - Gia đình: 'Ba mẹ mày ngu' → Hate (family attack)
> 
> **3. Positive Slang:**
> - 'Giỏi vcl' → Clean (từ tục nhấn mạnh khen)
> - 'Ngu vcl' → Toxic (từ tục chửi)
> 
> Guideline có 713 dòng với hơn 100 ví dụ cụ thể, được 3 annotators áp dụng và đạt 70-75% full consensus."

---

## 📋 Câu Trả Lời Chi Tiết (Nếu Hỏi Sâu)

### **1. Nguồn Gốc Guideline**

> "Guideline V7.2 được phát triển qua nhiều vòng iteration:
> 
> - **V1-V3:** Phiên bản đầu, còn nhiều ambiguity
> - **V4-V6:** Thêm edge cases, refine rules
> - **V7.2:** Phiên bản cuối, tiếp cận khoa học với Contextual Intelligence
> 
> Guideline dài 713 dòng, bao gồm:
> - Định nghĩa 3 labels rõ ràng
> - Hơn 100 ví dụ cụ thể
> - Quy tắc xử lý edge cases
> - Decision tree cho trường hợp khó"

---

### **2. Triết Lý: 'Ngữ Cảnh Quyết Định Nhãn'**

> "Khác với các guideline truyền thống chỉ dựa vào từ khóa, chúng em áp dụng **Contextual Intelligence** - cùng một từ nhưng khác context thì khác label.
> 
> **Ví dụ 1: Từ 'tử hình'**
> - 'Hình như bị tử hình rồi' → Label 0 (Clean)
>   - Lý do: Tường thuật khách quan (narrative)
> 
> - 'Nên tử hình thằng này' → Label 2 (Hate)
>   - Lý do: Kích động bạo lực (incitement)
> 
> **Ví dụ 2: Từ 'giết'**
> - 'Coi chừng nó giết đấy' → Label 0 (Clean)
>   - Lý do: Cảnh báo nguy hiểm (risk assessment)
> 
> - 'Gặp t là t giết nó luôn' → Label 2 (Hate)
>   - Lý do: Đe dọa trực tiếp (direct threat)
> 
> Đây là điểm khác biệt lớn nhất của guideline chúng em."

---

### **3. Hệ Thống 3 Labels**

#### **Label 0: Clean / Positive Slang**

**Định nghĩa:**
> "Bình luận không có ý định xúc phạm, công kích, hoặc kích động. Bao gồm cả Positive Slang - từ tục được dùng để nhấn mạnh khen ngợi."

**Tiêu chí:**
- ✅ Tường thuật khách quan
- ✅ Cảnh báo nguy hiểm
- ✅ Phẫn nộ văn minh (không công kích cá nhân)
- ✅ Positive Slang (từ tục nhấn mạnh khen)

**Ví dụ:**
```
"Nên xử phạt nghiêm"           → Clean (phẫn nộ văn minh)
"Hình như bị tử hình rồi"      → Clean (tường thuật)
"Coi chừng nó giết đấy"        → Clean (cảnh báo)
"Giỏi vcl, đỉnh vãi"           → Clean (Positive Slang)
```

---

#### **Label 1: Toxic / Offensive**

**Định nghĩa:**
> "Bình luận có ý định xúc phạm, công kích CÁ NHÂN, nhưng chưa đến mức hate speech."

**Tiêu chí:**
- ✅ Công kích cá nhân (không gia đình)
- ✅ Chửi thề tiêu cực
- ✅ Miệt thị ngoại hình, trí tuệ
- ✅ **Pronoun Trigger:** Đại từ hạ thấp (thằng, con, mày)

**Ví dụ:**
```
"Thằng này nên đi tù"          → Toxic (pronoun trigger)
"Mày nín đi"                   → Toxic (công kích + mày)
"Ngu vcl"                      → Toxic (chửi thề tiêu cực)
"Xấu quá"                      → Toxic (miệt thị ngoại hình)
```

**Quy tắc đặc biệt: Pronoun Trigger**
```
"Nên vào tù"                   → Clean (không có đại từ)
"Thằng này nên vào tù"         → Toxic (có "thằng" → hạ thấp)
```

---

#### **Label 2: Hate Speech / Dangerous**

**Định nghĩa:**
> "Bình luận kích động bạo lực, công kích GIA ĐÌNH, phân biệt đối xử nhóm người, hoặc phi nhân hóa."

**Tiêu chí:**
- ✅ **Family Attack:** Công kích gia đình
- ✅ **Incitement:** Kích động bạo lực, tử hình
- ✅ **Identity Hate:** Phân biệt vùng miền, LGBT, tôn giáo
- ✅ **Dehumanization:** So sánh với động vật (phi nhân hóa)

**Ví dụ:**
```
"Ba mẹ mày ngu"                → Hate (family attack)
"Nên tử hình thằng này"        → Hate (incitement)
"Bắc kỳ toàn gian"             → Hate (identity hate)
"Béo như lợn"                  → Hate (dehumanization)
```

---

### **4. Quy Tắc Đặc Biệt (Edge Cases)**

#### **A. Positive Slang**

**Nguyên tắc:**
> "Từ tục được dùng để NHẤN MẠNH KHEN NGỢI → Clean"

**Ví dụ:**
```
"Giỏi vcl"                     → Clean (khen + vcl)
"Đỉnh vãi"                     → Clean (khen + vãi)
"Hay đm luôn"                  → Clean (khen + đm)

VS

"Ngu vcl"                      → Toxic (chửi + vcl)
"Xấu vãi"                      → Toxic (chửi + vãi)
```

**Cách phân biệt:**
- Từ trước "vcl/vãi/đm" là khen (giỏi, đỉnh, hay) → Clean
- Từ trước "vcl/vãi/đm" là chửi (ngu, xấu, dở) → Toxic

---

#### **B. Pronoun Trigger**

**Nguyên tắc:**
> "Đại từ hạ thấp (thằng, con, mày) + hành động tiêu cực → Toxic"

**Ví dụ:**
```
"Nên vào tù"                   → Clean (không có đại từ)
"Thằng này nên vào tù"         → Toxic (có "thằng")

"Bạn tôi"                      → Clean (thân mật)
"Thằng bạn tôi"                → Clean (thân mật, không tiêu cực)
"Thằng này ngu"                → Toxic (hạ thấp + tiêu cực)
```

---

#### **C. Narrative vs Incitement**

**Nguyên tắc:**
> "Tường thuật khách quan → Clean | Kích động chủ quan → Hate"

**Ví dụ:**
```
"Hình như bị tử hình rồi"      → Clean (narrative - quá khứ)
"Nên tử hình thằng này"        → Hate (incitement - tương lai)

"Nghe nói bị giết"             → Clean (narrative)
"Nên giết nó đi"               → Hate (incitement)
```

**Cách phân biệt:**
- Quá khứ/hiện tại + khách quan → Clean
- Tương lai + chủ quan (nên, phải) → Hate

---

#### **D. Risk Assessment vs Threat**

**Nguyên tắc:**
> "Cảnh báo nguy hiểm → Clean | Đe dọa trực tiếp → Hate"

**Ví dụ:**
```
"Coi chừng nó giết đấy"        → Clean (cảnh báo người khác)
"Gặp t là t giết nó"           → Hate (đe dọa từ bản thân)

"Cẩn thận bị đánh"             → Clean (cảnh báo)
"Tao đánh mày"                 → Hate (đe dọa)
```

---

### **5. Quy Trình Gán Nhãn**

**Bước 1: Training (1-2 tuần)**
> "3 annotators học Guideline V7.2, làm quen với 100+ ví dụ"

**Bước 2: Round 1 - Independent Annotation**
> "Mỗi người gán nhãn độc lập, không trao đổi"

**Bước 3: Discussion Meeting**
> "Team họp để thảo luận các trường hợp disagreement:
> - Positive Slang vs Profanity
> - Narrative vs Incitement
> - Pronoun Trigger cases
> - Edge cases khó"

**Bước 4: Consensus**
> "Đạt được thống nhất qua discussion, resolve disagreements"

**Bước 5: Final Review**
> "Quality check toàn bộ dataset, đảm bảo consistency"

**Kết quả:**
> "70-75% full consensus (3 người đồng thuận hoàn toàn)"

---

### **6. So Sánh Với Các Guideline Khác**

| Aspect | Guideline Truyền Thống | Guideline V7.2 (Ours) |
|--------|------------------------|------------------------|
| **Approach** | Keyword-based | Context-based |
| **Positive Slang** | ❌ Không xử lý | ✅ Xử lý riêng |
| **Pronoun Trigger** | ❌ Không có | ✅ Có quy tắc rõ |
| **Narrative vs Incitement** | ❌ Không phân biệt | ✅ Phân biệt rõ |
| **Edge Cases** | ❌ Ít | ✅ 100+ ví dụ |
| **Length** | ~100 dòng | 713 dòng |

**Ví dụ so sánh:**

**Guideline truyền thống:**
```
"tử hình" → Hate (keyword-based)
```

**Guideline V7.2:**
```
"Hình như bị tử hình rồi" → Clean (narrative)
"Nên tử hình thằng này" → Hate (incitement)
```

---

## 🎯 Key Messages Khi Trả Lời

### **Message 1: Khoa học & Có hệ thống**
> "Guideline V7.2 - 713 dòng, 100+ ví dụ, tiếp cận khoa học"

### **Message 2: Contextual Intelligence**
> "Ngữ cảnh quyết định nhãn - cùng từ nhưng khác context thì khác label"

### **Message 3: Xử lý Edge Cases**
> "Positive Slang, Pronoun Trigger, Narrative vs Incitement - các guideline khác không có"

### **Message 4: Quality Assurance**
> "70-75% full consensus qua multiple rounds of review"

---

## 📝 Script Trả Lời Mẫu

### **Version Ngắn (30 giây):**

> "Chúng em gán nhãn theo **Guideline V7.2** với triết lý **'Ngữ cảnh quyết định Nhãn'**. 
> 
> Ví dụ: 'Hình như bị tử hình rồi' → Clean (tường thuật), nhưng 'Nên tử hình thằng này' → Hate (kích động).
> 
> Guideline có 713 dòng với 100+ ví dụ, xử lý các edge cases như Positive Slang ('Giỏi vcl' → Clean) và Pronoun Trigger ('Thằng này nên tù' → Toxic).
> 
> 3 annotators áp dụng và đạt 70-75% full consensus."

---

### **Version Dài (1-2 phút):**

> "Chúng em phát triển **Guideline V7.2 - Tiếp cận Khoa học** với triết lý cốt lõi là **Contextual Intelligence** - ngữ cảnh quyết định nhãn.
> 
> **3 nguyên tắc chính:**
> 
> **1. Phân biệt Ý định:**
> - Tường thuật: 'Hình như bị tử hình rồi' → Clean
> - Kích động: 'Nên tử hình thằng này' → Hate
> 
> **2. Phân biệt Đối tượng:**
> - Cá nhân: 'Thằng này ngu' → Toxic
> - Gia đình: 'Ba mẹ mày ngu' → Hate
> 
> **3. Positive Slang:**
> - 'Giỏi vcl' → Clean (từ tục nhấn mạnh khen)
> - 'Ngu vcl' → Toxic (từ tục chửi)
> 
> Guideline dài 713 dòng với hơn 100 ví dụ cụ thể, xử lý các edge cases mà guideline truyền thống không có như Pronoun Trigger, Narrative vs Incitement.
> 
> **Quy trình gán nhãn:**
> - 3 annotators training với guideline
> - Round 1: Gán nhãn độc lập
> - Discussion: Resolve disagreements
> - Final review: Quality check
> 
> Kết quả: 70-75% full consensus, đảm bảo chất lượng cao."

---

## ✅ Checklist Trước Khi Trả Lời

- [ ] Nhớ: "Guideline V7.2 - Tiếp cận Khoa học"
- [ ] Nhớ: "Ngữ cảnh quyết định Nhãn" (Contextual Intelligence)
- [ ] Nhớ: 3 nguyên tắc (Ý định, Đối tượng, Positive Slang)
- [ ] Nhớ: Ví dụ "tử hình" (narrative vs incitement)
- [ ] Nhớ: 713 dòng, 100+ ví dụ
- [ ] Nhớ: 70-75% full consensus
- [ ] Tự tin: Guideline này khoa học và có hệ thống

---

**Bạn đã sẵn sàng trả lời câu hỏi này! 🎯**
