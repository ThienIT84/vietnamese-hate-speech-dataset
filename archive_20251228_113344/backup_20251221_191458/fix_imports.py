#!/usr/bin/env python3
"""
IMPORT FIXER SCRIPT V2.0
Automatically fix all import statements after project restructure
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict
import ast

class ImportFixer:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.fixes_applied = []
        self.files_processed = []
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in project"""
        python_files = []
        
        # Search in specific directories
        search_dirs = [
            'src',
            'scripts',
            'tests',
            'examples',
        ]
        
        for dir_name in search_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                python_files.extend(dir_path.rglob('*.py'))
        
        # Root level Python files
        python_files.extend(self.project_root.glob('*.py'))
        
        return python_files
    
    def find_notebooks(self) -> List[Path]:
        """Find all Jupyter notebooks"""
        notebooks = []
        
        search_dirs = ['notebooks', 'data/labeled', 'data/processed']
        for dir_name in search_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                notebooks.extend(dir_path.rglob('*.ipynb'))
        
        return notebooks
    
    def analyze_imports(self, file_path: Path) -> List[str]:
        """Extract all import statements from a file"""
        imports = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find import statements
            import_pattern = r'^(?:from\s+[\w.]+\s+)?import\s+.+$'
            for line in content.split('\n'):
                if re.match(import_pattern, line.strip()):
                    imports.append(line.strip())
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return imports
    
    def fix_file_imports(self, file_path: Path, dry_run: bool = True) -> int:
        """Fix imports in a single Python file"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return 0
        
        original_content = content
        fixes_count = 0
        
        # Import fix rules (order matters!)
        import_rules = [
            # === PREPROCESSING MODULES ===
            # advanced_text_cleaning
            (r'from advanced_text_cleaning import (.+)',
             r'from src.preprocessing.advanced_text_cleaning import \1'),
            (r'import advanced_text_cleaning as (.+)',
             r'import src.preprocessing.advanced_text_cleaning as \1'),
            (r'import advanced_text_cleaning\b(?!\s+as)',
             r'import src.preprocessing.advanced_text_cleaning as advanced_text_cleaning'),
            
            # apify_to_csv
            (r'from apify_to_csv import (.+)',
             r'from src.preprocessing.apify_to_csv import \1'),
            (r'import apify_to_csv',
             r'import src.preprocessing.apify_to_csv as apify_to_csv'),
            
            # process_csv_with_context
            (r'from process_csv_with_context import (.+)',
             r'from src.preprocessing.process_csv_with_context import \1'),
            
            # === LABELING MODULES ===
            (r'from merge_labeled_data import (.+)',
             r'from src.labeling.merge_labeled_data import \1'),
            (r'from split_data_for_labeling import (.+)',
             r'from src.labeling.split_data_for_labeling import \1'),
            (r'from active_learning import (.+)',
             r'from src.labeling.active_learning import \1'),
            
            # === TRAINING MODULES ===
            (r'from train_baseline_model import (.+)',
             r'from src.training.train_baseline_model import \1'),
            (r'from prepare_training_data import (.+)',
             r'from src.training.prepare_training_data import \1'),
            
            # === UTILS ===
            (r'from csv_to_xlsx import (.+)',
             r'from src.utils.csv_to_xlsx import \1'),
        ]
        
        # Apply rules
        for old_pattern, new_pattern in import_rules:
            if re.search(old_pattern, content, re.MULTILINE):
                content = re.sub(old_pattern, new_pattern, content, flags=re.MULTILINE)
                fixes_count += 1
        
        # Fix relative imports in src/ to absolute imports
        if 'src/' in str(file_path):
            # Change relative imports to absolute
            content = re.sub(
                r'from \.(\w+) import',
                lambda m: f'from src.{file_path.parent.name}.{m.group(1)} import',
                content
            )
        
        # Save changes
        if content != original_content:
            if dry_run:
                print(f"   [DRY RUN] Would fix {fixes_count} imports in: {file_path.relative_to(self.project_root)}")
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Fixed {fixes_count} imports in: {file_path.relative_to(self.project_root)}")
            
            self.fixes_applied.append((str(file_path.relative_to(self.project_root)), fixes_count))
            return fixes_count
        
        return 0
    
    def fix_notebook_imports(self, notebook_path: Path, dry_run: bool = True) -> int:
        """Fix imports in Jupyter notebooks"""
        try:
            import json
            
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
        except Exception as e:
            print(f"❌ Error reading notebook {notebook_path}: {e}")
            return 0
        
        fixes_count = 0
        original_notebook = json.dumps(notebook)
        
        # Process each cell
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                original_source = source
                
                # Apply same import rules as Python files
                import_rules = [
                    (r'from advanced_text_cleaning import (.+)',
                     r'from src.preprocessing.advanced_text_cleaning import \1'),
                    (r'from apify_to_csv import (.+)',
                     r'from src.preprocessing.apify_to_csv import \1'),
                    (r'from process_csv_with_context import (.+)',
                     r'from src.preprocessing.process_csv_with_context import \1'),
                ]
                
                for old_pattern, new_pattern in import_rules:
                    source = re.sub(old_pattern, new_pattern, source, flags=re.MULTILINE)
                
                if source != original_source:
                    cell['source'] = source.split('\n')
                    fixes_count += 1
        
        # Add PROJECT_ROOT setup cell if needed
        has_project_root = any(
            'PROJECT_ROOT' in ''.join(cell.get('source', []))
            for cell in notebook.get('cells', [])
            if cell.get('cell_type') == 'code'
        )
        
        if not has_project_root and fixes_count > 0:
            # Insert PROJECT_ROOT cell at the beginning
            project_root_cell = {
                'cell_type': 'code',
                'execution_count': None,
                'metadata': {},
                'outputs': [],
                'source': [
                    '# Setup project root path\n',
                    'from pathlib import Path\n',
                    'import sys\n',
                    '\n',
                    'PROJECT_ROOT = Path().resolve().parent\n',
                    'sys.path.insert(0, str(PROJECT_ROOT))\n',
                    '\n',
                    'print(f"Project root: {PROJECT_ROOT}")'
                ]
            }
            notebook['cells'].insert(0, project_root_cell)
            fixes_count += 1
        
        # Save changes
        if json.dumps(notebook) != original_notebook:
            if dry_run:
                print(f"   [DRY RUN] Would fix {fixes_count} cells in: {notebook_path.relative_to(self.project_root)}")
            else:
                with open(notebook_path, 'w', encoding='utf-8') as f:
                    json.dump(notebook, f, indent=1, ensure_ascii=False)
                print(f"   ✅ Fixed {fixes_count} cells in: {notebook_path.relative_to(self.project_root)}")
            
            self.fixes_applied.append((str(notebook_path.relative_to(self.project_root)), fixes_count))
            return fixes_count
        
        return 0
    
    def fix_hardcoded_paths(self, file_path: Path, dry_run: bool = True) -> int:
        """Fix hardcoded absolute paths to use PROJECT_ROOT"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return 0
        
        original_content = content
        fixes_count = 0
        
        # Pattern: r'C:\\Học sâu\\Dataset\\...'
        hardcoded_pattern = r"r?['\"]C:\\\\Học sâu\\\\Dataset\\\\([^'\"]+)['\"]"
        
        def replace_path(match):
            nonlocal fixes_count
            rel_path = match.group(1).replace('\\\\', '/')
            fixes_count += 1
            return f"PROJECT_ROOT / '{rel_path}'"
        
        content = re.sub(hardcoded_pattern, replace_path, content)
        
        # Ensure PROJECT_ROOT is imported
        if fixes_count > 0 and 'PROJECT_ROOT' not in content:
            # Add import at the top
            import_block = '''
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

'''
            # Find first import statement
            import_pos = content.find('import ')
            if import_pos > 0:
                content = content[:import_pos] + import_block + content[import_pos:]
        
        # Save changes
        if content != original_content:
            if dry_run:
                print(f"   [DRY RUN] Would fix {fixes_count} paths in: {file_path.relative_to(self.project_root)}")
            else:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Fixed {fixes_count} paths in: {file_path.relative_to(self.project_root)}")
            
            return fixes_count
        
        return 0
    
    def generate_report(self):
        """Generate fix report"""
        print("\n" + "="*80)
        print("📊 IMPORT FIX REPORT")
        print("="*80)
        
        if not self.fixes_applied:
            print("✅ No import fixes needed!")
            return
        
        print(f"\n✅ Fixed imports in {len(self.fixes_applied)} files:\n")
        for file_path, count in sorted(self.fixes_applied):
            print(f"   • {file_path}: {count} fixes")
        
        print(f"\n📝 Total fixes: {sum(count for _, count in self.fixes_applied)}")
        
    def run(self, dry_run: bool = True, fix_paths: bool = False):
        """Run import fixer"""
        print("\n" + "="*80)
        print("🔧 IMPORT FIXER V2.0")
        print("="*80)
        print(f"Mode: {'DRY RUN' if dry_run else 'ACTUAL FIX'}\n")
        
        # Find all Python files
        python_files = self.find_python_files()
        print(f"Found {len(python_files)} Python files\n")
        
        # Fix Python files
        print("📝 Fixing Python files:")
        for file_path in python_files:
            self.fix_file_imports(file_path, dry_run)
            if fix_paths:
                self.fix_hardcoded_paths(file_path, dry_run)
        
        # Find and fix notebooks
        notebooks = self.find_notebooks()
        if notebooks:
            print(f"\n📓 Fixing {len(notebooks)} notebooks:")
            for notebook_path in notebooks:
                self.fix_notebook_imports(notebook_path, dry_run)
        
        self.generate_report()
        
        if dry_run:
            print("\n⚠️  Run with --execute to apply changes")
        else:
            print("\n✅ All imports have been fixed!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix imports after migration")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Simulate fixes without making changes')
    parser.add_argument('--execute', action='store_true',
                       help='Execute actual fixes')
    parser.add_argument('--fix-paths', action='store_true',
                       help='Also fix hardcoded absolute paths')
    parser.add_argument('--project-root', type=str, default='.',
                       help='Project root directory')
    
    args = parser.parse_args()
    
    dry_run = not args.execute
    
    fixer = ImportFixer(project_root=args.project_root)
    fixer.run(dry_run=dry_run, fix_paths=args.fix_paths)
