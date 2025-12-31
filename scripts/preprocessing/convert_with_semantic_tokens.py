"""
Convert PhoBERT segmented data to ViDeBERTa raw format
WITH SEMANTIC TOKENS instead of removing </s>

Strategy:
- </s> → <sep> (semantic separator between title and comment)
- OR use <post> ... </post> <comment> ... </comment>
- Preserve special tokens: <emo_pos>, <person>, etc.
- Remove underscores from regular words
"""

import pandas as pd
import re
import os

def protect_special_tokens(text):
    """Protect special tokens with unique placeholders"""
    if pd.isna(text):
        return text, {}
    
    text = str(text)
    protected = {}
    
    # Special tokens to protect
    special_tokens = [
        '<emo_pos>',
        '<emo_neg>',
        '<person>',
        '<user>',
        '<location>',
        '<organization>',
        '<time>',
        '<number>',
    ]
    
    # Replace with unique placeholders
    for i, token in enumerate(special_tokens):
        if token in text:
            placeholder = f"XSPECIALTOKENX{i}X"
            protected[placeholder] = token
            text = text.replace(token, placeholder)
    
    return text, protected

def restore_special_tokens(text, protected):
    """Restore special tokens from placeholders"""
    if pd.isna(text):
        return text
    
    text = str(text)
    for placeholder, token in protected.items():
        text = text.replace(placeholder, token)
    return text

def replace_separator_with_semantic(text):
    """
    Replace </s> with semantic separator
    
    Options:
    1. <sep> - Simple separator
    2. <post>...</post> <comment>...</comment> - Structured
    
    We use <sep> for simplicity
    """
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # Replace </s> with <sep>
    text = text.replace('</s>', '<sep>')
    
    # Remove <s> if exists
    text = text.replace('<s>', '')
    
    return text

def clean_punctuation(text):
    """Clean punctuation artifacts"""
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # Remove orphan underscores near punctuation
    text = re.sub(r'([.!?,;:])\s*_\s*', r'\1 ', text)
    text = re.sub(r'\s*_\s*([.!?,;:])', r' \1', text)
    
    # Normalize multiple punctuation
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'!{2,}', '!', text)
    text = re.sub(r'\?{2,}', '?', text)
    
    # Remove standalone underscores
    text = re.sub(r'\s+_\s+', ' ', text)
    text = re.sub(r'^_\s+', '', text)
    text = re.sub(r'\s+_$', '', text)
    
    return text

def convert_to_raw_with_semantic(text):
    """
    Convert segmented text to raw with semantic tokens
    
    Steps:
    1. Protect special tokens
    2. Replace </s> with <sep>
    3. Remove underscores from regular words
    4. Clean punctuation
    5. Restore special tokens
    6. Clean spaces
    
    Example:
        "học_sinh giỏi </s> bú_fame <emo_pos>"
        → "học sinh giỏi <sep> bú fame <emo_pos>"
    """
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # Step 1: Protect special tokens
    text, protected = protect_special_tokens(text)
    
    # Step 2: Replace </s> with <sep>
    text = replace_separator_with_semantic(text)
    
    # Step 3: Remove underscores
    text = text.replace('_', ' ')
    
    # Step 4: Clean punctuation
    text = clean_punctuation(text)
    
    # Step 5: Restore special tokens
    text = restore_special_tokens(text, protected)
    
    # Step 6: Clean spaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def main():
    print("="*80)
    print("🔄 CONVERTING WITH SEMANTIC TOKENS")
    print("="*80)
    
    # Input file
    input_file = 'data/final/final_train_data_v3_READY.xlsx'
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    # Load data
    print(f"\n📂 Loading: {input_file}")
    df = pd.read_excel(input_file)
    
    print(f"✅ Loaded: {len(df)} samples")
    
    text_col = 'training_text' if 'training_text' in df.columns else 'text'
    label_col = 'label'
    
    # Statistics before
    print("\n📊 BEFORE CONVERSION:")
    print("="*80)
    
    underscore_count = df[text_col].astype(str).str.count('_').sum()
    sep_count = df[text_col].astype(str).str.contains('</s>', regex=False).sum()
    emo_pos_count = df[text_col].astype(str).str.contains('<emo_pos>', regex=False).sum()
    person_count = df[text_col].astype(str).str.contains('<person>', regex=False).sum()
    
    print(f"Underscores: {underscore_count}")
    print(f"</s> tokens: {sep_count}")
    print(f"<emo_pos> tokens: {emo_pos_count}")
    print(f"<person> tokens: {person_count}")
    
    # Show sample with </s>
    if sep_count > 0:
        sample = df[df[text_col].astype(str).str.contains('</s>', regex=False)].iloc[0]
        print(f"\n📝 Sample with </s>:")
        print(f"   {sample[text_col][:120]}...")
    
    # Convert
    print("\n✅ Converting with SEMANTIC tokens...")
    df['training_text_semantic'] = df[text_col].apply(convert_to_raw_with_semantic)
    
    # Statistics after
    print("\n📊 AFTER CONVERSION:")
    print("="*80)
    
    underscore_count_after = df['training_text_semantic'].astype(str).str.count('_').sum()
    sep_count_after = df['training_text_semantic'].astype(str).str.contains('<sep>', regex=False).sum()
    old_sep_count_after = df['training_text_semantic'].astype(str).str.contains('</s>', regex=False).sum()
    emo_pos_count_after = df['training_text_semantic'].astype(str).str.contains('<emo_pos>', regex=False).sum()
    person_count_after = df['training_text_semantic'].astype(str).str.contains('<person>', regex=False).sum()
    
    print(f"Underscores: {underscore_count_after} (removed: {underscore_count - underscore_count_after})")
    print(f"</s> tokens: {old_sep_count_after} (replaced: {sep_count - old_sep_count_after})")
    print(f"<sep> tokens: {sep_count_after} (new semantic separator)")
    print(f"<emo_pos> tokens: {emo_pos_count_after} (preserved: {emo_pos_count_after}/{emo_pos_count})")
    print(f"<person> tokens: {person_count_after} (preserved: {person_count_after}/{person_count})")
    
    # Show examples
    print("\n📋 BEFORE vs AFTER (samples with separator):")
    print("="*80)
    
    samples_with_sep = df[df[text_col].astype(str).str.contains('</s>', regex=False)].head(10)
    
    for i, (idx, row) in enumerate(samples_with_sep.iterrows(), 1):
        before = row[text_col]
        after = row['training_text_semantic']
        label = row[label_col]
        
        print(f"\n{i}. Label: {label}")
        print(f"   BEFORE: {before[:100]}...")
        print(f"   AFTER:  {after[:100]}...")
        
        # Check
        if '<sep>' in after:
            print(f"   ✅ </s> → <sep>")
        if '<emo_pos>' in after:
            print(f"   ✅ <emo_pos> preserved")
        if '<person>' in after:
            print(f"   ✅ <person> preserved")
    
    # Save
    output_file = 'data/final/final_train_data_v3_SEMANTIC.xlsx'
    df_output = df[['training_text_semantic', label_col]].copy()
    df_output.columns = ['training_text', 'label']
    
    print(f"\n💾 Saving: {output_file}")
    df_output.to_excel(output_file, index=False)
    print(f"✅ Saved: {len(df_output)} samples")
    
    # CSV
    csv_file = output_file.replace('.xlsx', '.csv')
    df_output.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"✅ Saved: {csv_file}")
    
    # Final verification
    print("\n" + "="*80)
    print("🔍 FINAL VERIFICATION")
    print("="*80)
    
    df_check = pd.read_excel(output_file)
    
    remaining_underscores = df_check['training_text'].astype(str).str.count('_').sum()
    sep_tokens = df_check['training_text'].astype(str).str.contains('<sep>', regex=False).sum()
    old_sep_tokens = df_check['training_text'].astype(str).str.contains('</s>', regex=False).sum()
    preserved_emo_pos = df_check['training_text'].astype(str).str.contains('<emo_pos>', regex=False).sum()
    preserved_person = df_check['training_text'].astype(str).str.contains('<person>', regex=False).sum()
    
    print(f"\n🔍 Final checks:")
    print(f"   Underscores: {remaining_underscores}")
    print(f"   </s> tokens: {old_sep_tokens}")
    print(f"   <sep> tokens: {sep_tokens}")
    print(f"   <emo_pos> preserved: {preserved_emo_pos}/{emo_pos_count}")
    print(f"   <person> preserved: {preserved_person}/{person_count}")
    
    # Validation
    issues = []
    
    if old_sep_tokens > 0:
        issues.append(f"⚠️ {old_sep_tokens} </s> tokens not replaced")
    
    if preserved_emo_pos < emo_pos_count:
        issues.append(f"❌ Lost {emo_pos_count - preserved_emo_pos} <emo_pos> tokens")
    
    if preserved_person < person_count:
        issues.append(f"❌ Lost {person_count - preserved_person} <person> tokens")
    
    print("\n" + "="*80)
    if issues:
        print("⚠️ CONVERSION COMPLETE WITH ISSUES:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("✅ CONVERSION COMPLETE - ALL CHECKS PASSED!")
    print("="*80)
    
    print(f"\n📁 Output files:")
    print(f"   1. {output_file}")
    print(f"   2. {csv_file}")
    
    print(f"\n🎯 Key changes:")
    print(f"   ✅ </s> → <sep> (semantic separator)")
    print(f"   ✅ Special tokens preserved")
    print(f"   ✅ Underscores removed from regular words")
    print(f"   ✅ Punctuation cleaned")
    
    print(f"\n📝 Usage with ViDeBERTa:")
    print(f"   - Model will learn <sep> as title/comment boundary")
    print(f"   - Better semantic understanding than removing </s>")
    print(f"   - Add <sep> to tokenizer special tokens")

if __name__ == '__main__':
    main()
