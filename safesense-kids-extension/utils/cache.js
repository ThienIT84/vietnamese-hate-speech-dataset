/**
 * SafeSense Kids Guardian - Cache Manager
 * Manages local storage for video safety scores
 */

const CacheManager = {
  CACHE_PREFIX: 'safesense_',
  CACHE_EXPIRY: 24 * 60 * 60 * 1000, // 24 hours in milliseconds

  /**
   * Get cached safety report for a video
   * @param {string} videoId - YouTube video ID
   * @returns {Promise<Object|null>} Cached report or null
   */
  async get(videoId) {
    try {
      const key = this.CACHE_PREFIX + videoId;
      const result = await chrome.storage.local.get(key);
      
      if (!result[key]) {
        return null;
      }

      const cached = result[key];
      
      // Check if expired
      if (this.isExpired(cached)) {
        await this.remove(videoId);
        return null;
      }

      return cached;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  },

  /**
   * Set safety report in cache
   * @param {string} videoId - YouTube video ID
   * @param {Object} report - Safety report object
   * @returns {Promise<boolean>} Success status
   */
  async set(videoId, report) {
    try {
      const key = this.CACHE_PREFIX + videoId;
      const cacheData = {
        ...report,
        timestamp: Date.now(),
        version: '1.0'
      };

      await chrome.storage.local.set({ [key]: cacheData });
      return true;
    } catch (error) {
      console.error('Cache set error:', error);
      return false;
    }
  },

  /**
   * Remove cached report
   * @param {string} videoId - YouTube video ID
   * @returns {Promise<boolean>} Success status
   */
  async remove(videoId) {
    try {
      const key = this.CACHE_PREFIX + videoId;
      await chrome.storage.local.remove(key);
      return true;
    } catch (error) {
      console.error('Cache remove error:', error);
      return false;
    }
  },

  /**
   * Check if cache is expired
   * @param {Object} cached - Cached object with timestamp
   * @returns {boolean} True if expired
   */
  isExpired(cached) {
    if (!cached.timestamp) {
      return true;
    }
    
    const age = Date.now() - cached.timestamp;
    return age > this.CACHE_EXPIRY;
  },

  /**
   * Clear all cache
   * @returns {Promise<boolean>} Success status
   */
  async clearAll() {
    try {
      const result = await chrome.storage.local.get(null);
      const keysToRemove = Object.keys(result).filter(key => 
        key.startsWith(this.CACHE_PREFIX)
      );
      
      if (keysToRemove.length > 0) {
        await chrome.storage.local.remove(keysToRemove);
      }
      
      return true;
    } catch (error) {
      console.error('Cache clear error:', error);
      return false;
    }
  },

  /**
   * Get cache statistics
   * @returns {Promise<Object>} Cache stats
   */
  async getStats() {
    try {
      const result = await chrome.storage.local.get(null);
      const cacheKeys = Object.keys(result).filter(key => 
        key.startsWith(this.CACHE_PREFIX)
      );

      let totalSize = 0;
      let validCount = 0;
      let expiredCount = 0;

      for (const key of cacheKeys) {
        const cached = result[key];
        totalSize += JSON.stringify(cached).length;
        
        if (this.isExpired(cached)) {
          expiredCount++;
        } else {
          validCount++;
        }
      }

      return {
        total: cacheKeys.length,
        valid: validCount,
        expired: expiredCount,
        sizeKB: (totalSize / 1024).toFixed(2)
      };
    } catch (error) {
      console.error('Cache stats error:', error);
      return { total: 0, valid: 0, expired: 0, sizeKB: '0' };
    }
  }
};

// Make available globally
if (typeof window !== 'undefined') {
  window.CacheManager = CacheManager;
}
