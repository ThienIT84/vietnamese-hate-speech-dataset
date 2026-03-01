/**
 * SafeSense Kids Guardian - Popup Script
 * Manages popup UI and statistics
 */

document.addEventListener('DOMContentLoaded', async () => {
  console.log('Popup loaded');

  // Load and display statistics
  await loadStatistics();

  // Setup event listeners
  setupEventListeners();
});

/**
 * Load cache statistics
 */
async function loadStatistics() {
  try {
    const result = await chrome.storage.local.get(null);
    
    let videosAnalyzed = 0;
    let safeVideos = 0;
    let warningVideos = 0;
    let totalSize = 0;

    for (const [key, value] of Object.entries(result)) {
      if (key.startsWith('safesense_') && value.score !== undefined) {
        videosAnalyzed++;
        
        if (value.score >= 70) {
          safeVideos++;
        } else {
          warningVideos++;
        }
        
        totalSize += JSON.stringify(value).length;
      }
    }

    // Update UI
    document.getElementById('videosAnalyzed').textContent = videosAnalyzed;
    document.getElementById('safeVideos').textContent = safeVideos;
    document.getElementById('warningVideos').textContent = warningVideos;
    document.getElementById('cacheSize').textContent = (totalSize / 1024).toFixed(1) + ' KB';

  } catch (error) {
    console.error('Error loading statistics:', error);
  }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
  // Clear cache button
  document.getElementById('clearCache').addEventListener('click', async () => {
    if (confirm('Bạn có chắc muốn xóa toàn bộ cache?')) {
      const result = await chrome.storage.local.get(null);
      const keysToRemove = Object.keys(result).filter(key => 
        key.startsWith('safesense_')
      );
      
      await chrome.storage.local.remove(keysToRemove);
      
      alert(`Đã xóa ${keysToRemove.length} video từ cache`);
      await loadStatistics();
    }
  });

  // View guide button
  document.getElementById('viewGuide').addEventListener('click', () => {
    chrome.tabs.create({
      url: 'https://github.com/yourusername/safesense-kids-guardian#readme'
    });
  });

  // About button
  document.getElementById('aboutBtn').addEventListener('click', () => {
    alert(
      'SafeSense Kids Guardian v1.0.0\n\n' +
      'Browser extension bảo vệ trẻ em trên YouTube\n' +
      'Sử dụng AI model PhoBERT-v2\n\n' +
      'Metrics:\n' +
      '- F1 Score: 0.7995\n' +
      '- Accuracy: 80.87%\n' +
      '- Dataset: 7,626 samples\n\n' +
      'Developed by: SafeSense Team\n' +
      'License: MIT'
    );
  });

  // Toggle buttons
  const toggleAutoAnalyze = document.getElementById('toggleAutoAnalyze');
  const toggleWarnings = document.getElementById('toggleWarnings');

  toggleAutoAnalyze.addEventListener('click', () => {
    toggleAutoAnalyze.classList.toggle('active');
    const enabled = toggleAutoAnalyze.classList.contains('active');
    chrome.storage.local.set({ 'safesense_auto_analyze': enabled });
  });

  toggleWarnings.addEventListener('click', () => {
    toggleWarnings.classList.toggle('active');
    const enabled = toggleWarnings.classList.contains('active');
    chrome.storage.local.set({ 'safesense_show_warnings': enabled });
  });

  // Load current settings
  chrome.storage.local.get(['safesense_auto_analyze', 'safesense_show_warnings'], (result) => {
    if (result.safesense_auto_analyze === false) {
      toggleAutoAnalyze.classList.remove('active');
    }
    if (result.safesense_show_warnings === false) {
      toggleWarnings.classList.remove('active');
    }
  });
}
