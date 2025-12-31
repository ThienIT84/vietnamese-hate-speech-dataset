# 🔧 TEENCODE PROCESSING TOOL

Công cụ xử lý teencode với giao diện đơn giản, 3 chức năng chính.

## 📋 Mục lục

- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Chức năng](#chức-năng)
- [Ví dụ](#ví-dụ)

## 🚀 Cài đặt

```bash
# Đảm bảo đã cài đặt dependencies
pip install pandas openpyxl
```

## 💻 Sử dụng

### Chế độ Interactive (Giao diện menu)

```bash
python teencode_tool.py
```

### Chế độ Command Line (Tự động hóa)

```bash
# Chức năng 1
python teencode_tool.py 1 input.xlsx output.xlsx

# Chức năng 2
python teencode_tool.py 2 input.csv output.csv

# Chức năng 3
python teencode_tool.py 3 input.xlsx "text,comment,title" output.xlsx
```

## 🎯 Chức năng

### 1️⃣ Teencode cột 'training_text'

**Mục đích:** Xử lý teencode cho cột `training_text` có sẵn

**Input:** File Excel/CSV có cột `training_text`

**Output:** File mới với `training_text` đã được xử lý

**Ví dụ:**
- Input: `"nguoi ta ko biet"` 
- Output: `"người ta không biết"`

**Sử dụng:**
```bash
python teencode_tool.py 1 FINAL_TRAINING_DATASET.xlsx
```

---

### 2️⃣ Teencode từ 'raw_comment' & 'raw_title'

**Mục đích:** Tạo cột `training_text` mới từ 2 cột raw với format: `title </s> comment`

**Input:** File Excel/CSV có cột `raw_comment` và `raw_title`

**Output:** File mới với cột `training_text` đã được tạo và xử lý teencode

**Ví dụ:**
- Input: 
  - `raw_title`: `"Boy pho moi nhu"`
  - `raw_comment`: `"Te nan xa hoi"`
- Output: 
  - `training_text`: `"boy phố mới nhú </s> tệ nạn xã hội"`

**Sử dụng:**
```bash
python teencode_tool.py 2 merged_labeled_data.csv
```

---

### 3️⃣ Teencode từ bất kỳ file nào

**Mục đích:** Xử lý teencode cho bất kỳ cột nào trong file CSV/XLSX/JSON

**Input:** 
- File CSV/XLSX/JSON
- Danh sách các cột cần xử lý

**Output:** File mới với các cột đã được xử lý teencode

**Ví dụ:**
- Input: File có cột `text`, `comment`, `title`
- Chọn xử lý: `text, comment`
- Output: 2 cột `text` và `comment` đã được xử lý teencode

**Sử dụng:**
```bash
python teencode_tool.py 3 data.xlsx "text,comment,title"
```

## 📝 Ví dụ chi tiết

### Ví dụ 1: Xử lý file training

```bash
# Interactive mode
python teencode_tool.py

# Chọn: 1
# Input: FINAL_TRAINING_DATASET_TEENCODE_20251225_151716.xlsx
# Output: (tự động tạo) teencode_training_20251228_120000.xlsx
```

### Ví dụ 2: Tạo training_text từ raw

```bash
# Command line mode
python teencode_tool.py 2 data/processed/merged_labeled_data_UTF8_20251224_183407.csv output.xlsx
```

### Ví dụ 3: Xử lý file custom

```bash
# Interactive mode
python teencode_tool.py

# Chọn: 3
# Input: my_data.csv
# Các cột có sẵn: ['id', 'text', 'comment', 'label']
# Nhập các cột cần xử lý: text, comment
# Output: (tự động tạo) teencode_custom_20251228_120000.csv
```

## 🔍 Các tính năng xử lý

Tool sử dụng `advanced_text_cleaning.py` với các tính năng:

✅ **Intensity Preservation**: Giữ nguyên từ tục tĩu viết tắt (đm, vcl, cc...)
✅ **Separator Preservation**: Bảo tồn `</s>` cho PhoBERT
✅ **Teencode Normalization**: Chuẩn hóa teencode neutral (ko → không, mh → mình...)
✅ **Person Name Masking**: Thay tên người bằng `<person>`
✅ **Emoji to Tags**: Chuyển emoji thành tags (`<emo_pos>`, `<emo_neg>`)
✅ **Unicode Normalization**: Chuẩn hóa dấu tiếng Việt

## 📊 Output

Mỗi lần chạy sẽ:
1. ✅ Tự động backup file gốc
2. ✅ Hiển thị progress
3. ✅ Hiển thị thống kê (số dòng xử lý, % có separator...)
4. ✅ Hiển thị mẫu kết quả
5. ✅ Lưu file output

## ⚠️ Lưu ý

- File input phải có encoding UTF-8
- Tool tự động backup file gốc trước khi xử lý
- Output file sẽ có timestamp để tránh ghi đè
- Chức năng 2 yêu cầu có cột `raw_comment` và `raw_title`
- Chức năng 3 cho phép xử lý nhiều cột cùng lúc

## 🐛 Troubleshooting

**Lỗi: "File không có cột 'training_text'"**
→ Sử dụng chức năng 2 hoặc 3 thay vì chức năng 1

**Lỗi: "File phải là .xlsx hoặc .csv"**
→ Chuyển đổi file sang định dạng được hỗ trợ

**Lỗi: "KeyError: 'raw_comment'"**
→ File không có cột `raw_comment`, sử dụng chức năng 1 hoặc 3

## 📞 Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. File input có đúng format không?
2. Các cột cần thiết có tồn tại không?
3. File có encoding UTF-8 không?

---

**Version:** 1.0  
**Author:** Senior AI Engineer  
**Date:** 2025-12-28
