# apify_to_csv.py - Hướng Dẫn Sử Dụng

## 📋 Tổng Quan

Script này chuyển đổi dữ liệu từ Apify JSON sang CSV với **context (ngữ cảnh)** phù hợp cho việc gán nhãn và training model theo **Guideline V4.0**.

### Thay đổi chính so với phiên bản cũ:

| Phiên bản cũ | Phiên bản mới (V4.0) |
|--------------|----------------------|
| `text`, `cleaned_text`, `cleaned_text_norm` | `input_text` = "title </s> comment" |
| Nhiều cột phân tích | Tập trung vào format để gán nhãn |
| Không có ngữ cảnh | **Có context từ title/post** |

---

## 🎯 Output Format

### Cấu trúc file CSV đầu ra:

```csv
input_text,label,note
"video này hay quá </s> cảm ơn bạn đã chia sẻ",,
"hằng du mục về việt nam </s> mày béo như lợn",2,body_shaming
```

### Các cột chính:

- **`input_text`**: Cột chính để gán nhãn và train model
  - Format: `title </s> comment`
  - Đã được clean (emoji → text, xóa hashtag, normalize teencode)
  - Truncate thông minh: title ≤50 tokens, tổng ≤256 tokens
  
- **`label`**: Nhãn (0=Clean, 1=Toxic có từ tục, 2=Hate Speech)
  - Để trống khi chưa gán nhãn
  
- **`note`**: Ghi chú khi gán nhãn
  - VD: "body_shaming", "region_discrimination", "unclear"

### Các cột phụ (để tham khảo):

- `raw_comment`, `raw_title`: Dữ liệu gốc chưa xử lý
- `cleaned_comment`, `cleaned_title`: Đã clean nhưng chưa build context
- `topic`, `source_platform`, `timestamp`, etc.

---

## 🚀 Cách Sử Dụng

### 1. Chuẩn bị dữ liệu

Đặt file JSON từ Apify vào thư mục:
```
data/
  raw/
    facebook/
      - confession_fb.json
      - body_shaming.json
    youtube/
      - rap_battle.json
      - gaming_comment.json
```

### 2. Chạy script

```bash
cd src/preprocessing
python apify_to_csv.py
```

### 3. Kết quả

File output sẽ được tạo ở:
```
data/
  processed/
    - facebook_master.csv
    - youtube_master.csv
    - master_combined.csv  ← Gộp tất cả
```

---

## 🔧 Xử Lý Dữ Liệu

### 1. Emoji Mapping (14 emojis quan trọng)

```python
'🏳️‍🌈' → ' đồng tính '
'❤️' → ' yêu '
'💔' → ' chia tay '
```

**Tại sao quan trọng?**
- Emoji mang ngữ nghĩa trong LGBT, confession topics
- Model không học được từ emoji, cần chuyển thành text

### 2. Hashtag Cleaning

```python
"#fyp #xuhuong mày béo vậy" → "mày béo vậy"
```

- Xóa **TẤT CẢ** hashtag (spam + thông thường)
- Hashtag không mang thông tin toxic/hate

### 3. Teencode Normalization

```python
"tml" → "thằng mặt lồn"
"vcl" → "vãi chưởng"
"đcm" → "đụ cụ mày"
```

- Sử dụng `advanced_text_cleaning` với 251 từ teencode
- Quan trọng để model hiểu ngôn ngữ teen trên mạng

### 4. Context Building

```python
title = "Hằng Du Mục về Việt Nam"  # 50 tokens max
comment = "mày béo như lợn"
→ input_text = "hằng du mục về việt nam </s> mày béo như lợn"
```

**Truncate thông minh:**
- Title: tối đa 50 tokens (PhoBERT tokenizer)
- Total: tối đa 256 tokens
- Ưu tiên giữ comment đầy đủ, cắt title nếu cần

---

## 📊 Ví Dụ Thực Tế

### Input JSON (Facebook):
```json
{
  "id": "abc123",
  "postTitle": "Phân biệt vùng miền, miệt thị người dân vùng lũ",
  "text": "mày chửi dân miền nam giờ lại xin lỗi 🏳️‍🌈",
  "postUrl": "https://facebook.com/...",
  "likesCount": "1.2K"
}
```

### Output CSV:
```csv
id,input_text,raw_comment,raw_title,topic,label,note
abc123,"phân biệt vùng miền miệt thị người dân vùng lũ </s> mày chửi dân miền nam giờ lại xin lỗi đồng tính","mày chửi dân miền nam giờ lại xin lỗi 🏳️‍🌈","Phân biệt vùng miền, miệt thị người dân vùng lũ",Vùng miền,,
```

---

## 🎓 Guideline Gán Nhãn

Sau khi tạo file CSV, gán nhãn theo quy tắc:

### Nhãn 0: Clean
- Không có từ tục
- Không xúc phạm/tấn công ai

### Nhãn 1: Toxic (có từ tục)
- Có từ tục nhưng không target ai cụ thể
- VD: "đm", "vcl", "vl", "dm"

### Nhãn 2: Hate Speech (nặng nhất)
- Body shaming: "béo", "mập", "xấu", "lùn"
- Region: "bắc kỳ", "nam kỳ", "thổ dân"
- LGBT: "đồng tính", "chuyển giới" + từ xúc phạm
- Targeting cụ thể với từ tục

**⭐ Quy tắc vàng:** Nếu có cả label 1 và 2 → Chọn **label 2** (nặng nhất)

---

## 🔍 So Sánh Với Script Khác

### `prepare_unlabeled_with_context.py`
- **Mục đích:** Chuẩn bị unlabeled data để active learning
- **Input:** File `unlabeled_data.csv` (đã có sẵn)
- **Output:** Thêm context, lọc trùng với labeled data

### `apify_to_csv.py` (script này)
- **Mục đích:** Tạo dataset MỚI từ JSON gốc
- **Input:** Raw JSON từ Apify
- **Output:** Master dataset với context, sẵn sàng gán nhãn

---

## ⚙️ Cấu Hình

### Thay đổi max length:
```python
# Trong hàm build_input_text()
max_total_length=256  # Default
max_title_len=50      # Default
```

### Thay đổi emoji mapping:
```python
# Thêm emoji mới vào EMOJI_MAP
EMOJI_MAP = {
    '🏳️‍🌈': ' đồng tính ',
    '👨‍❤️‍💋‍👨': ' nam yêu nam ',
    # Thêm emoji khác...
}
```

### Thay đổi output directory:
```python
# Trong hàm convert_apify_to_master()
output_dir = os.path.join(os.path.dirname(input_dir), 'processed')
```

---

## 🐛 Troubleshooting

### ❌ Error: "No module named 'advanced_text_cleaning'"
**Giải pháp:** Đảm bảo file `advanced_text_cleaning.py` nằm cùng thư mục

### ❌ Error: "⚠️ Không load được PhoBERT tokenizer"
**Giải pháp:** 
```bash
pip install transformers
```
Hoặc script sẽ tự động fallback về word-based truncation

### ❌ Output file rỗng
**Nguyên nhân:** JSON format không đúng hoặc không có dữ liệu ≥5 ký tự
**Kiểm tra:**
- File JSON có đúng format `items` array không?
- Comments có ít nhất 5 ký tự không?

---

## 📌 Notes Quan Trọng

1. **Luôn backup dữ liệu cũ**: Script tự động tạo backup với timestamp
2. **Remove duplicates**: Theo `input_text` và `id`
3. **Không ghi đè nhãn cũ**: Nếu file master đã có nhãn, script sẽ merge không ghi đè
4. **PhoBERT tokenizer**: Cần thiết để truncate chính xác, nhưng không bắt buộc

---

## 📞 Liên Hệ / Issues

- Xem guideline đầy đủ: `docs/GUIDELLINE GÁN NHÃN V4.0.pdf`
- Script liên quan: `prepare_unlabeled_with_context.py`, `prepare_training_with_teencode.py`
