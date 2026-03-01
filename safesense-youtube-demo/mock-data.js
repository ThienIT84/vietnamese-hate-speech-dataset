// Mock Data for Demo
const MOCK_VIDEOS = [
    {
        id: 'dQw4w9WgXcQ',
        title: 'Rick Astley - Never Gonna Give You Up',
        channel: 'Rick Astley',
        thumbnail: 'https://i.ytimg.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
        stats: {
            total_comments: 487,  // Thực tế lấy được 487 comments
            clean: 463,
            toxic: 20,
            hate: 5,
            clean_pct: 95.0,
            toxic_pct: 4.0,
            hate_pct: 1.0
        },
        score: 97,
        level: 'safe'
    },
    {
        id: 'kJQP7kiw5Fk',
        title: 'Luis Fonsi - Despacito ft. Daddy Yankee',
        channel: 'Luis Fonsi',
        thumbnail: 'https://i.ytimg.com/vi/kJQP7kiw5Fk/mqdefault.jpg',
        stats: {
            total_comments: 352,  // Video này ít comment hơn
            clean: 299,
            toxic: 50,
            hate: 25,
            clean_pct: 85.0,
            toxic_pct: 10.0,
            hate_pct: 5.0
        },
        score: 72,
        level: 'caution'
    },
    {
        id: '9bZkp7q19f0',
        title: 'PSY - GANGNAM STYLE',
        channel: 'officialpsy',
        thumbnail: 'https://i.ytimg.com/vi/9bZkp7q19f0/mqdefault.jpg',
        stats: {
            total_comments: 500,
            clean: 450,
            toxic: 35,
            hate: 15,
            clean_pct: 90.0,
            toxic_pct: 7.0,
            hate_pct: 3.0
        },
        score: 87,
        level: 'safe'
    },
    {
        id: 'OPf0YbXqDm0',
        title: 'Mark Ronson - Uptown Funk ft. Bruno Mars',
        channel: 'Mark Ronson',
        thumbnail: 'https://i.ytimg.com/vi/OPf0YbXqDm0/mqdefault.jpg',
        stats: {
            total_comments: 500,
            clean: 380,
            toxic: 80,
            hate: 40,
            clean_pct: 76.0,
            toxic_pct: 16.0,
            hate_pct: 8.0
        },
        score: 56,
        level: 'risky'
    },
    {
        id: 'fRh_vgS2dFE',
        title: 'Justin Bieber - Sorry',
        channel: 'Justin Bieber',
        thumbnail: 'https://i.ytimg.com/vi/fRh_vgS2dFE/mqdefault.jpg',
        stats: {
            total_comments: 500,
            clean: 300,
            toxic: 120,
            hate: 80,
            clean_pct: 60.0,
            toxic_pct: 24.0,
            hate_pct: 16.0
        },
        score: 33,
        level: 'unsafe'
    },
    {
        id: 'Zi_XLOBDo_Y',
        title: '🎬 YouTube Shorts: Dance Challenge',
        channel: 'Popular Shorts',
        thumbnail: 'https://i.ytimg.com/vi/Zi_XLOBDo_Y/mqdefault.jpg',
        stats: {
            total_comments: 124,  // Shorts thường có ít comment
            clean: 114,
            toxic: 30,
            hate: 10,
            clean_pct: 92.0,
            toxic_pct: 6.0,
            hate_pct: 2.0
        },
        score: 92,
        level: 'safe',
        isShort: true
    },
    {
        id: 'aBcDeFgHiJk',
        title: '🎬 YouTube Shorts: Gaming Moment',
        channel: 'Gaming Shorts',
        thumbnail: 'https://i.ytimg.com/vi/aBcDeFgHiJk/mqdefault.jpg',
        stats: {
            total_comments: 89,   // Shorts gaming có ít comment
            clean: 62,
            toxic: 100,
            hate: 50,
            clean_pct: 70.0,
            toxic_pct: 20.0,
            hate_pct: 10.0
        },
        score: 60,
        level: 'risky',
        isShort: true
    }
];

// Safety levels configuration
const SAFETY_LEVELS = {
    safe: {
        emoji: '🟢',
        text: 'AN TOÀN',
        color: '#10b981',
        description: 'Video này rất an toàn cho trẻ em',
        recommendation: 'Video này có môi trường bình luận rất tích cực. Trẻ em có thể xem và tham gia bình luận một cách an toàn.',
        badge: 'badge-safe'
    },
    caution: {
        emoji: '🟡',
        text: 'THẬN TRỌNG',
        color: '#f59e0b',
        description: 'Cần giám sát khi trẻ xem video này',
        recommendation: 'Video có một số bình luận tiêu cực. Nên giám sát trẻ khi xem và có thể cân nhắc tắt phần bình luận.',
        badge: 'badge-caution'
    },
    risky: {
        emoji: '🟠',
        text: 'RỦI RO',
        color: '#f97316',
        description: 'Video có nhiều nội dung không phù hợp',
        recommendation: 'Video có tỷ lệ cao bình luận tiêu cực và ngôn từ thù ghét. Không nên cho trẻ xem hoặc cần giám sát chặt chẽ.',
        badge: 'badge-risky'
    },
    unsafe: {
        emoji: '🔴',
        text: 'KHÔNG AN TOÀN',
        color: '#ef4444',
        description: 'Video không phù hợp với trẻ em',
        recommendation: 'Video có môi trường bình luận rất tiêu cực với nhiều ngôn từ độc hại và thù ghét. Không nên cho trẻ em xem video này.',
        badge: 'badge-unsafe'
    }
};

// Get safety level from score
function getSafetyLevel(score) {
    if (score >= 90) return 'safe';
    if (score >= 70) return 'caution';
    if (score >= 50) return 'risky';
    return 'unsafe';
}

// Analyze concerns
function analyzeConcerns(stats) {
    const concerns = [];
    
    if (stats.toxic_pct > 15) {
        concerns.push({
            icon: '⚠️',
            message: `Tỷ lệ bình luận toxic cao (${stats.toxic_pct}%)`
        });
    }
    
    if (stats.hate_pct > 10) {
        concerns.push({
            icon: '🔴',
            message: `Phát hiện nhiều ngôn từ thù ghét (${stats.hate_pct}%)`
        });
    }
    
    if (stats.toxic + stats.hate > 100) {
        concerns.push({
            icon: '⚡',
            message: 'Phát hiện hơn 100 bình luận tiêu cực'
        });
    }
    
    return concerns;
}

// Extract video ID from YouTube URL (including Shorts)
function extractVideoId(url) {
    const patterns = [
        /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)/,
        /youtube\.com\/shorts\/([^&\n?#]+)/,
        /youtube\.com\/embed\/([^&\n?#]+)/,
        /youtube\.com\/v\/([^&\n?#]+)/
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match && match[1]) {
            return match[1];
        }
    }
    
    return null;
}

// Get mock video data
function getMockVideoData(videoId) {
    // Try to find in mock videos
    const mockVideo = MOCK_VIDEOS.find(v => v.id === videoId);
    if (mockVideo) {
        return mockVideo;
    }
    
    // Generate realistic data for unknown videos
    // Simulate varying comment counts (not always 500!)
    const totalComments = Math.floor(Math.random() * 400) + 100; // 100-500 comments
    
    const cleanPct = Math.floor(Math.random() * 30) + 70; // 70-100%
    const toxicPct = Math.floor(Math.random() * 15); // 0-15%
    const hatePct = 100 - cleanPct - toxicPct;
    
    const clean = Math.floor(totalComments * cleanPct / 100);
    const toxic = Math.floor(totalComments * toxicPct / 100);
    const hate = totalComments - clean - toxic;
    
    const score = Math.floor(100 - (toxicPct * 0.3) - (hatePct * 0.5));
    
    return {
        id: videoId,
        title: 'Video YouTube (Demo)',
        channel: 'Unknown Channel',
        thumbnail: `https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`,
        stats: {
            total_comments: totalComments,
            clean,
            toxic,
            hate,
            clean_pct: cleanPct,
            toxic_pct: toxicPct,
            hate_pct: hatePct
        },
        score,
        level: getSafetyLevel(score)
    };
}
