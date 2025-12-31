# 🧪 Test Cases cho SafeSense-Vi Demo

## Test Cases Theo Nhãn

### ✅ Label 0: CLEAN (Sạch / Tường thuật khách quan)

#### Test 1.1: Ngữ cảnh tường thuật pháp luật
**Tiêu đề**: Vụ án tham nhũng nghiêm trọng  
**Bình luận**: Đáng bị tử hình hết bọn tham nhũng  
**Kỳ vọng**: Label 0 (Clean) - vì có ngữ cảnh tường thuật

#### Test 1.2: Bình luận trung tính
**Tiêu đề**: Review phim mới  
**Bình luận**: ko biết ns gì luôn ạ phim tạm ổn  
**Kỳ vọng**: Label 0 (Clean)

#### Test 1.3: Bình luận tích cực
**Tiêu đề**: Ca sĩ biểu diễn  
**Bình luận**: Hát hay quá đi mất thôi yêu quá 😍  
**Kỳ vọng**: Label 0 (Clean)

---

### ⚠️ Label 1: OFFENSIVE (Phản cảm)

#### Test 2.1: Từ ngữ thô tục không nhắm vào danh tính
**Tiêu đề**:  
**Bình luận**: Ngu vcl không biết gì hết  
**Kỳ vọng**: Label 1 (Offensive)

#### Test 2.2: Công kích cá nhân nhẹ
**Tiêu đề**: Tranh cãi trên mạng  
**Bình luận**: m ngu quá đi thôi không nói chuyện nữa  
**Kỳ vọng**: Label 1 (Offensive)

#### Test 2.3: Phàn nàn với từ ngữ mạnh
**Tiêu đề**: Dịch vụ kém  
**Bình luận**: Đồ rác rưởi phục vụ tệ vcl  
**Kỳ vọng**: Label 1 (Offensive)

---

### 🚨 Label 2: HATE SPEECH (Thù ghét)

#### Test 3.1: Kích động bạo lực nhắm vào nhóm danh tính (LGBTQ+)
**Tiêu đề**:  
**Bình luận**: Bọn LGBT đáng chết hết đi bệnh hoạn vcl  
**Kỳ vọng**: Label 2 (Hate Speech)

#### Test 3.2: Phân biệt vùng miền
**Tiêu đề**: Tranh cãi về văn hóa  
**Bình luận**: Thằng parky đó ngu vl khốn nạn hết bọn  
**Kỳ vọng**: Label 2 (Hate Speech)

#### Test 3.3: Kích động bạo lực không có ngữ cảnh
**Tiêu đề**:  
**Bình luận**: Giết hết bọn chúng đi đáng chết lắm  
**Kỳ vọng**: Label 2 (Hate Speech)

#### Test 3.4: Body shaming nghiêm trọng + kích động
**Tiêu đề**:  
**Bình luận**: Con lợn béo ú đáng bị đánh chết  
**Kỳ vọng**: Label 2 (Hate Speech)

---

## Test Cases Theo Tính Năng Preprocessing

### 🔤 Teencode Normalization

#### Test 4.1: Teencode trung tính
**Input**: ko biết ns gì luôn ạ  
**Expected Output**: không biết nói gì luôn ạ

#### Test 4.2: Teencode nhạy cảm (giữ nguyên)
**Input**: Đ.m nguuuu vcl  
**Expected Output**: đm ngu \<intense\> vcl

#### Test 4.3: Context-aware "m" (positive)
**Input**: m yêu t không?  
**Expected Output**: em yêu tôi không?

#### Test 4.4: Context-aware "m" (toxic)
**Input**: m ngu vcl đéo biết gì  
**Expected Output**: mày ngu vcl đéo biết gì

---

### 😊 Emoji Processing

#### Test 5.1: Negative emoji
**Input**: Ngu quá 😡🤬  
**Expected Output**: ngu quá \<emo_neg\> \<emo_neg\>

#### Test 5.2: Positive emoji
**Input**: Đẹp trai quá 😍❤️  
**Expected Output**: đẹp trai quá \<emo_pos\> \<emo_pos\>

#### Test 5.3: Neutral emoji (remove)
**Input**: Vậy à 😅🙂  
**Expected Output**: vậy à

---

### 🔁 Intensity Markers

#### Test 6.1: Repeated chars - very intense
**Input**: nguuuuuu vcllllll  
**Expected Output**: ngu \<very_intense\> vcl \<very_intense\>

#### Test 6.2: Repeated chars - intense
**Input**: xấuuuu lắmmm  
**Expected Output**: xấu \<intense\> lắm \<intense\>

---

### 👤 Named Entity Masking

#### Test 7.1: Person name with title
**Input**: Anh Tuấn và chị Hoa đi chơi  
**Expected Output**: anh tuấn và \<person\> đi chơi

#### Test 7.2: Full name with surname
**Input**: Trần Ngọc Bảo rất xinh  
**Expected Output**: \<person\> rất xinh

#### Test 7.3: @mention
**Input**: @nguyenvana ngu vcl  
**Expected Output**: \<user\> ngu vcl

---

### 🔤 Bypass Patterns

#### Test 8.1: Dot bypass
**Input**: n.g.u quá  
**Expected Output**: ngu quá

#### Test 8.2: Dash bypass
**Input**: đ-m ch-ế-t  
**Expected Output**: đm chết

#### Test 8.3: Star bypass
**Input**: đ*m l*n  
**Expected Output**: đm lồn

---

### 🔢 Leetspeak

#### Test 9.1: Number to letter
**Input**: ch3t di ngu4  
**Expected Output**: chết đi ngua

#### Test 9.2: Keep standalone numbers
**Input**: 3-4 năm trước  
**Expected Output**: 3-4 năm trước

---

### 🌐 English Insults

#### Test 10.1: Vulgar words
**Input**: fuck you stupid idiot  
**Expected Output**: \<eng_vulgar\> you \<eng_insult\> \<eng_insult\>

#### Test 10.2: Mixed language
**Input**: m stupid vcl  
**Expected Output**: mày \<eng_insult\> vcl

---

## Edge Cases (Trường hợp đặc biệt)

### Test 11.1: Empty comment
**Tiêu đề**: Test  
**Bình luận**: (empty)  
**Kỳ vọng**: Handle gracefully

### Test 11.2: Very long text (>256 tokens)
**Bình luận**: [Very long text with 300+ words]  
**Kỳ vọng**: Truncate at 256 tokens

### Test 11.3: Only emojis
**Bình luận**: 😂😂😂😍😍  
**Kỳ vọng**: \<emo_pos\> \<emo_pos\> \<emo_pos\> \<emo_pos\> \<emo_pos\>

### Test 11.4: Mixed script (Vietnamese + English)
**Bình luận**: Người Việt mà stupid vcl  
**Kỳ vọng**: người việt mà \<eng_insult\> vcl

---

## 🎯 Priority Test List (Top 10 Must-Test)

1. **Ngữ cảnh tường thuật**: "Vụ án tham nhũng" + "Đáng bị tử hình"
2. **LGBTQ hate speech**: "Bọn LGBT đáng chết"
3. **Regional discrimination**: "Thằng parky ngu vcl"
4. **Context-aware m**: "m yêu t" vs "m ngu vcl"
5. **Teencode + emoji**: "Đ.m nguuuu 😡"
6. **Body shaming**: "Con lợn béo đáng chết"
7. **Death metaphor**: "Đáng bị tử hình/giết"
8. **Intensity markers**: "nguuuuuu vcllllll"
9. **Person name masking**: "Anh Tuấn và chị Hoa"
10. **English insults**: "stupid idiot fuck you"

---

## 📝 Notes

- Tất cả test cases trên có thể copy-paste trực tiếp vào demo
- Expected outputs chỉ áp dụng cho preprocessing, không phải model prediction
- Model prediction phụ thuộc vào training data và weights
- Nếu model chưa fine-tuned, có thể kết quả dự đoán không chính xác

---

## ✅ Checklist Testing

- [ ] Test tất cả 3 labels (Clean, Offensive, Hate)
- [ ] Test teencode normalization
- [ ] Test context-aware "m" mapping
- [ ] Test emoji processing
- [ ] Test intensity markers
- [ ] Test named entity masking
- [ ] Test bypass patterns
- [ ] Test leetspeak
- [ ] Test English insults
- [ ] Test edge cases

**Good Luck! 🍀**
