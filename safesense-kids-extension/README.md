# 🛡️ SafeSense Kids Guardian

**Browser Extension bảo vệ trẻ em trên YouTube với AI**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Model](https://img.shields.io/badge/model-PhoBERT--v2-purple)

---

## 📋 Tổng quan

SafeSense Kids Guardian là browser extension sử dụng AI để phân tích độ an toàn của video YouTube dựa trên nội dung bình luận. Extension tự động quét và đánh giá comments, đưa ra điểm số an toàn (0-100) giúp phụ huynh quyết định video có phù hợp cho trẻ em hay không.

### ✨ Tính năng chính

- 🤖 **AI-Powered Analysis**: Sử dụng model PhoBERT-v2 với F1 0.7995, Accuracy 80.87%
- ⚡ **Real-time Processing**: Phân tích 500 comments trong ~2 giây
- 🎯 **Safety Score**: Điểm số 0-100 dễ hiểu (🟢 Safe, 🟡 Caution, 🔴 Not Safe)
- 💾 **Smart Caching**: Cache kết quả 24h, không phân tích lại video đã xem
- 🎨 **Beautiful UI**: Giao diện đẹp, thân thiện với trẻ em
- 📊 **Detailed Stats**: Thống kê chi tiết về Clean/Toxic/Hate comments

---

## 🚀 Cài đặt

### Yêu cầu hệ thống

- Google Chrome 88+ hoặc Microsoft Edge 88+
- Internet connection

### Cài đặt từ Source (Developer Mode)

1. **Download source code**
   ```bash
   git clone https://github.com/yourusername/safesense-kids-guardian.git
   cd safesense-kids-guardian
   ```

2. **Mở Chrome Extensions**
   - Vào `chrome://extensions/`
   - Bật "Developer mode" (góc trên bên phải)

3. **Load extension**
   - Click "Load unpacked"
   - Chọn folder `safesense-kids-extension`

4. **Pin extension**
   - Click icon puzzle 🧩 trên toolbar
   - Pin "SafeSense Kids Guardian"

✅ **Hoàn tất!** Icon 🛡️ sẽ xuất hiện trên toolbar.

---

## 🎯 Cách sử dụng

### Cho Phụ huynh

1. **Tự động phân tích**
   - Vào bất kỳ video YouTube nào
   - Extension tự động phân tích và hiển thị kết quả
   - Xem điểm số an toàn và khuyến nghị

2. **Xem chi tiết**
   - Click "📊 Chi tiết" để xem breakdown
   - Số lượng Clean/Toxic/Hate comments
   - Recommendation cụ thể

3. **Ẩn bình luận**
   - Click "🙈 Ẩn bình luận" nếu cần
   - Trẻ không thể xem phần comment

4. **Quản lý cache**
   - Click icon 🛡️ trên toolbar
   - Xem statistics và xóa cache nếu cần

### Cho Trẻ em

- Nhìn vào màu sắc và emoji:
  - 🟢 **Xanh lá** = An toàn, có thể xem
  - 🟡 **Vàng** = Hỏi ba mẹ trước
  - 🔴 **Đỏ** = Không nên xem

---

## 📊 Cách tính Safety Score

```
Safety Score = 100 - (Toxic% × 30) - (Hate% × 50)

Ví dụ:
- 90% Clean, 8% Toxic, 2% Hate
→ Score = 100 - (8 × 3) - (2 × 5) = 66/100 🟡 CAUTION
```

### Thang điểm

| Score | Level | Emoji | Ý nghĩa |
|-------|-------|-------|---------|
| 90-100 | SAFE | 🟢 | An toàn cho trẻ em |
| 70-89 | CAUTION | 🟡 | Thận trọng, xem với phụ huynh |
| 50-69 | RISKY | 🟠 | Rủi ro, không khuyến nghị |
| 0-49 | NOT SAFE | 🔴 | Không an toàn, chặn |

---

## 🛠️ Configuration

### YouTube API Key (Optional)

Mặc định extension dùng mock data cho demo. Để phân tích comments thật:

1. Tạo API key tại [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3
3. Mở `utils/api.js`
4. Thay `YOUR_YOUTUBE_API_KEY` bằng key của bạn

```javascript
YOUTUBE_API_KEY: 'AIzaSy...' // Your actual key
```

### SafeSense Backend API

Để sử dụng model thật thay vì mock predictions:

1. Setup FastAPI backend (xem `/TOXIC_COMMENT/demo`)
2. Mở `utils/api.js`
3. Thay đổi `SAFESENSE_API_URL`:

```javascript
SAFESENSE_API_URL: 'https://your-api.com/api/v1'
```

---

## 📁 Cấu trúc Project

```
safesense-kids-extension/
├── manifest.json           # Chrome extension config
├── content.js             # Main logic, inject vào YouTube
├── background.js          # Service worker
├── popup.html            # Extension popup UI
├── popup.js              # Popup logic
├── styles.css            # Beautiful styling
├── utils/
│   ├── cache.js          # Cache management
│   ├── api.js            # API communication
│   └── safety-scorer.js  # Safety scoring logic
├── assets/
│   ├── icon-16.png       # Extension icons
│   ├── icon-48.png
│   └── icon-128.png
└── README.md
```

---

## 🤖 AI Model Specs

```
Model:       PhoBERT-v2 (vinai/phobert-base-v2)
Parameters:  135M
Training:    7,626 samples
Labels:      Clean (44.3%) | Toxic (27.0%) | Hate (28.6%)

Performance:
✅ Test F1:       0.7995 (Target >0.72, +11%)
✅ Test Accuracy: 80.87%
✅ Clean F1:      0.85
✅ Toxic F1:      0.73
✅ Hate F1:       0.82

Innovation: Intensity Preservation
→ Phân biệt "Giỏi vcl" (khen) vs "Ngu vcl" (chửi)
```

---

## 🎬 Demo Examples

### Example 1: Safe Video
```
Video: "Baby Shark Dance"
Comments: 150
- Clean: 145 (96.7%)
- Toxic: 5 (3.3%)
- Hate: 0 (0%)

Safety Score: 90/100 🟢 SAFE
Recommendation: Video này an toàn cho trẻ em
```

### Example 2: Risky Video
```
Video: "GTA V Gameplay"
Comments: 500
- Clean: 300 (60%)
- Toxic: 150 (30%)
- Hate: 50 (10%)

Safety Score: 10/100 🔴 NOT SAFE
Recommendation: ⚠️ Không phù hợp cho trẻ em!
```

---

## 🐛 Troubleshooting

### Extension không hoạt động?

1. **Check console logs**
   - F12 → Console tab
   - Xem error messages

2. **Reload extension**
   - `chrome://extensions/`
   - Click ↻ Reload

3. **Clear cache**
   - Click icon 🛡️
   - "🗑️ Xóa cache"

### Không thấy overlay trên YouTube?

1. Refresh trang YouTube (F5)
2. Kiểm tra Developer mode enabled
3. Xem console có error không

### API errors?

- Mock predictions sẽ được dùng tự động
- Check `utils/api.js` config
- Verify backend đang chạy (nếu dùng real API)

---

## 🚀 Deployment

### Publish to Chrome Web Store

1. **Package extension**
   ```bash
   zip -r safesense-kids-guardian.zip safesense-kids-extension/
   ```

2. **Upload to Chrome Web Store**
   - Tạo Developer account ($5 one-time)
   - Upload ZIP file
   - Fill store listing

3. **Review process**
   - Google review ~3-5 days
   - Fix issues nếu có
   - Publish!

### Pricing Model

```
🆓 Free tier:
   - 5 videos/ngày
   - Basic features

💎 Premium ($2.99/tháng):
   - Unlimited videos
   - Parent dashboard
   - Priority support

🏢 Enterprise ($99/tháng):
   - Schools & libraries
   - Bulk licenses
   - Custom features
```

---

## 📈 Roadmap

### Phase 1: MVP ✅
- [x] Basic extension structure
- [x] YouTube integration
- [x] Safety scoring
- [x] Beautiful UI
- [x] Cache system

### Phase 2: Beta (Q1 2026)
- [ ] YouTube API integration
- [ ] Real backend API
- [ ] User accounts
- [ ] Parent dashboard
- [ ] 100 beta testers

### Phase 3: Launch (Q2 2026)
- [ ] Chrome Web Store
- [ ] Marketing campaign
- [ ] School partnerships
- [ ] Press release

### Phase 4: Scale (Q3 2026)
- [ ] Firefox extension
- [ ] Mobile app
- [ ] More platforms (TikTok, FB)
- [ ] AI improvements

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 👥 Team

- **Trần Thanh Thiện** - Lead Developer - MSSV 2280603068
- **Nguyễn Đan Huy** - Co-Developer - MSSV 2280601170

### Contact

- Email: thientran805954@gmail.com
- GitHub: [@yourusername](https://github.com/yourusername)
- University: HUTECH, Lớp 22DTHG2

---

## 🙏 Acknowledgments

- **VinAI** - PhoBERT model
- **YouTube Data API** - Comments data
- **IT Got Talent 2025** - Competition platform
- **HUTECH** - Academic support

---

## 📊 Statistics

```
Downloads:       0 (launching soon)
Active Users:    0
Videos Analyzed: 0
Kids Protected:  TBD

Target:
- 10,000 users in 6 months
- 1,000,000 videos analyzed
- 100,000 kids protected
```

---

## 🎯 Impact

> "Bảo vệ 20+ triệu trẻ em Việt Nam trên YouTube với AI"

- ✅ Tự động phát hiện nội dung độc hại
- ✅ Tiết kiệm thời gian cho phụ huynh
- ✅ Tạo môi trường internet lành mạnh
- ✅ Giáo dục digital citizenship

---

**Made with ❤️ for Vietnamese kids**
