#!/usr/bin/env python3
"""
PROJECT MIGRATION SCRIPT V2.0
Automatically reorganize project structure with import fixing
"""

import os
import shutil
from pathlib import Path
import json
import re
from typing import List, Tuple, Dict
from datetime import datetime

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ProjectMigration:
    def __init__(self, project_root: Path, dry_run: bool = True):
        self.project_root = Path(project_root)
        self.dry_run = dry_run
        self.backup_dir = self.project_root / f"backup_{datetime.now():%Y%m%d_%H%M%S}"
        self.migration_log = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log migration action"""
        color = {
            "INFO": Colors.BLUE,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED
        }.get(level, "")
        
        print(f"{color}[{level}]{Colors.END} {message}")
        self.migration_log.append(f"[{level}] {message}")
    
    def backup_project(self):
        """Create full backup before migration"""
        if self.dry_run:
            self.log(f"[DRY RUN] Would create backup at: {self.backup_dir}", "INFO")
            return
        
        self.log(f"Creating backup at: {self.backup_dir}", "INFO")
        shutil.copytree(self.project_root, self.backup_dir, 
                       ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git', 'backup_*'))
        self.log("Backup completed successfully!", "SUCCESS")
    
    def delete_files(self):
        """Phase 1: Delete temporary and outdated files"""
        self.log("\n" + "="*80, "INFO")
        self.log("PHASE 1: CLEANUP - Deleting temporary files", "INFO")
        self.log("="*80, "INFO")
        
        files_to_delete = [
            # Root level temporary tests (7 files)
            "quick_test.py",
            "simple_test.py",
            "test_emoji.py",
            "test_person_masking.py",
            "test_split.py",
            "check_dict.py",
            "check_notebook.py",
            
            # Scripts directory (6 files)
            "scripts/check_ids.py",
            "scripts/check_output.py",
            "scripts/debug_mapping.py",
            "scripts/debug_youtube_mapping.py",
            "scripts/fix_encoding.py",
            "scripts/check_unlabeled_ids.py",
            
            # Preprocessing temporary files (4 files)
            "src/preprocessing/debug_context_m.py",
            "src/preprocessing/output.csv",
            "src/preprocessing/test_raw.csv",
            "src/preprocessing/test_raw_cleaned.csv",
            "src/preprocessing/labeling_task_Thien.csv",  # Data file in code dir
            
            # Data directory (3 files)
            "data/labeled/test.ipynb",
            "data/raw/processed/facebook_backup_20251216_130831.csv",
            "data/raw/processed/youtube_backup_20251216_130851.csv",
            
            # Project description (move to docs instead)
            "project_description.py",
        ]
        
        deleted_count = 0
        for file_path in files_to_delete:
            full_path = self.project_root / file_path
            if full_path.exists():
                if self.dry_run:
                    self.log(f"[DRY RUN] Would delete: {file_path}", "WARNING")
                else:
                    full_path.unlink()
                    self.log(f"Deleted: {file_path}", "SUCCESS")
                deleted_count += 1
        
        self.log(f"\nDeleted {deleted_count}/{len(files_to_delete)} files", "SUCCESS")
    
    def create_directories(self):
        """Create new directory structure"""
        self.log("\n" + "="*80, "INFO")
        self.log("PHASE 2A: Creating new directory structure", "INFO")
        self.log("="*80, "INFO")
        
        new_dirs = [
            "data/interim",
            "data/gold",
            "data/external",
            "data/raw/label_studio",
            "notebooks",
            "tests",
            "configs",
        ]
        
        for dir_path in new_dirs:
            full_path = self.project_root / dir_path
            if self.dry_run:
                self.log(f"[DRY RUN] Would create: {dir_path}/", "INFO")
            else:
                full_path.mkdir(parents=True, exist_ok=True)
                self.log(f"Created: {dir_path}/", "SUCCESS")
    
    def move_files(self):
        """Phase 2: Move files to new locations"""
        self.log("\n" + "="*80, "INFO")
        self.log("PHASE 2B: Moving files to new structure", "INFO")
        self.log("="*80, "INFO")
        
        # Define file moves: (source, destination)
        file_moves = [
            # Data files to gold/
            ("data/labeled/IAA_set_500_samples.xlsx", "data/gold/IAA_set_500_samples.xlsx"),
            ("data/labeled/labeling_task_Huy.csv", "data/gold/labeling_task_Huy.csv"),
            ("data/labeled/labeling_task_Kiet.csv", "data/gold/labeling_task_Kiet.csv"),
            ("data/labeled/labeling_task_Thien.csv", "data/gold/labeling_task_Thien.csv"),
            ("data/labeled/GanChung-Huy.csv", "data/gold/GanChung-Huy.csv"),
            ("data/labeled/Gán chung-Thiện.csv", "data/gold/Gan_chung_Thien.csv"),
            ("data/labeled/sampling_statistics.txt", "data/gold/sampling_statistics.txt"),
            
            # Label Studio exports to raw/label_studio/
            ("data/labeled/project-7-at-2025-12-18-15-15-805c1b43.json", 
             "data/raw/label_studio/project-7-at-2025-12-18-15-15-805c1b43.json"),
            ("data/labeled/project-7-at-2025-12-19-20-00-267d084d.json",
             "data/raw/label_studio/project-7-at-2025-12-19-20-00-267d084d.json"),
            ("data/labeled/tasks_split_context.json", 
             "data/raw/label_studio/tasks_split_context.json"),
            
            # Processed data to interim/
            ("data/processed/master_combined.csv", "data/interim/master_combined.csv"),
            ("data/processed/master_combined.parquet", "data/interim/master_combined.parquet"),
            ("data/processed/unlabeled_data.csv", "data/interim/unlabeled_data.csv"),
            ("data/processed/unlabeled_data_for_labeling.csv", "data/interim/unlabeled_data_for_labeling.csv"),
            ("data/processed/unlabeled_with_context_phobert.csv", "data/interim/unlabeled_with_context_phobert.csv"),
            
            # Master files from raw/processed to processed/
            ("data/raw/processed/facebook_master.csv", "data/processed/facebook_master.csv"),
            ("data/raw/processed/facebook_master.parquet", "data/processed/facebook_master.parquet"),
            ("data/raw/processed/youtube_master.csv", "data/processed/youtube_master.csv"),
            ("data/raw/processed/youtube_master.parquet", "data/processed/youtube_master.parquet"),
            
            # Notebooks
            ("data/processed/converttojson.ipynb", "notebooks/02_convert_to_json.ipynb"),
            ("TOXIC_COMMENT/notebooks/01_Data_Journey_Presentation.ipynb", 
             "notebooks/01_data_journey.ipynb"),
            ("TOXIC_COMMENT/notebooks/presentaion_data_pipeline.ipynb",
             "notebooks/04_data_pipeline_presentation.ipynb"),
            ("TOXIC_COMMENT/activate_learning_hate_speech_V2.ipynb",
             "notebooks/03_active_learning_v2.ipynb"),
            
            # Scripts to src/
            ("scripts/merge_labeled_files.py", "src/labeling/merge_labeled_files.py"),
            ("scripts/prepare_training_with_teencode.py", "src/training/prepare_training_data.py"),
            
            # Tests from src/preprocessing to tests/
            ("src/preprocessing/test_apify_to_csv.py", "tests/test_apify_to_csv.py"),
            ("src/preprocessing/test_process_csv.py", "tests/test_process_csv.py"),
            
            # Documentation
            ("du_an_tom_tat.md", "docs/PROJECT_SUMMARY.md"),
        ]
        
        moved_count = 0
        for src, dst in file_moves:
            src_path = self.project_root / src
            dst_path = self.project_root / dst
            
            if src_path.exists():
                if self.dry_run:
                    self.log(f"[DRY RUN] Would move: {src} → {dst}", "INFO")
                else:
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src_path), str(dst_path))
                    self.log(f"Moved: {src} → {dst}", "SUCCESS")
                moved_count += 1
            else:
                self.log(f"Not found: {src}", "WARNING")
        
        self.log(f"\nMoved {moved_count} files", "SUCCESS")
    
    def extract_dictionaries(self):
        """Extract dictionaries from code to data/external/"""
        self.log("\n" + "="*80, "INFO")
        self.log("PHASE 2C: Extracting dictionaries to data/external/", "INFO")
        self.log("="*80, "INFO")
        
        # Read advanced_text_cleaning.py
        cleaning_file = self.project_root / "src/preprocessing/advanced_text_cleaning.py"
        
        if not cleaning_file.exists():
            self.log("advanced_text_cleaning.py not found, skipping dictionary extraction", "WARNING")
            return
        
        if self.dry_run:
            self.log("[DRY RUN] Would extract TEENCODE_DICT to data/external/teencode_dict.json", "INFO")
            self.log("[DRY RUN] Would extract EMOJI_SENTIMENT to data/external/emoji_sentiment.json", "INFO")
            self.log("[DRY RUN] Would extract vietnamese_surnames to data/external/vietnamese_surnames.txt", "INFO")
            return
        
        # Read the file
        with open(cleaning_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract TEENCODE_DICT
        teencode_match = re.search(r'TEENCODE_DICT = \{([^}]+)\}', content, re.DOTALL)
        if teencode_match:
            # Parse teencode dict manually
            teencode_lines = teencode_match.group(1).strip().split('\n')
            teencode_dict = {}
            for line in teencode_lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    key = parts[0].strip().strip("'\"")
                    value = parts[1].strip().strip("',\"")
                    teencode_dict[key] = value
            
            output_file = self.project_root / "data/external/teencode_dict.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(teencode_dict, f, ensure_ascii=False, indent=2)
            self.log(f"Extracted TEENCODE_DICT ({len(teencode_dict)} entries) to data/external/teencode_dict.json", "SUCCESS")
        
        # Extract EMOJI_SENTIMENT
        emoji_match = re.search(r'EMOJI_SENTIMENT = \{([^}]+)\}', content, re.DOTALL)
        if emoji_match:
            # For emoji, just note it - complex to parse programmatically
            self.log("Found EMOJI_SENTIMENT dict - manual extraction recommended", "WARNING")
        
        self.log("Dictionary extraction completed", "SUCCESS")
    
    def fix_imports(self):
        """Phase 3: Fix all import statements"""
        self.log("\n" + "="*80, "INFO")
        self.log("PHASE 3: Fixing import statements", "INFO")
        self.log("="*80, "INFO")
        
        # Define import fixes: (old_import, new_import)
        import_fixes = [
            # Advanced text cleaning
            (r'from advanced_text_cleaning import', 
             'from src.preprocessing.advanced_text_cleaning import'),
            (r'import src.preprocessing.advanced_text_cleaning as advanced_text_cleaning',
             'import src.preprocessing.advanced_text_cleaning as advanced_text_cleaning'),
            
            # Apify to CSV
            (r'from apify_to_csv import',
             'from src.preprocessing.apify_to_csv import'),
            
            # Process CSV
            (r'from process_csv_with_context import',
             'from src.preprocessing.process_csv_with_context import'),
        ]
        
        # Files to fix
        files_to_fix = [
            # Source code
            "src/preprocessing/apify_to_csv.py",
            "src/preprocessing/advanced_text_cleaning.py",
            "src/preprocessing/process_csv_with_context.py",
            
            # Moved scripts
            "src/labeling/merge_labeled_files.py",
            "src/training/prepare_training_data.py",
            
            # Remaining scripts
            "scripts/prepare_unlabeled_with_context.py",
            "scripts/create_final_dataset_from_json.py",
            "scripts/auto_label_samples.py",
            
            # Tests
            "tests/test_apify_to_csv.py",
            "tests/test_process_csv.py",
        ]
        
        fixed_count = 0
        for file_path in files_to_fix:
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.log(f"File not found: {file_path}", "WARNING")
                continue
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            for old_import, new_import in import_fixes:
                content = re.sub(old_import, new_import, content)
            
            if content != original_content:
                if self.dry_run:
                    self.log(f"[DRY RUN] Would fix imports in: {file_path}", "INFO")
                else:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.log(f"Fixed imports in: {file_path}", "SUCCESS")
                fixed_count += 1
        
        self.log(f"\nFixed imports in {fixed_count} files", "SUCCESS")
    
    def add_project_root(self):
        """Add PROJECT_ROOT constant to files with hardcoded paths"""
        self.log("\n" + "="*80, "INFO")
        self.log("PHASE 3B: Adding PROJECT_ROOT to files", "INFO")
        self.log("="*80, "INFO")
        
        project_root_code = '''
# Project root path
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
'''
        
        files_with_paths = [
            "src/training/prepare_training_data.py",
            "src/labeling/merge_labeled_files.py",
            "src/preprocessing/apify_to_csv.py",
        ]
        
        for file_path in files_with_paths:
            full_path = self.project_root / file_path
            if not full_path.exists():
                continue
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if PROJECT_ROOT already exists
            if 'PROJECT_ROOT' in content:
                self.log(f"PROJECT_ROOT already exists in: {file_path}", "INFO")
                continue
            
            # Add after imports
            import_end = content.find('\n\n')
            if import_end > 0:
                new_content = content[:import_end] + project_root_code + content[import_end:]
                
                if self.dry_run:
                    self.log(f"[DRY RUN] Would add PROJECT_ROOT to: {file_path}", "INFO")
                else:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    self.log(f"Added PROJECT_ROOT to: {file_path}", "SUCCESS")
    
    def cleanup_empty_dirs(self):
        """Remove empty directories"""
        self.log("\n" + "="*80, "INFO")
        self.log("CLEANUP: Removing empty directories", "INFO")
        self.log("="*80, "INFO")
        
        dirs_to_check = [
            "data/raw/processed",
            "TOXIC_COMMENT/datasets",
            "TOXIC_COMMENT/experiments",
            "TOXIC_COMMENT/results",
        ]
        
        for dir_path in dirs_to_check:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                # Check if empty (excluding __pycache__)
                items = [x for x in full_path.iterdir() if x.name != '__pycache__']
                if len(items) == 0:
                    if self.dry_run:
                        self.log(f"[DRY RUN] Would remove empty dir: {dir_path}", "INFO")
                    else:
                        shutil.rmtree(full_path)
                        self.log(f"Removed empty dir: {dir_path}", "SUCCESS")
    
    def generate_summary(self):
        """Generate migration summary report"""
        self.log("\n" + "="*80, "SUCCESS")
        self.log("MIGRATION COMPLETE!", "SUCCESS")
        self.log("="*80, "SUCCESS")
        
        summary_file = self.project_root / "MIGRATION_SUMMARY.md"
        
        summary_content = f"""# Project Migration Summary

**Date:** {datetime.now():%Y-%m-%d %H:%M:%S}
**Mode:** {'DRY RUN' if self.dry_run else 'ACTUAL MIGRATION'}
**Backup Location:** {self.backup_dir if not self.dry_run else 'N/A (dry run)'}

## Actions Performed

"""
        summary_content += "\n".join(self.migration_log)
        
        summary_content += """

## Next Steps

1. ✅ Review migration log above
2. ⚠️ Test all imports: `python -m pytest tests/`
3. ⚠️ Run main scripts to verify functionality
4. ⚠️ Update absolute paths in code to use PROJECT_ROOT
5. ✅ Delete backup folder after verification: `rm -rf backup_*`

## Files to Manually Review

1. **src/preprocessing/apify_to_csv.py** - Check hardcoded paths
2. **src/training/prepare_training_data.py** - Check data paths
3. **src/labeling/merge_labeled_files.py** - Check input paths
4. **notebooks/*.ipynb** - Check import statements

## Import Changes Required

```python
# OLD (❌)
from src.preprocessing.advanced_text_cleaning import clean_text

# NEW (✅)
from src.preprocessing.advanced_text_cleaning import clean_text
```

## Potential Issues

- **Circular imports**: advanced_text_cleaning ↔ apify_to_csv
  - Solution: Extract shared code to src/preprocessing/text_utils.py
  
- **Hardcoded paths**: Many files still use absolute paths
  - Solution: Use PROJECT_ROOT variable

- **Notebook imports**: May need sys.path manipulation
  - Solution: Add PROJECT_ROOT to sys.path in notebooks
"""
        
        if self.dry_run:
            print("\n" + summary_content)
        else:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            self.log(f"\nSummary saved to: MIGRATION_SUMMARY.md", "SUCCESS")
    
    def run(self):
        """Execute full migration"""
        print(f"\n{Colors.BOLD}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}PROJECT MIGRATION SCRIPT V2.0{Colors.END}")
        print(f"{Colors.BOLD}{'='*80}{Colors.END}")
        
        if self.dry_run:
            print(f"{Colors.YELLOW}MODE: DRY RUN (No actual changes will be made){Colors.END}\n")
        else:
            print(f"{Colors.RED}MODE: ACTUAL MIGRATION (Files will be moved/deleted!){Colors.END}\n")
            confirm = input("Type 'YES' to proceed: ")
            if confirm != 'YES':
                print("Migration cancelled.")
                return
        
        try:
            self.backup_project()
            self.delete_files()
            self.create_directories()
            self.move_files()
            self.extract_dictionaries()
            self.fix_imports()
            self.add_project_root()
            self.cleanup_empty_dirs()
            self.generate_summary()
            
        except Exception as e:
            self.log(f"Error during migration: {e}", "ERROR")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate project structure")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Run in simulation mode (no actual changes)')
    parser.add_argument('--execute', action='store_true',
                       help='Execute actual migration')
    parser.add_argument('--project-root', type=str, default='.',
                       help='Project root directory (default: current directory)')
    
    args = parser.parse_args()
    
    # Default to dry run unless --execute is specified
    dry_run = not args.execute
    
    migration = ProjectMigration(
        project_root=args.project_root,
        dry_run=dry_run
    )
    
    migration.run()
