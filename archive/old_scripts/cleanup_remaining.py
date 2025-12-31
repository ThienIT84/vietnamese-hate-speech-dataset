"""
Cleanup remaining uncategorized files
"""

import os
import shutil
import glob

def move_files(pattern, destination):
    """Move files matching pattern to destination"""
    files = glob.glob(pattern)
    moved = []
    for f in files:
        if os.path.isfile(f):
            try:
                dest = os.path.join(destination, os.path.basename(f))
                shutil.move(f, dest)
                moved.append(f)
            except Exception as e:
                print(f"  ✗ {f}: {e}")
    return moved

print("🧹 CLEANING REMAINING FILES...")
print("="*80)

# Create folders if not exist
os.makedirs('archive/backups', exist_ok=True)
os.makedirs('archive/intermediate_data', exist_ok=True)
os.makedirs('archive/old_scripts', exist_ok=True)
os.makedirs('archive/test_files', exist_ok=True)

moved_count = 0

# 1. All backup files
print("\n📦 Moving backup files...")
patterns = [
    'backup_*.xlsx', 'backup_*.csv',
    'FINAL_TRAINING_*.xlsx',
    'final_train_data_v2_FIXED_*.csv',
    'final_train_data_v3_AUGMENTED_*.csv',
    'final_train_data_v3_AUGMENTED_*.xlsx',
    'final_train_data_v3_CLEANED.csv',
    'final_train_data_v3_SEGMENTED.csv',
    'final_train_data_v3_SEGMENTED.xlsx',
    'final_train_data_v3_SEGMENTED_FIXED.csv',
    'final_train_data_v3_SEGMENTED_FIXED.xlsx',
    'final_train_data_v3_SEGMENTED_FINAL.csv',
    'final_train_data_v3_TRUNCATED_*.csv',
    'final_train_data_v3_TRUNCATED_*.xlsx',
]
for pattern in patterns:
    moved = move_files(pattern, 'archive/backups')
    moved_count += len(moved)
    if moved:
        print(f"  ✓ {len(moved)} files: {pattern}")

# 2. Intermediate data
print("\n📊 Moving intermediate data...")
patterns = [
    'AUTO_LABELED_*.csv', 'AUTO_LABELED_*.xlsx',
    'STRATEGIC_SAMPLES_*.csv', 'STRATEGIC_SAMPLES_*.xlsx',
    'unlabeled_*.csv',
    'AUGMENTATION_SUMMARY_*.md',
    'review_conflicts*.csv',
    'REVIEW_*.csv', 'REVIEW_*.xlsx',
    'ERROR_*.xlsx',
]
for pattern in patterns:
    moved = move_files(pattern, 'archive/intermediate_data')
    moved_count += len(moved)
    if moved:
        print(f"  ✓ {len(moved)} files: {pattern}")

# 3. Test files
print("\n🧪 Moving test files...")
patterns = [
    'test_*.py',
    'quick_*.py',
    'check_*.py',
    'verify_*.py',
    'debug_*.py',
    'deep_*.py',
]
for pattern in patterns:
    moved = move_files(pattern, 'archive/test_files')
    moved_count += len(moved)
    if moved:
        print(f"  ✓ {len(moved)} files: {pattern}")

# 4. Old scripts
print("\n📜 Moving old scripts...")
patterns = [
    'fix_*.py',
    'rebuild_*.py',
    'import_*.py',
    'smart_*.py',
    'remove_*.py',
    'truncate_*.py',
    'convert_*.py',
    'merge_*.py',
    'filter_*.py',
    'create_*.py',
    'augment_*.py',
    'apply_*.py',
    'process_*.py',
]
for pattern in patterns:
    moved = move_files(pattern, 'archive/old_scripts')
    moved_count += len(moved)
    if moved:
        print(f"  ✓ {len(moved)} files: {pattern}")

# 5. Notebooks
print("\n📓 Moving notebooks...")
if os.path.exists('SafeSense_PhoBERT_Training_Complete.ipynb'):
    shutil.move('SafeSense_PhoBERT_Training_Complete.ipynb', 
                'archive/old_training/SafeSense_PhoBERT_Training_Complete.ipynb')
    moved_count += 1
    print("  ✓ SafeSense_PhoBERT_Training_Complete.ipynb")

print("\n" + "="*80)
print(f"✅ Moved {moved_count} additional files")
print("="*80)

# Show remaining files in root
print("\n📂 Remaining files in root:")
root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
important_files = ['.env', '.env.example', '.gitignore', 'requirements.txt', 
                   'LICENSE', 'cleanup_project.py', 'cleanup_remaining.py']
other_files = [f for f in root_files if f not in important_files and not f.startswith('~$')]

if other_files:
    print(f"\n⚠️ {len(other_files)} files still in root:")
    for f in sorted(other_files)[:20]:
        size = os.path.getsize(f) / 1024
        print(f"  - {f} ({size:.1f} KB)")
    if len(other_files) > 20:
        print(f"  ... and {len(other_files)-20} more")
else:
    print("  ✅ Root directory is clean!")

print("\n📁 Final structure:")
for folder in ['archive', 'scripts', 'data', 'docs', 'src', 'models', 'configs']:
    if os.path.exists(folder):
        count = sum(len(files) for _, _, files in os.walk(folder))
        print(f"  {folder}/: {count} files")
