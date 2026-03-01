/**
 * SafeSense Kids Guardian - API Manager
 * Handles communication with YouTube API and SafeSense backend
 */

const APIManager = {
  // Configuration
  YOUTUBE_API_KEY: 'YOUR_YOUTUBE_API_KEY', // TODO: Replace with actual key
  SAFESENSE_API_URL: 'http://localhost:8000/api/v1', // Local development
  MAX_COMMENTS: 500, // Maximum comments to analyze
  BATCH_SIZE: 50, // Process 50 comments at a time

  /**
   * Fetch comments from YouTube video
   * @param {string} videoId - YouTube video ID
   * @param {number} maxResults - Maximum number of comments
   * @returns {Promise<Array>} Array of comment objects
   */
  async fetchYouTubeComments(videoId, maxResults = 500) {
    try {
      const comments = [];
      let pageToken = null;
      
      while (comments.length < maxResults) {
        const url = new URL('https://www.googleapis.com/youtube/v3/commentThreads');
        url.searchParams.append('part', 'snippet');
        url.searchParams.append('videoId', videoId);
        url.searchParams.append('maxResults', Math.min(100, maxResults - comments.length));
        url.searchParams.append('order', 'relevance');
        url.searchParams.append('textFormat', 'plainText');
        url.searchParams.append('key', this.YOUTUBE_API_KEY);
        
        if (pageToken) {
          url.searchParams.append('pageToken', pageToken);
        }

        const response = await fetch(url.toString());
        
        if (!response.ok) {
          throw new Error(`YouTube API error: ${response.status}`);
        }

        const data = await response.json();
        
        if (!data.items || data.items.length === 0) {
          break;
        }

        // Extract comments
        for (const item of data.items) {
          const snippet = item.snippet.topLevelComment.snippet;
          comments.push({
            text: snippet.textDisplay,
            author: snippet.authorDisplayName,
            likeCount: snippet.likeCount,
            publishedAt: snippet.publishedAt
          });
        }

        pageToken = data.nextPageToken;
        
        if (!pageToken) {
          break;
        }
      }

      console.log(`Fetched ${comments.length} comments from YouTube`);
      return comments;
    } catch (error) {
      console.error('Error fetching YouTube comments:', error);
      throw error;
    }
  },

  /**
   * Get mock comments for demo (when YouTube API key is not available)
   * @param {string} videoId - YouTube video ID
   * @returns {Promise<Array>} Array of mock comments
   */
  async getMockComments(videoId) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return [
      { text: "Video hay quá, cảm ơn bạn!", author: "User1" },
      { text: "Rất bổ ích cho trẻ em", author: "Parent123" },
      { text: "Con tôi rất thích xem", author: "Mom456" },
      { text: "Giỏi vcl, đỉnh vãi luôn", author: "Fan789" },
      { text: "Nội dung tuyệt vời", author: "Viewer001" },
      // Add some toxic for testing
      { text: "Thằng này ngu vcl", author: "Troll1" },
      { text: "Ba mẹ mày ngu", author: "Hater2" },
      { text: "Video dở tệ", author: "Critic3" },
    ];
  },

  /**
   * Predict toxicity for batch of comments
   * @param {Array} comments - Array of comment objects
   * @returns {Promise<Array>} Array of predictions
   */
  async batchPredict(comments) {
    try {
      const texts = comments.map(c => c.text);
      const predictions = [];

      // Process in batches
      for (let i = 0; i < texts.length; i += this.BATCH_SIZE) {
        const batch = texts.slice(i, i + this.BATCH_SIZE);
        
        const response = await fetch(`${this.SAFESENSE_API_URL}/batch-classify`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            texts: batch
          })
        });

        if (!response.ok) {
          throw new Error(`SafeSense API error: ${response.status}`);
        }

        const data = await response.json();
        predictions.push(...data.predictions);
      }

      console.log(`Analyzed ${predictions.length} comments`);
      return predictions;
    } catch (error) {
      console.error('Error in batch prediction:', error);
      
      // Fallback to mock predictions for demo
      console.warn('Using mock predictions for demo');
      return this.getMockPredictions(comments);
    }
  },

  /**
   * Get mock predictions for demo
   * @param {Array} comments - Array of comment objects
   * @returns {Array} Mock predictions
   */
  getMockPredictions(comments) {
    return comments.map(comment => {
      const text = comment.text.toLowerCase();
      
      // Simple rule-based mock
      if (text.includes('ba mẹ') || text.includes('gia đình')) {
        return { label: 2, confidence: 0.95 }; // Hate
      } else if (text.includes('ngu') || text.includes('dở')) {
        return { label: 1, confidence: 0.85 }; // Toxic
      } else if (text.includes('giỏi vcl') || text.includes('đỉnh vãi')) {
        return { label: 0, confidence: 0.90 }; // Clean (positive slang)
      } else {
        return { label: 0, confidence: 0.95 }; // Clean
      }
    });
  },

  /**
   * Analyze video safety
   * @param {string} videoId - YouTube video ID
   * @returns {Promise<Object>} Safety report
   */
  async analyzeVideo(videoId) {
    console.log(`Analyzing video: ${videoId}`);
    
    try {
      // 1. Fetch comments
      let comments;
      if (this.YOUTUBE_API_KEY === 'YOUR_YOUTUBE_API_KEY') {
        console.warn('YouTube API key not configured, using mock data');
        comments = await this.getMockComments(videoId);
      } else {
        comments = await this.fetchYouTubeComments(videoId, this.MAX_COMMENTS);
      }

      if (comments.length === 0) {
        return {
          error: 'No comments found',
          score: 50,
          level: SafetyScorer.getLevel(50)
        };
      }

      // 2. Predict toxicity
      const predictions = await this.batchPredict(comments);

      // 3. Calculate safety score
      const report = SafetyScorer.calculateScore(predictions);

      // 4. Add metadata
      report.videoId = videoId;
      report.analyzed_at = new Date().toISOString();

      return report;
    } catch (error) {
      console.error('Error analyzing video:', error);
      throw error;
    }
  }
};

// Make available globally
if (typeof window !== 'undefined') {
  window.APIManager = APIManager;
}
