// 🥊 THE DUEL - SafeSense-VI vs Traditional AI - JavaScript Logic
// Mock data từ Python converted to JavaScript

const DUEL_TEST_CASES = [
    {
        id: 1,
        name: 'Bypass Detection',
        input: 'n.g.u',
        description: 'Phát hiện bypass với dấu chấm ngăn cách',
        traditional: {
            label: 'CLEAN',
            confidence: 87.3,
            color: 'success',
            reasoning: 'Không nhận diện được bypass pattern "n.g.u"',
            rawOutput: 'Text contains dots → Unknown pattern → Safe',
            issues: [
                '❌ Không có preprocessing',
                '❌ Coi "n.g.u" là chuỗi ký tự lạ',
                '❌ Miss toxic content hoàn toàn'
            ]
        },
        safesense: {
            label: 'HATE',
            confidence: 94.2,
            color: 'danger',
            reasoning: 'Decode bypass "n.g.u" → "ngu" → Nhận diện toxic',
            preprocessingSteps: [
                '1️⃣ Input: "n.g.u"',
                '2️⃣ Bypass removal: "n.g.u" → "ngu"',
                '3️⃣ Word segmentation: "ngu"',
                '4️⃣ PhoBERT classify → HATE (94.2%)'
            ],
            rawOutput: 'Decoded text: "ngu" → Offensive insult → HATE',
            strengths: [
                '✅ Decode bypass patterns',
                '✅ Nhận diện đúng toxic content',
                '✅ High confidence (94.2%)'
            ]
        },
        winner: 'safesense',
        accuracyGain: '+94.2%',
        explanation: 'Traditional AI hoàn toàn bỏ sót vì không hiểu bypass. SafeSense-VI decode chính xác nhờ preprocessing.'
    },
    {
        id: 2,
        name: 'Leetspeak Decoding',
        input: 'ch3t đi',
        description: 'Giải mã leetspeak (số thay chữ)',
        traditional: {
            label: 'CLEAN',
            confidence: 82.1,
            color: 'success',
            reasoning: 'Không nhận diện số "3" trong "ch3t"',
            rawOutput: '"ch3t" is unknown word → Likely misspelling → Safe',
            issues: [
                '❌ Không convert leetspeak',
                '❌ "ch3t" bị coi là lỗi chính tả',
                '❌ Miss death threat'
            ]
        },
        safesense: {
            label: 'HATE',
            confidence: 91.7,
            color: 'danger',
            reasoning: 'Convert "ch3t" → "chết" → Nhận diện death threat',
            preprocessingSteps: [
                '1️⃣ Input: "ch3t đi"',
                '2️⃣ Leetspeak: "ch3t" → "chết" (3→ê)',
                '3️⃣ Result: "chết đi"',
                '4️⃣ PhoBERT classify → HATE (91.7%)'
            ],
            rawOutput: 'Decoded: "chết đi" → Death threat → HATE',
            strengths: [
                '✅ Convert leetspeak correctly',
                '✅ Detect death threat',
                '✅ Context-aware classification'
            ]
        },
        winner: 'safesense',
        accuracyGain: '+91.7%',
        explanation: 'Traditional AI không hiểu leetspeak. SafeSense-VI convert "3"→"ê" nên decode đúng "chết".'
    },
    {
        id: 3,
        name: 'Teencode Normalization',
        input: 'vcl ngu vl',
        description: 'Chuẩn hóa teencode tiếng Việt',
        traditional: {
            label: 'CLEAN',
            confidence: 91.4,
            color: 'success',
            reasoning: 'Không hiểu teencode "vcl", "vl"',
            rawOutput: '"vcl" and "vl" are unknown abbreviations → Safe',
            issues: [
                '❌ Không có teencode dictionary',
                '❌ "vcl", "vl" bị coi là viết tắt thông thường',
                '❌ Completely miss vulgar language'
            ]
        },
        safesense: {
            label: 'HATE',
            confidence: 96.8,
            color: 'danger',
            reasoning: 'Normalize teencode → "vãi cả lồn ngu vãi lồn"',
            preprocessingSteps: [
                '1️⃣ Input: "vcl ngu vl"',
                '2️⃣ Teencode: "vcl" → "vãi cả lồn"',
                '3️⃣ Teencode: "vl" → "vãi lồn"',
                '4️⃣ Result: "vãi cả lồn ngu vãi lồn"',
                '5️⃣ PhoBERT → HATE (96.8%)'
            ],
            rawOutput: 'Decoded: "vãi cả lồn ngu vãi lồn" → Vulgar hate speech → HATE',
            strengths: [
                '✅ 500+ teencode dictionary',
                '✅ Decode vulgar language',
                '✅ Very high confidence (96.8%)'
            ]
        },
        winner: 'safesense',
        accuracyGain: '+96.8%',
        explanation: 'Traditional AI hoàn toàn bỏ sót vì không có teencode dict. SafeSense-VI có 500+ teencode → decode chính xác.'
    },
    {
        id: 4,
        name: 'Context Understanding',
        input: 'Vụ đó bị tử hình rồi',
        context: 'Title: Tin tức pháp luật - Cập nhật mới nhất',
        description: 'Hiểu ngữ cảnh tin tức vs toxic',
        traditional: {
            label: 'HATE',
            confidence: 78.9,
            color: 'danger',
            reasoning: 'Thấy từ nhạy cảm "tử hình" → Chặn nhầm',
            rawOutput: 'Contains sensitive word "tử hình" (death penalty) → HATE',
            issues: [
                '❌ Không có context awareness',
                '❌ Chặn nhầm tin tức',
                '❌ False positive - over-blocking'
            ]
        },
        safesense: {
            label: 'CLEAN',
            confidence: 89.4,
            color: 'success',
            reasoning: 'Hiểu context tin tức nhờ Title + </s> separator',
            preprocessingSteps: [
                '1️⃣ Input: "Vụ đó bị tử hình rồi"',
                '2️⃣ Context: "Tin tức pháp luật..."',
                '3️⃣ Combine: "Tin tức... </s> Vụ đó bị tử hình rồi"',
                '4️⃣ PhoBERT với context → CLEAN (89.4%)'
            ],
            rawOutput: 'Context: News reporting → Factual statement → CLEAN',
            strengths: [
                '✅ Context-aware với </s> separator',
                '✅ Phân biệt tin tức vs toxic',
                '✅ Tránh false positive'
            ]
        },
        winner: 'safesense',
        accuracyGain: '+89.4%',
        explanation: 'Traditional AI chặn nhầm vì chỉ nhìn từ "tử hình". SafeSense-VI hiểu context tin tức nhờ Title + separator.'
    },
    {
        id: 5,
        name: 'Dot Bypass Trick',
        input: 'đ.ồ n.g.u',
        description: 'Phát hiện bypass với dấu chấm trong từ',
        traditional: {
            label: 'CLEAN',
            confidence: 85.6,
            color: 'success',
            reasoning: 'Không xử lý dấu chấm → Coi là 2 từ riêng biệt',
            rawOutput: 'Tokens: ["đ.ồ", "n.g.u"] → Unknown words → Safe',
            issues: [
                '❌ Không remove dot bypass',
                '❌ Tokenization bị lỗi',
                '❌ Miss obvious insult'
            ]
        },
        safesense: {
            label: 'HATE',
            confidence: 93.5,
            color: 'danger',
            reasoning: 'Remove dots → "đồ ngu" → Toxic insult',
            preprocessingSteps: [
                '1️⃣ Input: "đ.ồ n.g.u"',
                '2️⃣ Dot bypass: "đ.ồ" → "đồ"',
                '3️⃣ Dot bypass: "n.g.u" → "ngu"',
                '4️⃣ Result: "đồ ngu"',
                '5️⃣ PhoBERT → HATE (93.5%)'
            ],
            rawOutput: 'Decoded: "đồ ngu" → Direct insult → HATE',
            strengths: [
                '✅ Handle multiple bypass types',
                '✅ Clean tokenization',
                '✅ Accurate detection'
            ]
        },
        winner: 'safesense',
        accuracyGain: '+93.5%',
        explanation: 'Traditional AI bị lừa bởi dấu chấm. SafeSense-VI có bypass removal nên decode chính xác.'
    },
    {
        id: 6,
        name: 'Death Metaphor',
        input: 'đăng xuất đi cho sạch',
        description: 'Nhận diện ẩn dụ cái chết',
        traditional: {
            label: 'CLEAN',
            confidence: 88.2,
            color: 'success',
            reasoning: 'Không hiểu "đăng xuất" là death metaphor',
            rawOutput: '"đăng xuất" means logout → Tech term → Safe',
            issues: [
                '❌ Không có death metaphor dictionary',
                '❌ Hiểu sai "đăng xuất" = logout',
                '❌ Miss serious hate speech'
            ]
        },
        safesense: {
            label: 'HATE',
            confidence: 92.1,
            color: 'danger',
            reasoning: '"đăng xuất" detected as death metaphor → Hate speech',
            preprocessingSteps: [
                '1️⃣ Input: "đăng xuất đi cho sạch"',
                '2️⃣ Death metaphor detected: "đăng xuất" (ẩn dụ chết)',
                '3️⃣ Context: "cho sạch" → Strong hate signal',
                '4️⃣ PhoBERT → HATE (92.1%)'
            ],
            rawOutput: 'Death metaphor "đăng xuất" + context → Serious hate speech → HATE',
            strengths: [
                '✅ Death metaphor dictionary',
                '✅ Context-aware detection',
                '✅ Catch indirect threats'
            ]
        },
        winner: 'safesense',
        accuracyGain: '+92.1%',
        explanation: 'Traditional AI hiểu sai "đăng xuất"=logout. SafeSense-VI nhận diện đây là death metaphor (ẩn dụ chết).'
    },
    {
        id: 7,
        name: 'Mixed Language + Teencode',
        input: '3 đê stupid vl',
        description: 'Xử lý hỗn hợp: leetspeak + tiếng Anh + teencode',
        traditional: {
            label: 'TOXIC',
            confidence: 62.4,
            color: 'warning',
            reasoning: 'Nhận "stupid" nhưng miss "3 đê" và "vl"',
            rawOutput: 'Detected: "stupid" → TOXIC (low confidence)',
            issues: [
                '⚠️ Chỉ catch "stupid"',
                '❌ Miss "3 đê" (leetspeak "ba đê" = LGBT insult)',
                '❌ Miss "vl" (teencode)',
                '❌ Underestimate severity'
            ]
        },
        safesense: {
            label: 'HATE',
            confidence: 95.3,
            color: 'danger',
            reasoning: 'Full decode: "ba đê stupid vãi lồn" → Severe hate',
            preprocessingSteps: [
                '1️⃣ Input: "3 đê stupid vl"',
                '2️⃣ Leetspeak: "3" → "ba" (context: "đê")',
                '3️⃣ English: "stupid" → "ngu" (normalize)',
                '4️⃣ Teencode: "vl" → "vãi lồn"',
                '5️⃣ Result: "ba đê ngu vãi lồn"',
                '6️⃣ PhoBERT → HATE (95.3%)'
            ],
            rawOutput: 'LGBT slur + insult + vulgar → Severe hate speech → HATE',
            strengths: [
                '✅ Handle mixed language',
                '✅ Multi-step preprocessing',
                '✅ Detect LGBT discrimination',
                '✅ Correct severity assessment'
            ]
        },
        winner: 'safesense',
        accuracyGain: '+32.9% (TOXIC→HATE)',
        explanation: 'Traditional AI chỉ catch "stupid". SafeSense-VI decode đầy đủ "3 đê"→LGBT slur + "vl"→vulgar → đánh giá đúng mức độ nghiêm trọng.'
    }
];

const OVERALL_STATS = {
    traditional: {
        correct: 1,
        wrong: 6,
        accuracy: 14.3,
        falseNegatives: 6,
        falsePositives: 1,
    },
    safesense: {
        correct: 7,
        wrong: 0,
        accuracy: 100.0,
        averageConfidence: 93.3,
        preprocessingSteps: 18,
    },
    improvement: {
        accuracy: '+85.7%',
        avgConfidence: '+30.9%',
        falseNegativesReduced: '100%',
    }
};

// DOM Elements
let casesGrid;
let commentInput;
let contextInput;
let analyzeBtn;
let arenaSection;
let arenaInput;
let traditionalResult;
let safesenseResult;
let safesenseSteps;
let traditionalIssues;
let safesenseStrengths;
let winnerSection;
let winnerName;
let winnerStats;
let explanationText;
let resetBtn;

// State
let currentTestCase = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initDOMElements();
    renderTestCases();
    attachEventListeners();
});

function initDOMElements() {
    casesGrid = document.getElementById('casesGrid');
    commentInput = document.getElementById('commentInput');
    contextInput = document.getElementById('contextInput');
    analyzeBtn = document.getElementById('analyzeBtn');
    arenaSection = document.getElementById('arenaSection');
    arenaInput = document.getElementById('arenaInput');
    traditionalResult = document.getElementById('traditionalResult');
    safesenseResult = document.getElementById('safesenseResult');
    safesenseSteps = document.getElementById('safesenseSteps');
    traditionalIssues = document.getElementById('traditionalIssues');
    safesenseStrengths = document.getElementById('safesenseStrengths');
    winnerSection = document.getElementById('winnerSection');
    winnerName = document.getElementById('winnerName');
    winnerStats = document.getElementById('winnerStats');
    explanationText = document.getElementById('explanationText');
    resetBtn = document.getElementById('resetBtn');
}

function renderTestCases() {
    casesGrid.innerHTML = DUEL_TEST_CASES.map(testCase => `
        <div class="case-card" data-case-id="${testCase.id}">
            <div class="case-header">
                <div class="case-number">${testCase.id}</div>
                <div class="case-name">${testCase.name}</div>
            </div>
            <div class="case-preview">"${testCase.input}"</div>
            <div class="case-description">${testCase.description}</div>
        </div>
    `).join('');
}

function attachEventListeners() {
    // Test case selection
    casesGrid.addEventListener('click', (e) => {
        const card = e.target.closest('.case-card');
        if (card) {
            const caseId = parseInt(card.dataset.caseId);
            selectTestCase(caseId);
        }
    });

    // Analyze button
    analyzeBtn.addEventListener('click', handleAnalyze);

    // Reset button
    resetBtn.addEventListener('click', resetDuel);

    // Enter key
    commentInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleAnalyze();
        }
    });
}

function selectTestCase(caseId) {
    const testCase = DUEL_TEST_CASES.find(tc => tc.id === caseId);
    if (testCase) {
        commentInput.value = testCase.input;
        contextInput.value = testCase.context || '';
        currentTestCase = testCase;
        
        // Highlight selected case
        document.querySelectorAll('.case-card').forEach(card => {
            card.style.borderColor = '';
            card.style.boxShadow = '';
        });
        const selectedCard = document.querySelector(`[data-case-id="${caseId}"]`);
        selectedCard.style.borderColor = 'var(--safesense-color)';
        selectedCard.style.boxShadow = 'var(--glow-safesense)';
    }
}

async function handleAnalyze() {
    const input = commentInput.value.trim();
    if (!input) {
        alert('⚠️ Vui lòng nhập comment để test!');
        return;
    }

    // If no test case selected, find matching or use custom
    if (!currentTestCase) {
        const matchingCase = DUEL_TEST_CASES.find(tc => tc.input === input);
        if (matchingCase) {
            currentTestCase = matchingCase;
        } else {
            // Custom input - use generic analysis (for demo purposes, show first case pattern)
            alert('💡 Demo mode: Chọn một trong 7 test cases để xem so sánh chi tiết!');
            return;
        }
    }

    // Show arena
    arenaSection.style.display = 'block';
    arenaInput.textContent = `"${input}"`;
    if (contextInput.value) {
        arenaInput.innerHTML += `<br><small style="opacity: 0.8">Context: ${contextInput.value}</small>`;
    }

    // Scroll to arena
    arenaSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Reset results
    winnerSection.style.display = 'none';
    resetResults();

    // Simulate analysis
    await simulateDuel(currentTestCase);
}

function resetResults() {
    // Reset Traditional AI
    const tradLabel = traditionalResult.querySelector('.label-badge');
    tradLabel.textContent = 'Đang phân tích...';
    tradLabel.className = 'label-badge';
    
    const tradConfBar = traditionalResult.querySelector('.confidence-fill');
    tradConfBar.style.width = '0%';
    
    traditionalResult.querySelector('.confidence-value').textContent = '--%';
    traditionalResult.querySelector('.reasoning-text').textContent = '--';
    traditionalResult.querySelector('.output-code').textContent = '--';
    
    traditionalIssues.querySelector('.issues-list').innerHTML = '';

    // Reset SafeSense-VI
    const safeLabel = safesenseResult.querySelector('.label-badge');
    safeLabel.textContent = 'Đang phân tích...';
    safeLabel.className = 'label-badge';
    
    const safeConfBar = safesenseResult.querySelector('.confidence-fill');
    safeConfBar.style.width = '0%';
    
    safesenseResult.querySelector('.confidence-value').textContent = '--%';
    safesenseResult.querySelector('.reasoning-text').textContent = '--';
    safesenseResult.querySelector('.output-code').textContent = '--';
    
    safesenseSteps.innerHTML = '';
    safesenseStrengths.querySelector('.strengths-list').innerHTML = '';
}

async function simulateDuel(testCase) {
    // Step 1: Show Traditional AI result (fast, no preprocessing)
    await sleep(800);
    displayTraditionalResult(testCase.traditional);
    
    // Step 2: Show SafeSense preprocessing steps (one by one)
    for (let i = 0; i < testCase.safesense.preprocessingSteps.length; i++) {
        await sleep(600);
        addPreprocessingStep(testCase.safesense.preprocessingSteps[i], i);
    }
    
    // Step 3: Show SafeSense result
    await sleep(800);
    displaySafeSenseResult(testCase.safesense);
    
    // Step 4: Show winner
    await sleep(1000);
    displayWinner(testCase);
}

function displayTraditionalResult(result) {
    const tradLabel = traditionalResult.querySelector('.label-badge');
    tradLabel.textContent = result.label;
    tradLabel.className = `label-badge ${result.color}`;
    
    const tradConfBar = traditionalResult.querySelector('.confidence-fill');
    tradConfBar.style.width = `${result.confidence}%`;
    
    traditionalResult.querySelector('.confidence-value').textContent = `${result.confidence}%`;
    traditionalResult.querySelector('.reasoning-text').textContent = result.reasoning;
    traditionalResult.querySelector('.output-code').textContent = result.rawOutput;
    
    // Show issues
    const issuesList = traditionalIssues.querySelector('.issues-list');
    issuesList.innerHTML = result.issues.map(issue => `<li>${issue}</li>`).join('');
}

function addPreprocessingStep(step, index) {
    const stepDiv = document.createElement('div');
    stepDiv.className = 'step-item';
    stepDiv.textContent = step;
    stepDiv.style.animationDelay = `${index * 0.1}s`;
    safesenseSteps.appendChild(stepDiv);
}

function displaySafeSenseResult(result) {
    const safeLabel = safesenseResult.querySelector('.label-badge');
    safeLabel.textContent = result.label;
    safeLabel.className = `label-badge ${result.color}`;
    
    const safeConfBar = safesenseResult.querySelector('.confidence-fill');
    safeConfBar.style.width = `${result.confidence}%`;
    
    safesenseResult.querySelector('.confidence-value').textContent = `${result.confidence}%`;
    safesenseResult.querySelector('.reasoning-text').textContent = result.reasoning;
    safesenseResult.querySelector('.output-code').textContent = result.rawOutput;
    
    // Show strengths
    const strengthsList = safesenseStrengths.querySelector('.strengths-list');
    strengthsList.innerHTML = result.strengths.map(strength => `<li>${strength}</li>`).join('');
}

function displayWinner(testCase) {
    winnerSection.style.display = 'block';
    winnerName.textContent = testCase.winner === 'safesense' ? '🛡️ SafeSense-VI' : '🤖 Traditional AI';
    winnerStats.textContent = `Accuracy Gain: ${testCase.accuracyGain}`;
    explanationText.textContent = testCase.explanation;
    
    // Scroll to winner
    setTimeout(() => {
        winnerSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

function resetDuel() {
    arenaSection.style.display = 'none';
    currentTestCase = null;
    commentInput.value = '';
    contextInput.value = '';
    
    // Remove highlights
    document.querySelectorAll('.case-card').forEach(card => {
        card.style.borderColor = '';
        card.style.boxShadow = '';
    });
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
