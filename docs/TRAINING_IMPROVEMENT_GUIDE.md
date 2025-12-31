# 🔥 HƯỚNG DẪN NÂNG CAO F1 SCORE TỪ 0.68 LÊN 0.80+

## 📊 Vấn đề ban đầu: F1 = 0.68

Sau khi train PhoBERT trên `final_train_data_v2.csv`, F1 score chỉ đạt **0.68** do 4 vấn đề nghiêm trọng:

---

## 🐛 4 NHÓM VẤN ĐỀ CHÍNH

### **Nhóm 1: VCL/VL làm mờ lý trí** 
**Số lượng: 14 cases**

**Vấn đề:**
- Các câu dùng `vcl/vl` để khen: "chất vl", "peak vcl", "vip vl", "quả đẹp vcl"
- AI nhầm tất cả là toxic vì trong training data, `vcl/vl` thường đi với chửi thề

**Nguyên nhân:**
- PhoBERT học: `vl/vcl` = Chửi thề (Label 1)
- Chưa học: Giới trẻ dùng như **trạng từ chỉ mức độ cực đại** (Superlative) cho context tích cực

**Giải pháp:**
```python
# Pattern nhận diện positive slang với vcl/vl
positive_vcl_patterns = [
    r'\b(chất|đỉnh|peak|vip|hay|đẹp|tuyệt)\s+(vcl|vl)\b',
    r'\b(sản phẩm|video|bài hát)\s+.{0,30}(chất|đỉnh)\s+(vcl|vl)\b'
]
# → Relabel từ Label 1 → Label 0
```

**Ví dụ đã fix:**
- ✅ "sản phẩm chất lượng vcl, mua về dùng thích lắm" → Label 0
- ✅ "video này đỉnh vcl, xem đi xem lại không chán" → Label 0

---

### **Nhóm 2: "Nặng" mang nghĩa kỹ thuật**
**Số lượng: 44 cases**

**Vấn đề:**
- Các câu về MV/video: "nặng khung hình", "mv nhìn nặng", "video lag do nặng"
- AI nhầm là toxic vì "nặng" thường đi với "xúc phạm nặng", "chửi nặng"

**Nguyên nhân:**
- Từ "nặng" trong toxic data: "xúc phạm nặng", "chửi nặng" (Intensity)
- AI không phân biệt "nặng" về **dung lượng** (Size) vs "nặng" về **lời lẽ** (Intensity)

**Giải pháp:**
```python
# Pattern nhận diện "nặng" kỹ thuật
technical_heavy_patterns = [
    r'\b(video|mv|render|khung hình)\s+.{0,20}nặng\b',
    r'\b(lag|giật|load)\s+.{0,20}(nặng|do nặng)\b'
]
# → Relabel từ Label 1 → Label 0
```

**Ví dụ đã fix:**
- ✅ "mv nhìn nặng vcl nhưng chất lượng cao" → Label 0
- ✅ "video lag quá do nặng khung hình" → Label 0

---

### **Nhóm 3: Kêu gọi công lý bị nhầm là toxic**
**Số lượng: 78 cases**

**Vấn đề:**
- Người dùng ủng hộ pháp luật: "pháp luật xử lý", "luật dạy dỗ thằng này", "cho vào tù"
- AI nhầm là gây hấn vì chứa từ "mày", "thằng", "bắt", "tù"

**Nguyên nhân:**
- Các câu chứa từ **trừng phạt** + đại từ **mày/thằng**
- AI mặc định: Chửi người khác hoặc đòi bắt bớ = Gây hấn
- Theo V7.2: **Ủng hộ pháp luật văn minh = Label 0**

**Giải pháp:**
```python
# Pattern nhận diện kêu gọi công lý
justice_patterns = [
    r'\b(pháp luật|công an)\s+.{0,30}(xử lý|bắt|phạt)\b',
    r'\b(đi|vào|cho vào)\s+(tù|nhà tù)\b',
    r'\b(ủng hộ|đúng|nên)\s+.{0,20}(pháp luật|xử lý)\b'
]
# → Relabel từ Label 1/2 → Label 0
# NHƯNG: Loại trừ "mày đi tù" (chửi trực tiếp)
```

**Ví dụ đã fix:**
- ✅ "pháp luật xử lý kẻ xấu này đi" → Label 0
- ✅ "ủng hộ công an bắt thằng này" → Label 0
- ❌ "mày đi tù đi" → Vẫn giữ Label 1 (chửi trực tiếp)

---

### **Nhóm 4: Noise từ mô tả MV quá dài**
**Số lượng: 412 cases (VẤN ĐỀ LỚN NHẤT!)**

**Vấn đề:**
- Các câu có phần mô tả MV dài (100-500 ký tự) trước `</s>`
- Ví dụ: "OFFICIAL POSTER | VISUALIZER MV BODY SHAMING ?- Awai x Win G... Body Shaming (Miệt thị ngoại hình) là một vấn đề phổ biến... </s> video hay quá"

**Nguyên nhân:**
- Phần mô tả chứa quá nhiều từ khóa: "miệt thị", "body shaming", "vô văn hóa"
- AI bị "ngợp" bởi từ khóa tiêu cực trong phần dẫn nhập
- Bỏ qua phần comment ngắn (tích cực) phía sau `</s>`

**Giải pháp:**
```python
# Cắt bỏ mô tả MV dài, chỉ giữ comment
mv_description_pattern = r'^(official poster|visualizer mv).{100,}?</s>'

if re.search(mv_description_pattern, text):
    parts = text.split('</s>')
    comment_part = parts[-1].strip()  # Chỉ lấy comment
    if len(comment_part) < 200:
        text = comment_part  # Bỏ phần mô tả
```

**Ví dụ đã fix:**
- ❌ Trước: "OFFICIAL POSTER... body shaming... miệt thị... vô văn hóa... </s> video hay quá"
- ✅ Sau: "video hay quá"

---

## 🎯 KẾT QUẢ SAU KHI FIX

### **Thống kê fix:**
```
Total fixes:                548 rows (10.8% dataset)
  - VCL/VL positive:        14 rows
  - "Nặng" kỹ thuật:        44 rows
  - Kêu gọi công lý:        78 rows
  - Cắt mô tả MV:           412 rows (76% fixes!)
  - Augmented examples:     8 rows
```

### **Label distribution sau fix:**
```
Label 0 (Clean):          2,171 (42.7%) ⬆️ +2.7%
Label 1 (Toxic):          1,331 (26.2%) ⬇️ -3.1%
Label 2 (Hate):           1,583 (31.1%)
```

---

## 🚀 HƯỚNG DẪN RETRAIN

### **Bước 1: Sử dụng data đã fix**
```bash
# File mới: final_train_data_v2_FIXED_20251229_013656.csv
# Thay thế DATA_PATH trong training script
```

### **Bước 2: Điều chỉnh hyperparameters**
```python
# Trong colab_phobert_v2_training.py hoặc kaggle_phobert_training.py

class Config:
    # Tăng epochs vì data đã sạch hơn
    EPOCHS = 6  # Từ 5 → 6
    
    # Giảm learning rate để học tốt hơn
    LEARNING_RATE = 1.5e-5  # Từ 2e-5 → 1.5e-5
    
    # Tăng patience
    PATIENCE = 3  # Từ 2 → 3
    
    # Bật Focal Loss nếu vẫn imbalance
    USE_FOCAL_LOSS = True  # Từ False → True
    FOCAL_GAMMA = 2.5  # Từ 2.0 → 2.5
```

### **Bước 3: Retrain và đánh giá**
```bash
# Trên Colab
python colab_phobert_v2_training.py

# Hoặc Kaggle
python kaggle_phobert_training.py
```

### **Kết quả kỳ vọng:**
```
Before fix:  F1 = 0.68
After fix:   F1 = 0.75 - 0.80+

Improvement: +7-12% F1 score
```

---

## 📝 CHECKLIST TRƯỚC KHI TRAIN

- [ ] Đã backup data gốc
- [ ] Đã chạy `fix_training_data_issues.py`
- [ ] Đã review file `final_train_data_v2_FIXED_*.csv`
- [ ] Đã cập nhật DATA_PATH trong training script
- [ ] Đã điều chỉnh hyperparameters (optional)
- [ ] Đã chọn GPU phù hợp (T4 trở lên)

---

## 🔍 PHÂN TÍCH SÂU HƠN

### **Tại sao Nhóm 4 (Noise MV) là vấn đề lớn nhất?**

**412/548 fixes (76%) là do mô tả MV dài!**

**Nguyên nhân:**
1. **Token budget**: PhoBERT chỉ xử lý 256 tokens
2. **Attention bias**: Model tập trung vào phần đầu (mô tả MV)
3. **Keyword flooding**: Quá nhiều từ "miệt thị", "body shaming" trong mô tả

**Ví dụ cụ thể:**
```
Input (500 tokens):
"OFFICIAL POSTER | VISUALIZER MV BODY SHAMING ?- Awai x Win G x Trà Bông
Ngày 15/08/2025 - 20:00「 ✦ Bàn về miệt thị ngoại hình ✦ 」
Body Shaming (Miệt thị ngoại hình) là một vấn đề phổ biến hiện nay...
[200 từ về body shaming, miệt thị, vô văn hóa...]
</s> video hay quá"

PhoBERT attention:
- 90% attention → Phần mô tả (chứa "miệt thị", "body shaming")
- 10% attention → Comment "video hay quá"
→ Kết luận: Toxic (SAI!)

After fix (20 tokens):
"video hay quá"
→ Kết luận: Clean (ĐÚNG!)
```

---

## 💡 KHUYẾN NGHỊ THÊM

### **1. Data Augmentation nâng cao**
Thêm nhiều ví dụ positive slang:
```python
augmented_examples = [
    "sản phẩm này xịn vcl, đáng tiền lắm",
    "game này hay vl, chơi mãi không chán",
    "đội này mạnh vcl, vô địch luôn",
    # ... thêm 50-100 examples
]
```

### **2. Active Learning**
Sử dụng 33,814 unlabeled data đã xử lý:
- Dùng model hiện tại predict
- Chọn những sample có confidence thấp
- Label thủ công 500-1000 samples
- Retrain

### **3. Ensemble Models**
Train nhiều models và vote:
- PhoBERT-base-v2
- PhoBERT-large
- XLM-RoBERTa-base

### **4. Post-processing Rules**
Thêm rules sau khi predict:
```python
if "vcl" in text and any(word in text for word in ["chất", "đỉnh", "hay"]):
    if prediction == 1:
        prediction = 0  # Override
```

---

## 📚 TÀI LIỆU THAM KHẢO

- `fix_training_data_issues.py` - Script fix data
- `final_train_data_v2_FIXED_*.csv` - Data đã fix
- `colab_phobert_v2_training.py` - Training script cho Colab
- `kaggle_phobert_training.py` - Training script cho Kaggle

---

**Author:** Thanh Thien  
**Date:** 29/12/2025  
**Version:** 1.0
