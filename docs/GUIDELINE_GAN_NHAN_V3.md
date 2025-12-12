# HƯỚNG DẪN GẮN NHÃN DỮ LIỆU (DATA LABELING GUIDELINE)
**Dự án:** Phát hiện Toxic Comment & Hate Speech tiếng Việt  
**Phiên bản:** 3.0 (Tối ưu hóa cho 3 nhãn + Topic)  
**Mục tiêu Cohen's Kappa:** ≥ 0.75

---

## 1. NGUYÊN TẮC ƯU TIÊN (QUAN TRỌNG NHẤT)

### 📌 Quy tắc vàng: Chọn nhãn NẶNG NHẤT
```
Nhãn 2 (Nặng nhất) → Nhãn 1 → Nhãn 0 (Nhẹ nhất)
```

**Ví dụ:**
- *"Địt mẹ (1) thằng bắc kỳ (2)"* → Có cả 1 và 2 → **Chọn Nhãn 2, Topic: Region**
- *"Mày béo như lợn (2) đm (1)"* → **Chọn Nhãn 2, Topic: Body**

---

## 2. CHI TIẾT CÁC NHÃN

### 🟢 Nhãn 0: CLEAN (Sạch / An toàn)

**Định nghĩa:** Bình luận không chứa từ ngữ tục tĩu, không tấn công/xúc phạm ai.

**Bao gồm:**
- ✅ Lời khen, hỏi đáp, chia sẻ ý kiến lịch sự
- ✅ Spam quảng cáo (không có từ tục)
- ✅ Chê bai/góp ý nhẹ nhàng với từ ngữ văn minh
- ✅ Tranh luận nhưng không có từ bậy, không xúc phạm
- ✅ Đá đểu/mỉa mai tinh tế (không có từ tục)

**Ví dụ:**
```
✅ "Video này hay quá, cảm ơn bạn!"
✅ "Mình không đồng ý với quan điểm này"
✅ "Chất lượng video chưa được tốt lắm"
✅ "Bạn nên tìm hiểu kỹ trước khi bình luận nhé"
✅ "Thật là một ý kiến thú vị" (mỉa mai nhưng lịch sự)
```

**❌ KHÔNG phải Nhãn 0:**
```
❌ "Bạn ngu thật đấy" → Nhãn 1 (có "ngu")
❌ "Ngon vãi" → Nhãn 1 (có từ tục "vãi")
❌ "Mày béo vậy" → Nhãn 2, Topic: Body
```

---

### 🟡 Nhãn 1: OFFENSIVE (Thô lỗ / Chửi thề / Xúc phạm chung)

**Định nghĩa:** Có từ ngữ thô tục, chửi thề hoặc xúc phạm cá nhân, NHƯNG không liên quan đến các chủ đề nhạy cảm (vùng miền, giới tính, ngoại hình, gia đình, bạo lực).

**Dấu hiệu nhận diện:**

#### 1️⃣ Chửi thề (Profanity)
Từ khóa: `đm, dm, vcl, vl, vãi, đéo, deo, cút, cc, lồn, lon, cặc, đít, cứt, shit, fuck`

```
✅ "Đm dở quá"
✅ "Vcl làm gì thế này"
✅ "Đéo hiểu luôn"
✅ "Vãi cả lồn"
```

#### 2️⃣ Xúc phạm cá nhân chung chung
Từ khóa: `ngu, ngốc, đần, điên, khùng, ngáo, dở hơi, mất dạy, hâm, rác, phế, óc chó, óc lợn`

```
✅ "Mày ngu thật"
✅ "Thằng này điên à"
✅ "Đồ mất dạy"
✅ "Rác thật sự"
```

#### 3️⃣ "Khen tục" (Vẫn là Nhãn 1)
**Lý do:** Model cần lọc mọi từ tục, dù không có ý tấn công.

```
✅ "Ngon vãi l*"
✅ "Đỉnh vcl"
✅ "Hay đm"
```

#### 4️⃣ Chửi chung chung (không rõ mục tiêu)
```
✅ "Đm trời mưa quá" (chỉ bày tỏ cảm xúc)
✅ "Vl ngày hôm nay" (không chửi ai cụ thể)
```

**❌ KHÔNG phải Nhãn 1:**
```
❌ "Mày béo như lợn" → Nhãn 2, Topic: Body
❌ "Bắc kỳ ngu" → Nhãn 2, Topic: Region
❌ "Mẹ mày dạy gì" → Nhãn 2, Topic: Family
❌ "Chết đi" → Nhãn 2, Topic: Violence
```

---

### 🔴 Nhãn 2: HATE SPEECH & DANGEROUS (Thù ghét & Nguy hiểm)

**Định nghĩa:** Tấn công vào các đặc điểm được bảo vệ HOẶC đe dọa an toàn/tính mạng.

**⚠️ QUY TẮC BẮT BUỘC:** Khi chọn Nhãn 2, PHẢI điền cột **Topic**.

---

#### 📍 **Topic 1: REGION** (Vùng miền / Chính trị)

**Định nghĩa:** Phân biệt, kỳ thị dựa trên nơi sinh sống, quê quán, chính kiến.

**Từ khóa:**
```
bắc kỳ, nam kỳ, parky, 3 que, bò đỏ, rau muống, cá rô,
dân bắc, dân nam, miền bắc ngu, miền nam, sài gòn, hà nội (khi dùng xúc phạm),
cộng sản, phản động, việt cộng (khi kèm từ xúc phạm)
```

**Ví dụ:**
```
🔴 "Bắc kỳ chó toàn lũ lừa đảo"
🔴 "Dân miền Nam ăn bám hết"
🔴 "3 que ngu như cc"
🔴 "Bọn rau muống về bắc đi"
🔴 "Giọng Sài Gòn nghe phát ói"
```

**✅ KHÔNG phải Region:**
```
✅ "Tôi sống ở Hà Nội" → Nhãn 0 (chỉ nói sự thật)
✅ "Miền Bắc thời tiết lạnh" → Nhãn 0 (không xúc phạm)
```

---

#### 📍 **Topic 2: BODY** (Ngoại hình / Body Shaming)

**Định nghĩa:** Chê bai, xúc phạm dựa trên ngoại hình, cân nặng, chiều cao, màu da, đặc điểm cơ thể.

**Từ khóa:**
```
béo, mập, heo, lợn, bò, voi,
gầy, que củi, xương, sọ,
lùn, tí hon, lê la,
xấu, thảm họa, tởm, dị hợm, mặt rỗ, mụn,
đen, da đen như than, trắng bệch,
phẫu thuật thẩm mỹ, dao kéo, mặt giả
```

**Ví dụ:**
```
🔴 "Con này béo như lợn, nhìn tởm"
🔴 "Gầy như que củi vậy"
🔴 "Lùn mà hay ra oai"
🔴 "Xấu như ma, đi phẫu thuật đi"
🔴 "Đen thui xì xấu vl"
🔴 "Mặt dao kéo kinh"
```

---

#### 📍 **Topic 3: GENDER** (Giới tính / LGBTQ+)

**Định nghĩa:** Kỳ thị dựa trên giới tính, xu hướng tình dục, bản dạng giới.

**Từ khóa:**
```
# LGBTQ+
bê đê, gay, đồng tính, bóng, pê đê, thằng bóng,
les, lesbian, đồng tính nữ,
bóng chó, thằng này là bê đê,

# Kỳ thị nữ
đàn bà, con gái (khi xúc phạm), đĩ, điếm, phò, cave,
gái là phải, đàn bà miệng loa,

# Kỳ thị nam
đàn ông vô dụng, thằng đàn ông (xúc phạm)
```

**Ví dụ:**
```
🔴 "Thứ bê đê tởm lợm"
🔴 "Bóng chó ra đường coi chừng"
🔴 "Con gái VN toàn đĩ"
🔴 "Đàn bà miệng hôi"
🔴 "Thằng đồng tính bệnh hoạn"
```

**✅ KHÔNG phải Gender:**
```
✅ "Tôi là nam/nữ" → Nhãn 0
✅ "Cộng đồng LGBTQ+" → Nhãn 0 (trung lập)
```

---

#### 📍 **Topic 4: FAMILY** (Gia đình)

**Định nghĩa:** Xúc phạm, lôi kéo gia đình người khác vào.

**⚠️ LƯU Ý QUAN TRỌNG:**
- ✅ **Nhãn 2, Topic: Family** → Khi xúc phạm GIA ĐÌNH người nghe
- ❌ **Nhãn 1** → Các từ như "đm", "vcl", "đcm" (chỉ là chửi thề, không nhắm gia đình)

**Từ khóa ĐÚNG cho Topic Family:**
```
cả nhà mày, bố mày, mẹ mày (khi xúc phạm gia đình),
cả lò, dòng họ, tổ tông, ông bà,
bố mày chết rồi à, mẹ mày dạy gì, gia đình mày
```

**Ví dụ:**
```
🔴 "Cả nhà mày toàn đồ rác" (Topic: Family)
🔴 "Bố mày chết rồi mà còn nói" (Topic: Family)
🔴 "Mẹ mày dạy con kiểu gì vậy" (Topic: Family)
🔴 "Cả dòng họ mày phải xấu hổ" (Topic: Family)
```

**✅ KHÔNG phải Topic Family (Chỉ là chửi thề → Nhãn 1):**
```
✅ "Đm làm gì thế" → Nhãn 1 (chỉ là từ chửi thề)
✅ "Vcl ngu quá" → Nhãn 1
✅ "Đcm dở thật" → Nhãn 1
```

---

#### 📍 **Topic 5: DISABILITY** (Khuyết tật / Trí tuệ)

**Định nghĩa:** Kỳ thị người khuyết tật về thể chất hoặc trí tuệ.

**Từ khóa:**
```
# Khuyết tật trí tuệ
thiểu năng, down, bại não, tự kỷ, autism, retard,
não cá vàng, não tôm,

# Khuyết tật thể chất
câm, điếc, đui, mù, què, liệt,
tàn tật, khuyết tật (khi xúc phạm)
```

**Ví dụ:**
```
🔴 "Mày thiểu năng à?"
🔴 "Não cá vàng đấy à"
🔴 "Bại não mới làm thế"
🔴 "Câm đi thằng ngu"
```

**✅ KHÔNG phải Disability:**
```
✅ "Tôi bị cận thị" → Nhãn 0 (tự nói về mình)
✅ "Hỗ trợ người khuyết tật" → Nhãn 0 (trung lập)
```

---

#### 📍 **Topic 6: VIOLENCE** (Bạo lực / Đe dọa)

**Định nghĩa:** Đe dọa, kích động bạo lực hoặc tự sát.

**Phân loại nhỏ:**

##### 🔪 6A. Đe dọa trực tiếp
Từ khóa: `giết, chém, đánh, đập, xiên, xử, coi chừng, ra đường, đợi đấy`

```
🔴 "Tao giết mày"
🔴 "Ra đường coi chừng tao xiên"
🔴 "Đợi đấy tao xử đẹp mày"
🔴 "Tao sẽ tìm mày"
```

##### ☠️ 6B. Kích động tự sát / Trù ẻo
Từ khóa: `chết đi, tự tử, nhảy lầu, uống thuốc, chết cho rồi, sống làm gì`

```
🔴 "Chết đi cho rồi"
🔴 "Sao mày chưa chết?"
🔴 "Tự tử đi đừng sống nữa"
🔴 "Nhảy lầu cho xã hội thanh thản"
🔴 "Sống chật đất"
```

##### ⚔️ 6C. Kích động bạo lực gián tiếp
Từ khóa: `ai đánh, bắn chết, ai giết, đáng chết, xứng đáng bị đánh`

```
🔴 "Ai bắn chết thằng này đi"
🔴 "Đáng bị đánh chết"
🔴 "Ai xiên nó giúp tôi"
```

**⚠️ Lưu ý phân biệt:**
```
🔴 "Chết đi" → Nhãn 2, Topic: Violence (kích động)
✅ "Chết cười" → Nhãn 0 (thành ngữ)
✅ "Chết mất" → Nhãn 0 (cảm thán)
```

---

## 3. QUY TRÌNH GÁN NHÃN 3 BƯỚC

```
┌─────────────────────────────────────┐
│  BƯỚC 1: Có từ tục/tiêu cực không?  │
└──────────┬──────────────────────────┘
           │
      ┌────▼────┐
      │  KHÔNG  │ → Nhãn 0 (CLEAN)
      └─────────┘
      ┌─────┐
      │  CÓ │
      └──┬──┘
         │
┌────────▼─────────────────────────────┐
│  BƯỚC 2: Thuộc 6 Topic nhạy cảm?     │
│  (Region/Body/Gender/Family/         │
│   Disability/Violence)               │
└──────────┬───────────────────────────┘
           │
      ┌────▼────┐
      │   CÓ    │ → Nhãn 2 + điền Topic
      └─────────┘
      ┌──────┐
      │ KHÔNG │
      └───┬──┘
          │
    ┌─────▼──────┐
    │  Nhãn 1    │ (Chửi thề/xúc phạm chung)
    └────────────┘
```

---

## 4. BẢN CHECKLIST GÁN NHÃN

### ✅ Trước khi gán nhãn, tự hỏi:

**Với Nhãn 0:**
- [ ] Không có từ tục nào cả?
- [ ] Không xúc phạm ai?
- [ ] Nếu chê bai, có lịch sự không?

**Với Nhãn 1:**
- [ ] Có từ tục (đm, vcl, vãi...)?
- [ ] Có chửi/xúc phạm nhưng KHÔNG thuộc 6 Topic?
- [ ] Nếu có "mày, m, thằng" → Có thuộc 6 Topic không?

**Với Nhãn 2:**
- [ ] Đã chọn đúng Topic?
- [ ] Có chắc chắn là tấn công nhóm người/gia đình/bạo lực?
- [ ] Đã phân biệt "đm" (Nhãn 1) vs "mẹ mày dạy gì" (Nhãn 2)?

---

## 5. BẢNG SO SÁNH NHANH

| Nội dung | Label | Topic | Lý do |
|----------|-------|-------|-------|
| "Video hay quá!" | 0 | - | Lịch sự |
| "Chất lượng chưa tốt" | 0 | - | Chê nhưng lịch sự |
| "Đm dở quá" | 1 | - | Chửi thề |
| "Mày ngu thật" | 1 | - | Xúc phạm chung |
| "Ngon vãi" | 1 | - | Khen tục |
| "Bắc kỳ ngu" | 2 | Region | Phân biệt vùng miền |
| "Béo như lợn" | 2 | Body | Body shaming |
| "Thằng bê đê" | 2 | Gender | Kỳ thị LGBTQ+ |
| "Mẹ mày dạy gì" | 2 | Family | Xúc phạm gia đình |
| "Mày thiểu năng à" | 2 | Disability | Kỳ thị khuyết tật |
| "Chết đi" | 2 | Violence | Kích động |
| "Đm" | 1 | - | Chỉ là chửi thề |
| "Vcl" | 1 | - | Chỉ là chửi thề |

---

## 6. TRƯỜNG HỢP ĐẶC BIỆT

### 🤔 Câu có nhiều vấn đề → Chọn nhãn nặng nhất

```
"Địt mẹ thằng bắc kỳ béo"
→ Có: Nhãn 1 (đm) + Region (bắc kỳ) + Body (béo)
→ Chọn: Nhãn 2, Topic: Region (hoặc Body, tùy cái nào nặng hơn)
→ Ghi chú: Có thể note thêm "Region + Body"
```

### 🤔 Đùa cợt với bạn bè

```
"Mày ngu vl =))"
→ Vẫn là Nhãn 1 (Model không phân biệt được đùa/thật)
```

### 🤔 Chửi idol/celeb/nhân vật công chúng

```
"Thằng streamer X là đồ rác"
→ Nhãn 1 (xúc phạm cá nhân chung)

"Streamer X béo như lợn"
→ Nhãn 2, Topic: Body
```

### 🤔 Chỉ có emoji tức giận

```
"🤬🤬🤬"
→ Nhãn 1 (thể hiện cảm xúc tiêu cực)
```

---

## 7. CỘT DỮ LIỆU CẦN ĐIỀN

| Cột | Bắt buộc | Giá trị | Ghi chú |
|-----|----------|---------|---------|
| `label` | ✅ Bắt buộc | 0 / 1 / 2 | Nhãn chính |
| `topic` | ⚠️ Nếu label=2 | Region / Body / Gender / Family / Disability / Violence | Bắt buộc khi label=2 |
| `confidence` | ✅ Bắt buộc | 1 (không chắc) / 2 (tương đối) / 3 (rất chắc) | Đánh giá độ tự tin |
| `note` | ❌ Tùy chọn | Text | Ghi chú nếu khó |

---

## 8. MẸO GHI NHỚ

```
🟢 Nhãn 0: Lịch sự + Không tục
🟡 Nhãn 1: Có tục NHƯNG không thuộc 6 Topic
🔴 Nhãn 2: Thuộc 6 Topic (Region/Body/Gender/Family/Disability/Violence)
```

**Công thức siêu nhanh:**
```
IF (có từ tục) {
    IF (thuộc 6 Topic) → Nhãn 2 + Topic
    ELSE → Nhãn 1
} ELSE {
    Nhãn 0
}
```

---

## 9. LIÊN HỆ KHI GẶP KHÓ KHĂN

- Trường hợp애매 → Ghi `confidence = 1` và note lại
- Thắc mắc → Hỏi trưởng nhóm
- Mục tiêu: Cohen's Kappa ≥ 0.75 (cần thống nhất cao)

---

**Chúc bạn gắn nhãn hiệu quả! 🎯**
