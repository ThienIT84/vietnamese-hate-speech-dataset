# HƯỚNG DẪN CRAWL DỮ LIỆU TỪ FACEBOOK

## 📋 CÁC BƯỚC THỰC HIỆN

### **BƯỚC 1: CÀI ĐẶT THƯ VIỆN**

Mở PowerShell/CMD trong thư mục hiện tại và chạy:

```bash
pip install selenium pandas openpyxl
```

---

### **BƯỚC 2: TẢI CHROMEDRIVER**

#### **Cách 1: Tự động (Khuyến nghị)**
```bash
pip install webdriver-manager
```

Sau đó sửa code, thay dòng:
```python
service = Service(executable_path="chromedriver.exe")
```

Thành:
```python
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())
```

#### **Cách 2: Tải thủ công**

1. **Kiểm tra phiên bản Chrome:**
   - Mở Chrome → Menu (3 chấm) → Help → About Google Chrome
   - Ghi nhớ phiên bản (VD: 120.0.6099.109)

2. **Tải ChromeDriver:**
   - Vào: https://googlechromelabs.github.io/chrome-for-testing/
   - Hoặc: https://chromedriver.chromium.org/downloads
   - Tải phiên bản ChromeDriver khớp với Chrome
   - Chọn file cho Windows (chromedriver-win64.zip)

3. **Giải nén và đặt file:**
   - Giải nén file ZIP
   - Copy `chromedriver.exe` vào thư mục: `c:\Học sâu\Dataset\`
   - Hoặc copy vào `C:\Windows\` để dùng global

4. **Cập nhật đường dẫn trong code** (nếu cần):
```python
# Nếu đặt trong thư mục khác:
service = Service(executable_path=r"C:\tools\chromedriver.exe")
```

---

### **BƯỚC 3: LẤY URL BÀI VIẾT FACEBOOK**

1. **Mở Facebook** và tìm bài viết có nhiều bình luận
2. **Click vào bài viết** để mở full
3. **Copy URL** từ thanh địa chỉ

**Ví dụ URL hợp lệ:**
```
https://www.facebook.com/share/p/ABC123XYZ/
https://www.facebook.com/username/posts/1234567890/
https://www.facebook.com/photo/?fbid=123456789
```

4. **Dán URL vào code:**
```python
POST_URLS = [
    "https://www.facebook.com/share/p/ABC123XYZ/",
    "https://www.facebook.com/username/posts/1234567890/",
]
```

---

### **BƯỚC 4: CẤU HÌNH TÀI KHOẢN FACEBOOK**

⚠️ **QUAN TRỌNG:**
- **Dùng tài khoản phụ**, không dùng tài khoản chính
- Tài khoản phải được tạo từ lâu (>6 tháng)
- Đã có hoạt động bình thường (like, comment, share)

Sửa trong code:
```python
FB_EMAIL = "email_tai_khoan_phu@gmail.com"
FB_PASSWORD = "mat_khau_cua_ban"
```

---

### **BƯỚC 5: CHẠY THỬ LẦN ĐẦU**

1. **Mở PowerShell** trong thư mục `c:\Học sâu\Dataset\`

2. **Chạy lệnh:**
```bash
python scapper_data_fromFaceBook.py
```

3. **Quan sát trình duyệt Chrome tự động:**
   - Nó sẽ mở Facebook
   - Tự động đăng nhập
   - Mở bài viết
   - Scroll xuống
   - Click "Xem thêm bình luận"

4. **Nếu gặp lỗi:**
   - Đọc thông báo lỗi trong PowerShell
   - Xem phần "KHẮC PHỤC LỖI" bên dưới

---

### **BƯỚC 6: XỬ LÝ CAPTCHA/CHECKPOINT (nếu có)**

Nếu Facebook yêu cầu xác minh:

1. **GIỮ NGUYÊN cửa sổ trình duyệt đang mở**
2. **Tự tay xử lý:**
   - Nhập mã xác minh từ email/SMS
   - Chọn ảnh captcha
   - Xác nhận thiết bị
3. **Chờ code tiếp tục chạy**

---

### **BƯỚC 7: KIỂM TRA KẾT QUẢ**

Sau khi chạy xong:

1. **Tìm file CSV** trong thư mục:
   ```
   fb_data_20251123_1430.csv
   ```

2. **Mở bằng Excel hoặc Notepad**

3. **Kiểm tra dữ liệu:**
   - Cột `text`: Nội dung bình luận
   - Cột `username`: Tên người dùng
   - Cột `timestamp`: Thời gian crawl
   - Cột `source_platform`: Facebook

---

## 🔧 KHẮC PHỤC LỖI THƯỜNG GẶP

### **Lỗi 1: "chromedriver.exe not found"**

**Nguyên nhân:** Không tìm thấy ChromeDriver

**Giải pháp:**
```bash
# Cách nhanh nhất:
pip install webdriver-manager
```

Rồi sửa code như BƯỚC 2 - Cách 1

---

### **Lỗi 2: "This version of ChromeDriver only supports Chrome version XXX"**

**Nguyên nhân:** ChromeDriver không khớp với Chrome

**Giải pháp:**
- Tải lại ChromeDriver đúng phiên bản Chrome (xem BƯỚC 2)
- Hoặc cập nhật Chrome lên bản mới nhất

---

### **Lỗi 3: "Unable to locate element"**

**Nguyên nhân:** Facebook thay đổi giao diện, XPath không tìm thấy element

**Giải pháp:**

1. **Kiểm tra URL có hợp lệ không**
2. **Tắt headless mode** để xem trình duyệt (đã tắt sẵn trong code)
3. **Xem trình duyệt đang mở đúng trang không**
4. **Tăng thời gian chờ:**

```python
# Tìm dòng này và sửa:
time.sleep(8 + random.uniform(0, 3))
# Thành:
time.sleep(15)  # Chờ lâu hơn
```

---

### **Lỗi 4: "Login failed" hoặc không thấy bình luận**

**Nguyên nhân:** 
- Sai email/password
- Facebook chặn đăng nhập tự động
- Bài viết ở chế độ riêng tư

**Giải pháp:**

**Cách 1: Đăng nhập thủ công bằng Cookies**

```python
# Thêm sau khi driver.get("https://www.facebook.com"):
# Đăng nhập thủ công 1 lần, sau đó lưu cookies
import pickle

# Lưu cookies (chạy 1 lần):
pickle.dump(driver.get_cookies(), open("fb_cookies.pkl", "wb"))

# Lần sau dùng cookies:
cookies = pickle.load(open("fb_cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
```

**Cách 2: Crawl bài viết Public (không cần login)**
- Tìm bài viết public (ai cũng xem được)
- Bỏ qua bước login

---

### **Lỗi 5: "No comments found" - Không tìm thấy bình luận**

**Nguyên nhân:** XPath không đúng với Facebook hiện tại

**Giải pháp - Tìm XPath mới:**

1. **Mở Facebook** trên Chrome
2. **Mở bài viết** có bình luận
3. **F12** → Tab "Elements"
4. **Ctrl+Shift+C** → Click vào 1 bình luận
5. **Chuột phải** vào code HTML → Copy → Copy XPath
6. **Sửa trong code:**

```python
# Thay XPath cũ bằng XPath mới:
comments = driver.find_elements(By.XPATH, "XPath_mới_copy_được")
```

**Ví dụ XPath mới có thể là:**
```python
"//div[@role='article']//div[@dir='auto']"
"//span[contains(@class, 'x193iq5w')]"
```

---

### **Lỗi 6: Bị Facebook chặn IP**

**Triệu chứng:**
- Yêu cầu captcha liên tục
- Không load được trang
- Báo "suspicious activity"

**Giải pháp:**
1. **Dừng crawl, chờ 24h**
2. **Dùng proxy** (cần trả phí):
   ```python
   USE_PROXY = True
   PROXY = "proxy.provider.com:8080"
   ```
3. **Đổi mạng** (dùng 4G thay Wi-Fi)
4. **Giảm tốc độ crawl:**
   ```python
   time.sleep(random.uniform(10, 20))  # Chờ lâu hơn
   ```

---

## 📊 TỐI ƯU HÓA

### **1. Tăng số lượng bình luận**
```python
# Tăng số lần scroll:
for i in range(50):  # Thay vì 20
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 4))
```

### **2. Crawl nhanh hơn (sau khi test ổn định)**
```python
# Bật headless mode:
chrome_options.add_argument("--headless")

# Giảm delay:
time.sleep(random.uniform(1, 2))  # Thay vì 2-4
```

### **3. Lưu tiến trình (phòng bị gián đoạn)**
```python
# Sau mỗi post:
df_temp = pd.DataFrame(all_data)
df_temp.to_csv(f"backup_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", 
               index=False, encoding='utf-8-sig')
```

---

## 🎯 CHECKLIST TRƯỚC KHI CHẠY

- [ ] Đã cài `selenium`, `pandas`
- [ ] Đã có `chromedriver.exe` trong thư mục hoặc dùng `webdriver-manager`
- [ ] Đã sửa URL bài viết thật trong `POST_URLS`
- [ ] Đã điền email/password Facebook
- [ ] Đã tắt headless mode (để xem trình duyệt)
- [ ] Đã test với 1 URL trước

---

## 💡 MẸO

1. **Test với 1 bài viết trước** rồi mới crawl nhiều
2. **Dùng bài viết có <1000 comment** để test nhanh
3. **Crawl vào ban đêm** (ít bị chặn hơn)
4. **Không crawl quá 5-10 bài/ngày** với 1 tài khoản
5. **Backup code** trước khi sửa XPath

---

## 📞 NẾU VẪN BỊ LỖI

Chụp màn hình lỗi và cung cấp:
1. Thông báo lỗi trong PowerShell
2. Screenshot trình duyệt (nếu mở được)
3. URL bài viết đang crawl
4. Phiên bản Chrome (chrome://version)

---

**Chúc bạn crawl data thành công! 🎉**
