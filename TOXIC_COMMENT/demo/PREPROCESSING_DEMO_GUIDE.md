# 🔥 Advanced Text Cleaning Demo - Hướng Dẫn

## Mô Tả
Giao diện demo **interactive** để xử lý và visualize preprocessing pipeline với 14 bước chuẩn.

## ✨ Tính Năng

### 1. 🔍 Single Text Processing
- Nhập text trực tiếp và xem kết quả ngay lập tức
- **Step-by-Step Visualization**: Xem từng bước transform của text
- **Statistics**: Thống kê độ dài, số lượng tags, features detected

### 2. 📊 Batch Processing
- Upload file `.txt` (mỗi dòng một text)
- Upload file `.csv` và chọn column cần clean
- Export kết quả thành CSV
- Progress tracking

### 3. 📖 Example Use Cases
- 9 ví dụ minh họa tính năng
- Test trực tiếp từ giao diện
- So sánh expected vs actual output

## 🎯 Các Tab Chức Năng

### Tab 1: Single Text
```
📝 Input                    ✨ Output
┌─────────────────┐         ┌─────────────────┐
│ Đ.m nguuuu vcl  │   →     │ đm ngu <intense>│
│ 😡 ko biết ns   │         │ vcl <emo_neg>   │
│ gì luôn ạ       │         │ không biết nói  │
└─────────────────┘         │ gì luôn ạ       │
                            └─────────────────┘
```

**Step-by-Step View:**
- ✅ Step 1: Unicode Normalize - CHANGED
- ✅ Step 6: Teencode Normalize - CHANGED
- ✅ Step 9: Emoji → Tags - CHANGED
- ⏭️ Step 11: Unicode Tricks - No change
- ...

**Statistics:**
- Original Length: 35
- Cleaned Length: 52
- Tags Added: 2
- Detected Features:
  - 😡 Negative Emotion
  - ⚡ Intensity Markers

### Tab 2: Batch Processing

#### Option A: Text File (.txt)
```txt
Đ.m nguuuu vcl 😡
ko biết ns gì ạ
m yêu t không?
Anh Tuấn đi Hà Nội
```

↓ Process

| ID | Original | Cleaned | Length_Before | Length_After |
|----|----------|---------|---------------|--------------|
| 1  | Đ.m...   | đm...   | 20            | 35           |
| 2  | ko...    | không...| 18            | 25           |
| ... | ...     | ...     | ...           | ...          |

#### Option B: CSV File
```csv
id,comment,label
1,"Đ.m nguuuu vcl",2
2,"ko biết ns gì",0
```

↓ Select column: `comment` → Process

```csv
id,comment,label,cleaned
1,"Đ.m nguuuu vcl",2,"đm ngu <intense> vcl"
2,"ko biết ns gì",0,"không biết nói gì"
```

### Tab 3: Examples

9 ví dụ test sẵn:

1. **Teencode Normalization**
   - Input: `ko biết ns gì luôn ạ`
   - Output: `không biết nói gì luôn ạ`

2. **Bypass Pattern**
   - Input: `Đ.m n.g.u vcl`
   - Output: `đm ngu vcl`

3. **Emoji & Intensity**
   - Input: `Nguuuuuu quáaaaa 😡`
   - Output: `ngu <very_intense> quá <very_intense> <emo_neg>`

4. **Context "m" Positive**
   - Input: `yêu m nhiều lắm`
   - Output: `yêu em nhiều lắm`

5. **Context "m" Toxic**
   - Input: `m ngu vcl`
   - Output: `mày ngu vcl`

6. **Person Name Masking**
   - Input: `Anh Tuấn và chị Hoa`
   - Output: `anh tuấn và <person>`

7. **English Insults**
   - Input: `stupid idiot fuck you`
   - Output: `<eng_insult> <eng_insult> <eng_vulgar> you`

8. **Leetspeak**
   - Input: `ch3t di ngu4`
   - Output: `chết đi ngua`

9. **Mixed Features**
   - Input: `@user Đ.m Trần Ngọc nguuuu 😡`
   - Output: `<user> đm <person> ngu <very_intense> <emo_neg>`

## 🚀 Cách Chạy

### Quick Start (Windows):
```bash
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"
run_preprocessing_demo.bat
```

### Manual:
```bash
streamlit run preprocessing_demo.py
```

### URL:
Mở trình duyệt: `http://localhost:8501`

## 🎨 Giao Diện

### Layout:
```
╔════════════════════════════════════════════╗
║  🔥 Advanced Text Cleaning Demo            ║
║  Interactive Preprocessing Pipeline        ║
╠════════════════════════════════════════════╣
║ Sidebar                Main Content        ║
║ ┌─────────┐          ┌──────────────────┐ ║
║ │⚙️ Settings│         │ 🔍 Single Text   │ ║
║ │         │          │ 📊 Batch Process │ ║
║ │☑️ Steps │          │ 📖 Examples      │ ║
║ │☑️ Stats │          └──────────────────┘ ║
║ │         │                               ║
║ │Pipeline │          [Tab Content]        ║
║ │1. Unicode│                              ║
║ │2. URLs  │                               ║
║ │3. Tags  │                               ║
║ │...      │                               ║
║ └─────────┘                               ║
╚════════════════════════════════════════════╝
```

### Color Scheme:
- **Input Box**: Yellow (`#fff3cd`)
- **Output Box**: Green (`#d4edda`)
- **Step Box**: Light Blue (`#f0f2f6`)
- **Changed**: Yellow highlight

## 📝 Use Cases

### 1. Development & Testing
```python
# Test new teencode entries
Input: "uh ns gì z"
Expected: "ừ nói gì vậy"
```

### 2. Data Quality Check
```python
# Upload dataset và check preprocessing
df['cleaned'] = preprocess(df['text'])
→ Download cleaned_dataset.csv
```

### 3. Demo for Stakeholders
```python
# Show preprocessing capabilities
- Live text transformation
- Explain each pipeline step
- Visual comparison
```

### 4. Training Data Preparation
```python
# Batch clean training data
Upload: train_raw.csv
Process: comment column
Download: train_cleaned.csv
```

## 🔧 Settings (Sidebar)

### Show Step-by-Step
✅ Enabled: Hiển thị 17 bước chi tiết
- Mỗi bước có before/after
- Chỉ show steps có thay đổi
- Expandable để tiết kiệm không gian

❌ Disabled: Chỉ show input → output

### Show Statistics
✅ Enabled: Hiển thị thống kê
- Length comparison
- Tag count
- Detected features

❌ Disabled: Ẩn thống kê

## 📊 Pipeline Steps (17 Steps)

1. **Unicode Normalize (NFC)** - Chuẩn hóa dấu tiếng Việt
2. **Remove URLs** - Xóa links
3. **Remove HTML** - Xóa HTML tags
4. **Remove Hashtags** - Xóa #hashtags
5. **Remove Mentions** - @user → `<user>`
6. **🔥 Teencode Normalize** - ko→không, ns→nói
7. **🔥 Person Names** - Trần Ngọc → `<person>`
8. **Lowercase** - CHỮ HOA → chữ thường
9. **🔥 Emoji → Tags** - 😡→`<emo_neg>`
10. **🔥 English Insults** - fuck→`<eng_vulgar>`
11. **Unicode Tricks** - Zero-width chars
12. **Bypass Patterns** - đ.m→đm
13. **Leetspeak** - ch3t→chết
14. **🔥 Repeated Chars** - nguuu→ngu `<intense>`
15. **🔥 Context "m"** - Smart m→em/mày
16. **Punctuation** - Normalize dấu câu
17. **Whitespace** - Normalize khoảng trắng

## 💡 Tips & Tricks

### Tip 1: Test Teencode
```
Input: "ko bik ns gì ak uh đc roi"
Expected: "không biết nói gì ạ ừ được rồi"
```

### Tip 2: Compare Outputs
```python
# Paste multiple versions và compare
Version 1: "m yêu t"
Version 2: "m ngu vcl"
→ See how context changes 'm' mapping
```

### Tip 3: Batch Process
```python
# Prepare file with multiple test cases
test_cases.txt:
Đ.m nguuuu vcl
ko biết ns gì
m yêu t không
...
→ Process all at once
```

### Tip 4: Export Results
```python
# After batch processing:
1. Click "Download Results (CSV)"
2. Use for training or analysis
3. Compare with expected outputs
```

## 🐛 Troubleshooting

### Issue 1: Encoding Error
**Error**: `UnicodeEncodeError`
**Fix**: Code đã có fix encoding cho Windows, restart nếu cần

### Issue 2: Import Error
**Error**: `ModuleNotFoundError: src.preprocessing`
**Fix**: 
```bash
cd "c:\Học sâu\Dataset"
streamlit run TOXIC_COMMENT/demo/preprocessing_demo.py
```

### Issue 3: File Upload Failed
**Error**: CSV parsing error
**Fix**: Ensure file is UTF-8 encoded

## 📈 Performance

- **Single Text**: < 0.1s (instant)
- **Batch 100 texts**: ~2-3s
- **Batch 1000 texts**: ~20-30s
- **File size limit**: 200MB (Streamlit default)

## 🎓 Learning Path

### Beginner:
1. Start with Tab 3 (Examples)
2. Test pre-made examples
3. Modify inputs slightly
4. Observe changes

### Intermediate:
1. Use Tab 1 (Single Text)
2. Enable Step-by-Step
3. Understand each pipeline step
4. Test custom inputs

### Advanced:
1. Use Tab 2 (Batch Processing)
2. Upload real datasets
3. Analyze statistics
4. Integrate with training pipeline

## ✅ Checklist

- [x] Single text processing
- [x] Step-by-step visualization
- [x] Statistics display
- [x] Batch processing (TXT)
- [x] Batch processing (CSV)
- [x] File upload/download
- [x] 9 example use cases
- [x] Settings sidebar
- [x] Responsive layout
- [x] Windows encoding fix

## 🎉 Conclusion

Demo này cung cấp:
- ✅ **Interactive interface** để test preprocessing
- ✅ **Visual pipeline** để hiểu từng bước
- ✅ **Batch processing** cho production
- ✅ **Ready for training** integration

**Perfect for:**
- Testing new teencode entries
- Data quality assurance
- Demo for stakeholders
- Training data preparation

---

**Happy Preprocessing! 🚀**

*Created: December 31, 2025*
