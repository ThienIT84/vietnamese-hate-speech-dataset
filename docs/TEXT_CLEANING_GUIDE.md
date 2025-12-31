# 🔥 Advanced Text Cleaning V2.1 - Documentation

## 📖 Tổng quan

Module xử lý text tiếng Việt chuyên nghiệp cho PhoBERT với các tính năng:

- ✅ Context-aware normalization
- ✅ Intensity markers cho toxic detection  
- ✅ Emoji sentiment tags
- ✅ English insult detection
- ✅ Teencode normalization (450+ từ)
- ✅ Person/User masking
- ✅ **Batch processing CSV/XLSX**
- ✅ **CLI interface**
- ✅ **Progress tracking**

---

## 🚀 Cài đặt

```bash
# Install dependencies
pip install pandas openpyxl tqdm

# Import module
from src.preprocessing.advanced_text_cleaning import clean_text, clean_dataframe, clean_file
```

---

## 📝 Sử dụng

### 1️⃣ **Clean Single Text**

```python
from src.preprocessing.advanced_text_cleaning import clean_text

text = "Đ.m thằng Nguyễn Văn A nguuuuu vcl 😡"
cleaned = clean_text(text)
print(cleaned)
# Output: địt mẹ thằng <person> ngu <very_intense> vãi lồn <emo_neg>
```

### 2️⃣ **Clean DataFrame**

```python
import pandas as pd
from src.preprocessing.advanced_text_cleaning import clean_dataframe

df = pd.DataFrame({
    'comment': ["nguuuu vcl 😡", "đẹp quá ❤️"]
})

df_cleaned = clean_dataframe(df, text_column='comment')
print(df_cleaned)
```

**Output:**
```
   comment                  comment_cleaned
0  nguuuu vcl 😡             ngu <very_intense> vãi lồn <emo_neg>
1  đẹp quá ❤️                đẹp quá <emo_pos>
```

### 3️⃣ **Clean CSV File**

```python
from src.preprocessing.advanced_text_cleaning import clean_file

# Process CSV
clean_file(
    input_path='data.csv',
    output_path='data_cleaned.csv',
    text_column='comment'
)
```

### 4️⃣ **Clean Excel File**

```python
# Process Excel
clean_file(
    input_path='data.xlsx',
    output_path='data_cleaned.xlsx',
    text_column='feedback',
    sheet_name='Sheet1'
)
```

---

## 💻 Command Line Interface (CLI)

### **Basic Usage**

```bash
# Clean CSV file
python src/preprocessing/advanced_text_cleaning.py input.csv -o output.csv -c text

# Clean Excel file
python src/preprocessing/advanced_text_cleaning.py data.xlsx -c comment -s Sheet1

# Custom output column
python src/preprocessing/advanced_text_cleaning.py data.csv -c raw_text --output-col cleaned
```

### **CLI Options**

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `input` | - | Input file path | Required |
| `--output` | `-o` | Output file path | `input_cleaned.ext` |
| `--column` | `-c` | Text column name | `text` |
| `--sheet` | `-s` | Excel sheet name | `0` (first sheet) |
| `--output-col` | - | Output column name | `column_cleaned` |
| `--no-progress` | - | Disable progress bar | `False` |
| `--stop-on-error` | - | Stop on first error | `False` |

### **Examples**

```bash
# Example 1: Basic CSV cleaning
python src/preprocessing/advanced_text_cleaning.py comments.csv

# Example 2: With custom output
python src/preprocessing/advanced_text_cleaning.py comments.csv -o processed.csv -c feedback

# Example 3: Excel with specific sheet
python src/preprocessing/advanced_text_cleaning.py data.xlsx -s "User Comments" -c text

# Example 4: Without progress bar
python src/preprocessing/advanced_text_cleaning.py large_file.csv --no-progress
```

---

## ⚙️ Advanced Options

### **Custom Output Column Name**

```python
df_cleaned = clean_dataframe(
    df, 
    text_column='raw_text',
    output_column='processed_text'
)
```

### **Error Handling**

```python
# Continue on errors (default)
df_cleaned = clean_dataframe(df, text_column='text', handle_errors=True)

# Stop on first error
df_cleaned = clean_dataframe(df, text_column='text', handle_errors=False)
```

### **Disable Progress Bar**

```python
df_cleaned = clean_dataframe(df, text_column='text', show_progress=False)
```

---

## 📊 Processing Pipeline

```
Input Text
    ↓
1. Unicode Normalize (NFC)
2. HTML/URL Removal
3. Named Entity Masking (<user>, <person>)
4. Lowercase
5. Emoji → Sentiment Tags (<emo_neg>, <emo_pos>)
6. English Insults → Tags (<eng_insult>, <eng_vulgar>)
7. Bypass Pattern Removal (n.g.u → ngu)
8. Leetspeak Conversion (ch3t → chết)
9. Repeated Chars + Intensity (nguuuu → ngu <intense>)
10. Teencode Normalization (vcl → vãi lồn)
11. Context-aware "m" Mapping (yêu m → yêu em)
12. Whitespace & Punctuation
    ↓
Cleaned Text
```

---

## 🎯 Features Details

### **1. Intensity Markers**

| Pattern | Output | Tag |
|---------|--------|-----|
| `nguuuu` (3-4 repeats) | `ngu <intense>` | Moderate |
| `nguuuuuuu` (5+ repeats) | `ngu <very_intense>` | High |

### **2. Emoji Sentiment**

| Emoji | Tag | Type |
|-------|-----|------|
| 😢😭😡 | `<emo_neg>` | Negative |
| 😍❤️👍 | `<emo_pos>` | Positive |
| 😅🙂 | (removed) | Neutral |

### **3. English Insults**

| Word | Tag | Type |
|------|-----|------|
| stupid, idiot | `<eng_insult>` | Insult |
| fuck, shit | `<eng_vulgar>` | Vulgar |

### **4. Person Masking**

✅ **Masked (có họ):**
- "Nguyễn Văn A" → `<person>`
- "Thạch Trang" → `<person>`

❌ **Kept (không có họ):**
- "Bộ Mặt Thật" → (giữ nguyên)
- "Nàng Thơ" → (giữ nguyên)

---

## 📈 Performance

| Dataset Size | Processing Time | Memory Usage |
|--------------|-----------------|--------------|
| 1K rows | ~2 seconds | ~50 MB |
| 10K rows | ~15 seconds | ~100 MB |
| 100K rows | ~2 minutes | ~300 MB |

---

## 🔧 Troubleshooting

### **Error: Column not found**
```python
# Check available columns
print(df.columns.tolist())

# Specify correct column name
df_cleaned = clean_dataframe(df, text_column='your_column_name')
```

### **Error: File format not supported**
```
Supported formats: .csv, .xlsx, .xls
```

### **Slow processing**
```python
# Disable progress bar for slight speed improvement
clean_file('large.csv', show_progress=False)
```

---

## 📚 Examples

Xem file đầy đủ: `examples/text_cleaning_usage.py`

```bash
python examples/text_cleaning_usage.py
```

---

## 🆘 Support

Nếu có vấn đề:
1. Check input data format (CSV/Excel)
2. Verify column name exists
3. Check for null/empty values
4. Enable error handling: `handle_errors=True`

---

## 📝 Changelog

### V2.1 (2025-12-21)
- ✨ Added CLI interface
- ✨ Added batch processing for CSV/XLSX
- ✨ Added progress tracking with tqdm
- ✨ Added flexible error handling
- ✨ Added custom output column name
- 🐛 Fixed person masking (chỉ mask khi có họ)
- 🐛 Fixed tag protection in bypass patterns

### V2.0 (2025-12-21)
- ✨ Context-aware "m" mapping
- ✨ Intensity markers
- ✨ Emoji sentiment tags
- ✨ English insult detection

---

## 📄 License

MIT License - Free to use for research and commercial purposes.
