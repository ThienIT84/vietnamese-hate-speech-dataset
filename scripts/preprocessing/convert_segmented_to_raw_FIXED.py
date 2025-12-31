"""
Convert PhoBERT segmented data to ViDeBERTa raw format - FIXED VERSION
Remove word segmentation underscores while PROTECTING special tokens

CRITICAL FIXES:
1. ✅ Protect special tokens: <emo_pos>, <emo_neg>, <person>, <user>
2. ✅ Remove </s> and <s> (tokenizer adds these automatically)
3. ✅ Clean punctuation artifacts
4. ✅ Remove orphan tokens

Input:  "học_sinh giỏi <emo_pos> </s>"
Output: "học sinh giỏi <emo_pos>"
"""

import pandas as pd
import re
import os

def protect_special_tokens(text):
    """
    Temporarily replace special tokens with placeholders
    to protect them during underscore removal
    """
    if pd.isna(text):
        return text, {}
    
    text = str(text)
    protected = {}
    
    # Special tokens to protect (keep underscores in these)
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
    
    # Replace with placeholders
    for i, token in enumerate(special_tokens):
        if token in text:
            placeholder = f"__SPECIAL_TOKEN_{i}__"
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

def remove_bos_eos_tokens(text):
    """
    Remove <s> and </s> tokens
    ViDeBERTa tokenizer adds these automatically
    """
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # Remove BOS/EOS tokens
    text = text.replace('<s>', '')
    text = text.replace('</s>', '')
    
    return text

def clean_punctuation(text):
    """
    Clean punctuation artifacts
    - Multiple dots: .. → .
    - Multiple exclamation: !!! → !
    - Multiple question: ??? → ?
    - Orphan underscores: ?_ → ?
    """
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # Remove orphan underscores near punctuation
    text = re.sub(r'([.!?,;:])\s*_\s*', r'\1 ', text)
    text = re.sub(r'\s*_\s*([.!?,;:])', r' \1', text)
    
    # Normalize multiple punctuation
    text = re.sub(r'\.{2,}', '.', text)  # .. → .
    text = re.sub(r'!{2,}', '!', text)   # !!! → !
    text = re.sub(r'\?{2,}', '?', text)  # ??? → ?
    
    # Remove standalone underscores
    text = re.sub(r'\s+_\s+', ' ', text)
    text = re.sub(r'^_\s+', '', text)
    text = re.sub(r'\s+_$', '', text)
    
    return text

def remove_segmentation_safe(text):
    """
    Remove word segmentation underscores SAFELY
    
    Steps:
    1. Protect special tokens (keep their underscores)
    2. Remove </s> and <s> tokens
    3. Remove underscores from regular words
    4. Clean punctuation artifacts
    5. Restore special tokens
    6. Clean multiple spaces
    
    Examples:
        "học_sinh <emo_pos> </s>" → "học sinh <emo_pos>"
        "bú_fame <person>" → "bú fame <person>"
        "?_ </s>" → "?"
    """
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # Step 1: Protect special tokens
    text, protected = protect_special_tokens(text)
    
    # Step 2: Remove BOS/EOS tokens
    text = remove_bos_eos_tokens(text)
    
    # Step 3: Remove underscores from regular words
    text = text.replace('_', ' ')
    
    # Step 4: Clean punctuation artifacts
    text = clean_punctuation(text)
    
    # Step 5: Restore special tokens
    text = restore_special_tokens(text, protected)
    
    # Step 6: Clean multiple spaces
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def verify_special_tokens(df, text_col):
    """
    Verify that special tokens are preserved correctly
    """
    print("\n🔍 VERIFYING SPECIAL TOKENS...")
    print("="*80)
    
    special_tokens = ['<emo_pos>', '<emo_neg>', '<person>', '<user>']
    
    for token in special_tokens:
        # Count in original
        count_before = df[text_col].astype(str).str.contains(re.escape(token), regex=True).sum()
        
        if count_before > 0:
            print(f"\n✅ {token}:")
            print(f"   Found in {count_before} samples")
            
            # Show examples
            samples = df[df[text_col].astype(str).str.contains(re.escape(token), regex=True)][text_col].head(3)
            for i, sample in enumerate(samples, 1):
                print(f"   {i}. {sample[:70]}...")

def verify_no_bos_eos(df, text_col):
    """
    Verify that <s> and </s> are removed
    """
    print("\n🔍 VERIFYING BOS/EOS REMOVAL...")
    print("="*80)
    
    bos_count = df[text_col].astype(str).str.contains('<s>', regex=False).sum()
    eos_count = df[text_col].astype(str).str.contains('</s>', regex=False).sum()
    
    print(f"\n<s> tokens remaining: {bos_count}")
    print(f"</s> tokens remaining: {eos_count}")
    
    if bos_count == 0 and eos_count == 0:
        print("✅ All BOS/EOS tokens removed successfully!")
    else:
        print("⚠️ Warning: Some BOS/EOS tokens still present")
        if bos_count > 0:
            samples = df[df[text_col].astype(str).str.contains('<s>', regex=False)][text_col].head(3)
            print("\nSamples with <s>:")
            for sample in samples:
                print(f"  - {sample[:70]}...")
        if eos_count > 0:
            samples = df[df[text_col].astype(str).str.contains('</s>', regex=False)][text_col].head(3)
            print("\nSamples with </s>:")
            for sample in samples:
                print(f"  - {sample[:70]}...")

def main():
    print("="*80)
    print("🔄 CONVERTING SEGMENTED DATA TO RAW FORMAT - FIXED VERSION")
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
    print(f"📊 Columns: {df.columns.tolist()}")
    
    # Check text column
    text_col = 'training_text' if 'training_text' in df.columns else 'text'
    label_col = 'label'
    
    print(f"\n📝 Text column: {text_col}")
    print(f"📝 Label column: {label_col}")
    
    # Statistics before
    print("\n📊 BEFORE CONVERSION:")
    print("="*80)
    
    underscore_count = df[text_col].astype(str).str.count('_').sum()
    bos_count = df[text_col].astype(str).str.contains('<s>', regex=False).sum()
    eos_count = df[text_col].astype(str).str.contains('</s>', regex=False).sum()
    emo_pos_count = df[text_col].astype(str).str.contains('<emo_pos>', regex=False).sum()
    person_count = df[text_col].astype(str).str.contains('<person>', regex=False).sum()
    
    print(f"Underscores: {underscore_count}")
    print(f"<s> tokens: {bos_count}")
    print(f"</s> tokens: {eos_count}")
    print(f"<emo_pos> tokens: {emo_pos_count}")
    print(f"<person> tokens: {person_count}")
    
    # Convert
    print("\n✅ Converting with SAFE method...")
    df['training_text_raw'] = df[text_col].apply(remove_segmentation_safe)
    
    # Statistics after
    print("\n📊 AFTER CONVERSION:")
    print("="*80)
    
    underscore_count_after = df['training_text_raw'].astype(str).str.count('_').sum()
    bos_count_after = df['training_text_raw'].astype(str).str.contains('<s>', regex=False).sum()
    eos_count_after = df['training_text_raw'].astype(str).str.contains('</s>', regex=False).sum()
    emo_pos_count_after = df['training_text_raw'].astype(str).str.contains('<emo_pos>', regex=False).sum()
    person_count_after = df['training_text_raw'].astype(str).str.contains('<person>', regex=False).sum()
    
    print(f"Underscores: {underscore_count_after} (removed: {underscore_count - underscore_count_after})")
    print(f"<s> tokens: {bos_count_after} (removed: {bos_count - bos_count_after})")
    print(f"</s> tokens: {eos_count_after} (removed: {eos_count - eos_count_after})")
    print(f"<emo_pos> tokens: {emo_pos_count_after} (preserved: {emo_pos_count_after}/{emo_pos_count})")
    print(f"<person> tokens: {person_count_after} (preserved: {person_count_after}/{person_count})")
    
    # Verify special tokens
    verify_special_tokens(df, 'training_text_raw')
    
    # Verify BOS/EOS removal
    verify_no_bos_eos(df, 'training_text_raw')
    
    # Show examples
    print("\n📋 BEFORE vs AFTER (first 10 samples):")
    print("="*80)
    for i in range(min(10, len(df))):
        before = df[text_col].iloc[i]
        after = df['training_text_raw'].iloc[i]
        label = df[label_col].iloc[i]
        
        print(f"\n{i+1}. Label: {label}")
        print(f"   BEFORE: {before[:80]}")
        print(f"   AFTER:  {after[:80]}")
        
        # Check for issues
        if '<emo pos>' in after or '<emo neg>' in after:
            print(f"   ⚠️ WARNING: Special token broken!")
        if '</s>' in after or '<s>' in after:
            print(f"   ⚠️ WARNING: BOS/EOS not removed!")
        if before != after:
            print(f"   ✅ Changed")
    
    # Save Excel
    output_file = 'data/final/final_train_data_v3_RAW_FIXED.xlsx'
    df_output = df[['training_text_raw', label_col]].copy()
    df_output.columns = ['training_text', 'label']
    
    print(f"\n💾 Saving Excel: {output_file}")
    df_output.to_excel(output_file, index=False)
    print(f"✅ Saved: {len(df_output)} samples")
    
    # Save CSV
    csv_file = output_file.replace('.xlsx', '.csv')
    print(f"\n💾 Saving CSV: {csv_file}")
    df_output.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"✅ Saved: {len(df_output)} samples")
    
    # Final verification
    print("\n" + "="*80)
    print("🔍 FINAL VERIFICATION")
    print("="*80)
    
    # Check file sizes
    input_size = os.path.getsize(input_file) / 1024 / 1024
    output_size = os.path.getsize(output_file) / 1024 / 1024
    
    print(f"\n📊 File sizes:")
    print(f"   Input (segmented):  {input_size:.2f} MB")
    print(f"   Output (raw):       {output_size:.2f} MB")
    
    # Final checks
    df_check = pd.read_excel(output_file)
    
    remaining_underscores = df_check['training_text'].astype(str).str.count('_').sum()
    remaining_bos = df_check['training_text'].astype(str).str.contains('<s>', regex=False).sum()
    remaining_eos = df_check['training_text'].astype(str).str.contains('</s>', regex=False).sum()
    preserved_emo_pos = df_check['training_text'].astype(str).str.contains('<emo_pos>', regex=False).sum()
    preserved_person = df_check['training_text'].astype(str).str.contains('<person>', regex=False).sum()
    
    print(f"\n🔍 Final checks:")
    print(f"   Underscores: {remaining_underscores}")
    print(f"   <s> tokens: {remaining_bos}")
    print(f"   </s> tokens: {remaining_eos}")
    print(f"   <emo_pos> preserved: {preserved_emo_pos}")
    print(f"   <person> preserved: {preserved_person}")
    
    # Validation
    issues = []
    if remaining_underscores > 0:
        # Check if underscores are only in special tokens
        samples_with_underscore = df_check[df_check['training_text'].astype(str).str.contains('_', regex=False)]
        special_token_underscores = samples_with_underscore['training_text'].astype(str).str.contains('<emo_|<person>|<user>', regex=True).sum()
        if special_token_underscores == len(samples_with_underscore):
            print(f"   ✅ Underscores only in special tokens (OK)")
        else:
            issues.append(f"⚠️ {remaining_underscores} underscores in regular words")
    
    if remaining_bos > 0:
        issues.append(f"❌ {remaining_bos} <s> tokens not removed")
    
    if remaining_eos > 0:
        issues.append(f"❌ {remaining_eos} </s> tokens not removed")
    
    if preserved_emo_pos < emo_pos_count:
        issues.append(f"❌ Lost {emo_pos_count - preserved_emo_pos} <emo_pos> tokens")
    
    if preserved_person < person_count:
        issues.append(f"❌ Lost {person_count - preserved_person} <person> tokens")
    
    # Label distribution check
    print(f"\n📊 Label distribution:")
    for label, count in df_output['label'].value_counts().sort_index().items():
        pct = count / len(df_output) * 100
        print(f"   Label {int(label)}: {count} ({pct:.1f}%)")
    
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
    
    print(f"\n🎯 Next steps:")
    print(f"   1. Verify output manually")
    print(f"   2. Upload {output_file} to Kaggle")
    print(f"   3. Use with ViDeBERTa training script")
    print(f"   4. Model: Fsoft-AIC/videberta-base")

if __name__ == '__main__':
    main()
