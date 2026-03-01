# SafeSense Kids Guardian - Demo Website

## 🎯 Giới thiệu
Demo website để trình diễn tính năng phân tích độ an toàn video YouTube cho trẻ em tại IT Got Talent 2025.

## ✨ Tính năng
- ✅ Nhập link YouTube để phân tích
- ✅ 5 video mẫu sẵn có để demo nhanh
- ✅ Loading animation đẹp mắt
- ✅ Hiển thị điểm an toàn 0-100
- ✅ Phân tích 4 mức độ: An toàn, Thận trọng, Rủi ro, Không an toàn
- ✅ Biểu đồ thống kê Clean/Toxic/Hate
- ✅ Khuyến nghị cụ thể cho phụ huynh
- ✅ Chia sẻ kết quả
- ✅ Responsive design

## 🚀 Cách chạy

### Cách 1: Mở trực tiếp file HTML
```bash
# Windows
start index.html

# hoặc double-click vào file index.html
```

### Cách 2: Dùng Python HTTP Server
```bash
cd safesense-youtube-demo
python -m http.server 8000
```
Sau đó mở trình duyệt: http://localhost:8000

### Cách 3: Dùng VS Code Live Server
1. Cài extension "Live Server" trong VS Code
2. Right-click vào index.html
3. Chọn "Open with Live Server"

## 📊 Video mẫu
1. **Rick Astley - Never Gonna Give You Up** - 🟢 An toàn (97/100)
2. **Luis Fonsi - Despacito** - 🟡 Thận trọng (72/100)
3. **PSY - GANGNAM STYLE** - 🟢 An toàn (87/100)
4. **Mark Ronson - Uptown Funk** - 🟠 Rủi ro (56/100)
5. **Justin Bieber - Sorry** - 🔴 Không an toàn (33/100)

## 🎬 Hướng dẫn demo cho IT Got Talent

### Bước 1: Giới thiệu (30s)
- Mở website, giới thiệu giao diện
- Nhấn mạnh: "Phân tích 500 bình luận bằng PhoBERT-v2, F1 0.7995"

### Bước 2: Demo video an toàn (1 phút)
- Click vào "Rick Astley - Never Gonna Give You Up"
- Quan sát loading animation (4 bước)
- Giải thích kết quả: 97/100, 95% clean
- Khuyến nghị: An toàn cho trẻ

### Bước 3: Demo video rủi ro (1 phút)
- Click "Phân tích video khác"
- Chọn "Mark Ronson - Uptown Funk"
- So sánh: 56/100, chỉ 76% clean, 8% hate
- Khuyến nghị: Cần giám sát

### Bước 4: Demo video không an toàn (1 phút)
- Chọn "Justin Bieber - Sorry"
- Nhấn mạnh: 33/100, 16% hate speech
- Khuyến nghị: Không nên cho trẻ xem

### Bước 5: Nhập link tùy chọn (30s)
- Paste link YouTube bất kỳ
- Click "Phân tích ngay"
- Giải thích: Có thể phân tích mọi video

## 💡 Điểm mạnh để nhấn mạnh
1. **Chính xác cao**: F1 0.7995, Accuracy 80.87%
2. **Nhanh**: Inference < 100ms
3. **Thực tiễn**: Bảo vệ trẻ em trên YouTube
4. **Dễ dùng**: Chỉ cần paste link
5. **Đầy đủ**: Phân tích 500 bình luận mỗi video
6. **Khuyến nghị cụ thể**: Cho từng mức độ an toàn

## 📁 Cấu trúc file
```
safesense-youtube-demo/
├── index.html          # Giao diện chính
├── styles.css          # Styling đẹp với gradient
├── app.js             # Logic xử lý
├── mock-data.js       # Dữ liệu video mẫu
├── API_GUIDE.md       # Hướng dẫn API & cơ chế lấy comment
├── PREPROCESSING_GUIDE.md  # Chi tiết về tiền xử lý (link to src/)
└── README.md          # File này

🔗 Preprocessing thực tế: ../src/preprocessing/advanced_text_cleaning.py
```

## 🎨 Công nghệ sử dụng
- **Frontend**: HTML5, CSS3 (Flexbox, Grid), Vanilla JavaScript
- **Design**: Gradient purple theme, responsive
- **Animation**: CSS transitions, loading steps
- **Data**: Mock data cho demo (không cần API)
- **Preprocessing**: Advanced Text Cleaning V2.1 (src/preprocessing/advanced_text_cleaning.py)
  - 500+ teencode dictionary
  - Intensity preservation
  - Death metaphors detection
  - Context-aware cleaning

## 🔧 Tùy chỉnh

### Thay đổi màu sắc
Chỉnh trong `styles.css`:
```css
:root {
    --primary: #8b5cf6;        /* Màu chính */
    --secondary: #ec4899;      /* Màu phụ */
    --success: #10b981;        /* Màu an toàn */
    --warning: #f59e0b;        /* Màu cảnh báo */
    --danger: #ef4444;         /* Màu nguy hiểm */
}
```

### Thêm video mẫu
Chỉnh trong `mock-data.js`:
```javascript
MOCK_VIDEOS.push({
    id: 'VIDEO_ID',
    title: 'Tên video',
    channel: 'Tên kênh',
    thumbnail: 'URL thumbnail',
    stats: {
        total_comments: 500,
        clean: 450,
        toxic: 40,
        hate: 10,
        clean_pct: 90,
        toxic_pct: 8,
        hate_pct: 2
    },
    score: 87,
    level: 'safe'
});
```

## 📱 Tương thích
- ✅ Chrome, Edge (khuyên dùng)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers
- ✅ Desktop & Mobile responsive

## 🎯 Mục đích
Demo này được tạo đặc biệt cho **IT Got Talent 2025** để:
1. Minh họa tính thực tiễn của SafeSense-Vi
2. Dễ dàng trình diễn trong 15 phút
3. Không cần cài đặt, không cần API key
4. Có dữ liệu mẫu sẵn để demo ổn định
5. Giao diện đẹp, chuyên nghiệp

## 📞 Hỗ trợ
- File không hoạt động? Kiểm tra JavaScript có bật không
- Muốn thay đổi? Chỉnh trực tiếp trong các file .html/.css/.js
- Cần thêm video mẫu? Chỉnh `mock-data.js`

---

**Chúc bạn demo thành công tại IT Got Talent 2025!** 🎉
