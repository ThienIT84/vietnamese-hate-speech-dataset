# 🏗️ PROJECT RESTRUCTURE ANALYSIS & MIGRATION PLAN

## 📊 Current Structure Analysis

### ✅ GOOD - Already Organized
```
src/
├── preprocessing/          # ✅ Core preprocessing logic
│   ├── advanced_text_cleaning.py
│   ├── apify_to_csv.py
│   └── process_csv_with_context.py
├── labeling/              # ✅ Data labeling utilities
├── training/              # ✅ Model training scripts
└── utils/                 # ✅ Helper utilities
```

### ❌ PROBLEMS - Need Reorganization

#### 1. Root Level Clutter (9 test files!)
```
❌ check_dict.py            → Should be in tests/ or delete
❌ check_notebook.py        → Should be in tests/ or delete
❌ quick_test.py            → DELETE (temporary test)
❌ simple_test.py           → DELETE (temporary test)
❌ test_emoji.py            → DELETE (temporary test)
❌ test_person_masking.py   → DELETE (temporary test)
❌ test_split.py            → DELETE (temporary test)
❌ project_description.py   → DELETE or move to docs/
❌ du_an_tom_tat.md         → Move to docs/PROJECT_SUMMARY.md
```

#### 2. Data Directory Issues
```
data/labeled/               # ❌ Mixed labeled/unlabeled, temp files
├── cac_comment_*.xlsx      # ❌ Temporary analysis files
├── data_cleaned.xlsx       # ❌ Unclear naming
├── IAA_set_500_samples.xlsx # ✅ Gold standard → data/gold/
├── labeling_task_*.csv     # ✅ Gold standard → data/gold/
├── project-7-*.json        # ❌ Label Studio exports → data/raw/label_studio/
├── test.ipynb              # ❌ DELETE (temporary notebook)
└── youtube_comment_craw.xlsx # ❌ Wrong location → data/raw/youtube/

data/processed/             # ❌ Mixed processed/intermediate files
├── converttojson.ipynb     # ❌ Should be in notebooks/
├── master_combined.*       # ✅ Keep (final processed data)
├── training_data*.csv      # ✅ Keep (model-ready data)
└── tasks_*.json            # ❌ Move to data/interim/

data/raw/processed/         # ❌ REDUNDANT - already have data/processed/
├── facebook_backup_*.csv   # ❌ DELETE (old backups)
└── *.parquet               # ✅ Keep main masters, delete backups
```

#### 3. Scripts Directory
```
scripts/                    # ❌ Mixed one-off scripts and reusable code
├── merge_labeled_files.py  # → Should be in src/labeling/
├── prepare_training_with_teencode.py # → Should be in src/training/
├── check_*.py              # → DELETE or move to tests/
├── debug_*.py              # → DELETE (temporary debug scripts)
└── fix_encoding.py         # → DELETE (one-time fix)
```

#### 4. Preprocessing Directory Issues
```
src/preprocessing/
├── labeling_task_Thien.csv # ❌ Data file in code directory!
├── output.csv              # ❌ Temporary output
├── test_*.csv              # ❌ Test files
├── debug_context_m.py      # ❌ Temporary debug script
└── test_*.py               # → Move to tests/
```

#### 5. TOXIC_COMMENT Directory
```
TOXIC_COMMENT/              # ❌ Redundant structure
├── notebooks/              # ❌ Duplicate of root notebooks
├── datasets/               # ❌ Empty directories
└── *.py                    # ❌ Duplicate scripts
```

---

## 🎯 PROPOSED NEW STRUCTURE (Standard Data Science Project)

```
Dataset/
├── 📄 README.md                    # Project overview
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
│
├── 📁 data/                        # ALL DATA FILES
│   ├── raw/                        # Original, immutable data
│   │   ├── facebook/               # ✅ Keep as is
│   │   ├── youtube/                # ✅ Keep as is
│   │   └── label_studio/           # 🆕 Label Studio exports
│   │       ├── project-7-*.json
│   │       └── tasks_split_context.json
│   │
│   ├── interim/                    # 🆕 Intermediate processing
│   │   ├── master_combined.csv     # MOVE from processed/
│   │   ├── master_combined.parquet
│   │   ├── unlabeled_data.csv
│   │   └── unlabeled_with_context_phobert.csv
│   │
│   ├── processed/                  # Final, model-ready data
│   │   ├── training_data_final_merged.csv
│   │   ├── training_data_with_context_phobert_clean.csv
│   │   └── facebook_master.csv     # MOVE from raw/processed/
│   │
│   ├── gold/                       # 🆕 Gold standard labeled data (190 samples)
│   │   ├── IAA_set_500_samples.xlsx
│   │   ├── labeling_task_Huy.csv
│   │   ├── labeling_task_Kiet.csv
│   │   ├── labeling_task_Thien.csv
│   │   ├── GanChung-Huy.csv
│   │   └── sampling_statistics.txt
│   │
│   ├── external/                   # 🆕 External resources
│   │   ├── teencode_dict.json      # EXTRACT from advanced_text_cleaning.py
│   │   ├── emoji_sentiment.json    # EXTRACT from advanced_text_cleaning.py
│   │   └── vietnamese_surnames.txt # EXTRACT from advanced_text_cleaning.py
│   │
│   └── final/                      # ✅ Keep as is
│       └── final_dataset_relaxed_fixed.csv
│
├── 📁 src/                         # SOURCE CODE (Reusable modules)
│   ├── __init__.py
│   │
│   ├── preprocessing/              # ✅ Already good
│   │   ├── __init__.py
│   │   ├── advanced_text_cleaning.py  # ✅ Core module
│   │   ├── apify_to_csv.py
│   │   └── process_csv_with_context.py
│   │
│   ├── labeling/                   # ✅ Already good + additions
│   │   ├── __init__.py
│   │   ├── active_learning.py
│   │   ├── merge_labeled_data.py   # MOVE from scripts/
│   │   ├── split_data_for_labeling.py
│   │   └── check_agreement.py
│   │
│   ├── training/                   # ✅ Already good + additions
│   │   ├── __init__.py
│   │   ├── train_baseline_model.py
│   │   ├── prepare_training_data.py  # RENAME from scripts/prepare_training_with_teencode.py
│   │   └── validate_dataset.py
│   │
│   └── utils/                      # ✅ Already good
│       ├── __init__.py
│       ├── csv_to_xlsx.py
│       └── file_helpers.py         # 🆕 Common file operations
│
├── 📁 notebooks/                   # 🆕 Jupyter Notebooks (Analysis only)
│   ├── 01_data_exploration.ipynb   # MOVE from TOXIC_COMMENT/notebooks/
│   ├── 02_data_cleaning_demo.ipynb # MOVE converttojson.ipynb here
│   ├── 03_active_learning.ipynb    # MOVE from TOXIC_COMMENT/
│   └── 04_data_journey.ipynb       # MOVE from TOXIC_COMMENT/notebooks/
│
├── 📁 tests/                       # 🆕 Unit tests
│   ├── __init__.py
│   ├── test_text_cleaning.py       # MOVE from src/preprocessing/
│   ├── test_apify_to_csv.py
│   └── test_process_csv.py
│
├── 📁 scripts/                     # One-off scripts (NOT imported)
│   ├── migrate_old_data.py         # 🆕 Data migration scripts
│   ├── analyze_coverage.py         # ✅ Keep (analysis tool)
│   └── filter_by_topics.py         # ✅ Keep (data prep)
│
├── 📁 docs/                        # ✅ Already good
│   ├── CRAWL_PLAN_SOCIAL_ISSUES_YOUTUBE.md
│   ├── GUIDELINE_GAN_NHAN_V3.md
│   ├── TEXT_CLEANING_GUIDE.md
│   ├── TEXT_CLEANING_V2_MODES.md
│   ├── PROJECT_SUMMARY.md          # MOVE from du_an_tom_tat.md
│   └── ARCHITECTURE.md             # 🆕 System architecture
│
├── 📁 examples/                    # ✅ Already good
│   └── text_cleaning_usage.py
│
└── 📁 configs/                     # 🆕 Configuration files
    ├── model_config.yaml
    ├── training_config.yaml
    └── preprocessing_config.yaml
```

---

## 🗑️ FILES TO DELETE (21 files)

### Root Level Temporary Files (7 files)
```bash
❌ quick_test.py              # Temporary test
❌ simple_test.py             # Temporary test
❌ test_emoji.py              # Temporary test
❌ test_person_masking.py     # Temporary test
❌ test_split.py              # Temporary test
❌ check_dict.py              # Temporary debug
❌ check_notebook.py          # Temporary debug
```

### Scripts Directory (6 files)
```bash
❌ scripts/check_ids.py       # One-time debug
❌ scripts/check_output.py    # One-time debug
❌ scripts/debug_mapping.py   # One-time debug
❌ scripts/debug_youtube_mapping.py  # One-time debug
❌ scripts/fix_encoding.py    # One-time fix
❌ scripts/check_unlabeled_ids.py  # One-time check
```

### Preprocessing Temporary Files (4 files)
```bash
❌ src/preprocessing/debug_context_m.py  # Temporary debug
❌ src/preprocessing/output.csv          # Temporary output
❌ src/preprocessing/test_raw.csv        # Test data
❌ src/preprocessing/test_raw_cleaned.csv  # Test output
```

### Data Directory (3 files)
```bash
❌ data/labeled/test.ipynb              # Temporary notebook
❌ data/raw/processed/facebook_backup_*.csv  # Old backups
❌ data/raw/processed/youtube_backup_*.csv   # Old backups
```

### TOXIC_COMMENT Directory (1 entire folder)
```bash
❌ TOXIC_COMMENT/                # Duplicate/outdated structure
   - Move useful notebooks to notebooks/
   - Delete empty datasets/, experiments/, results/
```

---

## 📝 FILES REQUIRING IMPORT FIXES (High Priority)

### 1. Scripts using advanced_text_cleaning
```python
# BEFORE (❌ Broken after move)
from advanced_text_cleaning import clean_text

# AFTER (✅ Correct)
from src.preprocessing.advanced_text_cleaning import clean_text
```

**Files to fix:**
- `scripts/prepare_training_with_teencode.py`
- `scripts/merge_labeled_files.py`
- `src/labeling/merge_labeled_data.py`
- `src/preprocessing/apify_to_csv.py` (imports advanced_text_cleaning)
- `src/preprocessing/process_csv_with_context.py`

### 2. Scripts using apify_to_csv
```python
# BEFORE (❌ Broken)
from apify_to_csv import convert_apify_to_master

# AFTER (✅ Correct)
from src.preprocessing.apify_to_csv import convert_apify_to_master
```

**Files to fix:**
- `src/preprocessing/advanced_text_cleaning.py` (process_json_to_csv function)

### 3. Notebooks with relative imports
```python
# BEFORE (❌ Broken)
import sys
sys.path.append('..')
from advanced_text_cleaning import clean_text

# AFTER (✅ Correct)
from src.preprocessing.advanced_text_cleaning import clean_text
```

**Files to fix:**
- All notebooks in `TOXIC_COMMENT/notebooks/`
- `data/processed/converttojson.ipynb`

### 4. Path references in code
```python
# BEFORE (❌ Hardcoded paths)
df = pd.read_csv('data/processed/master_combined.csv')

# AFTER (✅ Using pathlib)
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
df = pd.read_csv(PROJECT_ROOT / 'data' / 'interim' / 'master_combined.csv')
```

---

## ⚠️ CRITICAL WARNINGS

### 1. Data Integrity
```
🔴 BACKUP BEFORE MIGRATION!
   All files in data/ should be backed up to external location
   Use: python migration_script.py --dry-run first
```

### 2. Import Chain Breaks
```
🟡 EXPECTED BREAKS:
   - scripts/prepare_training_with_teencode.py → advanced_text_cleaning
   - src/preprocessing/apify_to_csv.py → advanced_text_cleaning
   - src/preprocessing/advanced_text_cleaning.py → apify_to_csv
   - All notebooks → src modules
```

### 3. Path Dependencies
```
🟡 FILES WITH HARDCODED PATHS:
   - scripts/prepare_training_with_teencode.py (17 hardcoded paths!)
   - scripts/merge_labeled_files.py (10 hardcoded paths)
   - src/preprocessing/apify_to_csv.py (6 hardcoded paths)
```

### 4. Circular Imports (After Fix)
```
🔴 POTENTIAL ISSUE:
   advanced_text_cleaning.py imports apify_to_csv (process_json_to_csv)
   apify_to_csv.py imports advanced_text_cleaning (advanced_clean_text)
   
   → SOLUTION: Extract shared code to src/preprocessing/text_utils.py
```

---

## 🚀 MIGRATION PLAN (3 Phases)

### Phase 1: Cleanup (Safe deletions)
1. Delete temporary test files (7 files)
2. Delete one-time debug scripts (6 files)
3. Delete old backups (3 files)
4. Delete TOXIC_COMMENT/ (after extracting notebooks)

### Phase 2: Reorganize Data (No code breaks)
1. Create new directories (interim/, gold/, external/)
2. Move data files to new locations
3. Extract dictionaries from code to data/external/

### Phase 3: Fix Imports (Breaking changes)
1. Update all import statements
2. Fix hardcoded paths
3. Add PROJECT_ROOT to all scripts
4. Test all imports

---

## 📊 IMPACT SUMMARY

| Category | Total Files | Keep | Move | Delete |
|----------|-------------|------|------|--------|
| Root tests | 7 | 0 | 0 | 7 |
| Scripts | 13 | 2 | 5 | 6 |
| Data files | 45 | 20 | 15 | 10 |
| Notebooks | 6 | 0 | 6 | 0 |
| Source code | 15 | 12 | 3 | 0 |
| **TOTAL** | **86** | **34** | **29** | **23** |

**26.7% deletion rate** - Good cleanup!
**33.7% files need moving** - Moderate effort
**39.5% files stay in place** - Stable core

---

## 🎯 NEXT STEPS

1. **Review this analysis** - Confirm deletions and moves
2. **Backup everything** - Copy entire Dataset/ folder
3. **Run migration script** with `--dry-run` first
4. **Execute migration** - Let script do the heavy lifting
5. **Fix imports** - Run import fixer script
6. **Test everything** - Run all tests and scripts
7. **Update documentation** - Reflect new structure

---

**Ready to proceed?** → Run `python migrate_project.py --dry-run`
