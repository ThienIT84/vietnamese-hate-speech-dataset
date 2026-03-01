/**
 * SafeSense Kids Guardian - Content Script
 * Injected into YouTube video pages to analyze and display safety information
 */

(function() {
  'use strict';

  console.log('SafeSense Kids Guardian loaded');

  let currentVideoId = null;
  let overlayElement = null;

  /**
   * Extract video ID from URL
   * @returns {string|null} Video ID or null
   */
  function getVideoId() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('v');
  }

  /**
   * Create loading overlay
   * @returns {HTMLElement} Loading element
   */
  function createLoadingOverlay() {
    const loading = document.createElement('div');
    loading.id = 'safesense-loading';
    loading.className = 'safesense-overlay';
    loading.innerHTML = `
      <div class="safesense-card safesense-loading-card">
        <div class="safesense-spinner"></div>
        <h3>🛡️ SafeSense Kids Guardian</h3>
        <p>Đang phân tích độ an toàn của video...</p>
        <p class="safesense-subtext">Đang kiểm tra bình luận</p>
      </div>
    `;
    return loading;
  }

  /**
   * Create safety report overlay
   * @param {Object} report - Safety report object
   * @returns {HTMLElement} Overlay element
   */
  function createSafetyOverlay(report) {
    const overlay = document.createElement('div');
    overlay.id = 'safesense-overlay';
    overlay.className = `safesense-overlay safesense-${report.level.level.toLowerCase()}`;
    
    const { score, level, stats, recommendation } = report;
    const concerns = SafetyScorer.analyzeConcerns(stats);

    overlay.innerHTML = `
      <div class="safesense-card">
        <div class="safesense-header">
          <h3>🛡️ SafeSense Kids Guardian</h3>
          <button class="safesense-close" title="Đóng">&times;</button>
        </div>
        
        <div class="safesense-score-section">
          <div class="safesense-score-circle" style="border-color: ${SafetyScorer.getScoreColor(score)}">
            <div class="safesense-score-emoji">${level.emoji}</div>
            <div class="safesense-score-value">${score}/100</div>
            <div class="safesense-score-label">${level.text}</div>
          </div>
        </div>

        <div class="safesense-stats-section">
          <p class="safesense-analyzed">Đã phân tích: <strong>${stats.total_comments} bình luận</strong></p>
          
          <div class="safesense-stats-bars">
            <div class="safesense-stat-row">
              <span class="safesense-stat-label">✅ An toàn</span>
              <div class="safesense-stat-bar">
                <div class="safesense-stat-fill safesense-clean" 
                     style="width: ${stats.clean_pct}%">
                  ${stats.clean} (${stats.clean_pct}%)
                </div>
              </div>
            </div>
            
            <div class="safesense-stat-row">
              <span class="safesense-stat-label">⚠️ Toxic</span>
              <div class="safesense-stat-bar">
                <div class="safesense-stat-fill safesense-toxic" 
                     style="width: ${stats.toxic_pct}%">
                  ${stats.toxic} (${stats.toxic_pct}%)
                </div>
              </div>
            </div>
            
            <div class="safesense-stat-row">
              <span class="safesense-stat-label">🔴 Hate</span>
              <div class="safesense-stat-bar">
                <div class="safesense-stat-fill safesense-hate" 
                     style="width: ${stats.hate_pct}%">
                  ${stats.hate} (${stats.hate_pct}%)
                </div>
              </div>
            </div>
          </div>
        </div>

        ${concerns.length > 0 ? `
          <div class="safesense-concerns">
            <p class="safesense-concerns-title">⚠️ Lưu ý:</p>
            ${concerns.map(c => `
              <div class="safesense-concern-item">
                ${c.icon} ${c.message}
              </div>
            `).join('')}
          </div>
        ` : ''}

        <div class="safesense-recommendation">
          <p><strong>Khuyến nghị:</strong></p>
          <p>${recommendation}</p>
        </div>

        <div class="safesense-actions">
          <button class="safesense-btn safesense-btn-primary" id="safesense-details">
            📊 Chi tiết
          </button>
          <button class="safesense-btn safesense-btn-secondary" id="safesense-hide-comments">
            🙈 Ẩn bình luận
          </button>
        </div>

        <div class="safesense-footer">
          <small>Phân tích bởi SafeSense AI | F1: 0.7995 | Độ chính xác: 80.87%</small>
        </div>
      </div>
    `;

    // Add event listeners
    const closeBtn = overlay.querySelector('.safesense-close');
    closeBtn.addEventListener('click', () => {
      overlay.remove();
    });

    const hideCommentsBtn = overlay.querySelector('#safesense-hide-comments');
    hideCommentsBtn.addEventListener('click', () => {
      toggleComments(false);
      hideCommentsBtn.textContent = '👁️ Hiện bình luận';
      hideCommentsBtn.onclick = () => {
        toggleComments(true);
        hideCommentsBtn.textContent = '🙈 Ẩn bình luận';
      };
    });

    const detailsBtn = overlay.querySelector('#safesense-details');
    detailsBtn.addEventListener('click', () => {
      showDetailedReport(report);
    });

    return overlay;
  }

  /**
   * Toggle YouTube comments visibility
   * @param {boolean} show - Show or hide
   */
  function toggleComments(show) {
    const commentsSection = document.querySelector('#comments');
    if (commentsSection) {
      commentsSection.style.display = show ? '' : 'none';
    }
  }

  /**
   * Show detailed report in modal
   * @param {Object} report - Safety report
   */
  function showDetailedReport(report) {
    alert(`Báo cáo chi tiết:\n\n` +
          `Điểm an toàn: ${report.score}/100\n` +
          `Tổng bình luận: ${report.stats.total_comments}\n` +
          `Clean: ${report.stats.clean} (${report.stats.clean_pct}%)\n` +
          `Toxic: ${report.stats.toxic} (${report.stats.toxic_pct}%)\n` +
          `Hate: ${report.stats.hate} (${report.stats.hate_pct}%)\n\n` +
          `Khuyến nghị: ${report.recommendation}`);
  }

  /**
   * Insert overlay into page
   * @param {HTMLElement} element - Element to insert
   */
  function insertOverlay(element) {
    // Remove existing overlay
    if (overlayElement) {
      overlayElement.remove();
    }

    // Try multiple insertion strategies
    const strategies = [
      // Strategy 1: Below video player (most reliable)
      () => {
        const player = document.querySelector('#movie_player');
        if (player && player.parentElement) {
          player.parentElement.insertAdjacentElement('afterend', element);
          return true;
        }
        return false;
      },
      
      // Strategy 2: Above secondary column
      () => {
        const secondary = document.querySelector('#secondary');
        if (secondary && secondary.parentElement) {
          secondary.parentElement.insertBefore(element, secondary);
          return true;
        }
        return false;
      },
      
      // Strategy 3: Below primary info
      () => {
        const primary = document.querySelector('#primary');
        if (primary) {
          primary.insertAdjacentElement('afterbegin', element);
          return true;
        }
        return false;
      },
      
      // Strategy 4: Top of content
      () => {
        const content = document.querySelector('#content');
        if (content) {
          content.insertAdjacentElement('afterbegin', element);
          return true;
        }
        return false;
      }
    ];

    // Try each strategy
    for (const strategy of strategies) {
      try {
        if (strategy()) {
          overlayElement = element;
          console.log('Successfully inserted overlay');
          return;
        }
      } catch (error) {
        console.debug('Strategy failed:', error.message);
      }
    }

    console.error('Could not find insertion point for overlay');
    // Last resort: append to body
    try {
      document.body.appendChild(element);
      overlayElement = element;
      element.style.position = 'fixed';
      element.style.top = '80px';
      element.style.left = '50%';
      element.style.transform = 'translateX(-50%)';
      element.style.zIndex = '9999';
      element.style.maxWidth = '90%';
    } catch (error) {
      console.error('Failed to insert overlay anywhere:', error);
    }
  }

  /**
   * Analyze current video
   */
  async function analyzeCurrentVideo() {
    const videoId = getVideoId();
    
    if (!videoId) {
      console.log('No video ID found');
      return;
    }

    if (videoId === currentVideoId) {
      console.log('Video already analyzed');
      return;
    }

    currentVideoId = videoId;
    console.log(`Analyzing video: ${videoId}`);

    // Wait for page to be ready
    await waitForElement('#movie_player', 5000);

    // Show loading
    const loading = createLoadingOverlay();
    insertOverlay(loading);

    try {
      // Check cache first
      const cached = await CacheManager.get(videoId);
      
      if (cached) {
        console.log('Using cached report');
        const overlay = createSafetyOverlay(cached);
        insertOverlay(overlay);
        return;
      }

      // Analyze video
      const report = await APIManager.analyzeVideo(videoId);

      // Cache result
      await CacheManager.set(videoId, report);

      // Display report
      const overlay = createSafetyOverlay(report);
      insertOverlay(overlay);

    } catch (error) {
      console.error('Error analyzing video:', error);
      
      // Show error overlay with better error handling
      const errorOverlay = document.createElement('div');
      errorOverlay.className = 'safesense-overlay';
      const errorMsg = error.message || error.toString() || 'Unknown error';
      errorOverlay.innerHTML = `
        <div class="safesense-card safesense-error">
          <h3>⚠️ Lỗi phân tích</h3>
          <p>Không thể phân tích video này.</p>
          <p><small>Đang sử dụng mock data cho demo</small></p>
          <button onclick="this.parentElement.parentElement.remove()" 
                  style="margin-top:10px;padding:8px 16px;background:white;color:#ef4444;border:none;border-radius:6px;cursor:pointer;font-weight:600;">
            Đóng
          </button>
        </div>
      `;
      insertOverlay(errorOverlay);
    }
  }

  /**
   * Wait for element to appear in DOM
   * @param {string} selector - CSS selector
   * @param {number} timeout - Timeout in ms
   * @returns {Promise<Element|null>}
   */
  function waitForElement(selector, timeout = 5000) {
    return new Promise((resolve) => {
      const element = document.querySelector(selector);
      if (element) {
        resolve(element);
        return;
      }

      const observer = new MutationObserver(() => {
        const element = document.querySelector(selector);
        if (element) {
          observer.disconnect();
          resolve(element);
        }
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true
      });

      setTimeout(() => {
        observer.disconnect();
        resolve(null);
      }, timeout);
    });
  }

  /**
   * Initialize extension
   */
  function init() {
    console.log('SafeSense initializing...');

    // Delay to let YouTube fully load
    setTimeout(() => {
      analyzeCurrentVideo();
    }, 1000);

    // Watch for URL changes (YouTube SPA)
    let lastUrl = location.href;
    new MutationObserver(() => {
      const url = location.href;
      if (url !== lastUrl) {
        lastUrl = url;
        console.log('URL changed, re-analyzing...');
        currentVideoId = null;
        // Delay to let YouTube load
        setTimeout(() => {
          analyzeCurrentVideo();
        }, 1000);
      }
    }).observe(document, { subtree: true, childList: true });
  }

  // Wait for page to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // Delay init to let YouTube fully load
    setTimeout(init, 1500);
  }

})();
