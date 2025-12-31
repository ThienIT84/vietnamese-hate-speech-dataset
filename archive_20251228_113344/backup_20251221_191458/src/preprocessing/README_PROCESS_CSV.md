# process_csv_with_context.py - Hướng Dẫn

## 📋 Mục Đích

Script xử lý file **CSV hoặc XLSX** có sẵn, thêm context (title </s> comment) và normalize teencode/emoji, tương tự như `apify_to_csv.py` nhưng input là CSV/Excel thay vì JSON.

## 🎯 Sử Dụng Khi Nào?

- ✅ Có file CSV/XLSX chưa xử lý teencode
- ✅ Có file CSV/XLSX chưa có context (title </s> comment)
- ✅ Muốn chuẩn hóa emoji và hashtag
- ✅ Cần format lại để gán nhãn theo guideline V4.0
- ✅ Có data trong Excel và muốn xử lý trực tiếp

## 🚀 Cách Sử Dụng

### Cài đặt (cho file Excel):
```bash
pip install openpyxl
```

### Cơ bản:
```bash
cd src/preprocessing

# CSV
python process_csv_with_context.py input.csv

# XLSX
python process_csv_with_context.py input.xlsx
```

### Chỉ định output:
```bash
# Output cùng format với input
python process_csv_with_context.py input.csv -o output.csv
python process_csv_with_context.py input.xlsx -o output.xlsx

# Chuyển đổi format
python process_csv_with_context.py input.xlsx -o output.csv
python process_csv_with_context.py input.csv -o output.xlsx
```

### Ví dụ cụ thể:
```bash
# Xử lý CSV
python process_csv_with_context.py ../../data/processed/unlabeled_data.csv

# Xử lý Excel
python process_csv_with_context.py ../../data/raw/comments.xlsx

# Với output tùy chỉnh
python process_csv_with_context.py data.xlsx -o processed_data.xlsx
```

## 📊 Input Format (CSV/XLSX)

Script tự động phát hiện các cột, hỗ trợ nhiều tên cột:

### Cột Comment (BẮT BUỘC):
- `text`
- `comment`
- `cleaned_text`
- `raw_comment`
- `content`
- `message`

### Cột Title (TÙY CHỌN):
- `title`
- `postTitle`
- `post_title`
- `cleaned_title`
- `raw_title`
- `videoTitle`

### Cột khác (TÙY CHỌN):
- `label` - Nhãn có sẵn (giữ nguyên)
- `note` - Ghi chú (giữ nguyên)
- `id` - ID (tự tạo nếu không có)

**Hỗ trợ:** `.csv`, `.xlsx`, `.xls`

## 📤 Output Format (CSV/XLSX)

```csv
id,input_text,label,note,raw_comment,raw_title
abc123,"hằng du mục về việt nam </s> mày béo như lợn vãi chưởng",,"","mày béo như lợn vcl","Hằng Du Mục về Việt Nam"
```

### Cột output:
- `id` - ID gốc hoặc tự tạo
- `input_text` - ⭐ Format: "title </s> comment"
- `label` - Giữ nguyên nếu có, null nếu chưa
- `note` - Giữ nguyên nếu có, rỗng nếu chưa
- `raw_comment` - Comment gốc (để tham khảo)
- `raw_title` - Title gốc (để tham khảo)

## 🔧 Xử Lý

### 1. Emoji Mapping
```
"Tôi yêu bạn ❤️" → "tôi yêu bạn  yêu "
"🏳️‍🌈 pride" → " đồng tính  pride"
```

### 2. Hashtag Removal
```
"#fyp #xuhuong video hay" → "video hay"
```

### 3. Teencode Normalization
```
"vcl bạn ơi" → "vãi chưởng bạn ơi"
"đcm mày" → "đụ cụ mày"
```

### 4. Context Building
```
Title: "Hằng Du Mục về Việt Nam"
Comment: "video hay quá"
→ Input: "hằng du mục về việt nam </s> video hay quá"
```

## 📝 Ví Dụ

### Input CSV:
```csv
text,title,label
"mày béo như lợn vcl","Hằng Du Mục về Việt Nam",
"video hay ❤️","Clip reaction",0
"#fyp mày ngu vl","",
```

### Output CSV:
```csv
id,input_text,label,note,raw_comment,raw_title
abc123,"hằng du mục về việt nam </s> mày béo như lợn vãi chưởng",,"","mày béo như lợn vcl","Hằng Du Mục về Việt Nam"
def456,"clip reaction </s> video hay  yêu ",0,"","video hay ❤️","Clip reaction"
ghi789,"mày ngu vãi lồn",,"","#fyp mày ngu vl",""
```

## ⚙️ Tùy Chỉnh

### Thay đổi max length:
Sửa trong function `build_input_text()`:
```python
max_total_length=256  # Thay đổi ở đây
max_title_len=50      # Max tokens cho title
```

### Thêm emoji mới:
Sửa dictionary `EMOJI_MAP`:
```python
EMOJI_MAP = {
    '🏳️‍🌈': ' đồng tính ',
    '🎉': ' chúc mừng ',  # Thêm mới
}
```

## 🔍 So Sánh Với Scripts Khác

| Script | Input | Output | Use Case |
|--------|-------|--------|----------/XLSX có sẵn | CSV/XLSX với context | Xử lý lại file có sẵn |
| `prepare_unlabeled_with_context.py` | CSV unlabeled cụ thể | CSV để active learning | Chuẩn bị cho active learning |

## 🐛 Troubleshooting

### ❌ "Cần cài đặt openpyxl để đọc file Excel"
**Solution:** 
```bash
pip install openpyxl
```with_context.py` | CSV unlabeled cụ thể | CSV để active learning | Chuẩn bị cho active learning |

## 🐛 Troubleshooting

### ❌ "KHÔNG TÌM THẤY CỘT COMMENT"
**Solution:** Đổi tên cột thành một trong: `text`, `comment`, `cleaned_text`, `content`

### ❌ "Loại bỏ nhiều dòng"
**Nguyên nhân:** Dòng có comment < 3 ký tự sau khi clean
**Kiểm tra:** Xem raw_comment có dữ liệu không?

### ❌ Output không có separator "</s>"
**Nguyên nhân:** CSV không có cột title
**Solution:** Thêm cột title hoặc chấp nhận output chỉ có comment

## 📌 Lưu Ý

1. **Encoding:** Script tự động xử lý UTF-8
2. **Duplicate:** Script KHÔNG tự động loại duplic openpyxl`
- [ ] File CSV/XLSX có cột comment với tên đúng
- [ ] Đã có file `advanced_text_cleaning.py` cùng folder
- [ ] Kiểm tra output có đúng format: `title </s> comment`
- [ ] Xác nhận emoji đã được convert
- [ ] Xác nhận hashtag đã bị xóa

## 🎉 Kết Luận

Script này giúp bạn xử lý nhanh file CSV/XLSXitle </s> comment`
- [ ] Xác nhận emoji đã được convert
- [ ] Xác nhận hashtag đã bị xóa

## 🎉 Kết Luận

Script này giúp bạn xử lý nhanh file CSV để:
- ✅ Thêm context (title </s> comment)
- ✅ Normalize teencode (251 từ)
- ✅ Convert emoji thành text
- ✅ Xóa hashtag spam
- ✅ Hỗ trợ cả CSV và Excel (.xlsx, .xls)
- ✅ Sẵn sàng để gán nhãn

**Sử dụng đơn giản, hỗ trợ nhiều format!** 🚀
