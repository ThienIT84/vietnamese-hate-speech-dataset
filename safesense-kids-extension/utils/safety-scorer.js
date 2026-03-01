/**
 * SafeSense Kids Guardian - Safety Scorer
 * Calculates safety scores for video content based on comment analysis
 */

const SafetyScorer = {
  
  /**
   * Calculate safety score from predictions (0-100)
   * Higher score = Safer for children
   * @param {Array} predictions - Array of {label: 0|1|2, confidence: float}
   * @returns {Object} Safety report
   */
  calculateScore(predictions) {
    if (!predictions || predictions.length === 0) {
      return {
        score: 50,
        level: this.getLevel(50),
        stats: {
          total_comments: 0,
          clean: 0,
          toxic: 0,
          hate: 0,
          clean_pct: 0,
          toxic_pct: 0,
          hate_pct: 0
        },
        recommendation: "Không có dữ liệu để đánh giá"
      };
    }

    const total = predictions.length;
    
    // Count by label
    const clean_count = predictions.filter(p => p.label === 0).length;
    const toxic_count = predictions.filter(p => p.label === 1).length;
    const hate_count = predictions.filter(p => p.label === 2).length;
    
    // Calculate percentages
    const clean_pct = (clean_count / total) * 100;
    const toxic_pct = (toxic_count / total) * 100;
    const hate_pct = (hate_count / total) * 100;
    
    // Scoring logic
    let base_score = 100;
    
    // Toxic comments: -30 points per 10%
    const toxic_penalty = (toxic_pct / 10) * 30;
    
    // Hate speech: -50 points per 10% (worse!)
    const hate_penalty = (hate_pct / 10) * 50;
    
    let safety_score = base_score - toxic_penalty - hate_penalty;
    
    // Clamp between 0-100
    safety_score = Math.max(0, Math.min(100, safety_score));
    
    // Round to 1 decimal
    safety_score = Math.round(safety_score * 10) / 10;
    
    const level = this.getLevel(safety_score);
    const recommendation = this.getRecommendation(safety_score, toxic_pct, hate_pct);
    
    return {
      score: safety_score,
      level: level,
      stats: {
        total_comments: total,
        clean: clean_count,
        toxic: toxic_count,
        hate: hate_count,
        clean_pct: Math.round(clean_pct * 10) / 10,
        toxic_pct: Math.round(toxic_pct * 10) / 10,
        hate_pct: Math.round(hate_pct * 10) / 10
      },
      recommendation: recommendation,
      analyzed_at: new Date().toISOString()
    };
  },

  /**
   * Get safety level based on score
   * @param {number} score - Safety score (0-100)
   * @returns {Object} Level info
   */
  getLevel(score) {
    if (score >= 90) {
      return {
        level: 'SAFE',
        color: 'green',
        emoji: '🟢',
        text: 'An toàn'
      };
    } else if (score >= 70) {
      return {
        level: 'CAUTION',
        color: 'yellow',
        emoji: '🟡',
        text: 'Thận trọng'
      };
    } else if (score >= 50) {
      return {
        level: 'RISKY',
        color: 'orange',
        emoji: '🟠',
        text: 'Rủi ro'
      };
    } else {
      return {
        level: 'NOT_SAFE',
        color: 'red',
        emoji: '🔴',
        text: 'Không an toàn'
      };
    }
  },

  /**
   * Get detailed recommendation
   * @param {number} score - Safety score
   * @param {number} toxic_pct - Toxic percentage
   * @param {number} hate_pct - Hate speech percentage
   * @returns {string} Recommendation text
   */
  getRecommendation(score, toxic_pct, hate_pct) {
    if (score >= 90) {
      return "Video này an toàn cho trẻ em. Nội dung bình luận lành mạnh.";
    } else if (score >= 70) {
      return "Video có một số bình luận không phù hợp. Nên xem cùng trẻ hoặc tắt phần bình luận.";
    } else if (score >= 50) {
      return "Video có nhiều bình luận tiêu cực. Khuyến nghị phụ huynh xem trước hoặc xem cùng trẻ.";
    } else {
      if (hate_pct > 10) {
        return "⚠️ Video có nội dung hate speech nghiêm trọng. KHÔNG phù hợp cho trẻ em!";
      } else {
        return "⚠️ Video có nhiều bình luận độc hại. KHÔNG khuyến nghị cho trẻ em!";
      }
    }
  },

  /**
   * Get child-friendly message
   * @param {number} score - Safety score
   * @returns {string} Simple message for kids
   */
  getKidFriendlyMessage(score) {
    if (score >= 90) {
      return "Video này an toàn! Bạn có thể xem.";
    } else if (score >= 70) {
      return "Video này có một số bình luận không tốt. Bạn nên xem với ba mẹ nhé!";
    } else {
      return "Video này có nhiều bình luận không phù hợp. Hãy hỏi ba mẹ trước khi xem nhé!";
    }
  },

  /**
   * Get color for score
   * @param {number} score - Safety score
   * @returns {string} CSS color
   */
  getScoreColor(score) {
    if (score >= 90) return '#22c55e';      // green
    if (score >= 70) return '#eab308';      // yellow
    if (score >= 50) return '#f97316';      // orange
    return '#ef4444';                        // red
  },

  /**
   * Analyze specific concerns
   * @param {Object} stats - Statistics object
   * @returns {Array} Array of concern objects
   */
  analyzeConcerns(stats) {
    const concerns = [];

    if (stats.hate_pct > 5) {
      concerns.push({
        type: 'hate',
        severity: 'high',
        message: `${stats.hate_pct}% bình luận chứa hate speech`,
        icon: '🔴'
      });
    }

    if (stats.toxic_pct > 20) {
      concerns.push({
        type: 'toxic',
        severity: stats.toxic_pct > 30 ? 'high' : 'medium',
        message: `${stats.toxic_pct}% bình luận toxic`,
        icon: '⚠️'
      });
    }

    if (stats.clean_pct < 50) {
      concerns.push({
        type: 'low_quality',
        severity: 'medium',
        message: 'Chất lượng bình luận thấp',
        icon: '⚡'
      });
    }

    return concerns;
  }
};

// Make available globally
if (typeof window !== 'undefined') {
  window.SafetyScorer = SafetyScorer;
}
