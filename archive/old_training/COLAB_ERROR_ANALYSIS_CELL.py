"""
═══════════════════════════════════════════════════════════════════════════════
COPY TOÀN BỘ CODE DƯỚI ĐÂY VÀO 1 CELL MỚI TRONG COLAB
Chạy ngay sau khi train xong để phân tích lỗi
═══════════════════════════════════════════════════════════════════════════════
"""

import pandas as pd

def analyze_errors(val_texts, val_labels, val_preds, save_path='/content/drive/MyDrive/'):
    """Phân tích và export lỗi model"""
    
    # Tạo DataFrame
    df = pd.DataFrame({
        'text': val_texts,
        'true_label': val_labels,
        'pred_label': val_preds,
        'is_error': [t != p for t, p in zip(val_labels, val_preds)]
    })
    
    df['error_type'] = df.apply(
        lambda x: f"{x['true_label']}→{x['pred_label']}" if x['is_error'] else 'Correct',
        axis=1
    )
    
    # Tách title/comment
    df['title'] = df['text'].apply(lambda x: x.split('</s>')[0].strip() if '</s>' in x else '')
    df['comment'] = df['text'].apply(lambda x: x.split('</s>')[1].strip() if '</s>' in x else x)
    
    # Stats
    total = len(df)
    errors = df['is_error'].sum()
    
    print("="*80)
    print("🔍 PHÂN TÍCH LỖI MODEL")
    print("="*80)
    print(f"\n📊 Total: {total} | ✅ Correct: {total-errors} ({(1-errors/total)*100:.1f}%) | ❌ Errors: {errors} ({errors/total*100:.1f}%)")
    
    if errors == 0:
        print("\n🎉 Perfect! No errors!")
        return
    
    # Error breakdown
    print(f"\n📊 PHÂN LOẠI LỖI:")
    error_counts = df[df['is_error']]['error_type'].value_counts()
    for et, cnt in error_counts.items():
        print(f"   {et}: {cnt} ({cnt/errors*100:.1f}%)")
    
    # Pattern detection
    print(f"\n🔍 PATTERNS:")
    for et in error_counts.index:
        edf = df[df['error_type'] == et]
        print(f"\n   {et} ({len(edf)} cases):")
        
        patterns = {
            'vcl/vl': sum(1 for t in edf['text'] if any(w in t.lower() for w in ['vcl', 'vl', 'vãi'])),
            'nặng': sum(1 for t in edf['text'] if any(w in t.lower() for w in ['nặng khung', 'mv nặng', 'lag'])),
            'justice': sum(1 for t in edf['text'] if any(w in t.lower() for w in ['pháp luật', 'tù', 'phạt'])),
            'family': sum(1 for t in edf['text'] if any(w in t.lower() for w in ['chết mẹ', 'đụ mẹ', 'địt mẹ'])),
            'animal': sum(1 for t in edf['text'] if any(w in t.lower() for w in ['con chó', 'thằng chó', 'lợn'])),
            'violence': sum(1 for t in edf['text'] if any(w in t.lower() for w in ['đánh', 'đập', 'giết', 'chém'])),
        }
        
        for pname, pcnt in patterns.items():
            if pcnt > 0:
                print(f"      • {pname}: {pcnt} ({pcnt/len(edf)*100:.0f}%)")
    
    # Save files
    print(f"\n💾 SAVING TO: {save_path}")
    
    errors_df = df[df['is_error']][['error_type', 'true_label', 'pred_label', 'title', 'comment', 'text']]
    errors_df = errors_df.sort_values(['error_type', 'true_label'])
    
    # All errors
    errors_df.to_excel(save_path + 'MODEL_ERRORS_ALL.xlsx', index=False)
    print(f"   ✅ MODEL_ERRORS_ALL.xlsx")
    
    # By type
    for et in error_counts.index:
        edf = df[df['error_type'] == et][['true_label', 'pred_label', 'title', 'comment', 'text']]
        edf.to_excel(save_path + f'MODEL_ERRORS_{et.replace("→", "_to_")}.xlsx', index=False)
        print(f"   ✅ MODEL_ERRORS_{et.replace("→", "_to_")}.xlsx")
    
    # Summary
    summary = pd.DataFrame([
        {
            'Error Type': et,
            'Count': cnt,
            'Percentage': f"{cnt/errors*100:.1f}%"
        }
        for et, cnt in error_counts.items()
    ])
    summary.to_excel(save_path + 'MODEL_ERRORS_SUMMARY.xlsx', index=False)
    print(f"   ✅ MODEL_ERRORS_SUMMARY.xlsx")
    
    # Show samples
    print(f"\n📋 SAMPLE ERRORS (first 5):")
    print("-" * 80)
    for _, row in errors_df.head(5).iterrows():
        print(f"\n{row['error_type']} | True: {row['true_label']} → Pred: {row['pred_label']}")
        print(f"{row['text'][:120]}...")
    
    print("\n" + "="*80)
    print("✅ DONE!")
    print("="*80)
    
    return errors_df, summary

# ═══════════════════════════════════════════════════════════════════════════════
# CHẠY LỆNH NÀY SAU KHI TRAIN XONG:
# ═══════════════════════════════════════════════════════════════════════════════

# errors_df, summary = analyze_errors(val_texts, val_labels, val_preds)

# Xem chi tiết lỗi 0→1:
# print(errors_df[errors_df['error_type'] == '0→1'][['title', 'comment']].head(10))
