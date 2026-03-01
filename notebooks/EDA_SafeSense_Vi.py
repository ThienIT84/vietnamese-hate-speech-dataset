# %% [markdown]
# # 📊 EDA - SafeSense-Vi Dataset Analysis
# ## IT Got Talent 2025 - Phân tích dữ liệu Toxic Comment tiếng Việt
# 
# **Mục tiêu:**
# - Phân tích phân bố dữ liệu
# - Khám phá đặc điểm văn bản  
# - Tạo biểu đồ cho slides thuyết trình

# %% [markdown]
# ## 1. Import Libraries & Load Data

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

# Style settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['figure.dpi'] = 150
plt.rcParams['axes.unicode_minus'] = False

# Colors
COLORS = {'clean': '#2ecc71', 'offensive': '#f39c12', 'hate': '#e74c3c'}
COLOR_LIST = [COLORS['clean'], COLORS['offensive'], COLORS['hate']]
LABEL_NAMES = {0: 'Clean', 1: 'Offensive', 2: 'Hate Speech'}
LABEL_NAMES_VI = {0: 'Sạch', 1: 'Phản cảm', 2: 'Thù ghét'}

print('✅ Libraries loaded!')

# %%
# Load dataset
DATA_PATH = 'data/final/dataset_hate_speech_Vietnamese_KAGGLE_V2.csv'
df = pd.read_csv(DATA_PATH)

print(f"📊 Dataset loaded: {len(df):,} samples")
print(f"📋 Columns: {list(df.columns)}")
print(f"\n🔍 First 3 rows:")
df.head(3)


# %% [markdown]
# ## 2. 📈 Tổng quan Dataset

# %%
print("="*60)
print("📊 TỔNG QUAN DATASET")
print("="*60)

print(f"\n📌 Tổng số mẫu: {len(df):,}")
print(f"📌 Số cột: {len(df.columns)}")
print(f"\n📋 Thông tin cột:")
print(df.info())

print(f"\n📋 Thống kê mô tả:")
df.describe()

# %% [markdown]
# ## 3. 🏷️ Phân bố nhãn (Label Distribution)

# %%
# Đếm số lượng mỗi label
label_counts = df['label'].value_counts().sort_index()
print("📊 Phân bố nhãn:")
for label, count in label_counts.items():
    pct = count / len(df) * 100
    print(f"   {label} ({LABEL_NAMES[label]}): {count:,} ({pct:.1f}%)")

# %%
# BIỂU ĐỒ 1: Phân bố nhãn (Pie + Bar)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
labels_pie = [f"{LABEL_NAMES[i]}\n({label_counts[i]:,})" for i in label_counts.index]
wedges, texts, autotexts = axes[0].pie(
    label_counts.values, 
    labels=labels_pie,
    colors=COLOR_LIST,
    autopct='%1.1f%%',
    startangle=90,
    explode=(0.02, 0.02, 0.02),
    shadow=True,
    textprops={'fontsize': 11}
)
axes[0].set_title('Tỷ lệ phân bố nhãn', fontsize=14, fontweight='bold')

# Bar chart
bars = axes[1].bar(
    [LABEL_NAMES[i] for i in label_counts.index], 
    label_counts.values, 
    color=COLOR_LIST, 
    edgecolor='black', 
    linewidth=1.5
)
axes[1].set_ylabel('Số lượng mẫu', fontsize=12)
axes[1].set_xlabel('Nhãn', fontsize=12)
axes[1].set_title('Số lượng mẫu theo nhãn', fontsize=14, fontweight='bold')

# Thêm số liệu trên bar
for bar, count in zip(bars, label_counts.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30, 
                f'{count:,}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.suptitle(f'PHÂN BỐ DỮ LIỆU - Tổng: {len(df):,} mẫu', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('EDA/01_label_distribution.png', bbox_inches='tight', dpi=200)
plt.show()
print("✅ Saved: EDA/01_label_distribution.png")


# %% [markdown]
# ## 4. 📏 Phân tích độ dài văn bản (Text Length Analysis)

# %%
# Tính độ dài
df['char_length'] = df['text'].astype(str).apply(len)
df['word_count'] = df['text'].astype(str).apply(lambda x: len(x.split()))

print("📏 THỐNG KÊ ĐỘ DÀI VĂN BẢN")
print("="*50)
print(f"\n📌 Độ dài ký tự:")
print(f"   Min: {df['char_length'].min():,}")
print(f"   Max: {df['char_length'].max():,}")
print(f"   Mean: {df['char_length'].mean():,.1f}")
print(f"   Median: {df['char_length'].median():,.1f}")
print(f"   Std: {df['char_length'].std():,.1f}")

print(f"\n📌 Số từ:")
print(f"   Min: {df['word_count'].min():,}")
print(f"   Max: {df['word_count'].max():,}")
print(f"   Mean: {df['word_count'].mean():,.1f}")
print(f"   Median: {df['word_count'].median():,.1f}")

# %%
# BIỂU ĐỒ 2: Phân bố độ dài text
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 2.1 Histogram độ dài ký tự theo label
for label, color in zip([0, 1, 2], COLOR_LIST):
    subset = df[df['label'] == label]['char_length']
    axes[0, 0].hist(subset, bins=50, alpha=0.6, label=LABEL_NAMES[label], color=color)
axes[0, 0].set_xlabel('Độ dài (ký tự)')
axes[0, 0].set_ylabel('Số lượng')
axes[0, 0].set_title('Phân bố độ dài text theo nhãn', fontweight='bold')
axes[0, 0].legend()

# 2.2 Boxplot độ dài theo label
data_by_label = [df[df['label'] == i]['char_length'] for i in [0, 1, 2]]
bp = axes[0, 1].boxplot(data_by_label, labels=['Clean', 'Offensive', 'Hate'], patch_artist=True)
for patch, color in zip(bp['boxes'], COLOR_LIST):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0, 1].set_ylabel('Độ dài (ký tự)')
axes[0, 1].set_title('So sánh độ dài text giữa các nhãn', fontweight='bold')

# 2.3 Histogram số từ
axes[1, 0].hist(df['word_count'], bins=50, color='#3498db', edgecolor='black', alpha=0.7)
axes[1, 0].axvline(df['word_count'].mean(), color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {df["word_count"].mean():.1f}')
axes[1, 0].axvline(df['word_count'].median(), color='orange', linestyle='--', linewidth=2,
                   label=f'Median: {df["word_count"].median():.1f}')
axes[1, 0].set_xlabel('Số từ')
axes[1, 0].set_ylabel('Số lượng')
axes[1, 0].set_title('Phân bố số từ trong text', fontweight='bold')
axes[1, 0].legend()

# 2.4 Violin plot
parts = axes[1, 1].violinplot([df[df['label'] == i]['word_count'] for i in [0, 1, 2]], 
                              positions=[1, 2, 3], showmeans=True, showmedians=True)
for i, pc in enumerate(parts['bodies']):
    pc.set_facecolor(COLOR_LIST[i])
    pc.set_alpha(0.7)
axes[1, 1].set_xticks([1, 2, 3])
axes[1, 1].set_xticklabels(['Clean', 'Offensive', 'Hate'])
axes[1, 1].set_ylabel('Số từ')
axes[1, 1].set_title('Violin Plot - Số từ theo nhãn', fontweight='bold')

plt.suptitle('PHÂN TÍCH ĐỘ DÀI VĂN BẢN', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('EDA/02_text_length_analysis.png', bbox_inches='tight', dpi=200)
plt.show()
print("✅ Saved: EDA/02_text_length_analysis.png")


# %% [markdown]
# ## 5. 🏷️ Phân tích Special Tokens

# %%
# Đếm special tokens
SPECIAL_TOKENS = [
    '<person>', '<user>', '<emo_pos>', '<emo_neg>', 
    '<intense>', '<very_intense>', '<eng_insult>', '<eng_vulgar>',
    '</s>'  # Separator token
]

token_counts = {}
for token in SPECIAL_TOKENS:
    count = df['text'].astype(str).str.count(re.escape(token)).sum()
    token_counts[token] = count

print("🏷️ THỐNG KÊ SPECIAL TOKENS")
print("="*50)
for token, count in sorted(token_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   {token}: {count:,}")

# %%
# BIỂU ĐỒ 3: Special Tokens Analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 3.1 Bar chart tần suất tokens
sorted_tokens = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)
token_names = [t[0] for t in sorted_tokens if t[1] > 0]
counts = [t[1] for t in sorted_tokens if t[1] > 0]

colors_gradient = plt.cm.Blues(np.linspace(0.4, 0.9, len(token_names)))
bars = axes[0].barh(token_names, counts, color=colors_gradient, edgecolor='black')
axes[0].set_xlabel('Số lần xuất hiện')
axes[0].set_title('Tần suất Special Tokens', fontweight='bold')
for bar, count in zip(bars, counts):
    axes[0].text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2, 
                f'{count:,}', va='center', fontsize=10)

# 3.2 Tokens theo label
tokens_to_analyze = ['<emo_pos>', '<emo_neg>', '<intense>', '<person>']
token_by_label = {token: [] for token in tokens_to_analyze}

for label in [0, 1, 2]:
    subset = df[df['label'] == label]['text'].astype(str)
    for token in tokens_to_analyze:
        count = subset.str.count(re.escape(token)).sum()
        token_by_label[token].append(count)

x = np.arange(3)
width = 0.2
for i, (token, counts_list) in enumerate(token_by_label.items()):
    axes[1].bar(x + i*width, counts_list, width, label=token, edgecolor='black')

axes[1].set_xlabel('Nhãn')
axes[1].set_ylabel('Số lượng')
axes[1].set_title('Special Tokens theo nhãn', fontweight='bold')
axes[1].set_xticks(x + width * 1.5)
axes[1].set_xticklabels(['Clean', 'Offensive', 'Hate'])
axes[1].legend(loc='upper right')

plt.suptitle('PHÂN TÍCH SPECIAL TOKENS', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('EDA/03_special_tokens.png', bbox_inches='tight', dpi=200)
plt.show()
print("✅ Saved: EDA/03_special_tokens.png")


# %% [markdown]
# ## 6. 📊 Class Imbalance Analysis

# %%
# BIỂU ĐỒ 4: Class Imbalance và Weights
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

label_counts = df['label'].value_counts().sort_index()
labels = ['Clean', 'Offensive', 'Hate']

# 4.1 Imbalance visualization
max_count = label_counts.max()
ratios = max_count / label_counts

bars = axes[0].bar(labels, label_counts.values, color=COLOR_LIST, edgecolor='black', linewidth=1.5)
axes[0].axhline(y=label_counts.mean(), color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {label_counts.mean():,.0f}')
axes[0].set_ylabel('Số lượng mẫu')
axes[0].set_title('Class Imbalance', fontsize=14, fontweight='bold')
axes[0].legend()

for bar, count, ratio in zip(bars, label_counts.values, ratios):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30, 
                f'{count:,}\n(ratio: {ratio:.2f})', ha='center', fontsize=10)

# 4.2 Class weights (inverse frequency)
total = label_counts.sum()
weights = total / (3 * label_counts)
weights_normalized = weights / weights.min()

bars2 = axes[1].bar(labels, weights_normalized.values, color=COLOR_LIST, edgecolor='black', linewidth=1.5)
axes[1].set_ylabel('Class Weight (normalized)')
axes[1].set_title('Weighted Loss để cân bằng', fontsize=14, fontweight='bold')
axes[1].axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)

for bar, w in zip(bars2, weights_normalized.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03, 
                f'{w:.2f}', ha='center', fontsize=12, fontweight='bold')

plt.suptitle('XỬ LÝ MẤT CÂN BẰNG DỮ LIỆU', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('EDA/04_class_imbalance.png', bbox_inches='tight', dpi=200)
plt.show()
print("✅ Saved: EDA/04_class_imbalance.png")

# In class weights
print("\n📊 CLASS WEIGHTS (cho Weighted Loss):")
print(f"   Clean (0): {weights_normalized[0]:.4f}")
print(f"   Offensive (1): {weights_normalized[1]:.4f}")
print(f"   Hate (2): {weights_normalized[2]:.4f}")


# %% [markdown]
# ## 7. 📝 Word Cloud & Top Words

# %%
try:
    from wordcloud import WordCloud
    HAS_WORDCLOUD = True
except ImportError:
    print("⚠️ wordcloud not installed. Skipping word cloud. Install with: pip install wordcloud")
    HAS_WORDCLOUD = False

if HAS_WORDCLOUD:
    # Tạo word cloud cho mỗi label
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for idx, (label, ax, color) in enumerate(zip([0, 1, 2], axes, ['Greens', 'Oranges', 'Reds'])):
        text_combined = ' '.join(df[df['label'] == label]['text'].astype(str).tolist())
        
        # Loại bỏ special tokens và separator
        text_combined = re.sub(r'<[^>]+>', '', text_combined)
        text_combined = re.sub(r'</s>', '', text_combined)
        
        wordcloud = WordCloud(
            width=800, height=400,
            background_color='white',
            colormap=color,
            max_words=100,
            min_font_size=10
        ).generate(text_combined)
        
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(f'{LABEL_NAMES[label]}', fontsize=14, fontweight='bold')

    plt.suptitle('WORD CLOUD THEO NHÃN', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('EDA/05_wordcloud.png', bbox_inches='tight', dpi=200)
    plt.show()
    print("✅ Saved: EDA/05_wordcloud.png")

# %% [markdown]
# ## 8. 🔤 Top Words Analysis

# %%
def get_top_words(texts, n=20):
    """Lấy top n từ phổ biến nhất"""
    all_words = []
    for text in texts:
        # Loại bỏ special tokens
        text = re.sub(r'<[^>]+>', '', str(text))
        text = re.sub(r'</s>', '', text)
        words = text.lower().split()
        # Lọc từ ngắn
        words = [w for w in words if len(w) > 1 and not w.isdigit()]
        all_words.extend(words)
    return Counter(all_words).most_common(n)

# Top words cho mỗi label
fig, axes = plt.subplots(1, 3, figsize=(18, 8))

for idx, (label, ax, color) in enumerate(zip([0, 1, 2], axes, COLOR_LIST)):
    texts = df[df['label'] == label]['text']
    top_words = get_top_words(texts, 15)
    
    words = [w[0] for w in top_words]
    counts = [w[1] for w in top_words]
    
    ax.barh(words[::-1], counts[::-1], color=color, edgecolor='black')
    ax.set_xlabel('Tần suất')
    ax.set_title(f'Top 15 từ - {LABEL_NAMES[label]}', fontweight='bold')

plt.suptitle('TOP WORDS THEO NHÃN', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('EDA/06_top_words.png', bbox_inches='tight', dpi=200)
plt.show()
print("✅ Saved: EDA/06_top_words.png")


# %% [markdown]
# ## 9. 📊 Data Split Visualization (80/10/10)

# %%
# BIỂU ĐỒ 7: Data Split
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

total = len(df)
train_size = int(total * 0.8)
val_size = int(total * 0.1)
test_size = total - train_size - val_size

# 7.1 Pie chart
sizes = [train_size, val_size, test_size]
labels_split = [f'Train\n{train_size:,}\n(80%)', f'Validation\n{val_size:,}\n(10%)', f'Test\n{test_size:,}\n(10%)']
colors_split = ['#3498db', '#f39c12', '#e74c3c']

wedges, texts, autotexts = axes[0].pie(
    sizes, labels=labels_split, colors=colors_split,
    autopct='', startangle=90, explode=(0.02, 0.02, 0.02),
    shadow=True, textprops={'fontsize': 11}
)
axes[0].set_title('Phân chia dữ liệu', fontsize=14, fontweight='bold')

# 7.2 Stacked bar - label distribution in each split (stratified)
label_counts = df['label'].value_counts().sort_index()
train_labels = (label_counts * 0.8).astype(int)
val_labels = (label_counts * 0.1).astype(int)
test_labels = label_counts - train_labels - val_labels

x = np.arange(3)
width = 0.25

for i, (label_name, color) in enumerate(zip(['Clean', 'Offensive', 'Hate'], COLOR_LIST)):
    values = [train_labels.iloc[i], val_labels.iloc[i], test_labels.iloc[i]]
    axes[1].bar(x + i*width, values, width, label=label_name, color=color, edgecolor='black')

axes[1].set_xlabel('Tập dữ liệu')
axes[1].set_ylabel('Số lượng mẫu')
axes[1].set_title('Phân bố nhãn trong mỗi tập (Stratified)', fontsize=14, fontweight='bold')
axes[1].set_xticks(x + width)
axes[1].set_xticklabels(['Train', 'Validation', 'Test'])
axes[1].legend()

plt.suptitle('DATA SPLIT - Stratified 80/10/10', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('EDA/07_data_split.png', bbox_inches='tight', dpi=200)
plt.show()
print("✅ Saved: EDA/07_data_split.png")

print(f"\n📊 DATA SPLIT:")
print(f"   Train: {train_size:,} samples (80%)")
print(f"   Validation: {val_size:,} samples (10%)")
print(f"   Test: {test_size:,} samples (10%)")


# %% [markdown]
# ## 10. 📋 Sample Examples

# %%
print("="*80)
print("📋 VÍ DỤ MẪU DỮ LIỆU THEO NHÃN")
print("="*80)

for label in [0, 1, 2]:
    print(f"\n{'='*80}")
    print(f"🏷️ LABEL {label} - {LABEL_NAMES[label].upper()}")
    print("="*80)
    
    samples = df[df['label'] == label].sample(min(3, len(df[df['label'] == label])))
    for idx, row in samples.iterrows():
        text = row['text'][:200] + "..." if len(row['text']) > 200 else row['text']
        print(f"\n📝 {text}")

# %% [markdown]
# ## 11. 📊 Summary Statistics

# %%
# BIỂU ĐỒ 8: Summary Dashboard
fig = plt.figure(figsize=(16, 12))

# 8.1 Label distribution (top left)
ax1 = fig.add_subplot(2, 2, 1)
label_counts = df['label'].value_counts().sort_index()
bars = ax1.bar(['Clean', 'Offensive', 'Hate'], label_counts.values, color=COLOR_LIST, edgecolor='black')
ax1.set_title('Phân bố nhãn', fontweight='bold')
ax1.set_ylabel('Số lượng')
for bar, count in zip(bars, label_counts.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, 
            f'{count:,}', ha='center', fontsize=10, fontweight='bold')

# 8.2 Text length distribution (top right)
ax2 = fig.add_subplot(2, 2, 2)
ax2.hist(df['word_count'], bins=40, color='#3498db', edgecolor='black', alpha=0.7)
ax2.axvline(df['word_count'].mean(), color='red', linestyle='--', linewidth=2)
ax2.set_title('Phân bố số từ', fontweight='bold')
ax2.set_xlabel('Số từ')
ax2.set_ylabel('Số lượng')

# 8.3 Boxplot by label (bottom left)
ax3 = fig.add_subplot(2, 2, 3)
data_by_label = [df[df['label'] == i]['word_count'] for i in [0, 1, 2]]
bp = ax3.boxplot(data_by_label, labels=['Clean', 'Offensive', 'Hate'], patch_artist=True)
for patch, color in zip(bp['boxes'], COLOR_LIST):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax3.set_title('Số từ theo nhãn', fontweight='bold')
ax3.set_ylabel('Số từ')

# 8.4 Summary text (bottom right)
ax4 = fig.add_subplot(2, 2, 4)
summary_text = f"""
📊 TỔNG KẾT DATASET
{'='*40}

📌 Tổng số mẫu: {len(df):,}

📌 Phân bố nhãn:
   • Clean: {label_counts[0]:,} ({label_counts[0]/len(df)*100:.1f}%)
   • Offensive: {label_counts[1]:,} ({label_counts[1]/len(df)*100:.1f}%)
   • Hate: {label_counts[2]:,} ({label_counts[2]/len(df)*100:.1f}%)

📌 Độ dài văn bản:
   • Trung bình: {df['word_count'].mean():.1f} từ
   • Median: {df['word_count'].median():.1f} từ
   • Max: {df['word_count'].max()} từ

📌 Data Split (80/10/10):
   • Train: {int(len(df)*0.8):,}
   • Val: {int(len(df)*0.1):,}
   • Test: {len(df) - int(len(df)*0.8) - int(len(df)*0.1):,}
"""
ax4.text(0.1, 0.5, summary_text, transform=ax4.transAxes, fontsize=11,
        verticalalignment='center', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax4.axis('off')
ax4.set_title('Tổng kết', fontweight='bold')

plt.suptitle('📊 SAFESENSE-VI DATASET SUMMARY', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('EDA/08_summary_dashboard.png', bbox_inches='tight', dpi=200)
plt.show()
print("✅ Saved: EDA/08_summary_dashboard.png")


# %% [markdown]
# ## 12. 🎯 Correlation & Heatmap

# %%
# Tạo features cho correlation
df['has_person'] = df['text'].str.contains('<person>', regex=False).astype(int)
df['has_emo_pos'] = df['text'].str.contains('<emo_pos>', regex=False).astype(int)
df['has_emo_neg'] = df['text'].str.contains('<emo_neg>', regex=False).astype(int)
df['has_intense'] = df['text'].str.contains('<intense>', regex=False).astype(int)

# Correlation matrix
features = ['label', 'char_length', 'word_count', 'has_person', 'has_emo_pos', 'has_emo_neg', 'has_intense']
corr_matrix = df[features].corr()

# BIỂU ĐỒ 9: Correlation Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0, 
            fmt='.2f', linewidths=0.5, ax=ax)
ax.set_title('Ma trận tương quan các đặc trưng', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('EDA/09_correlation_heatmap.png', bbox_inches='tight', dpi=200)
plt.show()
print("✅ Saved: EDA/09_correlation_heatmap.png")

# %% [markdown]
# ## 13. ✅ Hoàn tất EDA

# %%
import os

print("\n" + "="*60)
print("✅ EDA HOÀN TẤT!")
print("="*60)

# List all saved charts
eda_dir = 'EDA'
if os.path.exists(eda_dir):
    print(f"\n📁 Các biểu đồ đã lưu tại thư mục: {eda_dir}/")
    for f in sorted(os.listdir(eda_dir)):
        if f.endswith('.png'):
            print(f"   📊 {f}")

print(f"\n📊 TỔNG KẾT DATASET:")
print(f"   • Tổng mẫu: {len(df):,}")
print(f"   • Clean: {label_counts[0]:,} ({label_counts[0]/len(df)*100:.1f}%)")
print(f"   • Offensive: {label_counts[1]:,} ({label_counts[1]/len(df)*100:.1f}%)")
print(f"   • Hate: {label_counts[2]:,} ({label_counts[2]/len(df)*100:.1f}%)")
print(f"   • Avg words: {df['word_count'].mean():.1f}")

print("\n🎯 Sẵn sàng cho slides IT Got Talent 2025!")
