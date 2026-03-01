"""
🔬 Test 7 Cases trên Model Thật - Generate Real Comparison Data
Script này sẽ:
1. Load SafeSense-VI model (PhoBERT fine-tuned)
2. Test 7 cases qua model
3. Export results với confidence scores thực
4. Generate comparison data cho The Duel
"""

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import sys
import os
from pathlib import Path
import json

# Add project root
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.preprocessing.advanced_text_cleaning import clean_text

# ============================================================
# 1. CONFIGURATION
# ============================================================

MODEL_PATH = r"C:\Học sâu\Dataset\TOXIC_COMMENT\models\phobert-hate-speech-final"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Label mapping
LABEL_MAP = {
    0: "CLEAN",
    1: "TOXIC", 
    2: "HATE"
}

# ============================================================
# 2. TEST CASES (7 cases)
# ============================================================

TEST_CASES = [
    {
        'id': 1,
        'name': 'Bypass Detection',
        'input': 'n.g.u',
        'context': '',
        'description': 'Phát hiện bypass với dấu chấm ngăn cách',
        'expected_safesense': 'HATE',
        'preprocessing_steps': [
            '1️⃣ Input: "n.g.u"',
            '2️⃣ Bypass removal: "n.g.u" → "ngu"',
            '3️⃣ Word segmentation: "ngu"',
            '4️⃣ PhoBERT classify'
        ]
    },
    {
        'id': 2,
        'name': 'Leetspeak Decoding',
        'input': 'ch3t đi',
        'context': '',
        'description': 'Giải mã leetspeak (số thay chữ)',
        'expected_safesense': 'HATE',
        'preprocessing_steps': [
            '1️⃣ Input: "ch3t đi"',
            '2️⃣ Leetspeak: "ch3t" → "chết" (3→ê)',
            '3️⃣ Result: "chết đi"',
            '4️⃣ PhoBERT classify'
        ]
    },
    {
        'id': 3,
        'name': 'Teencode Normalization',
        'input': 'vcl ngu vl',
        'context': '',
        'description': 'Chuẩn hóa teencode tiếng Việt',
        'expected_safesense': 'HATE',
        'preprocessing_steps': [
            '1️⃣ Input: "vcl ngu vl"',
            '2️⃣ Teencode: "vcl" → "vãi cả lồn"',
            '3️⃣ Teencode: "vl" → "vãi lồn"',
            '4️⃣ Result: "vãi cả lồn ngu vãi lồn"',
            '5️⃣ PhoBERT classify'
        ]
    },
    {
        'id': 4,
        'name': 'Context Understanding',
        'input': 'Vụ đó bị tử hình rồi',
        'context': 'Tin tức pháp luật - Cập nhật mới nhất',
        'description': 'Hiểu ngữ cảnh tin tức vs toxic',
        'expected_safesense': 'CLEAN',
        'preprocessing_steps': [
            '1️⃣ Input: "Vụ đó bị tử hình rồi"',
            '2️⃣ Context: "Tin tức pháp luật..."',
            '3️⃣ Combine: "Tin tức... </s> Vụ đó bị tử hình rồi"',
            '4️⃣ PhoBERT với context'
        ]
    },
    {
        'id': 5,
        'name': 'Dot Bypass Trick',
        'input': 'đ.ồ n.g.u',
        'context': '',
        'description': 'Phát hiện bypass với dấu chấm trong từ',
        'expected_safesense': 'HATE',
        'preprocessing_steps': [
            '1️⃣ Input: "đ.ồ n.g.u"',
            '2️⃣ Dot bypass: "đ.ồ" → "đồ"',
            '3️⃣ Dot bypass: "n.g.u" → "ngu"',
            '4️⃣ Result: "đồ ngu"',
            '5️⃣ PhoBERT classify'
        ]
    },
    {
        'id': 6,
        'name': 'Death Metaphor',
        'input': 'đăng xuất đi cho sạch',
        'context': '',
        'description': 'Nhận diện ẩn dụ cái chết',
        'expected_safesense': 'HATE',
        'preprocessing_steps': [
            '1️⃣ Input: "đăng xuất đi cho sạch"',
            '2️⃣ Death metaphor detected: "đăng xuất"',
            '3️⃣ Context: "cho sạch" → Strong hate signal',
            '4️⃣ PhoBERT classify'
        ]
    },
    {
        'id': 7,
        'name': 'Mixed Language + Teencode',
        'input': '3 đê stupid vl',
        'context': '',
        'description': 'Xử lý hỗn hợp: leetspeak + tiếng Anh + teencode',
        'expected_safesense': 'HATE',
        'preprocessing_steps': [
            '1️⃣ Input: "3 đê stupid vl"',
            '2️⃣ Leetspeak: "3" → "ba" (context: "đê")',
            '3️⃣ English: "stupid" retained',
            '4️⃣ Teencode: "vl" → "vãi lồn"',
            '5️⃣ Result: "ba đê stupid vãi lồn"',
            '6️⃣ PhoBERT classify'
        ]
    }
]

# ============================================================
# 3. LOAD MODEL
# ============================================================

print("="*80)
print("🔬 TESTING 7 CASES ON REAL SAFESENSE-VI MODEL")
print("="*80)
print(f"\n📦 Loading model from: {MODEL_PATH}")

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=3)
    model.to(DEVICE)
    model.eval()
    print(f"✅ Model loaded successfully on {DEVICE}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print(f"💡 Kiểm tra path: {MODEL_PATH}")
    exit(1)

# ============================================================
# 4. TEST FUNCTION
# ============================================================

def preprocess_input(title, comment):
    """Preprocess với pipeline chuẩn"""
    cleaned_title = clean_text(title) if title.strip() else ""
    cleaned_comment = clean_text(comment)
    
    if cleaned_title:
        input_text = f"{cleaned_title} </s> {cleaned_comment}"
    else:
        input_text = f"</s> {cleaned_comment}"
    
    return input_text

def predict(text, context=""):
    """Predict với model thật"""
    # Preprocess
    processed = preprocess_input(context, text)
    
    # Tokenize
    inputs = tokenizer(processed, return_tensors="pt", truncation=True, max_length=256, padding=True)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}
    
    # Inference
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        confidence, predicted_class = torch.max(probs, dim=1)
        
        probs_np = probs.cpu().numpy()[0]
        pred_label = predicted_class.item()
        conf_score = confidence.item()
    
    return {
        'label': LABEL_MAP[pred_label],
        'confidence': round(conf_score * 100, 1),
        'probs': {
            'clean': round(probs_np[0] * 100, 1),
            'toxic': round(probs_np[1] * 100, 1),
            'hate': round(probs_np[2] * 100, 1)
        },
        'processed_text': processed
    }

# ============================================================
# 5. RUN TESTS
# ============================================================

print("\n" + "="*80)
print("🧪 RUNNING 7 TEST CASES")
print("="*80)

results = []

for case in TEST_CASES:
    print(f"\n{'─'*80}")
    print(f"Test Case {case['id']}: {case['name']}")
    print(f"Input: \"{case['input']}\"")
    if case['context']:
        print(f"Context: \"{case['context']}\"")
    
    # Predict
    result = predict(case['input'], case['context'])
    
    print(f"\n🛡️ SafeSense-VI Result:")
    print(f"  Label: {result['label']}")
    print(f"  Confidence: {result['confidence']}%")
    print(f"  Probs: Clean={result['probs']['clean']}%, Toxic={result['probs']['toxic']}%, Hate={result['probs']['hate']}%")
    print(f"  Processed: \"{result['processed_text']}\"")
    
    # Check correctness
    is_correct = result['label'] == case['expected_safesense']
    print(f"  Expected: {case['expected_safesense']}")
    print(f"  Status: {'✅ CORRECT' if is_correct else '❌ WRONG'}")
    
    # Store result
    results.append({
        'case_id': case['id'],
        'name': case['name'],
        'input': case['input'],
        'context': case['context'],
        'description': case['description'],
        'expected': case['expected_safesense'],
        'actual': result['label'],
        'confidence': result['confidence'],
        'probs': result['probs'],
        'processed_text': result['processed_text'],
        'preprocessing_steps': case['preprocessing_steps'],
        'correct': is_correct
    })

# ============================================================
# 6. SUMMARY & EXPORT
# ============================================================

print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)

correct_count = sum(1 for r in results if r['correct'])
accuracy = (correct_count / len(results)) * 100

print(f"\nTotal Cases: {len(results)}")
print(f"Correct: {correct_count}")
print(f"Wrong: {len(results) - correct_count}")
print(f"Accuracy: {accuracy:.1f}%")

# Average confidence
avg_conf = sum(r['confidence'] for r in results) / len(results)
print(f"Average Confidence: {avg_conf:.1f}%")

# Per-label breakdown
label_counts = {'CLEAN': 0, 'TOXIC': 0, 'HATE': 0}
for r in results:
    label_counts[r['actual']] += 1

print(f"\nPredictions Breakdown:")
for label, count in label_counts.items():
    print(f"  {label}: {count}/{len(results)}")

# ============================================================
# 7. EXPORT TO JSON
# ============================================================

output_file = "duel_real_data.json"
export_data = {
    'metadata': {
        'model_path': MODEL_PATH,
        'device': str(DEVICE),
        'total_cases': len(results),
        'correct': correct_count,
        'accuracy': round(accuracy, 1),
        'avg_confidence': round(avg_conf, 1)
    },
    'results': results
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Results exported to: {output_file}")
print("\n💡 Next steps:")
print("   1. Review results trong duel_real_data.json")
print("   2. Update duel_app.js với confidence scores thực")
print("   3. Verify preprocessing logic đang hoạt động đúng")

print("\n" + "="*80)
print("🎉 TEST COMPLETE")
print("="*80)
