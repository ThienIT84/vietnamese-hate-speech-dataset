"""
EDA Charts for IT Got Talent 2025 Slides
Tạo các biểu đồ phân tích dữ liệu chi tiết và đẹp mắt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os

# Cấu hình style đẹp cho slides
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.dpi'] = 150

# Màu sắc chuyên nghiệp
COLORS = {
    'clean': '#2ecc71',      # Xanh lá
    'offensive': '#f39c12',  # Cam
    'hate': '#e74c3c',       # Đỏ
    'primary': '#3498db',    # Xanh dương
    'secondary': '#9b59b6'   # Tím
}

LABEL_NAMES = {
    0: 'Clean (Sạch)',
    1: 'Offensive (Phản cảm)',
    2: 'Hate Speech (Thù ghét)'
}

# Tạo thư mục output
OUTPUT_DIR = 'EDA/charts_for_slides'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    """Load dataset"""
    # Thử các file có thể có
    possible_files = [
        'data/final/final_train_data_v3_READY.csv',
        'data/final/final_train_data_v3_SEMANTIC.csv',
        'data/final/final_train_data_v3_READY.xlsx',
    ]
    
    for file_path in possible_files:
        if os.path.exists(file_path):
            print(f"Loading: {file_path}")
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            else:
                return pd.read_excel(file_path)
    
    raise FileNotFoundError("Không tìm thấy file data!")

def chart1_label_distribution(df):
    """Biểu đồ 1: Phân bố nhãn (Pie + Bar)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Đếm số lượng mỗi label
    label_counts = df['label'].value_counts().sort_index()
    labels = [LABEL_NAMES[i] for i in label_counts.index]
    colors = [COLORS['clean'], COLORS['offensive'], COLORS['hate']]
    
    # Pie chart
    wedges, texts, autotexts = axes[0].pie(
        label_counts.values, 
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        explode=(0.02, 0.02, 0.02),
        shadow=True
    )
    axes[0].set_title('Tỷ lệ phân bố nhãn', fontsize=16, fontweight='bold')
    
    # Bar chart
    bars = axes[1].bar(labels, label_counts.values, color=colors, edgecolor='black', linewidth=1.2)
    axes[1].set_ylabel('Số lượng mẫu', fontsize=12)
    axes[1].set_title('Số lượng mẫu theo nhãn', fontsize=16, fontweight='bold')
    
    # Thêm số liệu trên bar
    for bar, count in zip(bars, label_counts.values):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                    f'{count:,}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Thêm tổng số
    total = label_counts.sum()
    fig.suptitle(f'PHÂN BỐ DỮ LIỆU - Tổng: {total:,} mẫu', fontsize=18, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/01_label_distribution.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("✅ Saved: 01_label_distribution.png")

def chart2_text_length_distribution(df):
    """Biểu đồ 2: Phân bố độ dài text"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Tính độ dài
    df['text_length'] = df['text'].astype(str).apply(len)
    df['word_count'] = df['text'].astype(str).apply(lambda x: len(x.split()))
    
    colors = [COLORS['clean'], COLORS['offensive'], COLORS['hate']]
    
    # Histogram độ dài ký tự theo label
    for i, (label, color) in enumerate(zip([0, 1, 2], colors)):
        subset = df[df['label'] == label]['text_length']
        axes[0, 0].hist(subset, bins=50, alpha=0.6, label=LABEL_NAMES[label], color=color)
    axes[0, 0].set_xlabel('Độ dài (ký tự)')
    axes[0, 0].set_ylabel('Số lượng')
    axes[0, 0].set_title('Phân bố độ dài text theo nhãn', fontweight='bold')
    axes[0, 0].legend()
    
    # Boxplot độ dài theo label
    data_by_label = [df[df['label'] == i]['text_length'] for i in [0, 1, 2]]
    bp = axes[0, 1].boxplot(data_by_label, labels=['Clean', 'Offensive', 'Hate'], patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    axes[0, 1].set_ylabel('Độ dài (ký tự)')
    axes[0, 1].set_title('So sánh độ dài text giữa các nhãn', fontweight='bold')
    
    # Histogram số từ
    axes[1, 0].hist(df['word_count'], bins=50, color=COLORS['primary'], edgecolor='black', alpha=0.7)
    axes[1, 0].axvline(df['word_count'].mean(), color='red', linestyle='--', label=f'Mean: {df["word_count"].mean():.1f}')
    axes[1, 0].axvline(df['word_count'].median(), color='orange', linestyle='--', label=f'Median: {df["word_count"].median():.1f}')
    axes[1, 0].set_xlabel('Số từ')
    axes[1, 0].set_ylabel('Số lượng')
    axes[1, 0].set_title('Phân bố số từ trong text', fontweight='bold')
    axes[1, 0].legend()
    
    # Thống kê tổng hợp
    stats_text = f"""
    THỐNG KÊ ĐỘ DÀI TEXT
    
    Độ dài ký tự:
    • Min: {df['text_length'].min():,}
    • Max: {df['text_length'].max():,}
    • Mean: {df['text_length'].mean():,.1f}
    • Median: {df['text_length'].median():,.1f}
    
    Số từ:
    • Min: {df['word_count'].min():,}
    • Max: {df['word_count'].max():,}
    • Mean: {df['word_count'].mean():,.1f}
    • Median: {df['word_count'].median():,.1f}
    """
    axes[1, 1].text(0.1, 0.5, stats_text, transform=axes[1, 1].transAxes, 
                   fontsize=12, verticalalignment='center', fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    axes[1, 1].axis('off')
    axes[1, 1].set_title('Thống kê tổng hợp', fontweight='bold')
    
    plt.suptitle('PHÂN TÍCH ĐỘ DÀI VĂN BẢN', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/02_text_length_distribution.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("✅ Saved: 02_text_length_distribution.png")

def chart3_special_tokens_analysis(df):
    """Biểu đồ 3: Phân tích special tokens"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Đếm special tokens
    tokens = ['<person>', '<user>', '<emo_pos>', '<emo_neg>', '<intense>', '<very_intense>', '<eng_insult>']
    token_counts = {token: df['text'].astype(str).str.count(re.escape(token)).sum() for token in tokens}
    
    # Bar chart
    sorted_tokens = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)
    token_names = [t[0] for t in sorted_tokens]
    counts = [t[1] for t in sorted_tokens]
    
    colors_gradient = plt.cm.Blues(np.linspace(0.4, 0.9, len(token_names)))
    bars = axes[0].barh(token_names, counts, color=colors_gradient, edgecolor='black')
    axes[0].set_xlabel('Số lần xuất hiện')
    axes[0].set_title('Tần suất Special Tokens', fontweight='bold')
    
    # Thêm số liệu
    for bar, count in zip(bars, counts):
        axes[0].text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2, 
                    f'{count:,}', va='center', fontsize=10)
    
    # Phân tích theo label
    token_by_label = []
    for label in [0, 1, 2]:
        subset = df[df['label'] == label]['text'].astype(str)
        total_tokens = sum(subset.str.count(re.escape(t)).sum() for t in tokens)
        token_by_label.append(total_tokens)
    
    colors = [COLORS['clean'], COLORS['offensive'], COLORS['hate']]
    bars2 = axes[1].bar(['Clean', 'Offensive', 'Hate'], token_by_label, color=colors, edgecolor='black')
    axes[1].set_ylabel('Tổng số special tokens')
    axes[1].set_title('Special Tokens theo nhãn', fontweight='bold')
    
    for bar, count in zip(bars2, token_by_label):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, 
                    f'{count:,}', ha='center', fontsize=11, fontweight='bold')
    
    plt.suptitle('PHÂN TÍCH SPECIAL TOKENS', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/03_special_tokens_analysis.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("✅ Saved: 03_special_tokens_analysis.png")

def chart4_data_split_visualization(df):
    """Biểu đồ 4: Minh họa Data Split 80/10/10"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    total = len(df)
    train_size = int(total * 0.8)
    val_size = int(total * 0.1)
    test_size = total - train_size - val_size
    
    # Pie chart
    sizes = [train_size, val_size, test_size]
    labels = [f'Train\n{train_size:,} (80%)', f'Validation\n{val_size:,} (10%)', f'Test\n{test_size:,} (10%)']
    colors = ['#3498db', '#f39c12', '#e74c3c']
    explode = (0.02, 0.02, 0.02)
    
    wedges, texts, autotexts = axes[0].pie(sizes, labels=labels, colors=colors, 
                                           autopct='', startangle=90, explode=explode,
                                           shadow=True, textprops={'fontsize': 12})
    axes[0].set_title('Phân chia dữ liệu', fontsize=16, fontweight='bold')
    
    # Stacked bar showing label distribution in each split
    # Giả lập stratified split
    label_counts = df['label'].value_counts().sort_index()
    
    train_labels = (label_counts * 0.8).astype(int)
    val_labels = (label_counts * 0.1).astype(int)
    test_labels = label_counts - train_labels - val_labels
    
    x = np.arange(3)
    width = 0.25
    
    colors_labels = [COLORS['clean'], COLORS['offensive'], COLORS['hate']]
    
    for i, (label_name, color) in enumerate(zip(['Clean', 'Offensive', 'Hate'], colors_labels)):
        values = [train_labels.iloc[i], val_labels.iloc[i], test_labels.iloc[i]]
        bars = axes[1].bar(x + i*width, values, width, label=label_name, color=color, edgecolor='black')
    
    axes[1].set_xlabel('Tập dữ liệu')
    axes[1].set_ylabel('Số lượng mẫu')
    axes[1].set_title('Phân bố nhãn trong mỗi tập (Stratified)', fontsize=14, fontweight='bold')
    axes[1].set_xticks(x + width)
    axes[1].set_xticklabels(['Train', 'Validation', 'Test'])
    axes[1].legend()
    
    plt.suptitle('DATA SPLIT - Stratified 80/10/10', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/04_data_split.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("✅ Saved: 04_data_split.png")

def chart5_class_imbalance(df):
    """Biểu đồ 5: Class Imbalance và Class Weights"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    label_counts = df['label'].value_counts().sort_index()
    labels = ['Clean', 'Offensive', 'Hate']
    colors = [COLORS['clean'], COLORS['offensive'], COLORS['hate']]
    
    # Imbalance ratio
    max_count = label_counts.max()
    ratios = max_count / label_counts
    
    # Bar chart với imbalance
    bars = axes[0].bar(labels, label_counts.values, color=colors, edgecolor='black', linewidth=1.5)
    axes[0].axhline(y=label_counts.mean(), color='red', linestyle='--', label=f'Mean: {label_counts.mean():.0f}')
    axes[0].set_ylabel('Số lượng mẫu')
    axes[0].set_title('Class Imbalance', fontsize=14, fontweight='bold')
    axes[0].legend()
    
    for bar, count, ratio in zip(bars, label_counts.values, ratios):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30, 
                    f'{count:,}\n(1:{ratio:.2f})', ha='center', fontsize=10)
    
    # Class weights visualization
    # Tính class weights (inverse frequency)
    total = label_counts.sum()
    weights = total / (3 * label_counts)
    weights_normalized = weights / weights.min()
    
    bars2 = axes[1].bar(labels, weights_normalized.values, color=colors, edgecolor='black', linewidth=1.5)
    axes[1].set_ylabel('Class Weight (normalized)')
    axes[1].set_title('Weighted Loss để cân bằng', fontsize=14, fontweight='bold')
    axes[1].axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    
    for bar, w in zip(bars2, weights_normalized.values):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                    f'{w:.2f}', ha='center', fontsize=12, fontweight='bold')
    
    plt.suptitle('XỬ LÝ MẤT CÂN BẰNG DỮ LIỆU', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/05_class_imbalance.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("✅ Saved: 05_class_imbalance.png")

def chart6_preprocessing_pipeline(df):
    """Biểu đồ 6: Minh họa Preprocessing Pipeline"""
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Pipeline steps
    steps = [
        ('1. Unicode NFC', 'Chuẩn hóa ký tự'),
        ('2. URL/HTML Removal', 'Xóa links, tags'),
        ('3. Hashtag Removal', 'Xóa #hashtags'),
        ('4. Mentions Masking', '@user → <user>'),
        ('5. Teencode Normalize', '1000+ biến thể'),
        ('6. NER Masking', 'Tên người → <person>'),
        ('7. Lowercase', 'Chữ thường'),
        ('8. Emoji Mapping', '🐷 → lợn <intense>'),
        ('9. English Insults', 'fuck → <eng_vulgar>'),
        ('10. Bypass Patterns', 'n.g.u → ngu'),
        ('11. Intensity Markers', 'nguuuu → ngu <intense>'),
        ('12. Context "m" Map', 'm → em/mày/mình'),
    ]
    
    # Vẽ flowchart
    y_positions = np.linspace(0.95, 0.05, len(steps))
    
    for i, ((step_name, desc), y) in enumerate(zip(steps, y_positions)):
        # Box
        color = plt.cm.Blues(0.3 + 0.5 * (i / len(steps)))
        rect = plt.Rectangle((0.1, y - 0.03), 0.35, 0.06, 
                             facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(0.275, y, step_name, ha='center', va='center', fontsize=11, fontweight='bold')
        
        # Description
        ax.text(0.5, y, desc, ha='left', va='center', fontsize=10, style='italic')
        
        # Arrow
        if i < len(steps) - 1:
            ax.annotate('', xy=(0.275, y - 0.04), xytext=(0.275, y - 0.06),
                       arrowprops=dict(arrowstyle='->', color='gray', lw=2))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('PREPROCESSING PIPELINE - 18 BƯỚC XỬ LÝ', fontsize=18, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/06_preprocessing_pipeline.png', bbox_inches='tight', dpi=200)
    plt.close()
    print("✅ Saved: 06_preprocessing_pipeline.png")

def main():
    print("="*60)
    print("🎨 TẠO BIỂU ĐỒ EDA CHO SLIDES IT GOT TALENT 2025")
    print("="*60)
    
    # Load data
    df = load_data()
    print(f"\n📊 Dataset: {len(df):,} samples")
    print(f"   Columns: {list(df.columns)}")
    
    # Tạo các biểu đồ
    print("\n🖼️ Đang tạo biểu đồ...")
    
    chart1_label_distribution(df)
    chart2_text_length_distribution(df)
    chart3_special_tokens_analysis(df)
    chart4_data_split_visualization(df)
    chart5_class_imbalance(df)
    chart6_preprocessing_pipeline(df)
    
    print("\n" + "="*60)
    print(f"✅ HOÀN TẤT! Các biểu đồ đã lưu tại: {OUTPUT_DIR}/")
    print("="*60)
    
    # List files
    print("\n📁 Danh sách file:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.endswith('.png'):
            print(f"   • {f}")

if __name__ == "__main__":
    main()
