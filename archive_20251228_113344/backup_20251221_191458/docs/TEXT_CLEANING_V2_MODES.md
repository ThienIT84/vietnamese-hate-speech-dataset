# 🔥 Advanced Text Cleaning V2.1 - Multi-Mode Processing Guide

## 📋 Tổng quan

Module hỗ trợ **3 quy trình xử lý** cho các giai đoạn khác nhau của pipeline:

| Mode | Input | Output | Use Case |
|------|-------|--------|----------|
| **Mode 1: JSON→CSV** | JSON từ Apify crawler | CSV với input_text & teencode | Dữ liệu thô từ web scraping |
| **Mode 2: Raw CSV** | CSV dữ liệu thô | CSV với input_text cleaned | CSV chưa xử lý teencode |
| **Mode 3: Labeled CSV** | CSV đã có input_text | CSV với input_text re-cleaned | File đã label cần xử lý lại |

---

## 🎯 Mode 1: JSON → CSV (Apify Workflow)

### **Mục đích**
Xử lý file JSON từ Apify crawler, gán tiêu đề, normalize teencode, tạo format `input_text`.

### **Input Format**
```
data/raw/facebook/
  ├── confession_voz.json
  ├── showbiz_drama.json
  └── social_issues_tai_nan.json
```

### **Sử dụng**

**Command Line:**
```bash
# Auto-detect (directory = JSON mode)
python advanced_text_cleaning.py data/raw/facebook

# Explicit mode
python advanced_text_cleaning.py data/raw/facebook --mode json -o output.csv
```

**Python API:**
```python
from advanced_text_cleaning import process_json_to_csv

df = process_json_to_csv('data/raw/facebook', 'data/processed')
```

### **Output Format**
```csv
id,input_text,raw_comment,raw_title,cleaned_comment,cleaned_title,...
123,tệ nạn xã hội </s> nguuuu vcl,nguuuu vcl,Tệ nạn xã hội,...
```

**Đặc điểm:**
- ✅ Tự động detect platform (Facebook/YouTube) từ directory name
- ✅ Extract topic từ filename (e.g., `confession_voz.json` → `confession`)
- ✅ Apply teencode normalization
- ✅ Format: `title </s> comment`
- ✅ Merge với master CSV nếu đã tồn tại
- ✅ Remove duplicates

---

## 🎯 Mode 2: Raw CSV → Cleaned CSV

### **Mục đích**
Xử lý CSV dữ liệu thô (chưa có teencode), normalize và tạo cột `input_text`.

### **Input Format**
```csv
comment,post_title,author,likes
nguuuu vcl,Tệ nạn xã hội,user123,10
đẹp quá,Showbiz drama,user456,25
```

### **Sử dụng**

**Command Line:**
```bash
# Auto-detect (CSV without input_text = raw mode)
python advanced_text_cleaning.py raw_data.csv -o cleaned.csv

# Explicit mode với title column
python advanced_text_cleaning.py raw_data.csv --mode raw -c comment --title post_title
```

**Python API:**
```python
from advanced_text_cleaning import process_raw_csv

df = process_raw_csv(
    'raw_data.csv',
    comment_column='comment',
    title_column='post_title',
    output_path='cleaned.csv'
)
```

### **Output Format**
```csv
comment,post_title,input_text
nguuuu vcl,Tệ nạn xã hội,tệ nạn xã hội </s> ngu <very_intense> vãi lồn
đẹp quá,Showbiz drama,showbiz drama </s> đẹp quá
```

**Đặc điểm:**
- ✅ Giữ nguyên tất cả columns gốc
- ✅ Thêm cột `input_text` mới
- ✅ Apply full teencode normalization
- ✅ Tự động gán context từ title (nếu có)
- ✅ Xử lý missing values an toàn

---

## 🎯 Mode 3: Labeled CSV → Re-cleaned

### **Mục đích**
Xử lý lại file đã có `input_text` (như `labeling_task_Thien.csv`), apply teencode normalization lại.

### **Input Format**
```csv
id,input_text,label,note
123,boy phố </s> nguuuu vcl,1,toxic
456,đẹp quá </s> yêu m,0,clean
```

### **Sử dụng**

**Command Line:**
```bash
# Auto-detect (CSV có input_text = labeled mode)
python advanced_text_cleaning.py labeling_task_Thien.csv -o output.csv

# Explicit mode
python advanced_text_cleaning.py labeling_task_Thien.csv --mode labeled

# Disable progress bar
python advanced_text_cleaning.py labeling_task_Thien.csv --no-progress
```

**Python API:**
```python
from advanced_text_cleaning import process_labeled_csv

df = process_labeled_csv(
    'labeling_task_Thien.csv',
    output_path='recleaned.csv',
    show_progress=True
)
```

### **Output Format**
```csv
id,input_text,input_text_original,label,note
123,boy phố nguuuu vcl,boy phố </s> nguuuu vcl,1,toxic
456,đẹp quá yêu em,đẹp quá </s> yêu m,0,clean
```

**Đặc điểm:**
- ✅ Giữ nguyên tất cả columns và metadata
- ✅ Backup original vào `input_text_original`
- ✅ Re-clean cột `input_text` với full pipeline
- ✅ Context-aware "m" mapping (yêu m → yêu em)
- ✅ Remove `</s>` separator
- ✅ Intensity markers, emoji tags, etc.

---

## 🔍 Auto-Detection Logic

Module tự động detect mode dựa trên input:

```python
if input.is_directory():
    mode = 'json'  # Mode 1
elif 'input_text' in csv.columns:
    mode = 'labeled'  # Mode 3
else:
    mode = 'raw'  # Mode 2
```

**Hoặc chỉ định rõ:**
```bash
python advanced_text_cleaning.py file.csv --mode labeled
```

---

## 📊 Comparison Examples

### **Mode 2 vs Mode 3**

**Mode 2 (Raw CSV):**
```bash
# Input: raw_comments.csv
comment,title
nguuuu vcl,Tệ nạn
yêu m,Confession

# Command
python advanced_text_cleaning.py raw_comments.csv --mode raw -c comment --title title

# Output: input_text = "title </s> comment" (NEW column)
comment,title,input_text
nguuuu vcl,Tệ nạn,tệ nạn </s> ngu <very_intense> vãi lồn
yêu m,Confession,confession </s> yêu em
```

**Mode 3 (Labeled CSV):**
```bash
# Input: labeled.csv
id,input_text,label
1,Tệ nạn </s> nguuuu vcl,1
2,Confession </s> yêu m,0

# Command
python advanced_text_cleaning.py labeled.csv --mode labeled

# Output: input_text REPLACED (no </s>)
id,input_text,input_text_original,label
1,tệ nạn nguuuu vcl,Tệ nạn </s> nguuuu vcl,1
2,confession yêu em,Confession </s> yêu m,0
```

---

## 🛠️ Advanced Usage

### **Custom Output Path**
```bash
python advanced_text_cleaning.py input.csv -o /path/to/output.csv
```

### **Disable Progress Bar**
```bash
python advanced_text_cleaning.py large_file.csv --no-progress
```

### **Stop on First Error**
```bash
python advanced_text_cleaning.py data.csv --stop-on-error
```

### **Python API - Batch Processing**
```python
from pathlib import Path
from advanced_text_cleaning import process_labeled_csv

# Process multiple files
input_dir = Path('data/labeled')
output_dir = Path('data/recleaned')

for csv_file in input_dir.glob('labeling_task_*.csv'):
    print(f"Processing {csv_file.name}...")
    output = output_dir / f"{csv_file.stem}_recleaned.csv"
    process_labeled_csv(csv_file, output, show_progress=False)
```

---

## 🔧 Troubleshooting

### **"Column 'text' not found"**
```bash
# Module sẽ auto-detect common names: text, comment, content, message, input_text
# Nếu không detect được, specify rõ:
python advanced_text_cleaning.py file.csv -c your_column_name
```

### **"Cannot auto-detect mode"**
```bash
# Chỉ định rõ mode:
python advanced_text_cleaning.py file.csv --mode labeled
```

### **Unicode encoding errors (Windows)**
```bash
# Đã fix trong V2.1 - sử dụng ASCII output thay vì emoji
[SUCCESS] Processing completed!  # Thay vì 🎉
```

---

## 📝 Complete Workflow Example

### **Quy trình đầy đủ từ crawl đến train:**

```bash
# Bước 1: Crawl data với Apify → JSON files
# Output: data/raw/facebook/*.json

# Bước 2: JSON → Master CSV (Mode 1)
python advanced_text_cleaning.py data/raw/facebook --mode json
# Output: data/processed/facebook_master.csv

# Bước 3: Sample & Split for labeling
python split_data_for_labeling.py

# Bước 4: Labeling (Label Studio)
# Output: labeling_task_Thien.csv, labeling_task_Kiet.csv, etc.

# Bước 5: Re-clean labeled data (Mode 3)
python advanced_text_cleaning.py labeling_task_Thien.csv --mode labeled
python advanced_text_cleaning.py labeling_task_Kiet.csv --mode labeled
# Output: *_recleaned.csv

# Bước 6: Merge & Train
python merge_labeled_data.py
python train_phobert.py
```

---

## 🎓 Best Practices

1. **Mode 1**: Dùng cho dữ liệu thô từ Apify/crawler
2. **Mode 2**: Dùng cho CSV tự thu thập (manual export từ social media)
3. **Mode 3**: Dùng cho file đã label cần update preprocessing
4. **Auto-detect**: Để module tự nhận diện (default, recommended)
5. **Progress bar**: Disable với `--no-progress` cho file lớn hoặc CI/CD

---

## 📄 Related Documentation

- [TEXT_CLEANING_GUIDE.md](TEXT_CLEANING_GUIDE.md) - Full API reference
- [GUIDELINE_GAN_NHAN_V3.md](GUIDELINE_GAN_NHAN_V3.md) - Labeling guidelines
- [examples/text_cleaning_usage.py](../examples/text_cleaning_usage.py) - Code examples

---

## ✅ Version History

**V2.1 (2025-12-21)**
- ✨ Added 3 processing modes (JSON, Raw, Labeled)
- ✨ Auto-detect mode from input structure
- ✨ Fixed Windows terminal encoding issues
- ✨ Auto-detect common column names
- 🐛 Fixed emoji output for Windows cmd/PowerShell
