"""
COPY SCRIPT NÀY VÀO 1 CELL MỚI TRONG COLAB
Chạy ngay sau khi train xong để xem model đoán sai
"""

import pandas as pd
import numpy as np
from collections import Counter

# ============================================================
# PHÂN TÍCH LỖI - CHẠY SAU KHI TRAIN XONG
# ============================================================

def analyze_and_export_errors(val_texts, val_labels, val_preds, save_path='/content/drive/MyDrive/'):
    """
    Phân tích và export lỗi dự đoán
    
    Args:
        val_texts: List validation texts từ training
        val_labels: List true labels từ training  
        val_preds: List predicted labels từ training
        save_path: Đường dẫn lưu file (Google Drive)
    """
    
    print("="*80)
    print("🔍 PHÂN TÍCH LỖI DỰ ĐOÁN CỦA MODEL")
    print("="*80)
    
    # Tạo DataFrame
    df = pd.DataFrame({
        'text': val_texts,
        'true_label': val_labels,
        'pred_label': val_preds
    })
    
    # Đánh dấu lỗi
    df['is_error'] = df['true_label'] != df['pred_label']
    df['error_type'] = df.apply(
        lambda x: f"{x['true_label']}→{x['pred_label']}" if x['is_error'] else 'Correct',
        axis=1
    )
    
    # Tách title và comment
    df['title'] = df['text'].apply(lambda x: x.split('</s>')[0].strip() if '</s>' in x else '')
    df['comment'] = df['text'].apply(lambda x: x.split('</s>')[1].strip() if '</s>' in x else x)
    
    # Thống kê
    total = len(df)
    errors = df['is_error'].sum()
    correct = total - errors
    
    print(f"\n📊 TỔNG QUAN:")
    print(f"   Total samples: {total}")
    print(f"   ✅ Correct: {correct} ({correct/total*100:.1f}%)")
    print(f"   ❌ Errors: {errors} ({errors/total*100:.1f}%)")
    
    if errors == 0:
        print("\n🎉 Model hoàn hảo! Không có lỗi nào!")
        return
    
    # Phân loại lỗi
    print(f"\n📊 PHÂN LOẠI LỖI:")
    error_counts = df[df['is_error']]['error_type'].value_counts()
    for error_type, count in error_counts.items():
        print(f"   {error_type}: {count} ({count/errors*100:.1f}%)")
    
    # Phát hiện patterns cho từng loại lỗi
    print(f"\n🔍 PHÂN TÍCH PATTERNS:")
    
    for error_type in error_counts.index:
        error_df = df[df['error_type'] == error_type]
        print(f"\n   📌 {error_type} ({len(error_df)} cases):")
        
        # Detect patterns
        patterns = {
            'vcl/vl positive': 0,
            'technical nặng': 0,
            'justice call': 0,
            'mv description': 0,
            'family attack': 0,
            'animal words': 0,
            'violence call': 0,
            'long title (>50 words)': 0
        }
        
        for text in error_df['text']:
            text_lower = text.lower()
            
            if any(w in text_lower for w in ['vcl', 'vl', 'vãi', 'chất vl', 'hay vl', 'đẹp vl']):
                patterns['vcl/vl positive'] += 1
            if any(w in text_lower for w in ['nặng khung', 'mv nặng', 'video nặng', 'lag', 'render']):
                patterns['technical nặng'] += 1
            if any(w in text_lower for w in ['pháp luật', 'luật', 'tù', 'giam', 'bắt', 'phạt']):
                patterns['justice call'] += 1
            if any(w in text_lower for w in ['official', 'visualizer', 'lyrics', 'mv', 'music video']):
                patterns['mv description'] += 1
            if any(w in text_lower for w in ['chết mẹ', 'đụ mẹ', 'địt mẹ', 'con mẹ', 'im mẹ']):
                patterns['family attack'] += 1
            if any(w in text_lower for w in ['con chó', 'thằng chó', 'con lợn', 'con heo', 'súc vật']):
                patterns['animal words'] += 1
            if any(w in text_lower for w in ['đánh', 'đập', 'giết', 'chém', 'tát', 'bạo hành']):
                patterns['violence call'] += 1
            
            # Check long title
            if '</s>' in text:
                title = text.split('</s>')[0]
                if len(title.split()) > 50:
                    patterns['long title (>50 words)'] += 1
        
        # Print patterns
        for pattern_name, count in patterns.items():
            if count > 0:
                print(f"      • {pattern_name}: {count} ({count/len(error_df)*100:.0f}%)")
    
    # Lưu files
    print(f"\n💾 ĐANG LƯU FILES VÀO: {save_path}")
    
    # 1. All errors
    errors_df = df[df['is_error']].copy()
    errors_df = errors_df[['error_type', 'true_label', 'pred_label', 'title', 'comment', 'text']]
    errors_df = errors_df.sort_values(['error_type', 'true_label'])
    
    all_errors_file = save_path + 'MODEL_ERRORS_ALL.xlsx'
    errors_df.to_excel(all_errors_file, index=False)
    print(f"   ✅ {all_errors_file}")
    
    # 2. By error type
    for error_type in error_counts.index:
        error_df = df[df['error_type'] == error_type].copy()
        error_df = error_df[['true_label', 'pred_label', 'title', 'comment', 'text']]
        
        filename = save_path + f'MODEL_ERRORS_{error_type.replace("→", "_to_")}.xlsx'
        error_df.to_excel(filename, index=False)
        print(f"   ✅ {filename}")
    
    # 3. Summary
    summary_data = []
    for error_type in error_counts.index:
        error_df = df[df['error_type'] == error_type]
        
        # Count patterns
        vcl_count = sum(1 for t in error_df['text'] if any(w in t.lower() for w in ['vcl', 'vl', 'vãi']))
        nang_count = sum(1 for t in error_df['text'] if any(w in t.lower() for w in ['nặng khung', 'mv nặng', 'lag']))
        justice_count = sum(1 for t in error_df['text'] if any(w in t.lower() for w in ['pháp luật', 'tù', 'phạt']))
        
        top_patterns = []
        if vcl_count > 0:
            top_patterns.append(f"vcl/vl({vcl_count})")
        if nang_count > 0:
            top_patterns.append(f"nặng({nang_count})")
        if justice_count > 0:
            top_patterns.append(f"justice({justice_count})")
        
        summary_data.append({
            'Error Type': error_type,
            'Count': len(error_df),
            'Percentage': f"{len(error_df)/errors*100:.1f}%",
            'Top Patterns': ', '.join(top_patterns) if top_patterns else 'N/A'
        })
    
    summary_df = pd.DataFrame(summary_data)
    summary_file = save_path + 'MODEL_ERRORS_SUMMARY.xlsx'
    summary_df.to_excel(summary_file, index=False)
    print(f"   ✅ {summary_file}")
    
    # Show sample errors
    print(f"\n📋 MẪU LỖI (5 mẫu đầu tiên):")
    print("-" * 80)
    for idx, row in errors_df.head(5).iterrows():
        print(f"\n{row['error_type']} | True: {row['true_label']} → Pred: {row['pred_label']}")
        print(f"Text: {row['text'][:150]}...")
    
    print("\n" + "="*80)
    print("✅ PHÂN TÍCH HOÀN TẤT!")
    print("="*80)
    print(f"\n📁 Đã tạo {len(error_counts) + 2} files:")
    print(f"   • MODEL_ERRORS_ALL.xlsx - Tất cả lỗi")
    print(f"   • MODEL_ERRORS_[type].xlsx - Lỗi theo từng loại")
    print(f"   • MODEL_ERRORS_SUMMARY.xlsx - Tóm tắt")
    
    return errors_df, summary_df


# ============================================================
# CÁCH SỬ DỤNG
# ============================================================
"""
📝 SAU KHI TRAIN XONG, CHẠY LỆNH NÀY:

# Phân tích lỗi
errors_df, summary_df = analyze_and_export_errors(
    val_texts, 
    val_labels, 
    val_preds,
    save_path='/content/drive/MyDrive/'
)

# Xem summary
print(summary_df)

# Xem chi tiết lỗi 0→1
errors_0_to_1 = errors_df[errors_df['error_type'] == '0→1']
print(f"\\nLỗi 0→1: {len(errors_0_to_1)} cases")
print(errors_0_to_1[['title', 'comment']].head(10))
"""

# ============================================================
# QUICK TEST (nếu muốn test ngay)
# ============================================================
if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*80)
    print("📝 HƯỚNG DẪN SỬ DỤNG")
    print("="*80)
    print("""
1. Copy toàn bộ script này vào 1 cell mới trong Colab

2. Sau khi train xong (có val_texts, val_labels, val_preds), chạy:

   errors_df, summary_df = analyze_and_export_errors(
       val_texts, 
       val_labels, 
       val_preds,
       save_path='/content/drive/MyDrive/'
   )

3. Xem kết quả:
   
   # Xem tóm tắt
   print(summary_df)
   
   # Xem lỗi cụ thể
   print(errors_df[errors_df['error_type'] == '0→1'].head())

4. Files sẽ được lưu vào Google Drive của bạn
    """)
