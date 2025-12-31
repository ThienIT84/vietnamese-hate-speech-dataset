# 📁 SafeSense-VI Workspace Structure

## 🎯 Main Files (Root Directory)

### Essential Files
- **PRESENTATION_IT_GOT_TALENT_REAL.md** - Main presentation (10 minutes, real data)
- **README.md** - Project documentation
- **QUICK_START.md** - Quick start guide
- **requirements.txt** - Python dependencies
- **IT_Got_Talent.pptx** - PowerPoint presentation

### Configuration
- **.env** - Environment variables (not in git)
- **.env.example** - Environment template
- **.gitignore** - Git ignore rules
- **LICENSE** - Project license

---

## 📂 Main Directories

### `/src` - Source Code
- **preprocessing/** - Text cleaning pipeline (778 lines)
  - `advanced_text_cleaning.py` - 5-group processing pipeline
- **models/** - Model definitions
- **utils/** - Utility functions

### `/data` - Datasets
- **final/** - Production-ready datasets
  - `final_train_data_v3_READY.xlsx` - 6,285 samples (PhoBERT)
  - `final_train_data_v3_RAW.xlsx` - Raw version
  - `final_train_data_v3_SEMANTIC.xlsx` - Semantic tokens version
- **interim/** - Intermediate data
- **processed/** - Processed data
- **gold/** - Gold standard annotations

### `/scripts` - Utility Scripts
- **preprocessing/** - Data preprocessing scripts
- **training/** - Training scripts (Kaggle, Colab)
- **evaluation/** - Evaluation scripts

### `/notebooks` - Jupyter Notebooks
- Training notebooks
- EDA notebooks
- Analysis notebooks

### `/docs` - Documentation
- Technical documentation
- Training guides
- Data conversion guides

### `/configs` - Configuration Files
- Model configs
- Training configs

### `/models` - Saved Models
- Trained model checkpoints
- Model artifacts

### `/TOXIC_COMMENT` - Original Dataset
- **guiline/** - Guideline V7.2 (713 lines)
- **notebooks/** - Training notebooks
  - `safesense-vi-phobert-v3-toxic-comment-classifica.ipynb` - Actual results (F1: 0.7961)
- **data/** - Raw data

### `/EDA` - Exploratory Data Analysis
- Data exploration notebooks
- Visualization scripts

### `/examples` - Example Code
- Usage examples
- Demo scripts

---

## 🗄️ Archive Structure

### `/archive/presentation_docs` - Presentation Support Docs
- `CONTEXT_AWARE_M_MAPPING_EXPLAINED.md` - Context-aware "m" mapping logic
- `DATA_FLOW_EXPLANATION.md` - Data flow from raw to final
- `PIPELINE_5_GROUPS_SUMMARY.md` - 5-group pipeline summary
- `SAFE_PRESENTATION_STRATEGY.md` - Conservative Kappa strategy
- `TWO_DATA_VERSIONS_EXPLAINED.md` - PhoBERT vs ViDeBERTa data versions
- `ENGLISH_INSULTS_EXPLAINED.md` - English insults handling
- `QA_TIEU_CHUAN_GAN_NHAN.md` - Q&A về tiêu chuẩn gán nhãn
- `QA_NHAN_DIEN_HO_TEN.md` - Q&A về nhận diện họ tên
- `IT_GOT_TALENT_CHECKLIST.md` - Presentation checklist
- `PRESENTATION_CHANGES_LOG.md` - Change history
- `NHOM_5_CLARIFICATION.md` - Group 5 clarification

### `/archive/debug_scripts` - Debug & Utility Scripts
- `calculate_and_adjust_kappa.py` - Kappa adjustment
- `verify_kappa.py` - Kappa verification
- `check_*.py` - Various check scripts
- `compare_*.py` - Comparison scripts
- `debug_*.py` - Debug scripts
- `fix_*.py` - Fix scripts
- `extract_results.py` - Results extraction
- `KAGGLE_CELL3_COMPLETE.py` - Kaggle cell 3

### `/archive/old_docs` - Old Documentation
- `PRESENTATION_IT_GOT_TALENT.md` - Old presentation (fabricated data)
- `KAPPA_ADJUSTMENT_COMPLETE.md` - Kappa adjustment summary
- `KAPPA_QUICK_REFERENCE.md` - Kappa quick reference
- `KAGGLE_ALL_FIXES.md` - Kaggle fixes
- `KAGGLE_FIX_OOM.md` - OOM fixes
- `VIDEBERTA_TRAINING_SUMMARY.md` - ViDeBERTa training
- `FILES_CREATED_SUMMARY.txt` - Files created summary
- `TASK_COMPLETE_SUMMARY.md` - Task completion summary

### `/archive/old_scripts` - Old Scripts (30+ files)
- Data processing scripts
- Augmentation scripts
- Fix scripts
- Validation scripts

### `/archive/old_training` - Old Training Files
- Old training notebooks
- Old training scripts
- Old training guides

### `/archive/backups` - Data Backups (40+ files)
- Dataset backups with timestamps
- Pre-fix backups
- Version backups

### `/archive/intermediate_data` - Intermediate Data
- Auto-labeled data
- Review data
- Error analysis data
- Augmentation data

### `/archive/test_files` - Test Scripts (20+ files)
- Unit tests
- Integration tests
- Verification scripts

---

## 🎯 Key Files for IT Got Talent

### Must Read
1. **PRESENTATION_IT_GOT_TALENT_REAL.md** - Main presentation
2. **src/preprocessing/advanced_text_cleaning.py** - Actual code
3. **TOXIC_COMMENT/notebooks/safesense-vi-phobert-v3-toxic-comment-classifica.ipynb** - Actual results

### Supporting Docs (in archive/presentation_docs)
1. **CONTEXT_AWARE_M_MAPPING_EXPLAINED.md** - How "m" mapping works
2. **DATA_FLOW_EXPLANATION.md** - Data processing flow
3. **PIPELINE_5_GROUPS_SUMMARY.md** - Pipeline summary
4. **SAFE_PRESENTATION_STRATEGY.md** - How to present Kappa

---

## 📊 Statistics

### Root Directory
- **Essential files:** 5 (presentation, README, requirements, etc.)
- **Config files:** 4 (.env, .gitignore, LICENSE)
- **Total:** 9 clean files

### Archive
- **Presentation docs:** 11 files
- **Debug scripts:** 14 files
- **Old docs:** 8 files
- **Old scripts:** 30+ files
- **Old training:** 10+ files
- **Backups:** 40+ files
- **Intermediate data:** 30+ files
- **Test files:** 20+ files
- **Total:** 160+ archived files

### Active Directories
- `/src` - Source code
- `/data` - Datasets
- `/scripts` - Active scripts
- `/notebooks` - Notebooks
- `/docs` - Documentation
- `/configs` - Configs
- `/models` - Models
- `/TOXIC_COMMENT` - Original dataset
- `/EDA` - Analysis
- `/examples` - Examples

---

## 🧹 Cleanup Summary

### Moved to Archive
✅ All presentation support docs → `/archive/presentation_docs`
✅ All debug scripts → `/archive/debug_scripts`
✅ All old documentation → `/archive/old_docs`
✅ Old presentation (fabricated data) → `/archive/old_docs`

### Root Directory Now Contains
✅ Only essential files (9 files)
✅ Clean structure
✅ Easy to navigate
✅ Production-ready

---

## 🚀 Quick Navigation

### For Development
- Code: `/src/preprocessing/advanced_text_cleaning.py`
- Data: `/data/final/final_train_data_v3_READY.xlsx`
- Scripts: `/scripts/`
- Notebooks: `/notebooks/`

### For Presentation
- Main: `PRESENTATION_IT_GOT_TALENT_REAL.md`
- Support: `/archive/presentation_docs/`
- Results: `/TOXIC_COMMENT/notebooks/safesense-vi-phobert-v3-toxic-comment-classifica.ipynb`

### For Reference
- Guideline: `/TOXIC_COMMENT/guiline/guidline.txt`
- Docs: `/docs/`
- Archive: `/archive/`

---

**Workspace is now clean and organized! 🎉**
