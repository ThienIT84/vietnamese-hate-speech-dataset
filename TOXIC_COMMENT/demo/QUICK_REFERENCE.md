# 🎯 QUICK REFERENCE - Demo Suite

## 🚀 Chạy Nhanh

```bash
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"

# Preprocessing Demo (Recommended để bắt đầu)
run_preprocessing_demo.bat

# Toxicity Detection Demo
run_demo.bat

# Test preprocessing
python test_preprocessing.py
```

---

## 📱 2 Demos Available

### 🔥 Preprocessing Demo
**File**: `preprocessing_demo.py`  
**Purpose**: Xử lý và visualize text cleaning  
**URL**: http://localhost:8501

**3 Tabs**:
1. 🔍 **Single Text** - Process 1 text, xem step-by-step
2. 📊 **Batch** - Upload TXT/CSV, process nhiều texts
3. 📖 **Examples** - 9 test cases có sẵn

**Key Features**:
- ✅ 17-step visualization
- ✅ Statistics & metrics
- ✅ Export to CSV
- ✅ No model required

### 🛡️ SafeSense-Vi
**File**: `Safesense_VI.py`  
**Purpose**: Phát hiện toxic comments  
**URL**: http://localhost:8501

**Input**: Title + Comment  
**Output**: Label (0/1/2) + Probability

**Labels**:
- 0 = Clean (Sạch)
- 1 = Offensive (Phản cảm)
- 2 = Hate Speech (Thù ghét)

---

## 🧪 Quick Tests

### Test 1: Teencode
```
Input:  "ko biết ns gì ạ"
Output: "không biết nói gì ạ"
```

### Test 2: Context "m"
```
Positive: "m yêu t" → "em yêu tôi"
Toxic:    "m ngu"   → "mày ngu"
```

### Test 3: Emoji
```
Input:  "nguuuu 😡"
Output: "ngu <intense> <emo_neg>"
```

### Test 4: Bypass
```
Input:  "Đ.m n.g.u"
Output: "đm ngu"
```

---

## 📊 Preprocessing Pipeline (14 Steps)

1. Unicode NFC
2. Remove URLs/HTML
3. Remove Hashtags
4. Remove Mentions → `<user>`
5. **🔥 Teencode** (300+ words)
6. **🔥 Person Names** → `<person>`
7. Lowercase
8. **🔥 Emoji** → `<emo_neg>` / `<emo_pos>`
9. **🔥 English Insults**
10. Bypass Patterns
11. Leetspeak
12. **🔥 Repeated Chars** + Intensity
13. **🔥 Context "m"**
14. Punctuation + Space

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `preprocessing_demo.py` | Interactive preprocessing |
| `Safesense_VI.py` | Toxicity detection |
| `test_preprocessing.py` | Unit tests (10 cases) |
| `run_preprocessing_demo.bat` | Quick start preprocessing |
| `run_demo.bat` | Quick start toxicity |

---

## 💡 Common Tasks

### Task 1: Test Teencode Entry
```bash
1. run_preprocessing_demo.bat
2. Tab 1: Single Text
3. Input: "ko bik ns gì"
4. Click "Process"
5. Check Step 6: Teencode
```

### Task 2: Batch Clean Dataset
```bash
1. run_preprocessing_demo.bat
2. Tab 2: Batch Processing
3. Upload CSV
4. Select column
5. Process → Download
```

### Task 3: Test Model Prediction
```bash
1. run_demo.bat
2. Enter Title + Comment
3. Click "Phân Tích"
4. View Label + Probability
```

### Task 4: Debug Preprocessing
```bash
1. python test_preprocessing.py
2. Check all 10 tests pass
3. Or use preprocessing_demo.py step-by-step
```

---

## 🎯 Which Demo When?

| Situation | Use Demo |
|-----------|----------|
| Test preprocessing | Preprocessing Demo |
| Prepare training data | Preprocessing Demo |
| Test model | SafeSense-Vi |
| Demo for users | SafeSense-Vi |
| Debug text cleaning | Preprocessing Demo |
| Learn pipeline | Preprocessing Demo |
| Product showcase | SafeSense-Vi |

---

## ⚡ Shortcuts

### Windows:
```bash
# From anywhere
cd "c:\Học sâu\Dataset\TOXIC_COMMENT\demo"

# Run preprocessing demo
run_preprocessing_demo.bat

# Run toxicity demo
run_demo.bat

# Test
python test_preprocessing.py
```

### Stop Server:
```
Press Ctrl+C in terminal
```

### Change Port:
```bash
streamlit run preprocessing_demo.py --server.port 8502
```

---

## 📚 Documentation

- **Preprocessing Guide**: `PREPROCESSING_DEMO_GUIDE.md`
- **SafeSense Guide**: `README_DEMO.md`
- **Test Cases**: `TEST_CASES.md` (40+ cases)
- **Full Comparison**: `README_DEMOS.md`
- **Updates**: `TOM_TAT_CAP_NHAT.md`

---

## ✅ Checklist

Before demo:
- [ ] Dependencies installed (`streamlit`, `torch`, `transformers`)
- [ ] Model available (for SafeSense-Vi)
- [ ] Test preprocessing working (`python test_preprocessing.py`)

During demo:
- [ ] Show preprocessing step-by-step
- [ ] Demo batch processing
- [ ] Show model predictions
- [ ] Explain context-awareness

After demo:
- [ ] Export cleaned data
- [ ] Save test results
- [ ] Document findings

---

## 🎓 Learning Path

**Beginner** (30 mins):
1. Run `test_preprocessing.py`
2. Open Preprocessing Demo
3. Try Tab 3 (Examples)
4. Test 1-2 custom inputs

**Intermediate** (1 hour):
1. Use Tab 1 with Step-by-Step
2. Understand each pipeline step
3. Test SafeSense-Vi predictions
4. Compare context-aware results

**Advanced** (2+ hours):
1. Batch process real dataset
2. Analyze preprocessing effects
3. Train model with cleaned data
4. Evaluate on test set

---

**Print This & Keep Handy! 📌**

*Quick Reference v1.0 - December 31, 2025*
