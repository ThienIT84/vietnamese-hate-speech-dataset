"""Test special token protection"""

import pandas as pd
import re

def protect_special_tokens(text):
    """Temporarily replace special tokens with placeholders"""
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
    ]
    
    # Replace with placeholders
    for i, token in enumerate(special_tokens):
        if token in text:
            placeholder = f"__SPECIAL_TOKEN_{i}__"
            protected[placeholder] = token
            text = text.replace(token, placeholder)
            print(f"  Protected: {token} → {placeholder}")
    
    return text, protected

def restore_special_tokens(text, protected):
    """Restore special tokens from placeholders"""
    if pd.isna(text):
        return text
    
    text = str(text)
    for placeholder, token in protected.items():
        text = text.replace(placeholder, token)
        print(f"  Restored: {placeholder} → {token}")
    return text

# Test
test_texts = [
    "học_sinh <emo_pos> </s>",
    "boy phố <emo_pos> _ <emo_pos> </s> _ <person>",
    "awai x <user> - body shaming",
]

for i, text in enumerate(test_texts, 1):
    print(f"\n{'='*60}")
    print(f"Test {i}: {text}")
    print(f"{'='*60}")
    
    # Protect
    print("\n1. PROTECT:")
    protected_text, protected_dict = protect_special_tokens(text)
    print(f"   Result: {protected_text}")
    print(f"   Dict: {protected_dict}")
    
    # Remove underscores
    print("\n2. REMOVE UNDERSCORES:")
    no_underscore = protected_text.replace('_', ' ')
    print(f"   Result: {no_underscore}")
    
    # Restore
    print("\n3. RESTORE:")
    final_text = restore_special_tokens(no_underscore, protected_dict)
    print(f"   Result: {final_text}")
    
    # Check
    print("\n4. CHECK:")
    if '<emo_pos>' in final_text:
        print(f"   ✅ <emo_pos> preserved")
    if '<person>' in final_text:
        print(f"   ✅ <person> preserved")
    if '<user>' in final_text:
        print(f"   ✅ <user> preserved")
    if 'SPECIAL_TOKEN' in final_text:
        print(f"   ❌ Placeholder not restored!")
