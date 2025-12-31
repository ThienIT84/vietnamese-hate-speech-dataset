# 🚀 Project Migration Guide

## 📋 Overview

This guide helps you migrate from the **current cluttered structure** to a **clean, professional Data Science project structure**.

**Current State:**
- ❌ 7 test files in root directory
- ❌ Data files mixed with code
- ❌ Hardcoded paths everywhere
- ❌ Import statements break easily

**Target State:**
- ✅ Clean PEP8-compliant structure
- ✅ Separation of data/code/docs
- ✅ Relative imports with PROJECT_ROOT
- ✅ Easy to maintain and scale

---

## 🎯 Quick Start (3 Steps)

### Step 1: Review the Analysis
```bash
# Read the full analysis
cat PROJECT_RESTRUCTURE_ANALYSIS.md

# Key sections:
# - Files to DELETE (23 files)
# - Files to MOVE (29 files)
# - Import fixes needed (15+ files)
```

### Step 2: Run Migration (DRY RUN first!)
```bash
# Simulate migration (safe - no changes)
python migrate_project.py --dry-run

# Review the output carefully!
# If everything looks good, run actual migration:
python migrate_project.py --execute
```

### Step 3: Fix Imports
```bash
# Simulate import fixes
python fix_imports.py --dry-run

# Apply import fixes
python fix_imports.py --execute

# Also fix hardcoded paths (optional)
python fix_imports.py --execute --fix-paths
```

---

## 📂 Before vs After Structure

### BEFORE (Cluttered)
```
Dataset/
├── quick_test.py              # ❌ Root clutter
├── test_emoji.py              # ❌ Root clutter
├── check_dict.py              # ❌ Root clutter
├── data/
│   ├── labeled/
│   │   ├── test.ipynb         # ❌ Wrong location
│   │   └── labeling_task_*.csv # ⚠️ Should be in gold/
│   ├── processed/
│   │   ├── converttojson.ipynb # ❌ Notebook in data/
│   │   └── master_combined.csv # ⚠️ Should be in interim/
│   └── raw/processed/         # ❌ Redundant nesting
├── scripts/
│   ├── debug_mapping.py       # ❌ One-time debug
│   └── merge_labeled_files.py # ⚠️ Should be in src/
├── src/preprocessing/
│   ├── output.csv             # ❌ Data in code dir
│   └── test_raw.csv           # ❌ Test data in code dir
└── TOXIC_COMMENT/             # ❌ Duplicate structure
```

### AFTER (Clean)
```
Dataset/
├── README.md                  # ✅ Clear documentation
├── requirements.txt           # ✅ Dependencies
├── migrate_project.py         # ✅ Migration tool
├── fix_imports.py             # ✅ Import fixer
│
├── data/                      # ✅ ALL DATA HERE
│   ├── raw/                   # Original data
│   │   ├── facebook/
│   │   ├── youtube/
│   │   └── label_studio/      # 🆕 Label exports
│   ├── interim/               # 🆕 Intermediate
│   │   └── master_combined.csv
│   ├── processed/             # Final datasets
│   │   └── training_data*.csv
│   ├── gold/                  # 🆕 Gold standard (190 samples)
│   │   └── labeling_task_*.csv
│   ├── external/              # 🆕 External resources
│   │   ├── teencode_dict.json
│   │   └── emoji_sentiment.json
│   └── final/                 # Production ready
│
├── src/                       # ✅ REUSABLE CODE
│   ├── preprocessing/
│   │   ├── advanced_text_cleaning.py
│   │   ├── apify_to_csv.py
│   │   └── process_csv_with_context.py
│   ├── labeling/
│   │   ├── merge_labeled_data.py  # Moved from scripts/
│   │   └── split_data_for_labeling.py
│   ├── training/
│   │   ├── prepare_training_data.py  # Moved from scripts/
│   │   └── train_baseline_model.py
│   └── utils/
│
├── notebooks/                 # 🆕 JUPYTER NOTEBOOKS
│   ├── 01_data_journey.ipynb
│   ├── 02_convert_to_json.ipynb
│   └── 03_active_learning.ipynb
│
├── tests/                     # 🆕 UNIT TESTS
│   ├── test_text_cleaning.py
│   └── test_apify_to_csv.py
│
├── scripts/                   # ✅ One-off scripts only
│   └── analyze_coverage.py
│
├── docs/                      # ✅ Documentation
│   ├── TEXT_CLEANING_GUIDE.md
│   └── PROJECT_SUMMARY.md
│
└── examples/                  # ✅ Usage examples
    └── text_cleaning_usage.py
```

---

## 🛠️ Detailed Migration Steps

### Step 1: Backup Everything
```bash
# Manual backup (recommended)
cp -r "C:\Học sâu\Dataset" "C:\Học sâu\Dataset_backup_$(date +%Y%m%d)"

# Or use git
git add .
git commit -m "Backup before migration"
git tag pre-migration
```

### Step 2: Run Analysis
```bash
# Review what will be changed
python migrate_project.py --dry-run > migration_preview.txt

# Check the preview
cat migration_preview.txt

# Key things to verify:
# 1. All files to delete are actually temporary
# 2. All files to move have correct destinations
# 3. No important files will be lost
```

### Step 3: Execute Migration
```bash
# Run actual migration
python migrate_project.py --execute

# Check results
tree /f data/gold/      # Should have 7 labeled files
tree /f data/interim/   # Should have master_combined.csv
tree /f notebooks/      # Should have 4 notebooks
```

### Step 4: Fix Imports
```bash
# Preview import fixes
python fix_imports.py --dry-run

# Apply fixes
python fix_imports.py --execute

# Fix hardcoded paths too
python fix_imports.py --execute --fix-paths
```

### Step 5: Test Everything
```bash
# Test imports
python -c "from src.preprocessing.advanced_text_cleaning import clean_text; print('✅ Import works!')"

# Test text cleaning
python -c "from src.preprocessing.advanced_text_cleaning import clean_text; print(clean_text('nguuuu vcl'))"

# Run unit tests (if exist)
python -m pytest tests/ -v

# Test apify_to_csv
cd src/preprocessing
python apify_to_csv.py  # Should work without errors
```

### Step 6: Verify Data Integrity
```bash
# Check no data was lost
wc -l data/gold/*.csv              # Count rows in labeled data
wc -l data/interim/*.csv           # Count rows in interim data
wc -l data/processed/*.csv         # Count rows in processed data

# Compare with backup
diff -r data/ ../Dataset_backup/data/ | grep -E "^Only in"
```

---

## 🔧 Import Changes Required

### Example 1: Scripts using advanced_text_cleaning

**BEFORE (❌ Broken):**
```python
from advanced_text_cleaning import clean_text, clean_dataframe

df = clean_dataframe(df, text_column='comment')
```

**AFTER (✅ Works):**
```python
from src.preprocessing.advanced_text_cleaning import clean_text, clean_dataframe

df = clean_dataframe(df, text_column='comment')
```

### Example 2: Scripts with hardcoded paths

**BEFORE (❌ Fragile):**
```python
df = pd.read_csv(r'C:\Học sâu\Dataset\data\processed\master_combined.csv')
```

**AFTER (✅ Portable):**
```python
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

df = pd.read_csv(PROJECT_ROOT / 'data' / 'interim' / 'master_combined.csv')
```

### Example 3: Notebooks

**BEFORE (❌ Messy):**
```python
import sys
sys.path.append('..')
sys.path.append('../src')

from advanced_text_cleaning import clean_text
```

**AFTER (✅ Clean):**
```python
# First cell: Setup
from pathlib import Path
import sys

PROJECT_ROOT = Path().resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Second cell: Imports
from src.preprocessing.advanced_text_cleaning import clean_text
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: ModuleNotFoundError after migration
```bash
# Error: ModuleNotFoundError: No module named 'advanced_text_cleaning'

# Solution: Fix the import
# BEFORE: from advanced_text_cleaning import ...
# AFTER:  from src.preprocessing.advanced_text_cleaning import ...

# Or run the fixer:
python fix_imports.py --execute
```

### Issue 2: FileNotFoundError for data files
```bash
# Error: FileNotFoundError: 'data/processed/master_combined.csv'

# Reason: File moved to data/interim/

# Solution 1: Update path in code
# BEFORE: 'data/processed/master_combined.csv'
# AFTER:  'data/interim/master_combined.csv'

# Solution 2: Use PROJECT_ROOT
PROJECT_ROOT / 'data' / 'interim' / 'master_combined.csv'
```

### Issue 3: Circular import between advanced_text_cleaning and apify_to_csv
```bash
# Error: ImportError: cannot import name 'X' from partially initialized module

# Reason: Both files import from each other

# Solution: Extract shared code
# Create src/preprocessing/text_utils.py for shared functions
# Import from text_utils in both files instead
```

### Issue 4: Notebooks can't find modules
```python
# Error in notebook: ModuleNotFoundError

# Solution: Add PROJECT_ROOT setup in first cell
from pathlib import Path
import sys
PROJECT_ROOT = Path().resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
```

---

## 📊 Migration Checklist

### Pre-Migration
- [ ] Read PROJECT_RESTRUCTURE_ANALYSIS.md
- [ ] Backup entire project folder
- [ ] Review files to be deleted (23 files)
- [ ] Review files to be moved (29 files)
- [ ] Commit current state to git

### During Migration
- [ ] Run `migrate_project.py --dry-run`
- [ ] Review dry-run output carefully
- [ ] Run `migrate_project.py --execute`
- [ ] Check no errors occurred
- [ ] Review MIGRATION_SUMMARY.md

### Post-Migration - Import Fixes
- [ ] Run `fix_imports.py --dry-run`
- [ ] Review import fixes
- [ ] Run `fix_imports.py --execute`
- [ ] Run `fix_imports.py --execute --fix-paths`

### Post-Migration - Testing
- [ ] Test: `from src.preprocessing.advanced_text_cleaning import clean_text`
- [ ] Test: `python src/preprocessing/apify_to_csv.py`
- [ ] Test: Run notebooks (check imports work)
- [ ] Test: Count data file rows (integrity check)
- [ ] Run unit tests: `python -m pytest tests/ -v`

### Post-Migration - Documentation
- [ ] Update README.md with new structure
- [ ] Update docs/ with import examples
- [ ] Add PROJECT_ROOT examples to documentation
- [ ] Create ARCHITECTURE.md (optional)

### Cleanup
- [ ] Verify everything works
- [ ] Delete backup folder (after 1 week)
- [ ] Remove migration scripts (optional)
- [ ] Commit new structure to git

---

## 🎯 Benefits After Migration

### Before Migration
❌ 23 temporary/debug files cluttering project  
❌ Import statements break when moving files  
❌ Hardcoded absolute paths (not portable)  
❌ Data files mixed with code  
❌ Difficult to find files  
❌ No clear separation of concerns  

### After Migration
✅ Clean, professional structure (PEP8-compliant)  
✅ Robust imports with `src.preprocessing.*`  
✅ Portable paths with `PROJECT_ROOT`  
✅ Clear data/code/docs separation  
✅ Easy to find files  
✅ Scalable architecture  
✅ Ready for collaboration  
✅ Ready for deployment  

---

## 🆘 Rollback Plan

If something goes wrong:

```bash
# Option 1: Restore from backup
rm -rf "C:\Học sâu\Dataset"
cp -r "C:\Học sâu\Dataset_backup" "C:\Học sâu\Dataset"

# Option 2: Git rollback (if you committed before)
git reset --hard pre-migration
git clean -fd

# Option 3: Use migration backup
# Migration creates: backup_YYYYMMDD_HHMMSS/
cp -r backup_20251221_*/* .
```

---

## 📞 Support

If you encounter issues:

1. Check MIGRATION_SUMMARY.md for migration log
2. Review PROJECT_RESTRUCTURE_ANALYSIS.md for details
3. Check this README's "Common Issues" section
4. Review the backup folder to verify what changed

---

## 📝 Version History

**V2.0 (2025-12-21)**
- ✅ Complete project restructure
- ✅ Automated migration script
- ✅ Import fixer with path resolution
- ✅ Comprehensive documentation
- ✅ Backup and rollback support

---

**Ready to migrate?** Run: `python migrate_project.py --dry-run`
