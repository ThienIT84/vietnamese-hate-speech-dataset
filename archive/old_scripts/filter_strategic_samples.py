"""
Filter strategic samples from unlabeled data based on keyword analysis
Target: 1000 samples covering 3 groups (Label 0, 1, 2)
"""
import pandas as pd
import numpy as np
from datetime import datetime
import re

print("="*80)
print("🎯 STRATEGIC SAMPLE FILTERING")
print("="*80)

# Load data
print("\n📂 Loading data...")
unlabeled_df = pd.read_csv('data/interim/unlabeled_data_for_labeling.csv')
train_df = pd.read_excel('final_train_data_v3_TRUNCATED_20251229.xlsx')

print(f"   Unlabeled: {len(unlabeled_df)} rows")
print(f"   Training: {len(train_df)} rows")

# Get training texts for deduplication
train_texts = set(train_df['training_text'].str.lower().str.strip())
print(f"   Training unique texts: {len(train_texts)}")

# ============================================================
# KEYWORD DEFINITIONS
# ============================================================

# GROUP 1: Label 0 (Clean) - Model nhầm là Toxic
LABEL_0_KEYWORDS = {
    'narrative_context': {
        'keywords': ['official poster', 'visualizer mv', 'visualizer', 'official music video', 
                    'người thứ 3', 'tập ', 'youtube', 'facebook', 'instagram', 'tiktok', 
                    'threads', 'tiktok music'],
        'weight': 1.0
    },
    'news_reporting': {
        'keywords': ['nghe báo đài', 'cận cảnh', 'bất chấp lệnh cấm', 'xử phạt rồi', 
                    'cập nhật thông tin', 'tin tức', 'thông báo'],
        'weight': 1.0
    },
    'positive_slang': {
        'keywords': ['chất vl', 'hay vl', 'đẹp vl', 'ngon vl', 'xịn vl', 'pro vl', 
                    'peak vcl', 'đỉnh', 'khét lẹt', 'cháy'],
        'weight': 1.5  # Higher weight - critical pattern
    }
}

# GROUP 2: Label 1 (Toxic) - Model nhầm là Clean hoặc Hate
LABEL_1_KEYWORDS = {
    'sarcasm_fame': {
        'keywords': ['chúa tể bú fame', 'bú fame', 'diễn lố', 'làm trò', 'khẹc', 
                    'như khẹc', 'diễn sâu'],
        'weight': 1.0
    },
    'intelligence_attack': {
        'keywords': ['ngoo', 'ngoo hết cứu', 'não tàn', 'óc', 'hãm', 'ngu', 
                    'đần', 'ngớ ngẩn'],
        'weight': 1.2
    },
    'frustration': {
        'keywords': ['cay vl', 'dắt như chó', 'vô vị', 'tởm', 'ghê', 'kinh'],
        'weight': 1.0
    },
    'pronoun_attack': {
        'keywords': ['thằng này', 'con này', 'lũ này', 'bọn này', 'mày', 'mi'],
        'weight': 1.3  # Important pattern
    }
}

# GROUP 3: Label 2 (Hate) - Model bỏ sót
LABEL_2_KEYWORDS = {
    'regional_discrimination': {
        'keywords': ['parky', 'pắc kỳ', 'bắc kỳ', 'nam kỳ', 'cali', 'vùng lũ', 
                    'miền bắc', 'miền nam', 'miền trung'],
        'weight': 2.0  # Critical - must catch
    },
    'lgbt_discrimination': {
        'keywords': ['bọn đồng tính', 'tém tém lại', 'bê đê', 'bóng', 'vô loài', 
                    'lgbt', 'đồng tính'],
        'weight': 2.0  # Critical
    },
    'dehumanization': {
        'keywords': ['súc vật', 'con chó', 'con lợn', 'con heo', 'vô loài', 
                    'ngắm gà khỏa thân', 'thú vật'],
        'weight': 2.0  # Critical
    },
    'violence_wish': {
        'keywords': ['ngắm gà khỏa thân', 'đầu thai', 'tông vào trụ cột', 'tử hình đi', 
                    'chết đi', 'giết đi'],
        'weight': 2.0  # Critical
    }
}

# ============================================================
# FILTERING FUNCTIONS
# ============================================================

def calculate_score(text, keyword_groups):
    """Calculate relevance score based on keyword groups"""
    text_lower = text.lower()
    total_score = 0
    matched_groups = []
    
    for group_name, group_info in keyword_groups.items():
        keywords = group_info['keywords']
        weight = group_info['weight']
        
        # Count matches
        matches = sum(1 for kw in keywords if kw in text_lower)
        if matches > 0:
            total_score += matches * weight
            matched_groups.append(group_name)
    
    return total_score, matched_groups

def is_duplicate(text, train_texts):
    """Check if text is duplicate with training set"""
    text_clean = text.lower().strip()
    return text_clean in train_texts

def filter_samples(df, train_texts, keyword_groups, target_label, target_count):
    """Filter samples for a specific label"""
    candidates = []
    
    for idx, row in df.iterrows():
        # Get text - use input_text column
        if 'input_text' in row and pd.notna(row['input_text']):
            text = str(row['input_text'])
        elif 'raw_comment' in row and pd.notna(row['raw_comment']):
            # Combine title and comment
            title = str(row.get('raw_title', '')) if pd.notna(row.get('raw_title')) else ''
            comment = str(row['raw_comment'])
            text = f"{title} </s> {comment}" if title else comment
        else:
            continue
        
        # Skip if duplicate
        if is_duplicate(text, train_texts):
            continue
        
        # Calculate score
        score, matched_groups = calculate_score(text, keyword_groups)
        
        if score > 0:
            # Get raw data
            raw_comment = row.get('raw_comment', row.get('cleaned_comment', ''))
            raw_title = row.get('raw_title', row.get('cleaned_title', ''))
            
            candidates.append({
                'text': text,
                'raw_comment': raw_comment if pd.notna(raw_comment) else '',
                'raw_title': raw_title if pd.notna(raw_title) else '',
                'score': score,
                'matched_groups': ', '.join(matched_groups),
                'suggested_label': target_label,
                'confidence': 'HIGH' if score >= 2.0 else 'MEDIUM',
                'source': 'unlabeled_strategic_filter'
            })
    
    # Sort by score and take top N
    candidates_df = pd.DataFrame(candidates)
    if len(candidates_df) > 0:
        candidates_df = candidates_df.sort_values('score', ascending=False)
        candidates_df = candidates_df.head(target_count)
    
    return candidates_df

# ============================================================
# FILTER SAMPLES FOR EACH LABEL
# ============================================================

print("\n" + "="*80)
print("🔍 FILTERING SAMPLES")
print("="*80)

# Label 0: 400 samples (40%)
print("\n📌 GROUP 1: Label 0 (Clean) - Narrative/Positive Slang")
label_0_samples = filter_samples(unlabeled_df, train_texts, LABEL_0_KEYWORDS, 0, 400)
print(f"   Found: {len(label_0_samples)} samples")
if len(label_0_samples) > 0:
    print(f"   Top patterns: {label_0_samples['matched_groups'].value_counts().head(3).to_dict()}")

# Label 1: 400 samples (40%)
print("\n📌 GROUP 2: Label 1 (Toxic) - Sarcasm/Attack")
label_1_samples = filter_samples(unlabeled_df, train_texts, LABEL_1_KEYWORDS, 1, 400)
print(f"   Found: {len(label_1_samples)} samples")
if len(label_1_samples) > 0:
    print(f"   Top patterns: {label_1_samples['matched_groups'].value_counts().head(3).to_dict()}")

# Label 2: 200 samples (20%)
print("\n📌 GROUP 3: Label 2 (Hate) - Discrimination/Violence")
label_2_samples = filter_samples(unlabeled_df, train_texts, LABEL_2_KEYWORDS, 2, 200)
print(f"   Found: {len(label_2_samples)} samples")
if len(label_2_samples) > 0:
    print(f"   Top patterns: {label_2_samples['matched_groups'].value_counts().head(3).to_dict()}")

# ============================================================
# COMBINE AND PROCESS
# ============================================================

print("\n" + "="*80)
print("📦 COMBINING SAMPLES")
print("="*80)

# Combine all
all_samples = pd.concat([label_0_samples, label_1_samples, label_2_samples], ignore_index=True)

print(f"\n📊 TOTAL FILTERED: {len(all_samples)} samples")

if len(all_samples) == 0:
    print("\n⚠️ NO SAMPLES FOUND!")
    print("   Possible reasons:")
    print("   1. All samples are duplicates with training data")
    print("   2. Keywords not found in unlabeled data")
    print("   3. Need to adjust keyword patterns")
    exit(0)

print(f"   Label 0: {len(label_0_samples)} ({len(label_0_samples)/len(all_samples)*100:.1f}%)")
print(f"   Label 1: {len(label_1_samples)} ({len(label_1_samples)/len(all_samples)*100:.1f}%)")
print(f"   Label 2: {len(label_2_samples)} ({len(label_2_samples)/len(all_samples)*100:.1f}%)")

# Use raw text for now (will process later during merge)
print("\n🔧 Preparing data...")

all_samples['training_text'] = all_samples['text']  # Will be processed during merge
all_samples['text_raw'] = all_samples['text']

# Add metadata
all_samples['note'] = 'Strategic filter - ' + all_samples['matched_groups']
all_samples['source_file'] = 'filter_strategic_samples'
all_samples['labeler'] = 'auto_strategic'
all_samples['has_teencode'] = True
all_samples['sampling_strategy'] = 'strategic_keyword_filter'

# Rename columns
all_samples = all_samples.rename(columns={'suggested_label': 'label'})

# Reorder columns
columns_order = ['training_text', 'text_raw', 'label', 'confidence', 'matched_groups', 
                'note', 'source_file', 'labeler', 'has_teencode', 'sampling_strategy']
all_samples = all_samples[columns_order]

# ============================================================
# SAVE RESULTS
# ============================================================

print("\n" + "="*80)
print("💾 SAVING RESULTS")
print("="*80)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save all
output_csv = f'STRATEGIC_SAMPLES_FOR_REVIEW_{timestamp}.csv'
output_xlsx = f'STRATEGIC_SAMPLES_FOR_REVIEW_{timestamp}.xlsx'

all_samples.to_csv(output_csv, index=False, encoding='utf-8-sig')
all_samples.to_excel(output_xlsx, index=False)

print(f"✅ Saved: {output_csv}")
print(f"✅ Saved: {output_xlsx}")

# Save by label
for label in [0, 1, 2]:
    label_df = all_samples[all_samples['label'] == label]
    if len(label_df) > 0:
        label_file = f'STRATEGIC_SAMPLES_LABEL_{label}_{timestamp}.xlsx'
        label_df.to_excel(label_file, index=False)
        print(f"✅ Saved: {label_file}")

# ============================================================
# SHOW SAMPLES
# ============================================================

print("\n" + "="*80)
print("📋 SAMPLE PREVIEW")
print("="*80)

for label in [0, 1, 2]:
    label_df = all_samples[all_samples['label'] == label]
    if len(label_df) > 0:
        print(f"\n{'='*80}")
        print(f"LABEL {label} - Top 5 samples:")
        print(f"{'='*80}")
        for i, row in label_df.head(5).iterrows():
            print(f"\n{i+1}. [{row['confidence']}] {row['matched_groups']}")
            print(f"   {row['training_text'][:150]}...")

# ============================================================
# STATISTICS
# ============================================================

print("\n" + "="*80)
print("📊 DETAILED STATISTICS")
print("="*80)

print(f"\n🎯 CONFIDENCE DISTRIBUTION:")
for conf in ['HIGH', 'MEDIUM']:
    count = len(all_samples[all_samples['confidence'] == conf])
    print(f"   {conf}: {count} ({count/len(all_samples)*100:.1f}%)")

print(f"\n🎯 TOP MATCHED PATTERNS:")
pattern_counts = all_samples['matched_groups'].value_counts().head(10)
for pattern, count in pattern_counts.items():
    print(f"   {pattern}: {count}")

print("\n" + "="*80)
print("✅ FILTERING COMPLETE!")
print("="*80)

print(f"""
📋 NEXT STEPS:

1. REVIEW FILE: {output_xlsx}
   - Check Label 0: Có đúng là Clean không?
   - Check Label 1: Có đúng là Toxic không?
   - Check Label 2: Có đúng là Hate không?

2. FIX LABELS (nếu cần):
   - Sửa trực tiếp trong Excel
   - Lưu lại với tên mới

3. MERGE VÀO TRAINING DATA:
   python merge_augmented_data.py

4. RETRAIN MODEL:
   - Upload lên Colab
   - Train với data mới
   - Expected: F1 > 0.72

🎯 TARGET:
   - Current errors: 191 cases
   - After augmentation: <150 cases
   - F1: 0.68 → 0.72+
""")
