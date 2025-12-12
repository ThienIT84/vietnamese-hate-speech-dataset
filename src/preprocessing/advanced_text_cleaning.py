"""
🔥 ADVANCED TEXT CLEANING FOR PhoBERT
Level 2 Cleaning: Xử lý teencode, lặp ký tự, bypass patterns, emoji
"""

import pandas as pd
import re
import unicodedata

# =====================================================
# 1. TEENCODE DICTIONARY MỞ RỘNG
# =====================================================

TEENCODE_DICT = {
    # === PHỦ ĐỊNH ===
    "ko": "không", "k": "không", "khj": "không", "hk": "không", 
    "hok": "không", "kh": "không", "hem": "không",
    "kp": "không phải", "kbh": "không bao giờ", "kc": "không có",
    "hn": "hà nội", "hcm": "hồ chí minh",  "ngkh": "người khác",
    "rảnh l": "rảnh lồn", "mh": "mình",
    "hà lội": "hà nội",
    
    # === TỪ VIẾT TẮT ===
    "đh": "đại học", "dh": "đại học",
    "thpt": "trung học phổ thông", "thcs": "trung học cơ sở",
    "gđ": "gia đình", "gd": "gia đình",
    
    # === ĐẠI TỪ ===
    "ng": "người", "ngta": "người ta", "nta": "người ta", 
    "mng": "mọi người", "mn": "mọi người", "mk": "mình", 
    "t": "tôi", "tui": "tôi", "m": "mày", "mày": "mày",
    "e": "em", "a": "anh", "c": "chị", "cj": "chị", 
    "ae": "anh em", "ck": "chồng", "vk": "vợ", "vc": "vợ chồng",
    "bạn": "bạn", "ổng": "ông ấy",
    "tụi": "tụi", "bọn": "bọn", "thg": "thằng", "con": "con",
    "đứa": "đứa", "pdb": "phố đi bộ",
    
    # === ĐỘNG TỪ ===
    "ns": "nói", "dc": "được", "đc": "được", "đx": "được",
    "ddc": "được", "dc": "được", "wc": "được",
    "vs": "với", "vj": "vì", "vi": "vì", "ms": "mới",
    "bik": "biết", "bit": "biết", "biet": "biết",
    "hiu": "hiểu", "hjeu": "hiểu",
    "lm": "làm", "lam": "làm",
    "đi": "đi", "di": "đi", "dj": "đi",
    "nch": "nói chuyện", "nc": "nói chuyện",
    "iu": "yêu", "yeu": "yêu", "thg": "thương",
    "nc": "nước", "nuoc": "nước",
    "chj": "chị", "ch": "chị", "cj": "chị",
    # === TRẠNG TỪ / TÍNH TỪ ===
    "ntn": "như thế nào", "ntnao": "như thế nào", "sao": "sao",
    "r": "rồi", "rùi": "rồi", "roi": "rồi",
    "z": "vậy", "v": "vậy", "vậy": "vậy", "zậy": "vậy",
    "lun": "luôn", "luon": "luôn",
    "qá": "quá", "wa": "quá", "wá": "quá",
    "bjo": "bây giờ", "bjh": "bây giờ", "h": "giờ",
    "j": "gì", "g": "gì", "ji": "gì",
    "xúc vật": "súc vật",
    "cg": "cũng", "cung": "cũng", "cux": "cũng",
    "cht": "chút", "chut": "chút", "xíu": "chút",
    "nhìu": "nhiều", "nhiu": "nhiều",
    "lắm": "lắm", "lam": "lắm", "9 xác": "chính xác",
    "bt": "bình thường", "bth": "bình thường", "bthuog": "bình thường",
    "xl": "xấu lắm", "đẹp": "đẹp", "xấu": "xấu", 
    "dị": "vậy",
    # === TỪ NỐI / CẢM THÁN ===
    "nha": "nhé", "nhe": "nhé", "nhá": "nhé",
    "nè": "này", "ne": "này", "như kg": "như không",
    "ơi": "ơi", "oi": "ơi", "ơyyy": "ơi",
    "đê": "đi", "đi": "đi", "mtq": "mạnh thường quân",
    "thui": "thôi", "thoi": "thôi", "xog": "xong", "xin lôi": "xin lỗi", "dới trẻ": "giới trẻ",
    "chớ": "chứ", "chu": "chứ",
    "thiệt": "thật", "thiet": "thật",
    "á": "à", "ak": "à", "ạ": "ạ",
    "oke": "ok", "okie": "ok", "okê": "ok",
    "zô": "vô", "zo": "vô", "vào": "vào",
    "quáaaaa": "quá", "cmt": "bình luận",
    "tar": "ta", "ngo": "ngu", "jv": "gì vậy", "gòi": "rồi",
    "nchung": "nói chung", "tr": "trời", "miên": "miễn", "noi": "nói",
    "giup": "giúp", "dk": "được", "csong": "cuộc sống", "đkh": "đúng không", "đk": "được", 
    "trc": "trước", "cừi chít": "cười chết", "cưng nón": "con nứng", "không âu": "không đâu",
    "tóp tóp": "tiktok", "cx": "cũng", "pbvm": "phân biệt vùng miền", "nầy": "này",
    "Dịt mẹ mầy": "Địt mẹ mày", "kg ăn": "không ăn", "ủ tờ": "ở tù",
    "chúng n": "chúng nó", "thây k": "thấy không", "đkm": "địt con mẹ",
    "đeo chết me": "đéo chết mẹ", "csgt": "cảnh sát giao thông",
    # === TỪ TOXIC (GIỮ NGUYÊN NGHĨA ĐỂ DETECT) ===
    # Vulgar
    "vl": "vãi lồn", "vcl": "vãi cả lồn", "vkl": "vãi cả lồn",
    "vlon": "vãi lồn", "vch": "vãi chó", "vcđ": "vãi cả đái",
    "vcc": "vãi cả cứt", "vleu": "vãi lồn",
    "page": "trang", "diễn diên": "diễn viên", "str": "câu truyện",
    "hãm L": "hãm lồn", "ham l": "hãm lồn", "dân hp": "dân hải phòng",
    "vãi l": "vãi lồn", "bl": "bình luận", "dje mẹ": "địt mẹ",
    
    # Insults - mẹ/má
    "đm": "địt mẹ", "dm": "địt mẹ", "đmm": "địt mẹ mày",
    "dmm": "địt mẹ mày", "đmmm": "địt mẹ mày",
    "dma": "đụ má", "duma": "đụ má", "đuma": "đụ má",
    "đcm": "địt con mẹ", "dcm": "địt con mẹ",
    "đcmm": "địt con mẹ mày", "dcmm": "địt con mẹ mày",
    "cmn": "con mẹ nó", "cmm": "con mẹ mày",
    "mẹ mày": "mẹ mày", "me may": "mẹ mày",
    "ddc": "được", "die": "chết",
    # Insults - body parts
    "cc": "con cặc", "cac": "cặc", "cặc": "cặc", "kặc": "cặc",
    "lồn": "lồn", "lon": "lồn", "loz": "lồn", "lol": "lồn",
    "cl": "cái lồn", "clm": "cái lồn mẹ",
    "đít": "đít", "dit": "đít",
    "cứt": "cứt", "cut": "cứt", "shit": "cứt",
    "con l": "con lồn", "con lon": "con lồn",
    # Insults - general
    "cđ": "cái đéo", "đéo": "đéo", "deo": "đéo",
    "qq": "quần què", "quần què": "quần què",
    "ngu": "ngu", "nguu": "ngu", "gu": "ngu",
    "đần": "đần", "ngan": "ngan",
    "ngáo": "ngáo", "ngao": "ngáo", "khùng": "khùng",
    "điên": "điên", "dien": "điên", "đin": "điên",
    "óc chó": "óc chó", "oc cho": "óc chó",
    "óc lợn": "óc lợn", "oc lon": "óc lợn",
    
    # Threats
    "chs": "chết", "chết": "chết", "chet": "chết",
    "giết": "giết", "giet": "giết",
    "đánh": "đánh", "danh": "đánh",
    "chém": "chém", "chem": "chém",
    
    # Slang toxic
    "tml": "thằng mày lìn", "tmd": "thằng mất dạy",
    "mmd": "mẹ mày đĩ", "cmmm": "con mẹ mày",
    "xạo l": "xạo lồn", "thật ln": "thật luôn",
    "đhs": "đéo hiểu sao", "dhs": "đéo hiểu sao",
    "xạo": "xạo", "xao": "xạo", "xạo lồn": "xạo lồn",
    "mất dạy": "mất dạy", "mat day": "mất dạy",
    "vô học": "vô học", "vo hoc": "vô học",
    "khốn nạn": "khốn nạn", "khon nan": "khốn nạn",
    "đồ khốn": "đồ khốn", "do khon": "đồ khốn",
    "rác": "rác", "rác rưởi": "rác rưởi",
    "phế": "phế", "đồ phế": "đồ phế", "mặt l": "mặt lồn",
    "vãi lìn": "vãi lồn", "đcu": "địt cụ",
    "hong": "không", "mik": "mình", "gđ": "gia đình", "paki": "bắc kỳ",
    # Body shaming
    "béo": "béo", "mập": "mập", "heo": "heo",
    "gầy": "gầy", "còm": "còm", "xương": "xương",
    "xấu": "xấu", "못생긴": "xấu",  # Korean slang
    "đen": "đen", "trắng": "trắng",
    
    # Drama/showbiz
    "phe": "phe", "anti": "anti", "hóng": "hóng",
    "tea": "tea", "bóc phốt": "bóc phốt", 
    "quay xe": "quay xe", "flop": "flop",
    "sân si": "ghen tị", "gato": "ghen tị",
    "câu like": "câu like", "câu view": "câu view",
    "làm lố": "làm quá", "lố": "quá lố",
    "mxh": "mạng xã hội", "xin loi": "xin lỗi",
    
    # Social media
    "ad": "admin", "ytb": "youtube", "fb": "facebook",
    "zl": "zalo", "ig": "instagram", "tt": "tiktok",
    "live": "livestream", "cmt": "bình luận", "sr": "xin lỗi",

    
    # Mixed language toxic
    "stupid": "ngu", "idiot": "đồ ngốc", "dumb": "ngu",
    "bitch": "con đĩ", "fuck": "địt", "shit": "cứt", "pakky": "bắc kỳ",
    "trash": "rác", "loser": "kẻ thua cuộc", "ni": "này", "bắt kì": "bắc kỳ",
    "ngu l": "ngu lồn", "sút vật": "súc vật", "tau": "tao", "2vc": "2 vợ chồng", "kg tha": "không tha",
    # Địa điểm 
    "pbd": "phố đi bộ", "ló": "nó", "zợ": "vợ", "seo": "sao", "khg": "không","dzaii": "đẹp trai",
    "6 tính": "xấu tính", "thui": "thôi", "hoi": "thôi", "cíu": "cứu", "dzai": "đẹp trai",
    "h": "giờ", "sg": "sài gòn", "toai": "tôi", "du ma": "đụ má", "vn": "việt nam", "chx": "chưa",
    "nốn lừg": "nứng lồn", "đừg": "đừng", "đánh chít": "đánh chết", "mien nam": "miền nam",
    # === TỪ TIẾNG ANH → TIẾNG VIỆT ===
    "acc": "tài khoản", "account": "tài khoản", "clgv": "cái lồn gì vậy",
    "block": "chặn", "blocked": "bị chặn", "rep": "trả lời", "kg chết": "không chết",
    "kg quan trọng": "không quan trọng", "cừi ỉe": "cười ỉa",
    "cty": "công ty", "zời ơi": "trời ơi", "đây b": "đây bạn", "chóo": "chó", "làm ny": "làm người yêu",
    "report": "báo cáo", "reported": "bị báo cáo",
    "follow": "theo dõi", "follower": "người theo dõi", "followers": "người theo dõi",
    "unfollow": "bỏ theo dõi", "hl": "hãm lồn",
    "post": "bài đăng", "posted": "đăng",
    "story": "tin", "stories": "tin", "ib": "nhắn tin",
    "view": "lượt xem", "views": "lượt xem",
    "sub": "đăng ký", "subscribe": "đăng ký", "subscriber": "người đăng ký",
    "upload": "tải lên", "download": "tải xuống",
    "online": "trực tuyến", "offline": "ngoại tuyến",
    "inbox": "tin nhắn", 
    "notify": "thông báo", "notification": "thông báo",
    "hashtag": "thẻ", "tag": "gắn thẻ", "content": "nội dung", "đ ngờ": "đéo ngờ",
    "viral": "lan truyền", "trending": "xu hướng",
    "caption": "chú thích",
    "repost": "đăng lại", "share": "chia sẻ",
    "fake": "giả", "real": "thật",
    "hater": "người ghét", "haters": "người ghét",
    "toxic": "độc hại", "toxic": "độc hại", "bửng": "bẩn", "hqa": "hôm qua", "bill": "hóa đơn",
    "cringe": "nhảm", "sus": "đáng ngờ",
    "simp": "lụy tình", "ship": "ghép đôi",
    "flex": "khoe", "slay": "xuất sắc", "vãi lòn": "vãi lồn",
    "admin": "quản trị viên", "ik": "đi", "xàm l": "xàm lồn", "ccjv": "con cặc gì vậy",
    "nhà thờ ĐB": "nhà thờ đức bà", "thế s": "thế sao", "cmnl": "con mẹ nó lồn", "cái l máy": "cái lồn má",

    
    # === PHÂN BIỆT VÙNG MIỀN ===
    "parky": "bắc kỳ", "bắc kì": "bắc kỳ", "bac ky": "bắc kỳ", "đ mời":"đéo mời","dkm":"địt con mẹ",
    "namky": "nam kỳ", "nam kì": "nam kỳ", "nam ky": "nam kỳ", "coa": "có", "cmnr": "con mẹ nó rồi",
    "bắc kỳ rau muống": "bắc kỳ rau muống", "thôi b": "thôi bạn", "noa": "nó","ykr": "ý kiến riêng",
    "nam kỳ quốc": "nam kỳ quốc", "ní": "bạn", "khum": "không", "fai": "phải", "tk hèn": "thằng hèn",
    "dân bắc": "dân bắc", "dân nam": "dân nam", "ksao": "không sao", "tôy": "tôi",
    "người bắc": "người bắc", "người nam": "người nam", "mtq": "mạnh thường quân", "nhảm l": "nhảm lồn",
    "mttq": "mặt trận tổ quốc", "đau l": "đau lồn",
    "giọng bắc": "giọng bắc", "giọng nam": "giọng nam",
}

# =====================================================
# 2. EMOJI MAPPING
# =====================================================

EMOJI_SENTIMENT = {
    # Negative
    "😢": "", "😭": "", "😡": "", "🤬": "", "😤": "",
    "💀": "", "☠️": "", "🖕": "", "😒": "", "😠": "",
    "🙄": "", "😑": "", "😐": "", "💩": "", "🤮": "",
    
    # Positive (có thể bỏ hoặc giữ)
    "😂": "", "🤣": "", "😆": "", "😁": "", "😊": "",
    "❤️": "", "💕": "", "👍": "", "🙏": "", "😍": "",
    
    # Neutral - xóa hết
    "🥲": "", "😅": "", "🙂": "", "😶": "",
}

# Text emoticons mapping (dạng ký tự ASCII)
# CHỈ xóa emoticons, KHÔNG xóa từ như haha, hihi (giữ lại vì có nghĩa)
TEXT_EMOTICONS = {
    # Cười - chỉ xóa ký tự đặc biệt
    ":)))": "", ":))": "", ":)": "", "(:": "",
    "=)))": "", "=))": "", "=)": "",
    ":D": "", ":d": "", "xD": "", "XD": "", "xd": "",
    ":v": "", ":V": "", ":3": "", "((": "",
    "^^": "", "^_^": "", "^-^": "", "kk": "", "kaka":"",    
    # KHÔNG xóa haha, hihi, hehe vì đây là từ có nghĩa
    
    # Buồn/Khóc
    ":(": "", ":((": "", ":(((": "",
    "='(": "", "T_T": "", "T.T": "",
    ";(": "", ";((": "",
    
    # Ngạc nhiên
    ":O": "", ":o": "", ":0": "",
    "O_O": "", "o_o": "", "O.O": "",
    
    # Khác
    ":-/": "", ":/": "", ":-|": "",
    ";)": "", ";-)": "",
    ":P": "", ":p": "", ":-P": "",
    "<3": "", "</3": "",
}

# =====================================================
# 3. CLEANING FUNCTIONS
# =====================================================

def remove_urls(text):
    """Xóa URLs"""
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    return text

def remove_html(text):
    """Xóa HTML tags"""
    return re.sub(r'<[^>]+>', '', text)

def remove_mentions(text):
    """Thay @mentions bằng <USER> và tên riêng bằng <PERSON>"""
    # Thay @username bằng <USER>
    text = re.sub(r'@[\w\-\.]+', '<USER>', text)
    return text

def replace_person_names(text):
    """Thay thế tên riêng tiếng Việt bằng <PERSON>
    Pattern: 2-4 từ viết hoa liên tiếp (Nguyễn Văn A, Trần Thị Bích Ngọc)
    """
    # Whitelist địa danh - KHÔNG thay thế
    location_whitelist = [
        # Thành phố lớn
        'Hà Nội', 'Hải Phòng', 'Hồ Chí Minh', 'Đà Nẵng', 'Cần Thơ',
        'Sài Gòn', 'Huế', 'Nha Trang', 'Đà Lạt', 'Vũng Tàu',
        'Hạ Long', 'Phú Quốc', 'Quy Nhơn', 'Thanh Hóa', 'Vinh',
        # Tỉnh/địa danh
        'Bình Dương', 'Đồng Nai', 'Long An', 'Bà Rịa', 'Tiền Giang',
        'An Giang', 'Kiên Giang', 'Bến Tre', 'Trà Vinh', 'Sóc Trăng',
        'Bạc Liêu', 'Cà Mau', 'Hậu Giang', 'Vĩnh Long', 'Đồng Tháp',
        'Lâm Đồng', 'Bình Phước', 'Tây Ninh', 'Bình Thuận', 'Ninh Thuận',
        'Khánh Hòa', 'Phú Yên', 'Bình Định', 'Quảng Ngãi', 'Quảng Nam',
        'Quảng Trị', 'Thừa Thiên Huế', 'Quảng Bình', 'Hà Tĩnh', 'Nghệ An',
        'Thanh Hóa', 'Ninh Bình', 'Nam Định', 'Thái Bình', 'Hà Nam',
        'Hưng Yên', 'Hải Dương', 'Bắc Ninh', 'Bắc Giang', 'Quảng Ninh',
        'Lạng Sơn', 'Cao Bằng', 'Hà Giang', 'Lào Cai', 'Yên Bái',
        'Tuyên Quang', 'Phú Thọ', 'Vĩnh Phúc', 'Thái Nguyên', 'Lai Châu',
        'Điện Biên', 'Sơn La', 'Hòa Bình', 'Kon Tum', 'Gia Lai',
        'Đắk Lắk', 'Đắk Nông', 'Lâm Đồng',
        # Quận/huyện/xã thường xuất hiện
        'Dĩ An', 'Thủ Đức', 'Tân Bình', 'Bình Thạnh', 'Gò Vấp',
        'Phú Nhuận', 'Tân Phú', 'Bình Tân', 'Hóc Môn', 'Củ Chi',
        'Nhà Bè', 'Cần Giờ', 'Hoàng Mai', 'Cầu Giấy', 'Đống Đa',
        'Hai Bà Trưng', 'Ba Đình', 'Hoàn Kiếm', 'Tây Hồ', 'Long Biên',
        # Khu vực
        'Bắc Kỳ', 'Trung Kỳ', 'Nam Kỳ', 'Bắc Bộ', 'Trung Bộ', 'Nam Bộ',
        'Miền Bắc', 'Miền Trung', 'Miền Nam', 'Tây Nguyên', 'Đồng Bằng Sông Cửu Long',
        'Tây Bắc', 'Đông Bắc', 'Đông Nam Bộ', 'Tây Nam Bộ',
        # Quốc gia
        'Việt Nam', 'Hàn Quốc', 'Trung Quốc', 'Nhật Bản', 'Mỹ', 'Anh',
        'Pháp', 'Đức', 'Nga', 'Úc', 'Ý', 'Tây Ban Nha', 'Bồ Đào Nha',
        'Thái Lan', 'Singapore', 'Malaysia', 'Indonesia', 'Philippines',
        'Campuchia', 'Lào', 'Myanmar', 'Ấn Độ', 'Pakistan', 'Bangladesh',
    ]
    
    # Bảo vệ địa danh bằng placeholder
    protected = {}
    for i, loc in enumerate(location_whitelist):
        if loc in text:
            placeholder = f'__LOC{i}__'
            protected[placeholder] = loc
            text = text.replace(loc, placeholder)
    
    # Danh sách họ phổ biến Việt Nam để tăng độ chính xác
    vietnamese_surnames = r'(?:Nguyễn|Trần|Lê|Phạm|Hoàng|Huỳnh|Phan|Vũ|Võ|Đặng|Bùi|Đỗ|Hồ|Ngô|Dương|Lý|Lưu|Trịnh|Đinh|Cao|Tạ|Tô|Tống|Đoàn|Lương|Hà|Văn|Vương|Trương|Quách|Châu|Mai|Đào|Lâm|Thái|Quang|Kiều|Tăng|Từ|Hứa)'
    
    # Pattern 1: Họ Việt Nam + 1-3 tên (Nguyễn Văn A, Trần Thị Bích Ngọc)
    pattern1 = vietnamese_surnames + r'(?:\s+[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]*){1,3}'
    text = re.sub(pattern1, '<PERSON>', text)
    
    # Pattern 2: 2-4 từ viết hoa liên tiếp (tên không có họ phổ biến)
    pattern2 = r'\b[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+(?:\s+[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+){1,3}\b'
    text = re.sub(pattern2, '<PERSON>', text)
    
    # Khôi phục địa danh
    for placeholder, loc in protected.items():
        text = text.replace(placeholder, loc)
    
    return text

def remove_repeated_chars(text):
    """Xử lý ký tự lặp: nguuuuu → ngu, đmmmmm → đm"""
    # Lặp 3+ ký tự → 1 ký tự (cho phụ âm)
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    return text

def remove_bypass_patterns(text):
    """Xử lý bypass patterns: n.g.u → ngu, đ-m → đm
    CHỈ xử lý giữa các CHỮ CÁI, không xử lý số
    """
    # Xóa dấu chấm giữa các chữ cái đơn (không phải số)
    text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\.([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\.?([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])?', r'\1\2\3', text)
    # Xóa dấu gạch giữa các chữ cái đơn (không phải số)
    text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\-([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r'\1\2', text)
    # Xóa dấu gạch dưới giữa các chữ cái đơn
    text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\_([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r'\1\2', text)
    # Xóa dấu * giữa các chữ cái
    text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\*([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r'\1\2', text)
    return text

def convert_leetspeak(text):
    """Chuyển số thành chữ CHỈ KHI số nằm trong từ có chữ cái
    Ví dụ: ngu4 → ngua, ch3t → chết
    KHÔNG convert: 3-4năm, 3v, 25k (số đứng riêng hoặc đầu từ)
    """
    import re
    
    # Chỉ convert số khi nằm GIỮA hoặc SAU chữ cái (không phải đầu từ)
    # Pattern: chữ + số → chữ + chữ
    leetspeak_map = {
        '0': 'o', '1': 'i', '3': 'e', '4': 'a',
        '5': 's', '7': 't', '8': 'b', '9': 'g',
    }
    
    for num, char in leetspeak_map.items():
        # Chỉ replace khi số đứng SAU chữ cái (ví dụ: ngu4, ch3t)
        text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])' + num, r'\1' + char, text)
    
    return text

def normalize_unicode(text):
    """Chuẩn hóa Unicode tricks: ηgu → ngu"""
    # Map các ký tự Unicode giống chữ Latin
    unicode_map = {
        'η': 'n',  # Greek eta
        'α': 'a',  # Greek alpha
        'ℓ': 'l',  # Script l
        'σ': 'o',  # Greek sigma
        'υ': 'u',  # Greek upsilon
        'ι': 'i',  # Greek iota
        '℮': 'e',  # Estimated sign
        'ο': 'o',  # Greek omicron
    }
    for uni, ascii_char in unicode_map.items():
        text = text.replace(uni, ascii_char)
    return text

def remove_emojis(text):
    """Xóa hoặc convert emoji"""
    # Convert emoji có sentiment
    for emoji, replacement in EMOJI_SENTIMENT.items():
        text = text.replace(emoji, replacement)
    
    # Xóa tất cả emoji còn lại
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # supplemental symbols
        u"\U0001FA00-\U0001FA6F"  # chess symbols
        u"\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    return text

def remove_text_emoticons(text):
    """Xóa text emoticons dạng ASCII như :)), =)), :D, :("""
    # Xử lý theo thứ tự dài -> ngắn để tránh replace sai
    sorted_emoticons = sorted(TEXT_EMOTICONS.keys(), key=len, reverse=True)
    for emoticon in sorted_emoticons:
        text = text.replace(emoticon, TEXT_EMOTICONS[emoticon])
    
    # Xóa pattern còn sót: nhiều dấu ngoặc liên tiếp sau dấu hai chấm hoặc bằng
    text = re.sub(r'[:;=]\)*', '', text)  # :))) hoặc =)))
    text = re.sub(r'[:;=]\(*', '', text)  # :(( hoặc ;((
    
    return text

def normalize_teencode(text):
    """Apply teencode dictionary với word boundary"""
    for teencode, standard in TEENCODE_DICT.items():
        # Word boundary để tránh replace substring
        pattern = r'\b' + re.escape(teencode) + r'\b'
        text = re.sub(pattern, standard, text, flags=re.IGNORECASE)
    return text

def normalize_whitespace(text):
    """Chuẩn hóa khoảng trắng"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def normalize_punctuation(text):
    """Chuẩn hóa dấu câu - thêm khoảng trắng sau dấu chấm, phẩy nếu thiếu"""
    # Thay nhiều dấu chấm liên tiếp thành 1 dấu chấm + khoảng trắng
    text = re.sub(r'\.{2,}', '. ', text)
    # Thêm khoảng trắng sau dấu chấm nếu theo sau là chữ cái (không phải số)
    text = re.sub(r'\.([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r'. \1', text)
    # Thêm khoảng trắng sau dấu phẩy nếu thiếu
    text = re.sub(r',([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r', \1', text)
    # Thêm khoảng trắng sau dấu chấm hỏi, chấm than nếu thiếu
    text = re.sub(r'([?!])([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r'\1 \2', text)
    return text

# =====================================================
# 4. MAIN CLEANING PIPELINE
# =====================================================

def advanced_clean_text(text):
    """
    Pipeline cleaning hoàn chỉnh cho PhoBERT
    """
    if not isinstance(text, str) or not text:
        return ""
    
    # Step 1: Remove URLs, HTML (trước khi xử lý khác)
    text = remove_urls(text)
    text = remove_html(text)
    
    # Step 2: Replace @mentions with <USER>
    text = remove_mentions(text)
    
    # Step 3: Replace person names with <PERSON> (TRƯỚC KHI lowercase)
    text = replace_person_names(text)
    
    # Step 5: Lowercase
    text = text.lower()
    
    # Step 6: Normalize Unicode tricks
    text = normalize_unicode(text)
    
    # Step 7: Remove bypass patterns (n.g.u → ngu)
    text = remove_bypass_patterns(text)
    
    # Step 8: Convert leetspeak (số → chữ)
    text = convert_leetspeak(text)
    
    # Step 9: Remove repeated chars (nguuuu → ngu)
    text = remove_repeated_chars(text)
    
    # Step 10: Apply teencode dictionary
    text = normalize_teencode(text)
    
    # Step 11: Remove/convert emojis (Unicode)
    text = remove_emojis(text)
    
    # Step 12: Remove text emoticons (ASCII như :)), =)), :D)
    text = remove_text_emoticons(text)
    
    # Step 13: Normalize punctuation (thêm khoảng trắng sau dấu câu)
    text = normalize_punctuation(text)
    
    # Step 14: Normalize whitespace
    text = normalize_whitespace(text)
    
    return text

# =====================================================
# 5. TEST
# =====================================================

if __name__ == "__main__":
    print("="*80)
    print("🔥 TEST ADVANCED TEXT CLEANING")
    print("="*80)
    
    test_cases = [
        # Teencode
        ("tui k bik m ns j", "tôi không biết mày nói gì"),
        ("ko dc đâu", "không được đâu"),
        
        # Lặp ký tự
        ("nguuuuuu quá", "ngu quá"),
        ("đmmmmmm", "địt mẹ"),
        
        # Bypass patterns
        ("đồ n.g.u", "đồ ngu"),
        ("v-l quá", "vãi lìn quá"),
        ("c_c", "cặc"),
        
        # Leetspeak
        ("ch3t đi", "chết đi"),
        ("ngu4 quá", "ngua quá"),
        
        # Emoji
        ("xấu quá 😢😭", "xấu quá"),
        ("ngu 💀💀💀", "ngu"),
        
        # Mentions
        ("@user123 mày ngu", "mày ngu"),
        ("Nguyễn Văn A mày ngu quá", "mày ngu quá"),
        
        # Mixed
        ("@abc nguuuu v.l 😡😡", "ngu vãi lìn"),
        ("Stupid vl", "ngu vãi lìn"),
        
        # Complex
        ("đ.m.m nguuuu quá 💀💀 @hater", "địt mẹ mày ngu quá"),
    ]
    
    print(f"\n{'INPUT':<45} | {'OUTPUT':<35} | {'EXPECTED':<35}")
    print("-"*120)
    
    passed = 0
    for input_text, expected in test_cases:
        output = advanced_clean_text(input_text)
        status = "✅" if output == expected else "❌"
        if output == expected:
            passed += 1
        print(f"{input_text:<45} | {output:<35} | {expected:<35} {status}")
    
    print("-"*120)
    print(f"\n📊 Passed: {passed}/{len(test_cases)} tests")
    
    print(f"\n" + "="*80)
    print(f"📋 TEENCODE DICTIONARY: {len(TEENCODE_DICT)} từ")
    print("="*80)
