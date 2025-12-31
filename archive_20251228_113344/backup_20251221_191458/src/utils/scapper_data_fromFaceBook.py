# fb_crawler.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import random
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# ========================= CONFIG =========================
# BƯỚC 1: Thay URL này bằng URL bài viết thật của bạn
POST_URLS = [
    "https://www.facebook.com/share/p/1BjvhvLAiq/",   # Thay bằng URL bài viết thật
    # Thêm nhiều URL khác nếu cần
]

# BƯỚC 2: Tài khoản Facebook (lấy từ file .env - AN TOÀN)
FB_EMAIL = os.getenv('FB_EMAIL', '')  # Đọc từ file .env
FB_PASSWORD = os.getenv('FB_PASSWORD', '')  # Đọc từ file .env

# Proxy (tùy chọn - bỏ qua nếu chưa có)
USE_PROXY = False  # Đổi thành True nếu muốn dùng proxy
PROXY = "gate.smartproxy.com:7000"
PROXY_USER = "user-xxx"
PROXY_PASS = "password-xxx"

# Delay ngẫu nhiên chống bot
SCROLL_PAUSE = random.uniform(6, 12)
COMMENT_PAUSE = random.uniform(1.5, 3.5)

# ========================= SETUP DRIVER =========================
def get_driver():
    chrome_options = Options()
    # Tắt headless để xem trình duyệt (dễ debug)
    # chrome_options.add_argument("--headless")  # Bật lại khi chạy ổn định
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=vi-VN")
    
    # TẮT popup "Lưu mật khẩu" của Chrome
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Thêm proxy (nếu có)
    if USE_PROXY and PROXY:
        chrome_options.add_argument(f'--proxy-server=http://{PROXY}')
    
    # Tự động tải ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")
    return driver

# ========================= LOGIN FUNCTION =========================
def login_facebook(driver):
    """Đăng nhập Facebook"""
    try:
        print("[+] Đang đăng nhập Facebook...")
        driver.get("https://www.facebook.com")
        time.sleep(3)
        
        # Nhập email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(FB_EMAIL)
        
        # Nhập password
        pass_input = driver.find_element(By.ID, "pass")
        pass_input.send_keys(FB_PASSWORD)
        
        # Click nút đăng nhập
        login_btn = driver.find_element(By.NAME, "login")
        login_btn.click()
        
        time.sleep(5)
        print("[✓] Đăng nhập thành công!")
        
        # Đóng các popup Facebook (thông báo, etc.)
        try:
            time.sleep(2)
            
            # 1. Đóng popup "Lưu thông tin đăng nhập" của Facebook
            try:
                not_now_btns = driver.find_elements(By.XPATH, 
                    "//div[@role='button' and contains(., 'Không phải bây giờ')]")
                if not_now_btns:
                    not_now_btns[0].click()
                    print("[✓] Đã đóng popup lưu thông tin đăng nhập")
                    time.sleep(1)
            except:
                pass
            
            # 2. Đóng popup "Hiện thông báo" - Click "Chặn"
            try:
                block_btns = driver.find_elements(By.XPATH, 
                    "//div[@role='button' and (contains(text(), 'Chặn') or contains(text(), 'Block'))]")
                if block_btns:
                    block_btns[0].click()
                    print("[✓] Đã đóng popup thông báo")
                    time.sleep(1)
            except:
                pass
                
            # 3. Đóng bất kỳ popup nào có nút X
            try:
                close_btns = driver.find_elements(By.XPATH, 
                    "//div[@aria-label='Đóng' or @aria-label='Close']")
                for btn in close_btns[:2]:
                    try:
                        if btn.is_displayed():
                            btn.click()
                            time.sleep(0.5)
                    except:
                        pass
            except:
                pass
                
        except Exception as e:
            pass
        
        return True
    except Exception as e:
        print(f"[!] Lỗi đăng nhập: {e}")
        return False


def _find_comment_container(driver):
    """Tìm phần tử scrollable chứa comment trong modal bài viết."""
    candidate_xpaths = [
        "//div[@role='dialog']//div[@role='feed']",
        "//div[@role='dialog']//div[contains(@data-visualcompletion,'ignore-dynamic') and contains(@class,'x1n2onr6')]",
        "//div[@role='main']//div[@role='feed']",
        "//div[contains(@aria-label,'Bình luận') and (@role='feed' or @role='main')]",
    ]

    for xpath in candidate_xpaths:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            if element.is_displayed():
                return element
        except Exception:
            continue
    return None

# ========================= CRAWL FUNCTION =========================
def crawl_facebook_comments(post_url, max_comments=2000, driver=None):
    if driver is None:
        driver = get_driver()
        login_facebook(driver)
    
    data = []
    
    try:
        driver.get(post_url)
        time.sleep(8 + random.uniform(0, 3))
        
        # KHÔNG đóng popup ở đây nữa - tránh đóng nhầm modal bài viết
        # Chỉ xử lý popup sau khi đăng nhập
        
        # Scroll xuống phần bình luận
        print(f"[+] Đang crawl: {post_url}")
        print("[+] Đang scroll để load bình luận...")
        
        # Tìm vùng chứa bình luận (trong modal/popup)
        comment_section = _find_comment_container(driver)
        if comment_section:
            print("[✓] Tìm thấy vùng bình luận")
        else:
            print("[!] Không xác định được vùng bình luận, fallback scroll toàn trang")
        
        # Scroll trong vùng bình luận (nếu tìm thấy) hoặc window (nếu không)
        scroll_attempts = 0
        max_scrolls = 30
        last_height = 0
        
        used_comment_scroll = False
        if comment_section:
            # Scroll trong vùng bình luận
            print("[+] Scroll trong vùng bình luận...")
            while scroll_attempts < max_scrolls:
                try:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 600;", comment_section)
                    time.sleep(random.uniform(1, 2))
                    scroll_height = driver.execute_script("return arguments[0].scrollHeight", comment_section)
                    scroll_top = driver.execute_script("return arguments[0].scrollTop", comment_section)
                    if scroll_height == last_height and scroll_top > 0 and scroll_attempts > 10:
                        break
                    
                    last_height = scroll_height
                    scroll_attempts += 1
                    
                    if scroll_attempts % 5 == 0:
                        print(f"   → Đã scroll {scroll_attempts} lần...")
                except Exception as e:
                    break
            used_comment_scroll = scroll_attempts > 0
        else:
            # Fallback: Scroll window
            print("[+] Scroll window (không tìm thấy vùng bình luận)...")
            while scroll_attempts < max_scrolls:
                driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(random.uniform(1.5, 2.5))
                
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height and scroll_attempts > 10:
                    break
                
                last_height = new_height
                scroll_attempts += 1
                
                if scroll_attempts % 5 == 0:
                    print(f"   → Đã scroll {scroll_attempts} lần...")
        
        # Nếu scroll nội bộ không chạy được, thêm một vòng scroll toàn trang để kích hoạt lazy load
        if comment_section and not used_comment_scroll:
            print("[!] Scroll nội bộ không hoạt động, chuyển sang scroll toàn trang")
            for _ in range(10):
                driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(random.uniform(1.5, 2.5))

        print(f"[✓] Hoàn tất scroll (Tổng: {scroll_attempts} lần)")
        time.sleep(2)

        # Click "Xem thêm bình luận" và "Xem thêm phản hồi"
        print("[+] Đang click 'Xem thêm bình luận'...")
        clicked_count = 0
        for attempt in range(30):
            try:
                # Tìm nút "Xem thêm bình luận" cụ thể (không phải link bài viết khác)
                search_root = comment_section if comment_section else driver
                buttons = search_root.find_elements(By.XPATH, 
                    "//div[@role='button' and (contains(text(), 'bình luận') or contains(text(), 'phản hồi'))]")
                
                # Lọc chỉ lấy nút thật sự liên quan đến bình luận
                valid_buttons = []
                for btn in buttons:
                    btn_text = btn.text.lower()
                    # Chỉ click nút có chứa "xem" và "bình luận" hoặc "phản hồi"
                    if ('xem' in btn_text or 'view' in btn_text) and \
                       ('bình luận' in btn_text or 'phản hồi' in btn_text or 'comment' in btn_text or 'repl' in btn_text):
                        # Kiểm tra không phải link bài viết (không có href)
                        try:
                            if not btn.find_elements(By.XPATH, ".//a[@href]"):
                                valid_buttons.append(btn)
                        except:
                            valid_buttons.append(btn)
                
                if not valid_buttons:
                    if attempt > 5:  # Sau 5 lần không tìm thấy thì dừng
                        print(f"   → Đã click {clicked_count} lần")
                        break
                    time.sleep(1)
                    continue
                    
                # Click các nút hợp lệ
                for btn in valid_buttons[:3]:  # Tối đa 3 nút mỗi lần
                    try:
                        # Kiểm tra nút có hiển thị không
                        if btn.is_displayed():
                            driver.execute_script("arguments[0].scrollIntoView(true);", btn)
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", btn)
                            clicked_count += 1
                            time.sleep(random.uniform(1.5, 2.5))
                    except Exception as e:
                        continue
                        
                if attempt % 10 == 0 and attempt > 0:
                    print(f"   → Đã thử click {attempt} lần, thành công {clicked_count} lần")
                    
            except Exception as e:
                continue
        
        print(f"[✓] Hoàn tất click (Tổng: {clicked_count} lần)")

        # Lấy tất cả bình luận - chỉ lấy trong phần comment, tránh lấy menu/sidebar
        print("[+] Đang thu thập bình luận...")
        time.sleep(2)
        
        # Tìm tất cả div chứa bình luận (bao gồm cả nested comments)
        comment_elements = []
        seen_texts = set()  # Tránh trùng lặp
        
        try:
            search_root = comment_section if comment_section else driver
            articles = search_root.find_elements(By.XPATH, ".//div[@role='article']")
            print(f"[+] Tìm thấy {len(articles)} article elements trong vùng comment")
            
            # Bỏ qua phần tử đầu tiên (bài viết gốc)
            for article in articles[1:]:
                try:
                    # Lấy tên người dùng
                    username = "unknown"
                    name_node = article.find_elements(By.XPATH, ".//strong//span") or \
                                article.find_elements(By.XPATH, ".//a[@role='link']//span[contains(@class,'x1lliihq')]")
                    if name_node:
                        username = name_node[0].text.strip() or "unknown"

                    # Lấy nội dung bình luận (chỉ phần body)
                    body_nodes = article.find_elements(By.XPATH, ".//div[@data-ad-preview='message']//span[@dir='auto']")
                    if not body_nodes:
                        body_nodes = article.find_elements(By.XPATH, ".//div[contains(@class,'x1vvkbs') and @dir='auto']")
                    if not body_nodes:
                        body_nodes = article.find_elements(By.XPATH, ".//span[@dir='auto' and not(ancestor::h3)]")

                    comment_text = " ".join([node.text.strip() for node in body_nodes if node.text.strip()])

                    if not comment_text or len(comment_text) < 3:
                        continue

                    # Bỏ qua nếu text bị lẫn menu/sidebar
                    menu_keywords = {
                        'bạn bè', 'video', 'marketplace', 'nhóm', 'bảng feed', 'meta ai',
                        'sự kiện', 'đã lưu', 'kỷ niệm', 'tạo tin', 'xem thêm', 'like',
                        'reply', 'share', 'đã trả lời'
                    }
                    lower_text = comment_text.lower()
                    if any(kw in lower_text for kw in menu_keywords) and len(comment_text) < 25:
                        continue

                    if comment_text in seen_texts:
                        continue

                    seen_texts.add(comment_text)
                    comment_elements.append({
                        'text': comment_text,
                        'username': username if username else 'unknown'
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"[!] Lỗi khi lấy comments: {e}")

        print(f"[+] Đã lọc được {len(comment_elements)} bình luận hợp lệ")

        # Chuyển sang format data
        for idx, comment in enumerate(comment_elements):
            if idx >= max_comments:
                break
            try:
                data.append({
                    "text": comment['text'],
                    "username": comment['username'][:30] + "_fb",
                    "post_url": post_url,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source_platform": "Facebook",
                    "label": None
                })
                if idx % 100 == 0 and idx > 0:
                    print(f"   → Đã xử lý {idx} bình luận")
            except:
                continue

    except Exception as e:
        print(f"[!] Lỗi: {e}")
        import traceback
        traceback.print_exc()
    
    return data

# ========================= MAIN =========================
if __name__ == "__main__":
    print("="*60)
    print("FACEBOOK COMMENT CRAWLER")
    print("="*60)
    
    # Tạo driver và login 1 lần
    driver = get_driver()
    
    try:
        # Login
        if not login_facebook(driver):
            print("[!] Không thể đăng nhập. Vui lòng kiểm tra email/password.")
            driver.quit()
            exit()
        
        # Crawl từng post
        all_data = []
        for idx, url in enumerate(POST_URLS, 1):
            print(f"\n[{idx}/{len(POST_URLS)}] Đang crawl post...")
            comments = crawl_facebook_comments(url, max_comments=3000, driver=driver)
            all_data.extend(comments)
            print(f"[✓] Đã crawl {len(comments)} bình luận từ post này")
            
            if idx < len(POST_URLS):
                wait_time = random.uniform(30, 60)
                print(f"[*] Nghỉ {wait_time:.0f}s trước khi crawl post tiếp theo...")
                time.sleep(wait_time)
    
    finally:
        driver.quit()

    df = pd.DataFrame(all_data)
    df.drop_duplicates(subset=['text'], inplace=True)
    filename = f"fb_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Hoàn thành! Lưu {len(df)} bình luận vào {filename}")