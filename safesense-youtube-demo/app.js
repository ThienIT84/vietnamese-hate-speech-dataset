// SafeSense Kids Guardian - Main Application Logic

// DOM Elements
const videoUrlInput = document.getElementById('videoUrl');
const analyzeBtn = document.getElementById('analyzeBtn');
const samplesGrid = document.getElementById('samplesGrid');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const analyzeAnotherBtn = document.getElementById('analyzeAnotherBtn');
const shareBtn = document.getElementById('shareBtn');

// State
let currentVideo = null;

/**
 * Initialize application
 */
function init() {
    console.log('SafeSense Kids Guardian - Demo Version');
    
    // Render sample videos
    renderSampleVideos();
    
    // Add event listeners
    analyzeBtn.addEventListener('click', handleAnalyzeClick);
    videoUrlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleAnalyzeClick();
        }
    });
    
    analyzeAnotherBtn.addEventListener('click', resetToInput);
    shareBtn.addEventListener('click', handleShare);
}

/**
 * Render sample videos
 */
function renderSampleVideos() {
    samplesGrid.innerHTML = '';
    
    MOCK_VIDEOS.forEach(video => {
        const level = SAFETY_LEVELS[video.level];
        const card = document.createElement('div');
        card.className = 'sample-card';
        card.onclick = () => analyzeVideo(video.id);
        
        const shortsBadge = video.isShort ? '<span class="shorts-badge">📱 Shorts</span>' : '';
        
        card.innerHTML = `
            <img src="${video.thumbnail}" alt="${video.title}">
            <h4>${video.title}</h4>
            <p>${video.channel}</p>
            ${shortsBadge}
            <span class="sample-badge ${level.badge}">
                ${level.emoji} ${level.text}
            </span>
        `;
        
        samplesGrid.appendChild(card);
    });
}

/**
 * Handle analyze button click
 */
function handleAnalyzeClick() {
    const url = videoUrlInput.value.trim();
    
    if (!url) {
        alert('Vui lòng nhập link YouTube!');
        return;
    }
    
    const videoId = extractVideoId(url);
    
    if (!videoId) {
        alert('Link YouTube không hợp lệ!\n\nVí dụ đúng:\n- https://www.youtube.com/watch?v=dQw4w9WgXcQ\n- https://youtu.be/dQw4w9WgXcQ');
        return;
    }
    
    analyzeVideo(videoId);
}

/**
 * Analyze video
 * @param {string} videoId - YouTube video ID
 */
async function analyzeVideo(videoId) {
    console.log(`Analyzing video: ${videoId}`);
    
    // Hide input sections
    document.querySelector('.input-section').classList.add('hidden');
    document.querySelector('.samples-section').classList.add('hidden');
    resultsSection.classList.add('hidden');
    
    // Show loading
    loadingSection.classList.remove('hidden');
    
    // Simulate loading steps
    await simulateLoadingSteps();
    
    // Get video data
    const videoData = getMockVideoData(videoId);
    currentVideo = videoData;
    
    // Display results
    displayResults(videoData);
    
    // Hide loading, show results
    loadingSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Simulate loading steps with animation
 */
async function simulateLoadingSteps() {
    const steps = ['step1', 'step2', 'step3', 'step4'];
    
    for (let i = 0; i < steps.length; i++) {
        // Remove active from all
        steps.forEach(s => {
            document.getElementById(s).classList.remove('active');
        });
        
        // Add active to current
        document.getElementById(steps[i]).classList.add('active');
        
        // Wait before next step
        await new Promise(resolve => setTimeout(resolve, 800));
    }
}

/**
 * Display analysis results
 * @param {Object} videoData - Video data with analysis results
 */
function displayResults(videoData) {
    const { title, channel, thumbnail, stats, score, level } = videoData;
    const levelConfig = SAFETY_LEVELS[level];
    
    // Video info
    document.getElementById('videoThumbnail').src = thumbnail;
    document.getElementById('videoTitle').textContent = title;
    document.getElementById('videoChannel').textContent = channel;
    
    // Safety score
    const scoreCircle = document.getElementById('scoreCircle');
    scoreCircle.style.borderColor = levelConfig.color;
    
    document.getElementById('scoreEmoji').textContent = levelConfig.emoji;
    document.getElementById('scoreValue').textContent = score;
    document.getElementById('scoreLabel').textContent = levelConfig.text;
    
    // Score description
    document.getElementById('scoreDescription').innerHTML = `
        <h4>${levelConfig.emoji} ${levelConfig.description}</h4>
        <p style="color: var(--text-secondary); margin-top: 10px;">
            Dựa trên phân tích ${stats.total_comments} bình luận bằng model PhoBERT-v2
        </p>
    `;
    
    // Statistics
    document.getElementById('totalComments').textContent = stats.total_comments;
    
    // Clean bar
    document.getElementById('cleanValue').textContent = `${stats.clean} (${stats.clean_pct}%)`;
    const cleanBar = document.getElementById('cleanBar');
    cleanBar.style.width = '0%';
    setTimeout(() => {
        cleanBar.style.width = `${stats.clean_pct}%`;
    }, 100);
    
    // Toxic bar
    document.getElementById('toxicValue').textContent = `${stats.toxic} (${stats.toxic_pct}%)`;
    const toxicBar = document.getElementById('toxicBar');
    toxicBar.style.width = '0%';
    setTimeout(() => {
        toxicBar.style.width = `${stats.toxic_pct}%`;
    }, 200);
    
    // Hate bar
    document.getElementById('hateValue').textContent = `${stats.hate} (${stats.hate_pct}%)`;
    const hateBar = document.getElementById('hateBar');
    hateBar.style.width = '0%';
    setTimeout(() => {
        hateBar.style.width = `${stats.hate_pct}%`;
    }, 300);
    
    // Concerns
    const concerns = analyzeConcerns(stats);
    const concernsSection = document.getElementById('concernsSection');
    
    if (concerns.length > 0) {
        concernsSection.innerHTML = `
            <h4>⚠️ Các vấn đề phát hiện:</h4>
            ${concerns.map(c => `
                <div class="concern-item">
                    ${c.icon} ${c.message}
                </div>
            `).join('')}
        `;
        concernsSection.style.display = 'block';
    } else {
        concernsSection.style.display = 'none';
    }
    
    // Recommendation
    document.getElementById('recommendation').textContent = levelConfig.recommendation;
}

/**
 * Reset to input section
 */
function resetToInput() {
    // Show input sections
    document.querySelector('.input-section').classList.remove('hidden');
    document.querySelector('.samples-section').classList.remove('hidden');
    
    // Hide results
    resultsSection.classList.add('hidden');
    
    // Clear input
    videoUrlInput.value = '';
    videoUrlInput.focus();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Handle share button
 */
function handleShare() {
    if (!currentVideo) return;
    
    const { title, score, level } = currentVideo;
    const levelConfig = SAFETY_LEVELS[level];
    
    const message = `SafeSense Kids Guardian - Kết quả phân tích\n\n` +
                   `📹 Video: ${title}\n` +
                   `${levelConfig.emoji} Điểm an toàn: ${score}/100\n` +
                   `🏷️ Mức độ: ${levelConfig.text}\n\n` +
                   `💡 Khuyến nghị: ${levelConfig.recommendation}\n\n` +
                   `Phân tích bởi SafeSense AI - F1: 0.7995 | Accuracy: 80.87%`;
    
    // Try to use Web Share API
    if (navigator.share) {
        navigator.share({
            title: 'SafeSense Kids Guardian - Kết quả phân tích',
            text: message
        }).catch(err => {
            console.log('Share cancelled:', err);
        });
    } else {
        // Fallback: Copy to clipboard
        navigator.clipboard.writeText(message).then(() => {
            alert('✅ Đã copy kết quả vào clipboard!');
        }).catch(() => {
            // Show in alert if clipboard fails
            alert(message);
        });
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
