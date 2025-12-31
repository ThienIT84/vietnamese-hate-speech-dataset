"""
Apply advanced_text_cleaning to convert emoji -> text for PhoBERT
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from preprocessing.advanced_text_cleaning import clean_text

print("="*60)
print("APPLY ADVANCED TEXT CLEANING")
print("="*60)

# Load data
input_file = Path(r"data\processed\FINAL_RECOVERED_FB_YT_20251224_142349.csv")
print(f"\n[1/3] Loading {input_file.name}...")
df = pd.read_csv(input_file, encoding='utf-8-sig')
print(f"  ✓ Loaded: {len(df)} samples")

# Apply cleaning
print("\n[2/3] Cleaning texts...")
print("  Processing with advanced_clean_text:")
print("  - Emoji → sentiment tags (<emo_pos>, <emo_neg>)")
print("  - Teencode normalization")
print("  - Intensity markers (<intense>, <very_intense>)")
print("  - Person tags preserved")

cleaned_texts = []
for i, text in enumerate(df['text'], 1):
    if i % 500 == 0:
        print(f"  Processing {i}/{len(df)}...")
    
    # Apply full advanced cleaning pipeline
    cleaned = clean_text(text)
    cleaned_texts.append(cleaned)

df['text_raw'] = df['text']  # Keep original with emoji
df['text'] = cleaned_texts    # Cleaned version for PhoBERT

print(f"  ✓ Cleaned: {len(cleaned_texts)} texts")

# Show examples
print("\n" + "="*60)
print("EXAMPLES (Before -> After)")
print("="*60)

import re
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"
    u"\U0001F300-\U0001F5FF"
    u"\U0001F680-\U0001F6FF"
    "]+", flags=re.UNICODE)

# Find samples with emoji
emoji_samples = df[df['text_raw'].str.contains(emoji_pattern, na=False)]

for i, (idx, row) in enumerate(emoji_samples.head(5).iterrows(), 1):
    print(f"\n{i}. BEFORE: {row['text_raw'][:100]}")
    print(f"   AFTER:  {row['text'][:100]}")
    print(f"   Label: {row['label']}")

# Save
output_dir = Path(r"data\processed")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

csv_path = output_dir / f"FINAL_TRAINING_DATASET_{timestamp}.csv"
df[['text', 'label', 'note', 'text_raw']].to_csv(csv_path, index=False, encoding='utf-8-sig')

json_path = output_dir / f"FINAL_TRAINING_DATASET_{timestamp}.json"
json_data = df[['text', 'label', 'note', 'text_raw']].to_dict(orient='records')
import json
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)
print(f"✓ Saved: {csv_path.name}")
print(f"✓ Saved: {json_path.name}")
print(f"\nTotal samples: {len(df)}")
print(f"\nColumns:")
print(f"  - text: Cleaned text for PhoBERT (emoji -> text)")
print(f"  - label: 0/1/2")
print(f"  - note: Annotation notes")
print(f"  - text_raw: Original text with emoji")
print(f"\nLabel distribution:")
for label, count in df['label'].value_counts().sort_index().items():
    pct = 100 * count / len(df)
    print(f"  Label {label}: {count:,} ({pct:.1f}%)")

print("\n" + "="*60)
print("✓ READY FOR SEMI-SUPERVISED LEARNING!")
print("="*60)
