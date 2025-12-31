"""
Deep Error Analysis - Phân tích chuyên sâu lỗi model từ góc độ NLP Expert
"""
import pandas as pd
import numpy as np
from collections import Counter
import re

# Load error data
df = pd.read_excel('safesense_error_analysis.xlsx')

print("="*80)
print("🔬 DEEP ERROR ANALYSIS - NLP EXPERT PERSPECTIVE")
print("="*80)

# Add error type
df['error_type'] = df.apply(lambda x: f"{x['True_Label']}→{x['Pred_Label']}", axis=1)

# Split title and comment
df['title'] = df['Text'].apply(lambda x: x.split('</s>')[0].strip() if '</s>' in x else '')
df['comment'] = df['Text'].apply(lambda x: x.split('</s>')[1].strip() if '</s>' in x else x)

print(f"\n📊 TỔNG QUAN:")
print(f"   Total errors: {len(df)}")
print(f"   Error types:")
for et, cnt in df['error_type'].value_counts().items():
    print(f"      {et}: {cnt} ({cnt/len(df)*100:.1f}%)")

# ============================================================
# PHÂN TÍCH CHI TIẾT TỪNG LOẠI LỖI
# ============================================================

print("\n" + "="*80)
print("🔍 PHÂN TÍCH CHI TIẾT TỪNG LOẠI LỖI")
print("="*80)

error_insights = {}

for error_type in df['error_type'].unique():
    edf = df[df['error_type'] == error_type]
    
    print(f"\n{'='*80}")
    print(f"📌 {error_type} ({len(edf)} cases - {len(edf)/len(df)*100:.1f}%)")
    print(f"{'='*80}")
    
    # Pattern detection
    patterns = {
        'vcl_vl_slang': {
            'keywords': ['vcl', 'vl', 'vãi lồn', 'vãi', 'chất vl', 'hay vl', 'đẹp vl', 'peak vcl'],
            'count': 0,
            'samples': []
        },
        'technical_heavy': {
            'keywords': ['nặng khung', 'mv nặng', 'video nặng', 'lag', 'render', 'nặng quá'],
            'count': 0,
            'samples': []
        },
        'justice_support': {
            'keywords': ['pháp luật', 'luật', 'tù', 'giam', 'bắt', 'phạt', 'xử lý', 'trừng phạt'],
            'count': 0,
            'samples': []
        },
        'mv_noise': {
            'keywords': ['official', 'visualizer', 'lyrics', 'mv', 'music video', 'teaser'],
            'count': 0,
            'samples': []
        },
        'family_attack': {
            'keywords': ['chết mẹ', 'đụ mẹ', 'địt mẹ', 'con mẹ', 'im mẹ', 'bỏ mẹ', 'dẹp mẹ'],
            'count': 0,
            'samples': []
        },
        'animal_dehumanize': {
            'keywords': ['con chó', 'thằng chó', 'con lợn', 'con heo', 'súc vật', 'con bò'],
            'count': 0,
            'samples': []
        },
        'violence_call': {
            'keywords': ['đánh', 'đập', 'giết', 'chém', 'tát', 'bạo hành', 'hành hung'],
            'count': 0,
            'samples': []
        },
        'sarcasm_irony': {
            'keywords': ['thật', 'quả', 'thực', 'đúng', 'hẳn', 'chắc'],
            'count': 0,
            'samples': []
        },
        'context_positive': {
            'keywords': ['hay', 'đẹp', 'tuyệt', 'ngon', 'chất', 'đỉnh', 'pro', 'xịn'],
            'count': 0,
            'samples': []
        },
        'ambiguous_pronoun': {
            'keywords': ['mày', 'tao', 'mi', 'thằng', 'con', 'đứa', 'bọn'],
            'count': 0,
            'samples': []
        }
    }
    
    # Detect patterns
    for idx, row in edf.iterrows():
        text_lower = row['Text'].lower()
        
        for pname, pinfo in patterns.items():
            if any(kw in text_lower for kw in pinfo['keywords']):
                patterns[pname]['count'] += 1
                if len(patterns[pname]['samples']) < 3:
                    patterns[pname]['samples'].append(row['Text'][:100])
    
    # Print patterns
    print(f"\n🔎 PATTERNS DETECTED:")
    sorted_patterns = sorted(patterns.items(), key=lambda x: -x[1]['count'])
    
    for pname, pinfo in sorted_patterns:
        if pinfo['count'] > 0:
            print(f"\n   • {pname}: {pinfo['count']} ({pinfo['count']/len(edf)*100:.0f}%)")
            if pinfo['samples']:
                print(f"     Examples:")
                for i, sample in enumerate(pinfo['samples'][:2], 1):
                    print(f"       {i}. {sample}...")
    
    # Statistical analysis
    title_lengths = [len(t.split()) for t in edf['title']]
    comment_lengths = [len(c.split()) for c in edf['comment']]
    
    print(f"\n📏 LENGTH STATISTICS:")
    print(f"   Title: mean={np.mean(title_lengths):.1f}, max={max(title_lengths)}")
    print(f"   Comment: mean={np.mean(comment_lengths):.1f}, max={max(comment_lengths)}")
    
    # Store insights
    error_insights[error_type] = {
        'count': len(edf),
        'patterns': {k: v['count'] for k, v in patterns.items() if v['count'] > 0},
        'avg_title_len': np.mean(title_lengths),
        'avg_comment_len': np.mean(comment_lengths)
    }

# ============================================================
# STRATEGIC RECOMMENDATIONS
# ============================================================

print("\n" + "="*80)
print("🎯 STRATEGIC RECOMMENDATIONS - NLP EXPERT")
print("="*80)

recommendations = []

# Analyze 0→1 errors (False Positive - Clean predicted as Toxic)
if '0→1' in error_insights:
    fp_count = error_insights['0→1']['count']
    fp_patterns = error_insights['0→1']['patterns']
    
    print(f"\n📍 FALSE POSITIVE (0→1): {fp_count} cases")
    print("   Problem: Model quá nhạy cảm, gán nhãn Toxic cho Clean text")
    
    if 'vcl_vl_slang' in fp_patterns and fp_patterns['vcl_vl_slang'] > fp_count * 0.2:
        print(f"\n   ⚠️ CRITICAL: VCL/VL Slang Pattern ({fp_patterns['vcl_vl_slang']} cases)")
        print("   → Model chưa học được: 'vcl/vl' trong context tích cực = Label 0")
        recommendations.append({
            'priority': 'HIGH',
            'issue': 'VCL/VL positive slang misclassified',
            'action': 'Augment training data with positive VCL/VL examples',
            'method': 'Filter unlabeled data for "chất vcl", "hay vl", "đẹp vl" + positive context'
        })
    
    if 'justice_support' in fp_patterns and fp_patterns['justice_support'] > 5:
        print(f"\n   ⚠️ Justice Support Pattern ({fp_patterns['justice_support']} cases)")
        print("   → Model nhầm: Ủng hộ pháp luật = Gây hấn")
        recommendations.append({
            'priority': 'MEDIUM',
            'issue': 'Justice support misclassified as toxic',
            'action': 'Add training samples: justice support = Label 0',
            'method': 'Create synthetic examples with "pháp luật xử lý", "bắt đi tù" in neutral tone'
        })

# Analyze 1→0 errors (False Negative - Toxic predicted as Clean)
if '1→0' in error_insights:
    fn_count = error_insights['1→0']['count']
    fn_patterns = error_insights['1→0']['patterns']
    
    print(f"\n📍 FALSE NEGATIVE (1→0): {fn_count} cases")
    print("   Problem: Model bỏ sót Toxic, gán nhãn Clean")
    
    if 'context_positive' in fn_patterns and fn_patterns['context_positive'] > fn_count * 0.3:
        print(f"\n   ⚠️ Context Confusion ({fn_patterns['context_positive']} cases)")
        print("   → Model bị nhiễu bởi từ tích cực, bỏ qua toxic words")
        recommendations.append({
            'priority': 'HIGH',
            'issue': 'Positive context masks toxic words',
            'action': 'Improve model attention to toxic keywords',
            'method': 'Add focal loss or increase weight for toxic class'
        })

# Analyze 1→2 and 2→1 errors (Severity confusion)
if '1→2' in error_insights or '2→1' in error_insights:
    print(f"\n📍 SEVERITY CONFUSION (1↔2)")
    print("   Problem: Model nhầm lẫn giữa Toxic (1) và Hate (2)")
    
    if '1→2' in error_insights:
        patterns_1_2 = error_insights['1→2']['patterns']
        if 'family_attack' in patterns_1_2 or 'animal_dehumanize' in patterns_1_2:
            print(f"\n   ⚠️ Underestimating Hate Speech")
            print("   → Model gán Label 1 cho text có family attack / dehumanization")
            recommendations.append({
                'priority': 'CRITICAL',
                'issue': 'Hate speech underestimated as toxic',
                'action': 'Fix training labels according to Guideline V7.2',
                'method': 'Run validate_against_guideline.py and fix violations'
            })
    
    if '2→1' in error_insights:
        print(f"\n   ⚠️ Overestimating Severity")
        print("   → Model gán Label 2 cho text chỉ nên là Label 1")
        recommendations.append({
            'priority': 'MEDIUM',
            'issue': 'Toxic overestimated as hate',
            'action': 'Review Label 2 definition in guideline',
            'method': 'Ensure clear distinction: Label 2 = dehumanization + family attack + violence call'
        })

# ============================================================
# ACTION PLAN
# ============================================================

print("\n" + "="*80)
print("📋 ACTION PLAN - PRIORITIZED")
print("="*80)

# Sort by priority
priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
recommendations.sort(key=lambda x: priority_order[x['priority']])

for i, rec in enumerate(recommendations, 1):
    print(f"\n{i}. [{rec['priority']}] {rec['issue']}")
    print(f"   Action: {rec['action']}")
    print(f"   Method: {rec['method']}")

# ============================================================
# CONCRETE NEXT STEPS
# ============================================================

print("\n" + "="*80)
print("🚀 CONCRETE NEXT STEPS")
print("="*80)

print("""
STEP 1: FIX GUIDELINE VIOLATIONS (CRITICAL)
   → Run: python fix_guideline_violations.py
   → Fix: Family attack, dehumanization → Label 2
   → Expected: Reduce 1→2 errors by 50%

STEP 2: AUGMENT VCL/VL POSITIVE DATA (HIGH)
   → Filter unlabeled data for positive VCL/VL context
   → Add ~200-300 samples: "chất vcl", "hay vl" + positive → Label 0
   → Expected: Reduce 0→1 errors by 30%

STEP 3: ADD JUSTICE SUPPORT SAMPLES (MEDIUM)
   → Create synthetic examples: "pháp luật xử lý", "bắt đi tù" → Label 0
   → Add ~100 samples
   → Expected: Reduce 0→1 errors by 10%

STEP 4: IMPROVE MODEL ARCHITECTURE (OPTIONAL)
   → Try focal loss with gamma=2.0
   → Increase class weights for minority class
   → Add attention mechanism for toxic keywords
   → Expected: Overall F1 +0.02-0.03

STEP 5: RETRAIN & EVALUATE
   → Train with fixed + augmented data
   → Target: F1 > 0.72 (current ~0.68)
   → Re-run error analysis
""")

# Save detailed report
report_df = pd.DataFrame(recommendations)
report_df.to_excel('ERROR_ANALYSIS_RECOMMENDATIONS.xlsx', index=False)
print(f"\n💾 Saved: ERROR_ANALYSIS_RECOMMENDATIONS.xlsx")

# Save error breakdown by pattern
pattern_summary = []
for et, insights in error_insights.items():
    for pattern, count in insights['patterns'].items():
        pattern_summary.append({
            'error_type': et,
            'pattern': pattern,
            'count': count,
            'percentage': f"{count/insights['count']*100:.1f}%"
        })

pattern_df = pd.DataFrame(pattern_summary)
pattern_df = pattern_df.sort_values(['error_type', 'count'], ascending=[True, False])
pattern_df.to_excel('ERROR_PATTERNS_BREAKDOWN.xlsx', index=False)
print(f"💾 Saved: ERROR_PATTERNS_BREAKDOWN.xlsx")

print("\n" + "="*80)
print("✅ DEEP ANALYSIS COMPLETE!")
print("="*80)
