# 🛡️ SafeSense-Vi Demo - Hướng Dẫn Sử Dụng

## Mô Tả
Demo ứng dụng phát hiện ngôn ngữ độc hại tiếng Việt với **preprocessing chuẩn** sử dụng PhoBERT.

## ✨ Tính Năng Mới

### 1. Tích Hợp Preprocessing Pipeline (14 Bước)
Code đã được cập nhật với pipeline tiền xử lý đầy đủ bao gồm:

- ✅ **Teencode Normalization**: k→không, đm→địt mẹ, vcl→vãi lồn
- ✅ **Emoji → Sentiment Tags**: 😡→\<emo_neg\>, 😍→\<emo_pos\>
- ✅ **Intensity Markers**: nguuuu→ngu \<intense\>
- ✅ **Context-Aware "m" Mapping**: 
  - "yêu m" → "yêu em" (positive context)
  - "m ngu" → "mày ngu" (toxic context)
- ✅ **Named Entity Masking**: Trần Ngọc → \<person\>, @user → \<user\>
- ✅ **Bypass Pattern Handling**: đ.m→đm, n.g.u→ngu
- ✅ **Leetspeak Conversion**: ch3t→chết, ngu4→ngua

### 2. Kết Quả Test Preprocessing

```python
# Test Case 1: Teencode + Emoji
INPUT:  "Đ.m nguuuu vcl 😡"
OUTPUT: "đm ngu <intense> vcl <emo_neg>"

# Test Case 2: Context-aware "m"
INPUT:  "m yêu t k?"
OUTPUT: "em yêu tôi không?"

INPUT:  "m ngu vcl đéo biết gì"
OUTPUT: "mày ngu vcl đéo biết gì"

# Test Case 3: Person Name + Emoji
INPUT:  "chị ak Trần Ngọc đẹp quá 😍"
OUTPUT: "chị ạ <person> đẹp quá <emo_pos>"

# Test Case 4: Title + Comment Format
Title:   "Vụ án tham nhũng nghiêm trọng"
Comment: "Đáng bị tử hình hết bọn tham nhũng vcl"
Combined: "vụ án tham nhũng nghiêm trọng </s> đáng bị tử hình hết bọn tham nhũng vcl"
```

## 🚀 Cách Chạy Demo

### Bước 1: Cài đặt dependencies (nếu chưa)
```bash
pip install streamlit torch transformers pandas
```

### Bước 2: Chạy test preprocessing
```bash
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"
python test_preprocessing.py
```

### Bước 3: Khởi động Streamlit app
```bash
streamlit run Safesense_VI.py
```

### Bước 4: Truy cập web interface
Mở trình duyệt tại: `http://localhost:8501`

## 📝 Cách Sử Dụng

1. **Nhập Tiêu Đề** (tùy chọn): Ngữ cảnh của bài viết
   - Ví dụ: "Vụ án tham nhũng nghiêm trọng"

2. **Nhập Bình Luận**: Nội dung cần kiểm tra
   - Ví dụ: "Đáng bị tử hình hết bọn đồ khốn"

3. **Nhấn "Phân Tích Độc Hại"**

4. **Xem Kết Quả**:
   - Nhãn dự đoán: Clean (0), Offensive (1), Hate (2)
   - Độ tin cậy (%)
   - Biểu đồ phân phối xác suất

## 🎯 Các Trường Hợp Test Nên Thử

### Test Case 1: Ngữ cảnh tường thuật (Label 0)
- **Tiêu đề**: "Vụ án tham nhũng nghiêm trọng"
- **Bình luận**: "Đáng bị tử hình hết bọn tham nhũng"
- **Dự đoán**: Clean (vì có ngữ cảnh tường thuật)

### Test Case 2: Phản cảm nhẹ (Label 1)
- **Tiêu đề**: ""
- **Bình luận**: "Ngu vcl không biết gì"
- **Dự đoán**: Offensive (từ ngữ thô tục nhưng không nhắm vào danh tính)

### Test Case 3: Thù ghét nghiêm trọng (Label 2)
- **Tiêu đề**: ""
- **Bình luận**: "Bọn LGBT đáng chết hết đi"
- **Dự đoán**: Hate Speech (kích động bạo lực + nhắm vào danh tính)

### Test Case 4: Teencode với emoji
- **Tiêu đề**: ""
- **Bình luận**: "ko biết ns gì luôn ạ 😅"
- **Dự đoán**: Clean (neutral teencode)

## 🔧 Thay Đổi Code

### File `Safesense_VI.py`

#### Thêm import:
```python
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import text cleaning module
from src.preprocessing.advanced_text_cleaning import clean_text
```

#### Cập nhật hàm preprocessing:
```python
def preprocess_input(title, comment):
    """
    Tiền xử lý theo pipeline chuẩn với teencode normalization.
    """
    # Clean title and comment using advanced pipeline
    cleaned_title = clean_text(title) if title.strip() else ""
    cleaned_comment = clean_text(comment)
    
    # Ghép Tiêu đề và Bình luận theo format PhoBERT
    input_text = f"{cleaned_title} </s> {cleaned_comment}" if cleaned_title else f"</s> {cleaned_comment}"
    
    return input_text
```

## 📊 Chi Tiết Preprocessing Pipeline

### Pipeline Order (14 Steps)
1. ✅ Unicode Normalize (NFC)
2. ✅ HTML/URL Removal
3. ✅ Hashtag Removal
4. ✅ **Teencode Normalization** (PRESERVE CASE!)
5. ✅ Named Entity Masking (\<PERSON\>, \<USER\>)
6. ✅ Lowercase
7. ✅ **Sentiment & Intensity Mapping**
8. ✅ **English Insult Detection**
9. ✅ Bypass & Leetspeak
10. ✅ Repeated Chars with Intensity
11. ✅ **Context-Aware "m" Mapping**
12. ✅ Whitespace & Punctuation

### Teencode Dictionary (300+ entries)
- **TEENCODE_NEUTRAL**: Safe to normalize (ko→không, ns→nói)
- **TEENCODE_INTENSITY_SENSITIVE**: Preserve for intensity (đm, vcl, đéo)

## 🎓 Training Use Case

Để sử dụng preprocessing này cho training:

```python
from src.preprocessing.advanced_text_cleaning import clean_text

# Clean your dataset
df['cleaned_title'] = df['title'].apply(clean_text)
df['cleaned_comment'] = df['comment'].apply(clean_text)
df['input_text'] = df['cleaned_title'] + ' </s> ' + df['cleaned_comment']

# Use input_text for training
train_texts = df['input_text'].tolist()
```

## 🐛 Troubleshooting

### Lỗi: Module not found
```bash
# Đảm bảo đang ở đúng thư mục
cd "c:\Học sâu\Dataset"

# Hoặc thêm vào PYTHONPATH
set PYTHONPATH=c:\Học sâu\Dataset
```

### Lỗi: Model not found
- Kiểm tra đường dẫn model trong file `Safesense_VI.py`
- Mặc định: `C:\\Học sâu\\Dataset\\TOXIC_COMMENT\\models`

## 📚 Tài Liệu Tham Khảo

- **Guideline V7.2**: `GUIDELINE_V7.2_TOM_TAT.md`
- **Advanced Cleaning**: `src/preprocessing/advanced_text_cleaning.py`
- **Quy trình xử lý**: `QUY_TRINH_XU_LY_TOM_TAT.md`

## ✅ Checklist

- [x] Tích hợp preprocessing pipeline đầy đủ
- [x] Test teencode normalization
- [x] Test context-aware "m" mapping
- [x] Test emoji → sentiment tags
- [x] Test intensity markers
- [x] Test named entity masking
- [x] Tạo test script
- [x] Tạo documentation

## 🎉 Kết Luận

Demo đã sẵn sàng để test với **preprocessing chuẩn** như trong quá trình training. Pipeline xử lý text giống hệt với data được dùng để train model, đảm bảo tính nhất quán giữa training và inference.

**Happy Testing! 🚀**
