# 🔧 FIX LỖI IMPORT - SafeSense-Vi Demo

## ❌ Lỗi Gặp Phải

```
File "C:\Học sâu\Dataset\TOXIC_COMMENT\demo\Safesense_VI.py", line 14, in <module>
    from src.preprocessing.advanced_text_cleaning import clean_text
ModuleNotFoundError: No module named 'src'
```

## ✅ ĐÃ FIX

### Thay Đổi Code:

1. **Safesense_VI.py** - Cải thiện import path với error handling
2. **preprocessing_demo.py** - Tương tự
3. **run_demo.bat** - Thêm error checking
4. **run_preprocessing_demo.bat** - Cải thiện

### Chi Tiết Fix:

#### Before:
```python
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
from src.preprocessing.advanced_text_cleaning import clean_text
```

#### After:
```python
# Resolve path tuyệt đối
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Kiểm tra file tồn tại
if not (project_root / "src" / "preprocessing" / "advanced_text_cleaning.py").exists():
    st.error("❌ Không tìm thấy module preprocessing")
    st.stop()

# Import với error handling
try:
    from src.preprocessing.advanced_text_cleaning import clean_text
except ImportError as e:
    st.error(f"❌ Lỗi import: {e}")
    st.stop()
```

## 🚀 Cách Chạy (SAU KHI FIX)

### Cách 1: Dùng Batch File (RECOMMENDED)
```bash
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"
run_demo.bat
```

### Cách 2: Manual
```bash
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"
streamlit run Safesense_VI.py
```

### Cách 3: Preprocessing Demo
```bash
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"
run_preprocessing_demo.bat
```

## 🧪 Test Fix

```bash
# Test 1: Chạy test preprocessing
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"
python test_preprocessing.py

# Nếu pass → Fix thành công!
```

## 📝 Giải Thích

### Tại Sao Lỗi?
- Khi chạy từ thư mục `demo`, Python không tìm thấy thư mục `src`
- Module `src.preprocessing.advanced_text_cleaning` cần project root trong `sys.path`

### Fix Làm Gì?
1. **Resolve absolute path**: Dùng `.resolve()` để có path tuyệt đối
2. **Check if exists**: Kiểm tra module có tồn tại không
3. **Error handling**: Catch ImportError và hiển thị thông báo rõ ràng
4. **Avoid duplicate**: Chỉ add path nếu chưa có trong sys.path

### Cấu Trúc Thư Mục:
```
c:\Học sâu\Dataset\              ← PROJECT ROOT
├── src/
│   └── preprocessing/
│       └── advanced_text_cleaning.py
└── TOXIC_COMMENT/
    └── demo/
        ├── Safesense_VI.py      ← Running here
        └── preprocessing_demo.py
```

## ✅ Checklist Fix

- [x] Update import path trong Safesense_VI.py
- [x] Update import path trong preprocessing_demo.py
- [x] Add error handling
- [x] Update batch files
- [x] Test preprocessing pass
- [x] Tạo documentation

## 🎯 Nếu Vẫn Lỗi

### Lỗi 1: Module not found (after fix)
```bash
# Kiểm tra cấu trúc thư mục
dir "c:\Học sâu\Dataset\src\preprocessing"

# Phải thấy: advanced_text_cleaning.py
```

### Lỗi 2: Permission denied
```bash
# Chạy cmd/PowerShell as Administrator
```

### Lỗi 3: Encoding error
```bash
# Đã fix trong code với UTF-8 encoding
# Restart terminal nếu cần
```

### Lỗi 4: Streamlit not found
```bash
pip install streamlit torch transformers pandas
```

## 📞 Debug Commands

```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check project structure
cd "c:\Học sâu\Dataset"
dir /s src\preprocessing\advanced_text_cleaning.py

# Test import directly
cd "c:\Học sâu\Dataset"
python -c "from src.preprocessing.advanced_text_cleaning import clean_text; print('OK!')"
```

## ✅ Kết Luận

**Status**: ✅ **FIXED**

Bây giờ bạn có thể:
1. Chạy `run_demo.bat` từ thư mục demo
2. Chạy `run_preprocessing_demo.bat` từ thư mục demo
3. Code tự động tìm và import đúng module
4. Error messages rõ ràng nếu có vấn đề

**Chúc chạy thành công! 🚀**

---

*Fixed: December 31, 2025*
