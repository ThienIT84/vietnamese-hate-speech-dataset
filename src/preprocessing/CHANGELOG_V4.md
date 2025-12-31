# 📝 TÓM TẮT THAY ĐỔI - apify_to_csv.py V4.0

**Ngày cập nhật:** 16/12/2025  
**Phiên bản:** V4.0 - Context-aware Dataset

---

## 🎯 MỤC ĐÍCH

Cập nhật script `apify_to_csv.py` để tạo dataset **có ngữ cảnh (context)** phù hợp với:
- Guideline gán nhãn V4.0
- Format training hiện tại: `title </s> comment`
- Quy trình gán nhãn 3 labels (0, 1, 2)

---

## 🔄 THAY ĐỔI CHÍNH

### 1. OUTPUT FORMAT (⭐ QUAN TRỌNG NHẤT)

**Trước đây:**
```csv
id,text,cleaned_text,cleaned_text_norm,label,prediction,...
abc123,"mày béo vậy","mày béo vậy","mày béo vậy",,
```

**Bây giờ:**
```csvnote
id,input_text,label,
abc123,"hằng du mục về việt nam </s> mày béo vậy",,
```

### 2. CONTEXT BUILDING

**Thêm mới:** Hàm `build_input_text(title, comment)`
- Format: `title </s> comment`
- Truncate thông minh:
  - Title: max 50 tokens
  - Total: max 256 tokens
  - Dùng PhoBERT tokenizer (fallback về word split)
- Nếu không có title: chỉ trả về comment

### 3. EMOJI MAPPING

**Thêm mới:** Dictionary `EMOJI_MAP` với 14 emojis quan trọng
```python
'🏳️‍🌈' → ' đồng tính '
'❤️' → ' yêu '
'💔' → ' chia tay '
```

**Lý do:** 
- Emoji mang ngữ nghĩa trong LGBT, confession topics
- Model không học được từ emoji raw

### 4. TEXT CLEANING PIPELINE

**Trước:** `clean_text()` → `normalize_text()`

**Bây giờ:** `clean_text_with_emoji()`
1. **Emoji → Text** (TRƯỚC tiên)
2. **Xóa hashtags** (tất cả)
3. **Advanced cleaning** (teencode, lowercase, v.v.)

### 5. COLUMNS OUTPUT

**Cột mới:**
- `input_text` ⭐ - Cột chính để gán nhãn
- `raw_comment`, `raw_title` - Dữ liệu gốc
- `cleaned_comment`, `cleaned_title` - Đã clean
- `note` - Ghi chú khi gán nhãn

**Cột bỏ:**
- `cleaned_text_norm` (merge vào cleaned_comment)
- `annotator_id`, `confidence`, `is_crosscheck` (không cần trong raw data)
- `prediction`, `pred_prob_toxic` (chỉ có sau khi train)

---

## 📊 SO SÁNH VỚI SCRIPTS KHÁC

### `prepare_unlabeled_with_context.py`
- **Giống:** 
  - Cùng dùng `build_input_text()`
  - Cùng emoji mapping
  - Cùng format output
- **Khác:**
  - `prepare_unlabeled`: Xử lý file CSV có sẵn
  - `apify_to_csv`: Xử lý JSON từ Apify

### `prepare_training_with_teencode.py`
- **Giống:**
  - Cùng emoji mapping
  - Cùng teencode normalization
- **Khác:**
  - `prepare_training`: Chỉ xử lý labeled data
  - `apify_to_csv`: Xử lý raw data mới

---

## 🚀 CÁCH SỬ DỤNG

### Trước khi chạy:
```bash
# 1. Kiểm tra dependencies
pip install transformers pandas tqdm

# 2. Đảm bảo có advanced_text_cleaning.py
ls src/preprocessing/advanced_text_cleaning.py

# 3. Chuẩn bị dữ liệu JSON
# Đặt vào data/raw/facebook/ hoặc data/raw/youtube/
```

### Chạy script:
```bash
cd src/preprocessing
python apify_to_csv.py
```

### Test trước khi chạy:
```bash
python test_apify_to_csv.py
```

### Output:
```
data/processed/
  ├── facebook_master.csv
  ├── youtube_master.csv
  ├── master_combined.csv  ← Gộp tất cả
  └── facebook_backup_20251216_143022.csv
```

---

## 🔍 VÍ DỤ THỰC TẾ

### Input (JSON từ Apify):
```json
{
  "postTitle": "Phân biệt vùng miền 🏳️‍🌈",
  "text": "#fyp mày béo như lợn vcl 💔",
  "likesCount": "1.2K"
}
```

### Output (CSV):
```csv
id,input_text,raw_comment,raw_title,cleaned_comment,cleaned_title,topic,label,note
abc123,"phân biệt vùng miền đồng tính </s> mày béo như lợn vãi chưởng chia tay","#fyp mày béo như lợn vcl 💔","Phân biệt vùng miền 🏳️‍🌈","mày béo như lợn vãi chưởng chia tay","phân biệt vùng miền đồng tính",Vùng miền,,
```

### Sau khi gán nhãn:
```csv
id,input_text,label,note
abc123,"phân biệt vùng miền đồng tính </s> mày béo như lợn vãi chưởng chia tay",2,"body_shaming + toxic"
```

---

## ✅ CHECKLIST KHI SỬ DỤNG

- [ ] Đã có file `advanced_text_cleaning.py` cùng folder
- [ ] Đã cài đặt transformers (hoặc chấp nhận fallback)
- [ ] Đã đặt JSON files vào `data/raw/facebook/` và `data/raw/youtube/`
- [ ] Đã backup dữ liệu cũ (nếu có)
- [ ] Đã chạy test: `python test_apify_to_csv.py`
- [ ] Kiểm tra output có đúng format: `title </s> comment`
- [ ] Kiểm tra emoji đã được convert
- [ ] Kiểm tra hashtag đã bị xóa

---

## 🐛 KNOWN ISSUES & SOLUTIONS

### Issue 1: PhoBERT tokenizer không load được
**Solution:** Script tự động fallback về word-based truncation. Không ảnh hưởng nhiều.

### Issue 2: File JSON không đúng format
**Check:**
```python
# JSON phải có format:
{
  "items": [...]  # Array of comments
}
# HOẶC
[...]  # Array trực tiếp
```

### Issue 3: Output rỗng
**Check:**
- Comments có ít nhất 5 ký tự không?
- Có bỏ qua nested replies (parentId) không?
- File JSON có đúng encoding UTF-8 không?

---

## 📌 LƯU Ý QUAN TRỌNG

1. **Không ghi đè nhãn cũ:** 
   - Nếu master file đã có labels → Script merge, không ghi đè
   - Backup tự động được tạo với timestamp

2. **Duplicate handling:**
   - Remove duplicate theo `input_text` (không phải `id`)
   - Vì `input_text` là cột chính để train

3. **Topic detection:**
   - Ưu tiên từ filename
   - Fallback về auto-detect từ content
   - Có thể custom trong hàm `auto_topic()`

4. **PhoBERT tokenizer:**
   - Cần thiết để truncate chính xác
   - Nhưng không bắt buộc (có fallback)
   - First run sẽ download model (~1GB)

---

## 📞 HỖ TRỢ

- **Guideline:** `docs/GUIDELLINE GÁN NHÃN V4.0.pdf`
- **README:** `src/preprocessing/README_APIFY_TO_CSV.md`
- **Test:** `src/preprocessing/test_apify_to_csv.py`
- **Scripts liên quan:**
  - `prepare_unlabeled_with_context.py`
  - `prepare_training_with_teencode.py`
  - `create_final_dataset_from_json.py`

---

## 🎉 KẾT LUẬN

Script đã được cập nhật để:
- ✅ Tạo dataset với context (title </s> comment)
- ✅ Phù hợp với guideline gán nhãn V4.0
- ✅ Xử lý emoji và teencode đúng cách
- ✅ Format output giống file training hiện tại
- ✅ Sẵn sàng để gán nhãn và train model

**Sẵn sàng sử dụng ngay! 🚀**
