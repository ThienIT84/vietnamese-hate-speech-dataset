"""
🥊 THE DUEL: SafeSense-VI vs Traditional AI
Mock Comparison Data cho demo IT Got Talent 2025

Philosophy:
- Traditional AI: mBERT/toxic-bert cơ bản, KHÔNG preprocessing
- SafeSense-VI: PhoBERT-v2 + 18-step preprocessing pipeline

Test cases chọn lọc để showcase điểm mạnh của SafeSense-VI
"""

DUEL_TEST_CASES = [
    {
        'id': 1,
        'name': 'Bypass Detection',
        'input': 'n.g.u',
        'description': 'Phát hiện bypass với dấu chấm ngăn cách',
        'traditional': {
            'label': 'CLEAN',
            'confidence': 87.3,
            'color': 'success',
            'reasoning': 'Không nhận diện được bypass pattern "n.g.u"',
            'raw_output': 'Text contains dots → Unknown pattern → Safe',
            'issues': [
                '❌ Không có preprocessing',
                '❌ Coi "n.g.u" là chuỗi ký tự lạ',
                '❌ Miss toxic content hoàn toàn'
            ]
        },
        'safesense': {
            'label': 'HATE',
            'confidence': 94.2,
            'color': 'danger',
            'reasoning': 'Decode bypass "n.g.u" → "ngu" → Nhận diện toxic',
            'preprocessing_steps': [
                '1️⃣ Input: "n.g.u"',
                '2️⃣ Bypass removal: "n.g.u" → "ngu"',
                '3️⃣ Word segmentation: "ngu"',
                '4️⃣ PhoBERT classify → HATE (94.2%)'
            ],
            'raw_output': 'Decoded text: "ngu" → Offensive insult → HATE',
            'strengths': [
                '✅ Decode bypass patterns',
                '✅ Nhận diện đúng toxic content',
                '✅ High confidence (94.2%)'
            ]
        },
        'winner': 'safesense',
        'accuracy_gain': '+94.2%',
        'explanation': 'Traditional AI hoàn toàn bỏ sót vì không hiểu bypass. SafeSense-VI decode chính xác nhờ preprocessing.'
    },
    
    {
        'id': 2,
        'name': 'Leetspeak Decoding',
        'input': 'ch3t đi',
        'description': 'Giải mã leetspeak (số thay chữ)',
        'traditional': {
            'label': 'CLEAN',
            'confidence': 82.1,
            'color': 'success',
            'reasoning': 'Không nhận diện số "3" trong "ch3t"',
            'raw_output': '"ch3t" is unknown word → Likely misspelling → Safe',
            'issues': [
                '❌ Không convert leetspeak',
                '❌ "ch3t" bị coi là lỗi chính tả',
                '❌ Miss death threat'
            ]
        },
        'safesense': {
            'label': 'HATE',
            'confidence': 91.7,
            'color': 'danger',
            'reasoning': 'Convert "ch3t" → "chết" → Nhận diện death threat',
            'preprocessing_steps': [
                '1️⃣ Input: "ch3t đi"',
                '2️⃣ Leetspeak: "ch3t" → "chết" (3→ê)',
                '3️⃣ Result: "chết đi"',
                '4️⃣ PhoBERT classify → HATE (91.7%)'
            ],
            'raw_output': 'Decoded: "chết đi" → Death threat → HATE',
            'strengths': [
                '✅ Convert leetspeak correctly',
                '✅ Detect death threat',
                '✅ Context-aware classification'
            ]
        },
        'winner': 'safesense',
        'accuracy_gain': '+91.7%',
        'explanation': 'Traditional AI không hiểu leetspeak. SafeSense-VI convert "3"→"ê" nên decode đúng "chết".'
    },
    
    {
        'id': 3,
        'name': 'Teencode Normalization',
        'input': 'vcl ngu vl',
        'description': 'Chuẩn hóa teencode tiếng Việt',
        'traditional': {
            'label': 'CLEAN',
            'confidence': 91.4,
            'color': 'success',
            'reasoning': 'Không hiểu teencode "vcl", "vl"',
            'raw_output': '"vcl" and "vl" are unknown abbreviations → Safe',
            'issues': [
                '❌ Không có teencode dictionary',
                '❌ "vcl", "vl" bị coi là viết tắt thông thường',
                '❌ Completely miss vulgar language'
            ]
        },
        'safesense': {
            'label': 'HATE',
            'confidence': 96.8,
            'color': 'danger',
            'reasoning': 'Normalize teencode → "vãi cả lồn ngu vãi lồn"',
            'preprocessing_steps': [
                '1️⃣ Input: "vcl ngu vl"',
                '2️⃣ Teencode: "vcl" → "vãi cả lồn"',
                '3️⃣ Teencode: "vl" → "vãi lồn"',
                '4️⃣ Result: "vãi cả lồn ngu vãi lồn"',
                '5️⃣ PhoBERT → HATE (96.8%)'
            ],
            'raw_output': 'Decoded: "vãi cả lồn ngu vãi lồn" → Vulgar hate speech → HATE',
            'strengths': [
                '✅ 500+ teencode dictionary',
                '✅ Decode vulgar language',
                '✅ Very high confidence (96.8%)'
            ]
        },
        'winner': 'safesense',
        'accuracy_gain': '+96.8%',
        'explanation': 'Traditional AI hoàn toàn bỏ sót vì không có teencode dict. SafeSense-VI có 500+ teencode → decode chính xác.'
    },
    
    {
        'id': 4,
        'name': 'Context Understanding',
        'input': 'Vụ đó bị tử hình rồi',
        'context': 'Title: Tin tức pháp luật - Cập nhật mới nhất',
        'description': 'Hiểu ngữ cảnh tin tức vs toxic',
        'traditional': {
            'label': 'HATE',
            'confidence': 78.9,
            'color': 'danger',
            'reasoning': 'Thấy từ nhạy cảm "tử hình" → Chặn nhầm',
            'raw_output': 'Contains sensitive word "tử hình" (death penalty) → HATE',
            'issues': [
                '❌ Không có context awareness',
                '❌ Chặn nhầm tin tức',
                '❌ False positive - over-blocking'
            ]
        },
        'safesense': {
            'label': 'CLEAN',
            'confidence': 89.4,
            'color': 'success',
            'reasoning': 'Hiểu context tin tức nhờ Title + </s> separator',
            'preprocessing_steps': [
                '1️⃣ Input: "Vụ đó bị tử hình rồi"',
                '2️⃣ Context: "Tin tức pháp luật..."',
                '3️⃣ Combine: "Tin tức... </s> Vụ đó bị tử hình rồi"',
                '4️⃣ PhoBERT với context → CLEAN (89.4%)'
            ],
            'raw_output': 'Context: News reporting → Factual statement → CLEAN',
            'strengths': [
                '✅ Context-aware với </s> separator',
                '✅ Phân biệt tin tức vs toxic',
                '✅ Tránh false positive'
            ]
        },
        'winner': 'safesense',
        'accuracy_gain': '+89.4%',
        'explanation': 'Traditional AI chặn nhầm vì chỉ nhìn từ "tử hình". SafeSense-VI hiểu context tin tức nhờ Title + separator.'
    },
    
    {
        'id': 5,
        'name': 'Dot Bypass Trick',
        'input': 'đ.ồ n.g.u',
        'description': 'Phát hiện bypass với dấu chấm trong từ',
        'traditional': {
            'label': 'CLEAN',
            'confidence': 85.6,
            'color': 'success',
            'reasoning': 'Không xử lý dấu chấm → Coi là 2 từ riêng biệt',
            'raw_output': 'Tokens: ["đ.ồ", "n.g.u"] → Unknown words → Safe',
            'issues': [
                '❌ Không remove dot bypass',
                '❌ Tokenization bị lỗi',
                '❌ Miss obvious insult'
            ]
        },
        'safesense': {
            'label': 'HATE',
            'confidence': 93.5,
            'color': 'danger',
            'reasoning': 'Remove dots → "đồ ngu" → Toxic insult',
            'preprocessing_steps': [
                '1️⃣ Input: "đ.ồ n.g.u"',
                '2️⃣ Dot bypass: "đ.ồ" → "đồ"',
                '3️⃣ Dot bypass: "n.g.u" → "ngu"',
                '4️⃣ Result: "đồ ngu"',
                '5️⃣ PhoBERT → HATE (93.5%)'
            ],
            'raw_output': 'Decoded: "đồ ngu" → Direct insult → HATE',
            'strengths': [
                '✅ Handle multiple bypass types',
                '✅ Clean tokenization',
                '✅ Accurate detection'
            ]
        },
        'winner': 'safesense',
        'accuracy_gain': '+93.5%',
        'explanation': 'Traditional AI bị lừa bởi dấu chấm. SafeSense-VI có bypass removal nên decode chính xác.'
    },
    
    {
        'id': 6,
        'name': 'Death Metaphor',
        'input': 'đăng xuất đi cho sạch',
        'description': 'Nhận diện ẩn dụ cái chết',
        'traditional': {
            'label': 'CLEAN',
            'confidence': 88.2,
            'color': 'success',
            'reasoning': 'Không hiểu "đăng xuất" là death metaphor',
            'raw_output': '"đăng xuất" means logout → Tech term → Safe',
            'issues': [
                '❌ Không có death metaphor dictionary',
                '❌ Hiểu sai "đăng xuất" = logout',
                '❌ Miss serious hate speech'
            ]
        },
        'safesense': {
            'label': 'HATE',
            'confidence': 92.1,
            'color': 'danger',
            'reasoning': '"đăng xuất" detected as death metaphor → Hate speech',
            'preprocessing_steps': [
                '1️⃣ Input: "đăng xuất đi cho sạch"',
                '2️⃣ Death metaphor detected: "đăng xuất" (ẩn dụ chết)',
                '3️⃣ Context: "cho sạch" → Strong hate signal',
                '4️⃣ PhoBERT → HATE (92.1%)'
            ],
            'raw_output': 'Death metaphor "đăng xuất" + context → Serious hate speech → HATE',
            'strengths': [
                '✅ Death metaphor dictionary',
                '✅ Context-aware detection',
                '✅ Catch indirect threats'
            ]
        },
        'winner': 'safesense',
        'accuracy_gain': '+92.1%',
        'explanation': 'Traditional AI hiểu sai "đăng xuất"=logout. SafeSense-VI nhận diện đây là death metaphor (ẩn dụ chết).'
    },
    
    {
        'id': 7,
        'name': 'Mixed Language + Teencode',
        'input': '3 đê stupid vl',
        'description': 'Xử lý hỗn hợp: leetspeak + tiếng Anh + teencode',
        'traditional': {
            'label': 'TOXIC',
            'confidence': 62.4,
            'color': 'warning',
            'reasoning': 'Nhận "stupid" nhưng miss "3 đê" và "vl"',
            'raw_output': 'Detected: "stupid" → TOXIC (low confidence)',
            'issues': [
                '⚠️ Chỉ catch "stupid"',
                '❌ Miss "3 đê" (leetspeak "ba đê" = LGBT insult)',
                '❌ Miss "vl" (teencode)',
                '❌ Underestimate severity'
            ]
        },
        'safesense': {
            'label': 'HATE',
            'confidence': 95.3,
            'color': 'danger',
            'reasoning': 'Full decode: "ba đê stupid vãi lồn" → Severe hate',
            'preprocessing_steps': [
                '1️⃣ Input: "3 đê stupid vl"',
                '2️⃣ Leetspeak: "3" → "ba" (context: "đê")',
                '3️⃣ English: "stupid" → "ngu" (normalize)',
                '4️⃣ Teencode: "vl" → "vãi lồn"',
                '5️⃣ Result: "ba đê ngu vãi lồn"',
                '6️⃣ PhoBERT → HATE (95.3%)'
            ],
            'raw_output': 'LGBT slur + insult + vulgar → Severe hate speech → HATE',
            'strengths': [
                '✅ Handle mixed language',
                '✅ Multi-step preprocessing',
                '✅ Detect LGBT discrimination',
                '✅ Correct severity assessment'
            ]
        },
        'winner': 'safesense',
        'accuracy_gain': '+32.9% (TOXIC→HATE)',
        'explanation': 'Traditional AI chỉ catch "stupid". SafeSense-VI decode đầy đủ "3 đê"→LGBT slur + "vl"→vulgar → đánh giá đúng mức độ nghiêm trọng.'
    }
]

# Summary statistics
OVERALL_STATS = {
    'traditional': {
        'correct': 1,  # Only case 4 got right result (but wrong reason)
        'wrong': 6,
        'accuracy': 14.3,  # 1/7
        'false_negatives': 6,  # Miss 6 toxic cases
        'false_positives': 1,  # Over-block 1 clean case (case 4)
    },
    'safesense': {
        'correct': 7,
        'wrong': 0,
        'accuracy': 100.0,
        'average_confidence': 93.3,
        'preprocessing_steps': 18,
    },
    'improvement': {
        'accuracy': '+85.7%',
        'avg_confidence': '+30.9%',
        'false_negatives_reduced': '100%',
    }
}

def get_test_case(case_id):
    """Get test case by ID"""
    for case in DUEL_TEST_CASES:
        if case['id'] == case_id:
            return case
    return None

def get_all_cases():
    """Get all test cases"""
    return DUEL_TEST_CASES

def get_summary_stats():
    """Get overall comparison statistics"""
    return OVERALL_STATS
