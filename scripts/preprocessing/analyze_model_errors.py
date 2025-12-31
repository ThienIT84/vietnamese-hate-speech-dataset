"""
Analyze model prediction errors from validation set
Extract all misclassified samples for further analysis
"""
import pandas as pd
import numpy as np
from collections import Counter
import re

def load_predictions(val_texts, val_labels, val_preds):
    """
    Load validation predictions from training script
    
    Usage in Colab after training:
    >>> analyze_errors(val_texts, val_labels, val_preds)
    """
    df = pd.DataFrame({
        'text': val_texts,
        'true_label': val_labels,
        'pred_label': val_preds
    })
    
    # Mark errors
    df['is_error'] = df['true_label'] != df['pred_label']
    df['error_type'] = df.apply(lambda x: f"{x['true_label']}→{x['pred_label']}" if x['is_error'] else 'Correct', axis=1)
    
    return df

def analyze_errors(val_texts, val_labels, val_preds, output_path='/content/drive/MyDrive/'):
    """
    Main analysis function - call this after training
    
    Args:
        val_texts: List of validation texts
        val_labels: List of true labels
        val_preds: List of predicted labels
        output_path: Where to save results (Google Drive path)
    """
    print("="*80)
    print("🔍 PHÂN TÍCH LỖI DỰ ĐOÁN CỦA MODEL")
    print("="*80)
    
    df = load_predictions(val_texts, val_labels, val_preds)
    
    # Overall stats
    total = len(df)
    errors = df['is_error'].sum()
    accuracy = (total - errors) / total
    
    print(f"\n📊 TỔNG QUAN:")
    print(f"   Total samples: {total}")
    print(f"   Correct: {total - errors} ({(1-errors/total)*100:.1f}%)")
    print(f"   Errors: {errors} ({errors/total*100:.1f}%)")
    
    # Error breakdown by type
    print(f"\n📊 PHÂN LOẠI LỖI:")
    error_counts = df[df['is_error']]['error_type'].value_counts()
    for error_type, count in error_counts.items():
        print(f"   {error_type}: {count} ({count/errors*100:.1f}%)")
    
    # Analyze each error type
    error_analysis = {}
    
    for error_type in error_counts.index:
        error_df = df[df['error_type'] == error_type].copy()
        
        print(f"\n{'='*80}")
        print(f"🔍 PHÂN TÍCH LỖI: {error_type}")
        print(f"{'='*80}")
        print(f"Số lượng: {len(error_df)}")
        
        # Pattern detection
        patterns = detect_patterns(error_df['text'].tolist())
        
        print(f"\n🔎 CÁC PATTERN PHÁT HIỆN:")
        for pattern_name, pattern_info in patterns.items():
            if pattern_info['count'] > 0:
                print(f"   {pattern_name}: {pattern_info['count']} ({pattern_info['count']/len(error_df)*100:.1f}%)")
                print(f"      Keywords: {', '.join(pattern_info['keywords'][:5])}")
        
        error_analysis[error_type] = {
            'count': len(error_df),
            'patterns': patterns,
            'samples': error_df
        }
    
    # Save detailed error reports
    print(f"\n{'='*80}")
    print("💾 LƯU BÁO CÁO CHI TIẾT")
    print(f"{'='*80}")
    
    # 1. All errors in one file
    errors_df = df[df['is_error']].copy()
    errors_df = errors_df.sort_values('error_type')
    
    all_errors_file = output_path + 'MODEL_ERRORS_ALL.xlsx'
    errors_df.to_excel(all_errors_file, index=False)
    print(f"✅ Saved: {all_errors_file}")
    
    # 2. Separate file for each error type
    for error_type in error_counts.index:
        error_df = df[df['error_type'] == error_type].copy()
        
        # Add pattern flags
        for pattern_name, pattern_info in error_analysis[error_type]['patterns'].items():
            if pattern_info['count'] > 0:
                error_df[f'has_{pattern_name}'] = error_df['text'].apply(
                    lambda x: any(kw in x.lower() for kw in pattern_info['keywords'])
                )
        
        filename = output_path + f'MODEL_ERRORS_{error_type.replace("→", "_to_")}.xlsx'
        error_df.to_excel(filename, index=False)
        print(f"✅ Saved: {filename}")
    
    # 3. Summary report
    summary = []
    for error_type, analysis in error_analysis.items():
        summary.append({
            'error_type': error_type,
            'count': analysis['count'],
            'percentage': f"{analysis['count']/errors*100:.1f}%",
            'top_patterns': ', '.join([k for k, v in analysis['patterns'].items() if v['count'] > 0][:3])
        })
    
    summary_df = pd.DataFrame(summary)
    summary_file = output_path + 'MODEL_ERRORS_SUMMARY.xlsx'
    summary_df.to_excel(summary_file, index=False)
    print(f"✅ Saved: {summary_file}")
    
    print(f"\n{'='*80}")
    print("✅ PHÂN TÍCH HOÀN TẤT!")
    print(f"{'='*80}")
    print(f"\n📁 Các file đã tạo:")
    print(f"   1. MODEL_ERRORS_ALL.xlsx - Tất cả lỗi")
    print(f"   2. MODEL_ERRORS_[type].xlsx - Lỗi theo từng loại")
    print(f"   3. MODEL_ERRORS_SUMMARY.xlsx - Tóm tắt")
    
    return error_analysis, errors_df

def detect_patterns(texts):
    """Detect common patterns in error texts"""
    patterns = {
        'vcl_vl_positive': {
            'keywords': ['vcl', 'vl', 'vãi', 'chất vl', 'hay vl', 'đẹp vl', 'peak vcl'],
            'count': 0
        },
        'technical_nang': {
            'keywords': ['nặng khung', 'mv nặng', 'video nặng', 'lag', 'render'],
            'count': 0
        },
        'justice_call': {
            'keywords': ['pháp luật', 'luật', 'tù', 'giam', 'bắt', 'phạt', 'xử lý'],
            'count': 0
        },
        'mv_description': {
            'keywords': ['official', 'visualizer', 'lyrics', 'mv', 'music video', 'teaser'],
            'count': 0
        },
        'family_attack': {
            'keywords': ['mẹ', 'ba', 'cha', 'bố', 'má', 'chết mẹ', 'đụ mẹ', 'địt mẹ'],
            'count': 0
        },
        'animal_words': {
            'keywords': ['chó', 'lợn', 'heo', 'bò', 'trâu', 'khỉ', 'vượn', 'súc vật'],
            'count': 0
        },
        'violence_call': {
            'keywords': ['đánh', 'đập', 'giết', 'chém', 'tát', 'bạo hành', 'hành hung'],
            'count': 0
        },
        'sarcasm': {
            'keywords': ['thật', 'quả', 'thực', 'đúng', 'hẳn', 'chắc'],
            'count': 0
        },
        'positive_slang': {
            'keywords': ['xịn', 'chất', 'đỉnh', 'pro', 'ngon', 'hay', 'đẹp', 'tuyệt'],
            'count': 0
        },
        'long_title': {
            'keywords': [],
            'count': 0
        }
    }
    
    for text in texts:
        text_lower = text.lower()
        
        # Check each pattern
        for pattern_name, pattern_info in patterns.items():
            if pattern_name == 'long_title':
                # Check if title (before </s>) is long
                if '</s>' in text:
                    title = text.split('</s>')[0]
                    if len(title.split()) > 50:
                        patterns[pattern_name]['count'] += 1
            else:
                # Check if any keyword matches
                if any(kw in text_lower for kw in pattern_info['keywords']):
                    patterns[pattern_name]['count'] += 1
    
    return patterns

# ============================================================
# USAGE INSTRUCTIONS FOR COLAB
# ============================================================
"""
📝 HƯỚNG DẪN SỬ DỤNG TRONG COLAB:

1. Copy script này vào cell mới trong Colab notebook

2. Sau khi train xong (trong main execution), thêm code này:

   # Analyze errors
   from analyze_model_errors import analyze_errors
   
   error_analysis, errors_df = analyze_errors(
       val_texts, 
       val_labels, 
       val_preds,
       output_path='/content/drive/MyDrive/'
   )

3. Hoặc nếu muốn chạy riêng, load lại model và predict:

   # Load model
   model, tokenizer = load_model("/content/drive/MyDrive/phobert_toxic_model")
   
   # Load data
   df = pd.read_excel("/content/final_train_data_v3_TRUNCATED_20251229.xlsx")
   texts = df['training_text'].tolist()
   labels = df['label'].tolist()
   
   # Predict
   preds, probs = predict(texts, model, tokenizer)
   
   # Analyze
   error_analysis, errors_df = analyze_errors(
       texts, 
       labels, 
       preds,
       output_path='/content/drive/MyDrive/'
   )

4. Kết quả sẽ được lưu vào Google Drive:
   - MODEL_ERRORS_ALL.xlsx: Tất cả lỗi
   - MODEL_ERRORS_0_to_1.xlsx: Lỗi dự đoán 0→1
   - MODEL_ERRORS_0_to_2.xlsx: Lỗi dự đoán 0→2
   - MODEL_ERRORS_1_to_0.xlsx: Lỗi dự đoán 1→0
   - MODEL_ERRORS_1_to_2.xlsx: Lỗi dự đoán 1→2
   - MODEL_ERRORS_2_to_0.xlsx: Lỗi dự đoán 2→0
   - MODEL_ERRORS_2_to_1.xlsx: Lỗi dự đoán 2→1
   - MODEL_ERRORS_SUMMARY.xlsx: Tóm tắt
"""

if __name__ == "__main__":
    print(__doc__)
