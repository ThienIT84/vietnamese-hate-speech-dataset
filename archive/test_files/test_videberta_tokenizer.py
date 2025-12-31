"""
Test ViDeBERTa tokenizer để xem cách xử lý data
So sánh với PhoBERT
"""

print("="*80)
print("🔍 TESTING VIDEBERTA vs PHOBERT TOKENIZER")
print("="*80)

# Test samples
test_texts = [
    "học sinh giỏi bú fame",  # Raw text (no segmentation)
    "học_sinh giỏi bú_fame",  # Segmented text (PhoBERT format)
    "thằng ngu vcl đm",  # Toxic with teencode
    "bọn bắc kỳ lừa đảo",  # Hate speech
    "video hay quá cảm ơn bạn",  # Clean
]

print("\n📝 Test samples:")
for i, text in enumerate(test_texts, 1):
    print(f"{i}. {text}")

# Try to load tokenizers
print("\n" + "="*80)
print("📥 LOADING TOKENIZERS")
print("="*80)

try:
    from transformers import AutoTokenizer
    
    # PhoBERT tokenizer
    print("\n1️⃣ PhoBERT tokenizer...")
    phobert_tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
    print(f"   ✅ Loaded: vinai/phobert-base-v2")
    print(f"   Vocab size: {phobert_tokenizer.vocab_size}")
    print(f"   Type: {type(phobert_tokenizer).__name__}")
    
    # ViDeBERTa tokenizer
    print("\n2️⃣ ViDeBERTa tokenizer...")
    videberta_tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")
    print(f"   ✅ Loaded: Fsoft-AIC/videberta-base")
    print(f"   Vocab size: {videberta_tokenizer.vocab_size}")
    print(f"   Type: {type(videberta_tokenizer).__name__}")
    
    # Compare tokenization
    print("\n" + "="*80)
    print("🔬 TOKENIZATION COMPARISON")
    print("="*80)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'='*80}")
        print(f"Sample {i}: {text}")
        print(f"{'='*80}")
        
        # PhoBERT
        phobert_tokens = phobert_tokenizer.tokenize(text)
        phobert_ids = phobert_tokenizer.encode(text, add_special_tokens=False)
        print(f"\n📘 PhoBERT:")
        print(f"   Tokens: {phobert_tokens[:20]}")  # First 20
        print(f"   Count: {len(phobert_tokens)} tokens")
        print(f"   IDs: {phobert_ids[:10]}...")  # First 10
        
        # ViDeBERTa
        videberta_tokens = videberta_tokenizer.tokenize(text)
        videberta_ids = videberta_tokenizer.encode(text, add_special_tokens=False)
        print(f"\n📗 ViDeBERTa:")
        print(f"   Tokens: {videberta_tokens[:20]}")  # First 20
        print(f"   Count: {len(videberta_tokens)} tokens")
        print(f"   IDs: {videberta_ids[:10]}...")  # First 10
        
        # Comparison
        print(f"\n📊 Comparison:")
        print(f"   Token count diff: {len(videberta_tokens) - len(phobert_tokens)}")
        if len(phobert_tokens) != len(videberta_tokens):
            print(f"   ⚠️ Different tokenization!")
        else:
            print(f"   ✅ Same token count")
    
    # Test with segmented vs raw
    print("\n" + "="*80)
    print("🧪 SEGMENTED vs RAW TEXT TEST")
    print("="*80)
    
    raw_text = "học sinh giỏi bú fame"
    segmented_text = "học_sinh giỏi bú_fame"
    
    print(f"\nRaw:       {raw_text}")
    print(f"Segmented: {segmented_text}")
    
    print(f"\n📘 PhoBERT with RAW:")
    phobert_raw = phobert_tokenizer.tokenize(raw_text)
    print(f"   {phobert_raw}")
    
    print(f"\n📘 PhoBERT with SEGMENTED:")
    phobert_seg = phobert_tokenizer.tokenize(segmented_text)
    print(f"   {phobert_seg}")
    
    print(f"\n📗 ViDeBERTa with RAW:")
    videberta_raw = videberta_tokenizer.tokenize(raw_text)
    print(f"   {videberta_raw}")
    
    print(f"\n📗 ViDeBERTa with SEGMENTED:")
    videberta_seg = videberta_tokenizer.tokenize(segmented_text)
    print(f"   {videberta_seg}")
    
    # Conclusion
    print("\n" + "="*80)
    print("📋 CONCLUSION")
    print("="*80)
    
    print("\n✅ PhoBERT:")
    print("   - Tokenizer type: RobertaTokenizer (BPE)")
    print("   - Expects: Word-segmented text (học_sinh)")
    print("   - Vocab: Trained on segmented Vietnamese")
    
    print("\n✅ ViDeBERTa:")
    print("   - Tokenizer type: DebertaV2Tokenizer (SentencePiece)")
    print("   - Expects: Raw text (học sinh)")
    print("   - Vocab: Trained on raw Vietnamese text")
    
    print("\n🎯 RECOMMENDATION:")
    if '_' in segmented_text:
        print("   ⚠️ Your current data is SEGMENTED (has underscores)")
        print("   ✅ Good for PhoBERT")
        print("   ⚠️ Need to REMOVE underscores for ViDeBERTa")
        print("\n   Action: Convert 'học_sinh' → 'học sinh'")
    
except ImportError as e:
    print(f"❌ Error: {e}")
    print("Please install: pip install transformers")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✅ TEST COMPLETE")
print("="*80)
