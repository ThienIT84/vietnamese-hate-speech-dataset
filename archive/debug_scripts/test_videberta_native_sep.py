"""
Test if using native [SEP] token improves ViDeBERTa performance
"""

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")

print("="*60)
print("VIDEBERTA NATIVE TOKENS")
print("="*60)

# Check native tokens
print(f"CLS token: {tokenizer.cls_token} (ID: {tokenizer.cls_token_id})")
print(f"SEP token: {tokenizer.sep_token} (ID: {tokenizer.sep_token_id})")
print(f"PAD token: {tokenizer.pad_token} (ID: {tokenizer.pad_token_id})")
print(f"UNK token: {tokenizer.unk_token} (ID: {tokenizer.unk_token_id})")

# Test tokenization with native SEP
title = "boy phố mới nhú hay sao"
comment = "tệ nạn xã hội tương lai"

print("\n" + "="*60)
print("TOKENIZATION COMPARISON")
print("="*60)

# Method 1: Custom <sep> (current approach)
text_custom = f"{title} <sep> {comment}"
tokens_custom = tokenizer(text_custom, max_length=256, truncation=True)
print(f"\n1. Custom <sep>:")
print(f"   Text: {text_custom}")
print(f"   Tokens: {len(tokens_custom['input_ids'])}")
print(f"   Decoded: {tokenizer.decode(tokens_custom['input_ids'])}")

# Method 2: Native [SEP] with text_pair
tokens_native = tokenizer(
    text=title,
    text_pair=comment,
    max_length=256,
    truncation=True
)
print(f"\n2. Native [SEP] with text_pair:")
print(f"   Title: {title}")
print(f"   Comment: {comment}")
print(f"   Tokens: {len(tokens_native['input_ids'])}")
print(f"   Decoded: {tokenizer.decode(tokens_native['input_ids'])}")
print(f"   Token type IDs: {tokens_native['token_type_ids'][:20]}...")

# Check if <sep> is in vocabulary
print("\n" + "="*60)
print("VOCABULARY CHECK")
print("="*60)
sep_id = tokenizer.convert_tokens_to_ids("<sep>")
print(f"<sep> token ID: {sep_id}")
print(f"Is <sep> in vocab? {sep_id != tokenizer.unk_token_id}")

if sep_id == tokenizer.unk_token_id:
    print("\n⚠️ WARNING: <sep> is treated as UNK token!")
    print("   This means model doesn't understand <sep>")
    print("   → Should use native [SEP] with text_pair instead!")
