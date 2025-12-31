# 🎯 TOXIC_COMMENT Demo Suite

## 📦 Available Demos

Thư mục này chứa 2 ứng dụng demo:

### 1. 🛡️ SafeSense-Vi Demo (`Safesense_VI.py`)
**Mục đích**: Demo phát hiện ngôn ngữ độc hại với PhoBERT model

**Tính năng**:
- Phân tích toxic comments (3 labels: Clean, Offensive, Hate)
- Context-aware detection (Title + Comment)
- Real-time prediction với model trained
- Probability distribution visualization

**Run:**
```bash
run_demo.bat
# hoặc
streamlit run Safesense_VI.py
```

**Use Case**: 
- Demo cho stakeholders
- Test model predictions
- Product showcase

---

### 2. 🔥 Preprocessing Demo (`preprocessing_demo.py`)
**Mục đích**: Interactive interface để test và visualize preprocessing pipeline

**Tính năng**:
- ✨ **Single Text**: Process và xem step-by-step
- 📊 **Batch Processing**: Upload TXT/CSV và clean hàng loạt
- 📖 **Examples**: 9 test cases minh họa
- 📈 **Statistics**: Length, tags, features detected
- 🔬 **Step-by-Step View**: Xem 17 bước transform

**Run:**
```bash
run_preprocessing_demo.bat
# hoặc
streamlit run preprocessing_demo.py
```

**Use Case**:
- Development & testing teencode
- Data quality check
- Training data preparation
- Learning preprocessing pipeline

---

## 🚀 Quick Start

### Method 1: Batch Scripts (Recommended)
```bash
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"

# Run SafeSense-Vi (Toxicity Detection)
run_demo.bat

# Run Preprocessing Demo (Text Cleaning)
run_preprocessing_demo.bat
```

### Method 2: Manual
```bash
# Test preprocessing first
python test_preprocessing.py

# Run SafeSense-Vi
streamlit run Safesense_VI.py

# Run Preprocessing Demo
streamlit run preprocessing_demo.py
```

---

## 📁 File Structure

```
demo/
├── Safesense_VI.py              # Toxicity detection demo
├── preprocessing_demo.py        # Preprocessing pipeline demo
├── test_preprocessing.py        # Test script (10 tests)
│
├── run_demo.bat                 # Quick start for SafeSense-Vi
├── run_preprocessing_demo.bat   # Quick start for Preprocessing
│
├── README_DEMO.md               # SafeSense-Vi guide
├── PREPROCESSING_DEMO_GUIDE.md  # Preprocessing demo guide
├── TEST_CASES.md                # 40+ test cases
├── TOM_TAT_CAP_NHAT.md         # Update summary (Vietnamese)
├── UPDATE_SUMMARY.md            # Update summary (English)
├── CHECKLIST.md                 # Quick checklist
└── README_DEMOS.md              # This file
```

---

## 🎯 Comparison: Which Demo to Use?

| Feature | SafeSense-Vi | Preprocessing Demo |
|---------|--------------|-------------------|
| **Purpose** | Model prediction | Data preprocessing |
| **Input** | Title + Comment | Raw text |
| **Output** | Label (0/1/2) + Probability | Cleaned text |
| **Visualization** | Probability chart | Step-by-step pipeline |
| **Use Case** | Product demo | Development/Testing |
| **Model Required** | ✅ Yes | ❌ No |
| **Batch Processing** | ❌ No | ✅ Yes (TXT/CSV) |
| **Step View** | ❌ No | ✅ Yes (17 steps) |
| **Export** | ❌ No | ✅ Yes (CSV) |

---

## 💡 Workflow Recommendations

### For Development:
```
1. Use Preprocessing Demo
   → Test teencode entries
   → Check pipeline steps
   → Validate transformations

2. Export cleaned data
   → Use for training

3. Use SafeSense-Vi
   → Test trained model
   → Demo predictions
```

### For Data Preparation:
```
1. Upload dataset to Preprocessing Demo
2. Select column to clean
3. Process & download CSV
4. Use cleaned data for training
```

### For Stakeholder Demo:
```
1. Start with Preprocessing Demo
   → Show text cleaning capabilities
   → Explain pipeline steps

2. Move to SafeSense-Vi
   → Show model predictions
   → Demonstrate context-awareness
```

---

## 🧪 Test Both Demos

### Test 1: Context-Aware Detection

**Preprocessing Demo:**
```
Input: "Đáng bị tử hình hết bọn tham nhũng"
Output: "đáng bị tử hình hết bọn tham nhũng"
```

**SafeSense-Vi:**
```
Title: "Vụ án tham nhũng nghiêm trọng"
Comment: "Đáng bị tử hình hết bọn tham nhũng"
→ Label 0 (Clean - tường thuật)
```

**Without Context:**
```
Title: (empty)
Comment: "Đáng bị tử hình hết bọn tham nhũng"
→ Label 2 (Hate - kích động)
```

### Test 2: Teencode Processing

**Preprocessing Demo:**
```
Input: "m yêu t k? ko bik ns gì ạ"
Output: "em yêu tôi không? không biết nói gì ạ"
```

**SafeSense-Vi:**
```
Comment: "m yêu t k? ko bik ns gì ạ"
→ Auto-clean → Predict
→ Label 0 (Clean)
```

---

## 📊 Features Summary

### SafeSense-Vi Features:
- ✅ Title + Comment input
- ✅ Real-time preprocessing
- ✅ Model prediction (3 labels)
- ✅ Confidence scores
- ✅ Probability distribution chart
- ✅ Label explanations
- ✅ Example test cases

### Preprocessing Demo Features:
- ✅ Single text processing
- ✅ Step-by-step visualization (17 steps)
- ✅ Statistics (length, tags, features)
- ✅ Batch processing (TXT/CSV)
- ✅ File upload/download
- ✅ 9 example use cases
- ✅ Settings sidebar
- ✅ Export results to CSV

---

## 🎓 Learning Resources

### Documentation:
- **SafeSense-Vi**: See `README_DEMO.md`
- **Preprocessing**: See `PREPROCESSING_DEMO_GUIDE.md`
- **Test Cases**: See `TEST_CASES.md`
- **Updates**: See `TOM_TAT_CAP_NHAT.md`

### Code References:
- **Preprocessing Logic**: `src/preprocessing/advanced_text_cleaning.py`
- **Pipeline Guideline**: `GUIDELINE_V7.2_TOM_TAT.md`
- **Process Flow**: `QUY_TRINH_XU_LY_TOM_TAT.md`

---

## ✅ Prerequisites

### Required:
```bash
pip install streamlit torch transformers pandas
```

### Optional (for full features):
```bash
pip install tqdm numpy scikit-learn
```

### Model Files:
- SafeSense-Vi requires trained model at: `C:\Học sâu\Dataset\TOXIC_COMMENT\models`
- Preprocessing Demo: No model required

---

## 🐛 Troubleshooting

### Issue: Module not found
```bash
# Solution: Run from correct directory
cd "c:\Học sâu\Dataset"
streamlit run TOXIC_COMMENT/demo/preprocessing_demo.py
```

### Issue: Encoding error
```bash
# Already fixed in code with UTF-8 encoding
# Restart terminal if issue persists
```

### Issue: Model not found (SafeSense-Vi)
```python
# Update model path in Safesense_VI.py line 35
model = AutoModelForSequenceClassification.from_pretrained(
    "YOUR_MODEL_PATH", 
    num_labels=3
)
```

### Issue: Port already in use
```bash
# Streamlit default: 8501
# If busy, Streamlit auto-increments to 8502, 8503...
# Or manually specify:
streamlit run preprocessing_demo.py --server.port 8502
```

---

## 📈 Performance Tips

### For Large Batch Processing:
1. Use Preprocessing Demo (Tab 2)
2. Split large files into chunks (< 10k rows)
3. Process separately and merge results

### For Real-time Testing:
1. Use Preprocessing Demo (Tab 1)
2. Enable Step-by-Step for learning
3. Disable for faster processing

### For Production:
```python
# Use Python API directly (faster)
from src.preprocessing.advanced_text_cleaning import clean_text

# Batch process
cleaned = [clean_text(text) for text in texts]
```

---

## 🎉 Summary

**Two Powerful Demos:**

1. **SafeSense-Vi**: Product-ready toxicity detection
2. **Preprocessing Demo**: Development-friendly text cleaning

**Both Include:**
- ✅ Real preprocessing (14 steps)
- ✅ Teencode normalization (300+ entries)
- ✅ Context-aware features
- ✅ Interactive interface
- ✅ Ready for production

**Choose Based On:**
- **Testing model?** → Use SafeSense-Vi
- **Preparing data?** → Use Preprocessing Demo
- **Learning pipeline?** → Use Preprocessing Demo
- **Demo for users?** → Use SafeSense-Vi

---

**Happy Testing! 🚀**

*Last Updated: December 31, 2025*
