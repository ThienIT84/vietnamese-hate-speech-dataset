"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔬 KAGGLE: Deep Error Analysis với Pattern Detection                       ║
║  Phân tích sâu các lỗi của model và tìm pattern                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CELL: Deep Error Analysis với Keyword Detection
# ═══════════════════════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import re
from datetime import datetime
from collections import Counter

print("="*80)
print("🔬 DEEP ERROR ANALYSIS")
print("="*80)

# Kiểm tra xem val_texts có tồn tại không
if 'val_texts' not in globals():
    print("⚠️ val_texts not found. Recreating from validation dataset...")
    val_texts = [val_dataset.texts[i] for i in range(len(val_dataset))]
    print(f"✅ Recreated val_texts: {len(val_texts)} samples")

# Định nghĩa các keyword patterns (từ guideline)
KEYWORD_PATTERNS = {
    'Label_0_Keywords': {
        'narrative_context': ['youtube', 'facebook', 'instagram', 'tiktok', 'mv', 'official', 'visualizer', 'poster'],
        'positive_slang': ['vcl', 'vl', 'vđ', 'khét lẹt', 'đỉnh', 'cháy'],
        'news_context': ['nghe báo đài', 'cận cảnh', 'bất chấp', 'xử phạt', 'cập nhật']
    },
    'Label_1_Keywords': {
        'sarcasm': ['bú fame', 'diễn lố', 'làm trò', 'khẹc'],
        'intelligence_attack': ['ngoo', 'não tàn', 'óc', 'hãm'],
        'complaint': ['cay vl', 'dắt như chó', 'vô vị', 'tởm'],
        'derogatory_pronouns': ['thằng này', 'con này', 'lũ này']
    },
    'Label_2_Keywords': {
        'regional_discrimination': ['parky', 'pắc kỳ', 'bắc kỳ', 'nam kỳ', 'cali', 'vùng lũ'],
        'lgbt_discrimination': ['bọn này', 'bọn đồng tính', 'tém tém', 'bê đê', 'bóng', 'vô loài'],
        'dehumanization': ['súc vật', 'chó', 'lợn', 'ngắm gà khỏa thân'],
        'violence_incitement': ['đầu thai', 'tông vào trụ', 'tử hình']
    }
}

def detect_keywords(text, keyword_dict):
    """Phát hiện keywords trong text"""
    text_lower = text.lower()
    detected = {}
    for category, keywords in keyword_dict.items():
        found = [kw for kw in keywords if kw in text_lower]
        if found:
            detected[category] = found
    return detected

def analyze_error_patterns(df_errors):
    """Phân tích patterns trong các lỗi"""
    
    results = []
    
    for idx, row in df_errors.iterrows():
        text = str(row['text'])
        true_label = int(row['true_label'])
        pred_label = int(row['pred_label'])
        
        # Detect keywords
        true_keywords = detect_keywords(text, KEYWORD_PATTERNS.get(f'Label_{true_label}_Keywords', {}))
        pred_keywords = detect_keywords(text, KEYWORD_PATTERNS.get(f'Label_{pred_label}_Keywords', {}))
        
        # Text features
        has_caps = any(c.isupper() for c in text)
        has_repeat_chars = bool(re.search(r'(.)\1{2,}', text))
        has_emoji = bool(re.search(r'[😀-🙏🌀-🗿🚀-🛿]', text))
        
        results.append({
            'id': row['id'],
            'text': text,
            'error_type': row['error_type'],
            'true_label': true_label,
            'pred_label': pred_label,
            'confidence': row['max_confidence'],
            'text_length': row['text_length'],
            'has_caps': has_caps,
            'has_repeat_chars': has_repeat_chars,
            'has_emoji': has_emoji,
            'true_keywords_found': str(true_keywords) if true_keywords else 'None',
            'pred_keywords_found': str(pred_keywords) if pred_keywords else 'None',
            'keyword_conflict': 'Yes' if (true_keywords and pred_keywords) else 'No'
        })
    
    return pd.DataFrame(results)

# Tạo error DataFrame
label_names = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}

error_data = []
for i, (text, true_label, pred_label, probs) in enumerate(zip(val_texts, final_true, final_preds, final_probs)):
    if true_label != pred_label:
        error_data.append({
            'id': i + 1,
            'text': text,
            'true_label': int(true_label),
            'pred_label': int(pred_label),
            'error_type': f"{int(true_label)}→{int(pred_label)}",
            'max_confidence': float(probs.max()),
            'text_length': len(str(text).split())
        })

df_errors = pd.DataFrame(error_data)

print(f"\n📊 Analyzing {len(df_errors)} errors...")

# Phân tích patterns
df_analysis = analyze_error_patterns(df_errors)

# Statistics
print(f"\n📊 ERROR PATTERN STATISTICS:")
print(f"   Errors with CAPS: {df_analysis['has_caps'].sum()} ({df_analysis['has_caps'].sum()/len(df_analysis)*100:.1f}%)")
print(f"   Errors with repeated chars: {df_analysis['has_repeat_chars'].sum()} ({df_analysis['has_repeat_chars'].sum()/len(df_analysis)*100:.1f}%)")
print(f"   Errors with emoji: {df_analysis['has_emoji'].sum()} ({df_analysis['has_emoji'].sum()/len(df_analysis)*100:.1f}%)")
print(f"   Errors with keyword conflicts: {(df_analysis['keyword_conflict'] == 'Yes').sum()}")

# Phân tích theo error type
print(f"\n📊 ERRORS BY TYPE:")
for error_type in df_analysis['error_type'].value_counts().index:
    subset = df_analysis[df_analysis['error_type'] == error_type]
    avg_conf = subset['confidence'].mean()
    avg_len = subset['text_length'].mean()
    print(f"\n   {error_type}:")
    print(f"      Count: {len(subset)}")
    print(f"      Avg Confidence: {avg_conf:.2%}")
    print(f"      Avg Text Length: {avg_len:.1f} words")

# Export to Excel
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'/kaggle/working/deep_error_analysis_{timestamp}.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Sheet 1: Full analysis
    df_analysis.to_excel(writer, sheet_name='Full_Analysis', index=False)
    
    # Sheet 2: High confidence errors (>80%)
    high_conf = df_analysis[df_analysis['confidence'] > 0.8].sort_values('confidence', ascending=False)
    high_conf.to_excel(writer, sheet_name='High_Confidence_Errors', index=False)
    
    # Sheet 3: Keyword conflicts
    conflicts = df_analysis[df_analysis['keyword_conflict'] == 'Yes']
    conflicts.to_excel(writer, sheet_name='Keyword_Conflicts', index=False)
    
    # Sheet 4: By error type
    for error_type in df_analysis['error_type'].unique():
        sheet_name = f"Type_{error_type.replace('→', '_to_')}"
        subset = df_analysis[df_analysis['error_type'] == error_type]
        subset.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\n💾 EXPORTED:")
print(f"   File: {output_file}")
print(f"   Sheets: Full_Analysis, High_Confidence_Errors, Keyword_Conflicts, + error types")

# Hiển thị top errors với keywords
print(f"\n🔥 TOP 10 ERRORS WITH KEYWORD ANALYSIS:")
print("="*80)
for idx, row in df_analysis.head(10).iterrows():
    print(f"\n{row['id']}. [{row['error_type']}] Confidence: {row['confidence']:.2%}")
    print(f"   Text: {row['text'][:80]}...")
    print(f"   True keywords: {row['true_keywords_found']}")
    print(f"   Pred keywords: {row['pred_keywords_found']}")

print("\n" + "="*80)
print("✅ DEEP ANALYSIS COMPLETE!")
print("="*80)
print(f"\n📥 Download: {output_file}")
