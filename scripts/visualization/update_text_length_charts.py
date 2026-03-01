"""
Script cập nhật 2 biểu đồ Text Length Distribution
Sử dụng dữ liệu thực tế từ dataset 6,974 samples

Usage:
    python scripts/visualization/update_text_length_charts.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ===== Load Data =====
print("📂 Loading data...")
data_path = "data/final/final_train_data_v3_READY_PHOBERT_20260102_053035_SEGMENTED_20260102_053456.csv"

if not Path(data_path).exists():
    print(f"❌ File not found: {data_path}")
    print("Please check the path!")
    exit(1)

df = pd.read_csv(data_path)
print(f"✅ Loaded {len(df):,} samples")

# Identify columns
text_col = 'training_text' if 'training_text' in df.columns else 'text'
label_col = 'label'

# Calculate text length (number of words)
df['text_length'] = df[text_col].apply(lambda x: len(str(x).split()))

print(f"\n📊 Text Length Statistics:")
print(f"   Mean: {df['text_length'].mean():.1f} words")
print(f"   Median: {df['text_length'].median():.1f} words")
print(f"   Min: {df['text_length'].min()} words")
print(f"   Max: {df['text_length'].max()} words")
print(f"   Std: {df['text_length'].std():.1f} words")

# ===== Chart 1: Text Length Distribution (Overall) =====
print("\n📊 Creating Chart 1: Text Length Distribution...")

fig, ax = plt.subplots(figsize=(10, 6))

# Histogram
n, bins, patches = ax.hist(df['text_length'], bins=50, color='#3498db', 
                            edgecolor='black', alpha=0.7)

# Mean line
mean_length = df['text_length'].mean()
ax.axvline(mean_length, color='red', linestyle='--', linewidth=2, 
           label=f'Mean: {mean_length:.1f}')

# Labels and title
ax.set_xlabel('Text Length (words)', fontsize=12, fontweight='bold')
ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('Text Length Distribution', fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# Add statistics text box
stats_text = f'Total: {len(df):,} samples\n'
stats_text += f'Mean: {mean_length:.1f} words\n'
stats_text += f'Median: {df["text_length"].median():.1f} words\n'
stats_text += f'Std: {df["text_length"].std():.1f} words'

ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('text_length_distribution.png', dpi=300, bbox_inches='tight')
print("✅ Saved: text_length_distribution.png")
plt.close()

# ===== Chart 2: Text Length by Label =====
print("\n📊 Creating Chart 2: Text Length by Label...")

fig, ax = plt.subplots(figsize=(10, 6))

# Separate data by label
label_names = {0: 'Label 0 (Clean)', 1: 'Label 1 (Offensive)', 2: 'Label 2 (Hate)'}
colors = ['#3498db', '#e74c3c', '#2ecc71']

for label in [0, 1, 2]:
    data = df[df[label_col] == label]['text_length']
    ax.hist(data, bins=50, alpha=0.6, label=label_names[label], 
            color=colors[label], edgecolor='black')

# Labels and title
ax.set_xlabel('Text Length (words)', fontsize=12, fontweight='bold')
ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('Text Length by Label', fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=11, loc='upper right')
ax.grid(True, alpha=0.3)

# Add statistics for each label
stats_by_label = []
for label in [0, 1, 2]:
    data = df[df[label_col] == label]['text_length']
    stats_by_label.append(f"{label_names[label]}: {data.mean():.1f} words (n={len(data):,})")

stats_text = '\n'.join(stats_by_label)
ax.text(0.98, 0.60, stats_text, transform=ax.transAxes,
        fontsize=9, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('text_length_by_label.png', dpi=300, bbox_inches='tight')
print("✅ Saved: text_length_by_label.png")
plt.close()

# ===== Summary Statistics =====
print("\n" + "="*60)
print("📊 SUMMARY STATISTICS BY LABEL")
print("="*60)

for label in [0, 1, 2]:
    data = df[df[label_col] == label]['text_length']
    print(f"\n{label_names[label]}:")
    print(f"   Count: {len(data):,} samples")
    print(f"   Mean: {data.mean():.1f} words")
    print(f"   Median: {data.median():.1f} words")
    print(f"   Min: {data.min()} words")
    print(f"   Max: {data.max()} words")
    print(f"   Std: {data.std():.1f} words")

print("\n" + "="*60)
print("✅ COMPLETED!")
print("="*60)
print("\n📁 Output files:")
print("   1. text_length_distribution.png")
print("   2. text_length_by_label.png")
print("\n💡 Use these charts for presentation!")
