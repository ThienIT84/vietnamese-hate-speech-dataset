# 🎯 CRAWL SOCIAL_ISSUES - YOUTUBE VIDEOS

## Mục tiêu: ~1,000 comments (8-10 videos, mỗi video ~100-150 comments)

---

## 📺 DANH SÁCH VIDEO ĐỀ XUẤT:

### 🚗 **Giao thông / Tai nạn** (300 comments - 3 videos)

**Video 1: Tai nạn giao thông kinh hoàng**
- Từ khóa tìm: "tai nạn giao thông việt nam"
- Kênh đề xuất: VTV24, An Ninh TV, Chuyện Lạ Có Thật
- Filter: Video có >50K views, >500 comments
- Gợi ý: Tìm video tổng hợp tai nạn, camera hành trình

**Video 2: Tình trạng vi phạm luật giao thông**
- Từ khóa: "vi phạm giao thông", "phóng nhanh vượt đèn đỏ"
- Video phổ biến: Các clip về đua xe, vượt đèn đỏ, không đội mũ bảo hiểm

**Video 3: Ùn tắc giao thông**
- Từ khóa: "tắc đường hà nội", "kẹt xe sài gòn"
- Comments thường toxic về quy hoạch, cơ sở hạ tầng

---

### 🌊 **Thiên tai / Lũ lụt** (300 comments - 3 videos)

**Video 4: Lũ lụt miền Trung**
- Từ khóa: "lũ lụt miền trung", "ngập lụt quy nhơn", "mưa bão"
- Kênh: VnExpress, Tuổi Trẻ Online, Báo Thanh Niên
- Chọn video: Bão số mới nhất, thiệt hại nặng

**Video 5: Thủy điện xả lũ**
- Từ khóa: "thủy điện xả lũ", "xả đập không báo trước"
- Comments toxic về trách nhiệm, quản lý

**Video 6: Cứu trợ lũ lụt**
- Từ khóa: "cứu trợ miền trung", "từ thiện lũ lụt"
- Video về hoạt động từ thiện, comments có tranh cãi

---

### 🏙️ **Vấn đề xã hội khác** (400 comments - 4 videos)

**Video 7: Tệ nạn xã hội**
- Từ khóa: "tệ nạn xã hội việt nam", "ma túy", "mại dâm"
- Kênh: VTC News, An Ninh TV

**Video 8: Trộm cắp / Cướp giật**
- Từ khóa: "trộm cắp tại việt nam", "cướp giật táo tợn"
- Video: Camera an ninh bắt được cảnh trộm

**Video 9: Xây dựng lấn chiếm**
- Từ khóa: "xây trái phép", "lấn chiếm vỉa hè", "nhà siêu mỏng"

**Video 10: Ô nhiễm môi trường**
- Từ khóa: "ô nhiễm môi trường", "rác thải nhựa", "ô nhiễm không khí"
- Comments về ý thức, trách nhiệm

---

## 🔧 HƯỚNG DẪN SỬ DỤNG APIFY:

### **Cách 1: Tìm theo từ khóa (Khuyến nghị)**

```
Vào: https://apify.com/bernardo/youtube-scraper

Input JSON:
{
  "searchKeywords": "tai nạn giao thông việt nam",
  "maxResults": 3,
  "maxComments": 150,
  "searchSortBy": "upload date"
}

→ Run → Download JSON
```

### **Cách 2: Crawl video cụ thể (Nhanh hơn)**

Nếu bạn đã có link video YouTube:

```json
{
  "startUrls": [
    {"url": "https://www.youtube.com/watch?v=VIDEO_ID_1"},
    {"url": "https://www.youtube.com/watch?v=VIDEO_ID_2"}
  ],
  "maxComments": 150
}
```

---

## 📝 SAU KHI CRAWL:

**Bước 1:** Download file JSON từ Apify

**Bước 2:** Đổi tên file theo format:
- `social_issues_tai_nan_giao_thong.json`
- `social_issues_lu_lut_mien_trung.json`
- `social_issues_te_nan_xa_hoi.json`

**Bước 3:** Copy tất cả file JSON vào:
```
raw/youtube/
```

**Bước 4:** Chạy script merge:
```bash
cd "c:\Học sâu\Dataset"
python apify_to_csv.py
```

Script sẽ tự động:
- Đọc tất cả file JSON trong raw/youtube/
- Detect topic từ tên file (social_issues_*.json → social_issues)
- Merge vào facebook_master.csv
- Loại bỏ duplicate

---

## 💡 TIPS:

✅ **Chọn video có nhiều tranh cãi** → comments toxic/non-toxic cân bằng
✅ **Tránh video quá cũ** (>2 năm) → ngôn ngữ lỗi thời
✅ **Chọn kênh uy tín** → comments chất lượng hơn
✅ **Filter video >50K views** → đủ comments

❌ **Tránh video nhạy cảm chính trị** → không phù hợp với dataset
❌ **Tránh video clickbait** → comments spam nhiều

---

## 🎯 TARGET:

- [ ] Giao thông: 3 videos × 100 comments = 300 ✓
- [ ] Thiên tai: 3 videos × 100 comments = 300 ✓
- [ ] Vấn đề XH: 4 videos × 100 comments = 400 ✓

**TỔNG: ~1,000 comments social_issues từ YouTube**

---

Bắt đầu với giao thông trước nhé! Tìm 3 video về tai nạn/vi phạm giao thông và crawl ~100-150 comments mỗi video.
