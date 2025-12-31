"""
Compare PhoBERT vs ViDeBERTa tokenization
"""

from transformers import AutoTokenizer

text = "boy phố mới nhú hay sao mà mặt ông cháu"

print("="*60)
print("TOKENIZATION COMPARISON")
print("="*60)
print(f"Input text: {text}\n")

# PhoBERT
phobert_tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
phobert_tokens = phobert_tokenizer.tokenize(text)
print(f"PhoBERT tokens ({len(phobert_tokens)}):")
print(phobert_tokens)
print(f"Decoded: {phobert_tokenizer.convert_tokens_to_string(phobert_tokens)}\n")

# ViDeBERTa
videberta_tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")
videberta_tokens = videberta_tokenizer.tokenize(text)
print(f"ViDeBERTa tokens ({len(videberta_tokens)}):")
print(videberta_tokens)
print(f"Decoded: {videberta_tokenizer.convert_tokens_to_string(videberta_tokens)}\n")

print("="*60)
print("ANALYSIS")
print("="*60)
print(f"PhoBERT uses word segmentation: {len(phobert_tokens) > len(videberta_tokens)}")
print(f"Token count difference: {len(phobert_tokens) - len(videberta_tokens)}")

# Check vocab size
print(f"\nVocab size:")
print(f"  PhoBERT: {len(phobert_tokenizer)}")
print(f"  ViDeBERTa: {len(videberta_tokenizer)}")

# Check if PhoBERT uses syllable-level
print(f"\nPhoBERT tokenization style:")
if '_' in ' '.join(phobert_tokens):
    print("  ✅ Uses word segmentation (syllables joined with _)")
else:
    print("  ❌ No word segmentation")

print(f"\nViDeBERTa tokenization style:")
if '_' in ' '.join(videberta_tokens):
    print("  ✅ Uses word segmentation")
else:
    print("  ❌ Raw text (no segmentation)")
