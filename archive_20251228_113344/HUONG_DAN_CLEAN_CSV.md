# 📖 HƯỚNG DẪN SỬ DỤNG ADVANCED TEXT CLEANING

## 🎯 Mục đích
File `advanced_text_cleaning.py` được thiết kế để làm sạch text tiếng Việt cho mô hình PhoBERT, bao gồm:
- Chuẩn hóa Unicode
- Chuyển đổi teencode → tiếng Việt chuẩn
- Xử lý emoji → sentiment tags
- Mask tên người → `<person>`
- Xử lý từ toxic, intensity markers
- Và nhiều tính năng khác

## 📁 Các cách sử dụng

### 1️⃣ Sử dụng với CSV file (KHUYẾN NGHỊ)

#### Cú pháp cơ bản:
```bash
python clean_csv.py <file_input.csv> -c <tên_cột_text> -o <file_output.csv>
```

#### Ví dụ cụ thể:

**Ví dụ 1: File có cột tên "text"**
```bash
python clean_csv.py data.csv -c text -o data_cleaned.csv
```

**Ví dụ 2: File có cột tên "comment"**
```bash
python clean_csv.py comments.csv -c comment -o comments_cleaned.csv
```

**Ví dụ 3: File có encoding đặc biệt**
```bash
python clean_csv.py data.csv -c content -o output.csv --encoding utf-8-sig
```

**Ví dụ 4: Tự động tạo tên file output**
```bash
python clean_csv.py data.csv -c text
# Sẽ tạo file: data_cleaned.csv
```

#### Tham số:
- `input_file`: File CSV đầu vào (bắt buộc)
- `-c, --column`: Tên cột chứa text cần clean (bắt buộc)
- `-o, --output`: File CSV đầu ra (tùy chọn, mặc định: `<input>_cleaned.csv`)
- `--encoding`: Encoding của file (tùy chọn, mặc định: `utf-8`)

---

### 2️⃣ Sử dụng trong Python code

#### Import và sử dụng trực tiếp:

```python
from src.preprocessing.advanced_text_cleaning import advanced_clean_text

# Làm sạch 1 câu
text = "Mày ngu vl, đm 😡😡😡"
cleaned = advanced_clean_text(text)
print(cleaned)
# Output: "mày ngu vãi lồn địt mẹ <emo_neg> <intense>"
```

#### Xử lý DataFrame:

```python
import pandas as pd
from src.preprocessing.advanced_text_cleaning import advanced_clean_text

# Đọc CSV
df = pd.read_csv('data.csv')

# Áp dụng cleaning cho cột 'comment'
df['comment_cleaned'] = df['comment'].apply(
    lambda x: advanced_clean_text(str(x)) if pd.notna(x) else ""
)

# Lưu kết quả
df.to_csv('data_cleaned.csv', index=False, encoding='utf-8-sig')
```

#### Xử lý với progress bar:

```python
import pandas as pd
from tqdm import tqdm
from src.preprocessing.advanced_text_cleaning import advanced_clean_text

tqdm.pandas(desc="Cleaning text")

df = pd.read_csv('data.csv')
df['cleaned'] = df['text'].progress_apply(
    lambda x: advanced_clean_text(str(x)) if pd.notna(x) else ""
)
```

---

### 3️⃣ Các tính năng nâng cao

#### A. Mask tên người
```python
from src.preprocessing.advanced_text_cleaning import replace_person_names

text = "Nguyễn Văn A nói rằng anh Tuấn rất giỏi"
masked = replace_person_names(text)
print(masked)
# Output: "<person> nói rằng <person> rất giỏi"
```

#### B. Xử lý emoji đặc biệt (LGBT, sentiment)
```python
from src.preprocessing.advanced_text_cleaning import clean_text_with_special_emoji

text = "Tôi ủng hộ 🏳️‍🌈 và yêu bạn 😘"
cleaned = clean_text_with_special_emoji(text)
print(cleaned)
# Output: "tôi ủng hộ lgbt và yêu bạn <emo_pos>"
```

#### C. Demo Person Name Detector
```bash
python src/preprocessing/advanced_text_cleaning.py --demo-names
```

#### D. Chạy test suite
```bash
python src/preprocessing/advanced_text_cleaning.py
```

---

## 📊 Ví dụ thực tế

### Ví dụ 1: Dataset hate speech

**File: hate_speech.csv**
```csv
id,text,label
1,"Mày ngu vl 😡",1
2,"Bắc kỳ rau muống 🐕",1
3,"Bạn rất đẹp ❤️",0
```

**Lệnh:**
```bash
python clean_csv.py hate_speech.csv -c text -o hate_speech_cleaned.csv
```

**Kết quả: hate_speech_cleaned.csv**
```csv
id,text,label,text_cleaned
1,"Mày ngu vl 😡",1,"mày ngu vãi lồn <emo_neg>"
2,"Bắc kỳ rau muống 🐕",1,"bắc kỳ rau muống chó"
3,"Bạn rất đẹp ❤️",0,"bạn rất đẹp <emo_pos>"
```

### Ví dụ 2: Dataset comments

**File: youtube_comments.csv**
```csv
video_id,comment,likes
v123,"Ko hiểu sao mấy thg này ngu thế",10
v123,"Video hay quá bạn ơi 😍",5
```

**Lệnh:**
```bash
python clean_csv.py youtube_comments.csv -c comment -o comments_cleaned.csv
```

---

## 🔧 Xử lý lỗi thường gặp

### Lỗi 1: Không tìm thấy cột
```
❌ KHÔNG TÌM THẤY CỘT 'text'
📋 Các cột có sẵn: id, comment, label
```

**Giải pháp:** Kiểm tra tên cột trong CSV và dùng đúng tên:
```bash
python clean_csv.py data.csv -c comment -o output.csv
```

### Lỗi 2: Encoding không đúng
```
UnicodeDecodeError: 'utf-8' codec can't decode...
```

**Giải pháp:** Thử encoding khác:
```bash
python clean_csv.py data.csv -c text --encoding utf-8-sig
# hoặc
python clean_csv.py data.csv -c text --encoding cp1252
```

### Lỗi 3: Module không tìm thấy
```
ModuleNotFoundError: No module named 'src.preprocessing.advanced_text_cleaning'
```

**Giải pháp:** Đảm bảo chạy từ thư mục gốc của project:
```bash
cd "c:\Học sâu\Dataset"
python clean_csv.py data.csv -c text
```

---

## 📝 Checklist trước khi chạy

- [ ] File CSV tồn tại
- [ ] Biết tên cột chứa text cần clean
- [ ] Đã cài đặt dependencies: `pandas`, `tqdm`, `transformers` (optional)
- [ ] Đang ở thư mục gốc của project (`c:\Học sâu\Dataset`)

---

## 🚀 Quick Start

**Bước 1:** Kiểm tra cột trong CSV
```bash
python -c "import pandas as pd; df = pd.read_csv('data.csv'); print(df.columns.tolist())"
```

**Bước 2:** Chạy cleaning
```bash
python clean_csv.py data.csv -c <tên_cột> -o output.csv
```

**Bước 3:** Kiểm tra kết quả
```bash
python -c "import pandas as pd; df = pd.read_csv('output.csv'); print(df.head())"
```

---

## 💡 Tips

1. **Luôn backup file gốc** trước khi clean
2. **Kiểm tra preview** sau khi clean để đảm bảo kết quả đúng
3. **Sử dụng encoding `utf-8-sig`** nếu file có BOM
4. **Tên cột phân biệt hoa thường**: `Text` ≠ `text`
5. **Kết quả sẽ tạo cột mới** `<tên_cột>_cleaned`, giữ nguyên cột gốc

---

## 📞 Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. File `advanced_text_cleaning.py` có tồn tại tại `src/preprocessing/`
2. Đã cài đặt đủ dependencies
3. Đang chạy từ đúng thư mục
4. Tên cột và encoding đúng
