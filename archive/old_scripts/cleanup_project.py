"""
Script để dọn dẹp project SafeSense
Phân loại và di chuyển files vào folders phù hợp
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Tạo folder archive với timestamp
archive_folder = f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Định nghĩa cấu trúc folders
folders = {
    'archive/backups': [],  # Các file backup
    'archive/old_scripts': [],  # Scripts cũ không dùng
    'archive/test_files': [],  # Test files
    'archive/intermediate_data': [],  # Data trung gian
    'archive/old_training': [],  # Training scripts cũ
    'scripts/preprocessing': [],  # Scripts preprocessing
    'scripts/training': [],  # Scripts training hiện tại
    'scripts/analysis': [],  # Scripts phân tích
    'docs': [],  # Documentation
    'data/final': [],  # Data cuối cùng để train
    'data/review': [],  # Data cần review
}

# Phân loại files
file_categories = {
    # BACKUPS - Xóa hoặc archive
    'archive/backups': [
        'backup_*.xlsx', 'backup_*.csv',
        '*_backup_*.xlsx', '*_backup_*.csv',
        'FINAL_TRAINING_*.xlsx',  # Các version cũ
        'final_dataset.xlsx',
        'final_dataset_cleaned.csv',
        'final_dataset_fixed_v8.csv',
        'final_dataset_thanhthien.xlsx',
        'final_train_data_v2.csv',
        'final_train_data_v2_FIXED_*.csv',
    ],
    
    # INTERMEDIATE DATA - Archive
    'archive/intermediate_data': [
        'AUTO_LABELED_*.csv', 'AUTO_LABELED_*.xlsx',
        'STRATEGIC_SAMPLES_*.csv', 'STRATEGIC_SAMPLES_*.xlsx',
        'unlabeled_*.csv',
        'AUGMENTATION_SUMMARY_*.md',
        'review_conflicts*.csv',
        'REVIEW_*.csv',
        'ERROR_*.xlsx',
        'safesense_error_analysis.xlsx',
    ],
    
    # TEST FILES - Archive
    'archive/test_files': [
        'test_*.py',
        'quick_*.py',
        'check_*.py',
        'verify_*.py',
        'debug_*.py',
        'deep_check_*.py',
        'deep_error_*.py',
    ],
    
    # OLD SCRIPTS - Archive
    'archive/old_scripts': [
        'fix_*.py',
        'rebuild_*.py',
        'import_*.py',
        'smart_rebuild_*.py',
        'remove_*.py',
        'truncate_*.py',
        'convert_*.py',
        'merge_*.py',
        'filter_*.py',
        'create_*.py',
        'augment_*.py',
        'apply_*.py',
        'process_unlabeled_data.py',
        'process_strategic_*.py',
        'review_fixed_data.py',
        'validate_against_guideline.py',
    ],
    
    # OLD TRAINING SCRIPTS - Archive
    'archive/old_training': [
        'kaggle_phobert_training.py',
        'colab_phobert_v2_training.py',
        'colab_phobert_v2_with_error_analysis.py',
        'colab_analyze_errors_simple.py',
        'COLAB_TRAINING_CELLS.py',
        'COLAB_ERROR_ANALYSIS_CELL.py',
        'KAGGLE_TRAINING_CELLS.py',  # V1 cũ
        'KAGGLE_ERROR_EXPORT_CELL.py',
        'KAGGLE_DEEP_ERROR_ANALYSIS_CELL.py',
        'HUONG_DAN_KAGGLE_TRAINING.md',  # V1 cũ
        'HUONG_DAN_COLAB_TRAINING.md',
        'HUONG_DAN_PHAN_TICH_LOI_COLAB.md',
    ],
    
    # PREPROCESSING SCRIPTS - Keep organized
    'scripts/preprocessing': [
        'analyze_and_augment_data.py',
        'analyze_final_balance.py',
        'analyze_model_errors.py',
        'check_and_clean_final_data.py',
        'teencode_tool.py',
    ],
    
    # CURRENT TRAINING SCRIPTS - Keep in root or scripts/training
    'scripts/training': [
        'KAGGLE_TRAINING_CELLS_V2.py',
    ],
    
    # ANALYSIS SCRIPTS
    'scripts/analysis': [
        'check_title_length.py',
        'check_processed.py',
    ],
    
    # DOCUMENTATION - Keep organized
    'docs': [
        'README.md',
        'README_PREPROCESSING.md',
        'PREPROCESSING_DOCUMENTATION.md',
        'WORD_SEGMENTATION_GUIDE.md',
        'TRAINING_IMPROVEMENT_GUIDE.md',
        'NLP_EXPERT_ROADMAP.md',
        'REVIEW_GUIDE.md',
        'TEENCODE_TOOL_README.md',
        'HUONG_DAN_KAGGLE_V2.md',  # Current version
        'preprocessing_demo.html',
        'teencode_tester.html',
    ],
    
    # FINAL DATA - Keep
    'data/final': [
        'final_train_data_v3_READY.xlsx',  # MAIN TRAINING DATA
        'final_train_data_v3_READY.csv',
        'final_train_data_v3_CLEANED.xlsx',
        'final_train_data_v3_SEGMENTED_FINAL.xlsx',
    ],
    
    # REVIEW DATA
    'data/review': [
        'REVIEW_FIXED_DATA_*.xlsx',
    ],
}

def should_delete(filename):
    """Files nên xóa hẳn"""
    delete_patterns = [
        '~$',  # Excel temp files
        '.ipynb_checkpoints',
        '__pycache__',
        '*.pyc',
    ]
    for pattern in delete_patterns:
        if pattern in filename:
            return True
    return False

def get_file_size(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def main():
    print("="*80)
    print("🧹 CLEANING UP PROJECT")
    print("="*80)
    
    # Scan all files in root
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    print(f"\n📊 Found {len(root_files)} files in root directory")
    
    # Categorize files
    categorized = {cat: [] for cat in file_categories.keys()}
    uncategorized = []
    to_delete = []
    
    for file in root_files:
        if should_delete(file):
            to_delete.append(file)
            continue
        
        matched = False
        for category, patterns in file_categories.items():
            for pattern in patterns:
                if pattern.replace('*', '') in file or file == pattern:
                    categorized[category].append(file)
                    matched = True
                    break
            if matched:
                break
        
        if not matched and file not in ['cleanup_project.py', '.env', '.env.example', 
                                        '.gitignore', 'requirements.txt', 'LICENSE',
                                        'reser_title.ipynb']:
            uncategorized.append(file)
    
    # Print summary
    print("\n📋 CATEGORIZATION SUMMARY:")
    print("-"*80)
    
    total_size = 0
    for category, files in categorized.items():
        if files:
            size = sum(get_file_size(f) for f in files)
            total_size += size
            print(f"\n{category}: {len(files)} files ({size:.1f} MB)")
            for f in sorted(files)[:5]:  # Show first 5
                print(f"  - {f}")
            if len(files) > 5:
                print(f"  ... and {len(files)-5} more")
    
    if uncategorized:
        print(f"\n⚠️ UNCATEGORIZED: {len(uncategorized)} files")
        for f in uncategorized:
            print(f"  - {f}")
    
    if to_delete:
        print(f"\n🗑️ TO DELETE: {len(to_delete)} files")
        for f in to_delete[:10]:
            print(f"  - {f}")
    
    print(f"\n💾 Total size to archive: {total_size:.1f} MB")
    
    # Ask for confirmation
    print("\n" + "="*80)
    response = input("Proceed with cleanup? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("❌ Cleanup cancelled")
        return
    
    # Create folders
    print("\n📁 Creating folder structure...")
    for folder in set(categorized.keys()):
        os.makedirs(folder, exist_ok=True)
        print(f"  ✓ {folder}")
    
    # Move files
    print("\n📦 Moving files...")
    moved_count = 0
    for category, files in categorized.items():
        for file in files:
            try:
                dest = os.path.join(category, file)
                shutil.move(file, dest)
                moved_count += 1
                print(f"  ✓ {file} → {category}")
            except Exception as e:
                print(f"  ✗ Error moving {file}: {e}")
    
    # Delete temp files
    print("\n🗑️ Deleting temp files...")
    deleted_count = 0
    for file in to_delete:
        try:
            os.remove(file)
            deleted_count += 1
            print(f"  ✓ Deleted {file}")
        except Exception as e:
            print(f"  ✗ Error deleting {file}: {e}")
    
    print("\n" + "="*80)
    print("✅ CLEANUP COMPLETE!")
    print("="*80)
    print(f"📦 Moved: {moved_count} files")
    print(f"🗑️ Deleted: {deleted_count} files")
    print(f"📁 Created: {len(set(categorized.keys()))} folders")
    
    print("\n📂 NEW PROJECT STRUCTURE:")
    print("""
    project/
    ├── scripts/
    │   ├── preprocessing/    # Preprocessing scripts
    │   ├── training/         # Current training scripts
    │   └── analysis/         # Analysis scripts
    ├── data/
    │   ├── final/           # Final training data
    │   └── review/          # Data for review
    ├── docs/                # Documentation
    ├── archive/             # Old files (can delete later)
    │   ├── backups/
    │   ├── old_scripts/
    │   ├── test_files/
    │   ├── intermediate_data/
    │   └── old_training/
    ├── src/                 # Source code (existing)
    ├── models/              # Saved models (existing)
    └── configs/             # Configs (existing)
    """)

if __name__ == '__main__':
    main()
