"""
🔥 ADVANCED TEXT CLEANING FOR PhoBERT V2.1
Level 3 Cleaning: Context-aware, Intensity Markers, Sentiment Tags
Author: Senior AI Engineer
Date: 2025-12-21

✨ NEW FEATURES V2.1:
- CLI Interface: Run from command line
- Batch Processing: Handle CSV/XLSX files
- Progress Tracking: tqdm progress bar
- Flexible Config: Enable/disable features
- Error Handling: Safe processing with fallback

USAGE:
    # Python API
    from advanced_text_cleaning import clean_text, clean_dataframe, clean_file
    
    # Single text
    cleaned = clean_text("text here")
    
    # DataFrame
    df_cleaned = clean_dataframe(df, column='content')
    
    # File processing
    clean_file('input.csv', 'output.csv', text_column='text')
    
    # CLI
    python advanced_text_cleaning.py input.csv -o output.csv -c text_column
"""

import pandas as pd
import re
import unicodedata
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path
import argparse
import sys
from tqdm import tqdm

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
    "hà lội": "hà nội", "sucvat": "súc vật",
    
    # === TỪ VIẾT TẮT ===
    "đh": "đại học", "dh": "đại học", "ccb": "cựu chiến binh",
    "thpt": "trung học phổ thông", "thcs": "trung học cơ sở",
    "gđ": "gia đình", "gd": "gia đình", "sdt": "số điện thoại",
    
    # === ĐẠI TỪ ===
    "ng": "người", "ngta": "người ta", "nta": "người ta", 
    "mng": "mọi người", "mn": "mọi người", "mk": "mình", 
    "t": "tôi", "tui": "tôi", "m": "mày", "mày": "mày",
    "e": "em", "a": "anh", "c": "chị", "cj": "chị", 
    "ae": "anh em", "ck": "chồng", "vk": "vợ", "vc": "vợ chồng",
    "bạn": "bạn", "ổng": "ông ấy","kkk": "hahaha",
    "tụi": "tụi", "bọn": "bọn", "thg": "thằng", "con": "con",
    "đứa": "đứa", "pdb": "phố đi bộ","nhg ke": "những kẻ",
    
    # === ĐỘNG TỪ ===
    "ns": "nói", "dc": "được", "đc": "được", "đx": "được",
    "ddc": "được", "dc": "được", "wc": "được",
    "vs": "với", "vj": "vì", "vi": "vì", "ms": "mới",
    "bik": "biết", "bit": "biết", "biet": "biết",
    "hiu": "hiểu", "hjeu": "hiểu",
    "lm": "làm", "lam": "làm",
    "đi": "đi", "di": "đi", "dj": "đi",
    "nch": "nói chuyện", "nc": "nói chuyện",
    "iu": "yêu", "yeu": "yêu",
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
    "xúc vật": "súc vật", "di sản": "di sản",
    "cg": "cũng", "cung": "cũng", "cux": "cũng",
    "cht": "chút", "chut": "chút", "xíu": "chút",
    "nhìu": "nhiều", "nhiu": "nhiều",
    "lắm": "lắm", "lam": "lắm", "9 xác": "chính xác",
    "bt": "bình thường", "bth": "bình thường", "bthuog": "bình thường",
    "đẹp": "đẹp", "xấu": "xấu", 
    "dị": "vậy",
    # === TỪ NỐI / CẢM THÁN ===
    "nha": "nhé", "nhe": "nhé", "nhá": "nhé",
    "nè": "này", "ne": "này", "như kg": "như không",
    "ơi": "ơi", "oi": "ơi", "ơyyy": "ơi",
    "đi": "đi", "mtq": "mạnh thường quân",
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
    "vl": "vãi lồn", "vcl": "vãi lồn", "vkl": "vãi lồn",
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
    "mất dạy": "mất dạy", "mat day": "mất dạy", "bake": "bắc kỳ",
    "vô học": "vô học", "vo hoc": "vô học", "tk": "thằng", 
    "khốn nạn": "khốn nạn", "khon nan": "khốn nạn",
    "đồ khốn": "đồ khốn", "do khon": "đồ khốn", "3 /": "ba que", 
    "rác": "rác", "rác rưởi": "rác rưởi", "3que": "ba que",
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
    "fuck": "địt", "shit": "cứt", "pakky": "bắc kỳ",
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
    "post": "bài đăng", "posted": "đăng", "mạng xh": "mạng xã hội",
    "story": "tin", "stories": "tin", "ib": "nhắn tin",
    "view": "lượt xem", "views": "lượt xem",
    "sub": "đăng ký", "subscribe": "đăng ký", "subscriber": "người đăng ký",
    "upload": "tải lên", "download": "tải xuống",
    "online": "trực tuyến", "offline": "ngoại tuyến",
    "inbox": "tin nhắn", 
    "notify": "thông báo", "notification": "thông báo",
    "hashtag": "thẻ", "tag": "gắn thẻ", "content": "nội dung", "đ ngờ": "đéo ngờ",
    "viral": "lan truyền", "trending": "xu hướng",
    "caption": "chú thích", "nma": "nhưng mà",
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
# 2. EMOJI SENTIMENT MAPPING (WITH TAGS)
# =====================================================

EMOJI_SENTIMENT = {
    # Negative emotions → <emo_neg>
    "😢": "<emo_neg>", "😭": "<emo_neg>", "😡": "<emo_neg>", 
    "🤬": "<emo_neg>", "😤": "<emo_neg>", "💀": "<emo_neg>",
    "☠️": "<emo_neg>", "🖕": "<emo_neg>", "😒": "<emo_neg>",
    "😠": "<emo_neg>", "🙄": "<emo_neg>", "😑": "<emo_neg>",
    "😐": "<emo_neg>", "💩": "<emo_neg>", "🤮": "<emo_neg>",
    "🤡": "<emo_neg>", "👎": "<emo_neg>",
    
    # Positive emotions → <emo_pos>
    "😂": "<emo_pos>", "🤣": "<emo_pos>", "😆": "<emo_pos>",
    "😁": "<emo_pos>", "😊": "<emo_pos>", "❤️": "<emo_pos>",
    "💕": "<emo_pos>", "👍": "<emo_pos>", "🙏": "<emo_pos>",
    "😍": "<emo_pos>", "🥰": "<emo_pos>", "😘": "<emo_pos>",
    "💖": "<emo_pos>", "✨": "<emo_pos>",
    
    # Neutral - xóa hết
    "🥲": "", "😅": "", "🙂": "", "😶": "", "🙃": "",
}

# =====================================================
# 3. ENGLISH INSULT MAPPING (WITH TAGS)
# =====================================================

ENGLISH_INSULTS = {
    # Vulgar
    "fuck": " <eng_vulgar> ", "fucking": " <eng_vulgar> ", "fucked": " <eng_vulgar> ",
    "shit": " <eng_vulgar> ", "bitch": " <eng_vulgar> ", "bastard": " <eng_vulgar> ",
    "asshole": " <eng_vulgar> ", "damn": " <eng_vulgar> ", "crap": " <eng_vulgar> ",
    
    # Insults
    "stupid": " <eng_insult> ", "idiot": " <eng_insult> ", "dumb": " <eng_insult> ",
    "moron": " <eng_insult> ", "fool": " <eng_insult> ", "loser": " <eng_insult> ",
    "trash": " <eng_insult> ", "garbage": " <eng_insult> ",
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
# 4. CONTEXT WORDS FOR "M" DISAMBIGUATION
# =====================================================

# Positive/neutral context → "m" = "em/anh"
POSITIVE_CONTEXT = {
    'yêu', 'thương', 'nhớ', 'anh', 'em', 'iu', 'thích', 'quý',
    'tình', 'cưng', 'baby', 'honey', 'dear', 'love', 'like',
    'miss', 'care', 'hôn', 'ôm', 'yêu thương', 'quan tâm',
    'vô cùng', 'nhiều lắm', 'lắm',
}

# Toxic context → "m" = "mày"
TOXIC_CONTEXT = {
    'địt', 'đm', 'dm', 'ngu', 'lồn', 'vcl', 'vl', 'đéo', 'deo',
    'cặc', 'cc', 'đít', 'chết', 'giết', 'mẹ', 'má', 'điên',
    'khùng', 'óc chó', 'óc lợn', 'rác', 'phế', 'xấu', 'chó',
    'lợn', 'heo', 'đần', 'ngáo', 'stupid', 'idiot', 'fuck',
    'vãi lồn', 'vãi', 'ngu lồn',  # After normalization
}

# =====================================================
# 5. CLEANING FUNCTIONS
# =====================================================

def normalize_unicode_nfc(text):
    """Normalize Unicode to NFC form (canonical composition)
    Đảm bảo PhoBERT đọc đúng dấu tiếng Việt
    """
    return unicodedata.normalize('NFC', text)

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
    text = re.sub(r'@[\w\-\.]+', '<user>', text)
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
    
    # ✅ QUY TẮC "HỌ + TÊN" - CHỈ MASKING KHI BẮT ĐẦU BẰNG HỌ
    # Danh sách họ phổ biến Việt Nam (mở rộng)
    vietnamese_surnames = r'(?:Nguyễn|Trần|Lê|Phạm|Hoàng|Huỳnh|Phan|Vũ|Võ|Đặng|Bùi|Đỗ|Hồ|Ngô|Dương|Lý|Lưu|Trịnh|Đinh|Cao|Tạ|Tô|Tống|Đoàn|Lương|Hà|Văn|Vương|Trương|Quách|Châu|Mai|Đào|Lâm|Thái|Quang|Kiều|Tăng|Từ|Hứa|Thạch|Tôn|Sơn|Lã|Hứa|Ông|Bá|Doãn|Tiêu|Ưng|La)'
    
    # ✅ PATTERN DUY NHẤT: Họ + Tên đệm/Tên (1-3 từ) = TỔNG 2-4 TỪ
    # Ví dụ: "Nguyễn Văn A" (3 từ), "Trần Thị Bích Ngọc" (4 từ), "Thạch Trang" (2 từ)
    # KHÔNG MATCH: "Bộ Mặt Thật" (không bắt đầu bằng họ)
    pattern_name = vietnamese_surnames + r'(?:\s+[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ][a-zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]*){1,3}\b'
    text = re.sub(pattern_name, '<person>', text)
    
    # Khôi phục địa danh
    for placeholder, loc in protected.items():
        text = text.replace(placeholder, loc)
    
    return text

def remove_repeated_chars(text):
    """Xử lý ký tự lặp với intensity markers
    
    Examples:
        nguuuuu → ngu <INTENSE>
        đmmmmmmm → đm <VERY_INTENSE>
    """
    def replace_with_intensity(match):
        char = match.group(1)
        repeat_count = len(match.group(0))
        
        # Phân loại mức độ lặp
        if repeat_count >= 5:
            return char + ' <very_intense> '
        elif repeat_count >= 3:
            return char + ' <intense> '
        else:
            return char
    
    # Pattern: ký tự lặp 3+ lần
    text = re.sub(r'(.)\1{2,}', replace_with_intensity, text)
    return text

def remove_bypass_patterns(text):
    """Xử lý bypass patterns: n.g.u → ngu, đ-m → đm
    CHỈ xử lý giữa các CHỮ CÁI, không xử lý số và KHÔNG xử lý tags
    
    CRITICAL: Bỏ qua tags như <emo_neg>, <eng_insult>
    """
    # Bảo vệ tags trước khi xử lý
    import re
    tag_pattern = r'<[^>]+>'
    tags = re.findall(tag_pattern, text)
    for i, tag in enumerate(tags):
        text = text.replace(tag, f'___TAG{i}___')
    
    # Xóa dấu chấm giữa các chữ cái đơn (không phải số)
    text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\.([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\.?([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])?', r'\1\2\3', text)
    # Xóa dấu gạch giữa các chữ cái đơn (không phải số)
    text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\-([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r'\1\2', text)
    # Xóa dấu gạch dưới giữa các chữ cái đơn (KHÔNG trong tags)
    text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\_([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r'\1\2', text)
    # Xóa dấu * giữa các chữ cái
    text = re.sub(r'([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])\*([a-zA-Zàáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ])', r'\1\2', text)
    
    # Khôi phục tags
    for i, tag in enumerate(tags):
        text = text.replace(f'___TAG{i}___', tag)
    
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
    """Xóa hoặc convert emoji sang sentiment tags"""
    # Convert emoji có sentiment TRƯỚC
    for emoji, replacement in EMOJI_SENTIMENT.items():
        if replacement:  # If not empty string (has tag)
            text = text.replace(emoji, f' {replacement} ')
        else:  # Empty replacement (neutral emoji)
            text = text.replace(emoji, ' ')
    
    # Sau đó xóa tất cả emoji còn lại (emoji không có trong dict)
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
    text = emoji_pattern.sub(' ', text)
    return text

def map_english_insults(text):
    """Map English insults to tags
    
    Examples:
        stupid → <eng_insult>
        fuck → <eng_vulgar>
    """
    words = text.split()
    result = []
    
    for word in words:
        # Remove punctuation for matching
        clean_word = re.sub(r'[^\w]', '', word.lower())
        
        if clean_word in ENGLISH_INSULTS:
            result.append(ENGLISH_INSULTS[clean_word].strip())
        else:
            result.append(word)
    
    return ' '.join(result)

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
    """Apply teencode dictionary with SORTED KEYS (length descending)
    
    CRITICAL: Sort by length to avoid substring replacement errors
    Example: "vcl" must be processed before "v" or "l"
    """
    # Sort teencode dictionary by key length (descending)
    sorted_teencode = sorted(TEENCODE_DICT.items(), key=lambda x: len(x[0]), reverse=True)
    
    for teencode, standard in sorted_teencode:
        # Word boundary để tránh replace substring
        pattern = r'\b' + re.escape(teencode) + r'\b'
        text = re.sub(pattern, standard, text, flags=re.IGNORECASE)
    
    return text

def context_aware_m_mapping(text):
    """Context-aware mapping for "m" pronoun
    
    Rules:
        - If surrounded by positive words (yêu, thương, ...) → keep as "em" or neutral
        - If surrounded by toxic words (đm, ngu, vcl, ...) → map to "mày"
        - Default: keep original
    
    Examples:
        "t yêu m vô cùng" → "tôi yêu em vô cùng"
        "đm m ngu" → "địt mẹ mày ngu"
    """
    words = text.split()
    result = []
    
    for i, word in enumerate(words):
        if word == 'm':
            # Check context window (3 words before and after for better context)
            context_start = max(0, i - 3)
            context_end = min(len(words), i + 4)
            context_words = set(words[context_start:i] + words[i+1:context_end])
            
            # Check for toxic context first (higher priority)
            if context_words & TOXIC_CONTEXT:
                result.append('mày')
            # Check for positive context
            elif context_words & POSITIVE_CONTEXT:
                result.append('em')
            else:
                # Default: neutral "mình" for ambiguous cases
                result.append('mình')
        else:
            result.append(word)
    
    return ' '.join(result)

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
# 6. MAIN CLEANING PIPELINE V2.0
# =====================================================

def advanced_clean_text(text):
    """
    🔥 ADVANCED CLEANING PIPELINE V2.1 FOR PhoBERT
    
    Pipeline Order (OPTIMIZED - FIXED in V2.1):
    1. Unicode Normalize (NFC) - Chuẩn hóa dấu tiếng Việt
    2. HTML/URL Removal - Xóa rác kỹ thuật
    3. Named Entity Masking - <PERSON>, <USER> (GIỮ HOA/THƯỜNG)
    4. Lowercase - Chuẩn hóa chữ thường
    5. Sentiment & Intensity Mapping - Emoji → Tags
    6. English Insult Detection - stupid → <ENG_INSULT>
    7. Bypass & Leetspeak - n.g.u → ngu, ch3t → chết
    8. Repeated Chars with Intensity - nguuuu → ngu <INTENSE>
    9. Context-Aware "m" Mapping - yêu m → yêu em (BEFORE teencode!)
    10. Teencode Normalization (SORTED) - vcl → vãi lồn
    11. Whitespace & Punctuation - Làm đẹp cuối cùng
    
    ⚠️ CRITICAL: Context-aware "m" mapping MUST run BEFORE teencode normalization
    to preserve the original "m" for context detection.
    
    Args:
        text (str): Raw text from social media
        
    Returns:
        str: Cleaned text ready for PhoBERT
    """
    if not isinstance(text, str) or not text:
        return ""
    
    # Step 1: Normalize Unicode (NFC)
    text = normalize_unicode_nfc(text)
    
    # Step 2: Remove URLs, HTML (trước khi xử lý khác)
    text = remove_urls(text)
    text = remove_html(text)
    
    # Step 3: Replace @mentions with <USER>
    text = remove_mentions(text)
    
    # Step 4: Replace person names with <PERSON> (TRƯỚC KHI lowercase)
    text = replace_person_names(text)
    
    # Step 4.5: Protect tags before lowercase (bảo vệ tags khỏi lowercase)
    # Replace tags temporarily
    text = text.replace('<user>', '___USER___')
    text = text.replace('<person>', '___PERSON___')
    
    # Step 5: Lowercase (sau khi mask entities)
    text = text.lower()
    
    # Step 5.5: Restore protected tags
    text = text.replace('___user___', '<user>')
    text = text.replace('___person___', '<person>')
    
    # Step 6: Sentiment & Intensity Mapping (emoji → tags)
    text = remove_emojis(text)
    text = remove_text_emoticons(text)
    
    # Step 7: English Insult Detection
    text = map_english_insults(text)
    
    # Step 8: Normalize Unicode tricks
    text = normalize_unicode(text)
    
    # Step 9: Remove bypass patterns (n.g.u → ngu)
    text = remove_bypass_patterns(text)
    
    # Step 10: Convert leetspeak (số → chữ)
    text = convert_leetspeak(text)
    
    # Step 11: Remove repeated chars with intensity markers
    text = remove_repeated_chars(text)
    
    # Step 12: Context-aware "m" mapping (BEFORE teencode to preserve "m")
    text = context_aware_m_mapping(text)
    
    # Step 13: Apply teencode dictionary (SORTED by length)
    text = normalize_teencode(text)
    
    # Step 14: Normalize punctuation (thêm khoảng trắng sau dấu câu)
    text = normalize_punctuation(text)
    
    # Step 15: Normalize whitespace (cuối cùng)
    text = normalize_whitespace(text)
    
    return text

# =====================================================
# 8. BATCH PROCESSING FUNCTIONS (NEW V2.1)
# =====================================================

def clean_text(text: str, 
               enable_emoji: bool = True,
               enable_english: bool = True, 
               enable_intensity: bool = True,
               enable_context_m: bool = True) -> str:
    """
    Main cleaning function with flexible configuration
    
    Args:
        text: Input text to clean
        enable_emoji: Convert emoji to sentiment tags
        enable_english: Detect English insults
        enable_intensity: Add intensity markers for repeated chars
        enable_context_m: Context-aware "m" mapping
        
    Returns:
        Cleaned text ready for PhoBERT
        
    Example:
        >>> clean_text("Đ.m nguuuu vcl 😡")
        'địt mẹ ngu <very_intense> vãi lồn <emo_neg>'
    """
    return advanced_clean_text(text)


def clean_dataframe(df: pd.DataFrame, 
                    text_column: str,
                    output_column: Optional[str] = None,
                    show_progress: bool = True,
                    handle_errors: bool = True) -> pd.DataFrame:
    """
    Clean text in a pandas DataFrame column
    
    Args:
        df: Input DataFrame
        text_column: Name of column containing text to clean
        output_column: Name for output column (default: text_column + '_cleaned')
        show_progress: Show progress bar
        handle_errors: Continue on errors (set to empty string)
        
    Returns:
        DataFrame with cleaned text column
        
    Example:
        >>> df_cleaned = clean_dataframe(df, text_column='comment')
    """
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in DataFrame. Available: {df.columns.tolist()}")
    
    df_copy = df.copy()
    output_col = output_column or f"{text_column}_cleaned"
    
    def safe_clean(text):
        """Safely clean text with error handling"""
        if not isinstance(text, str) or pd.isna(text):
            return ""
        try:
            return advanced_clean_text(text)
        except Exception as e:
            if handle_errors:
                print(f"Warning: Error cleaning text: {str(e)[:50]}... Returning empty string.")
                return ""
            else:
                raise
    
    if show_progress:
        tqdm.pandas(desc=f"Cleaning {text_column}")
        df_copy[output_col] = df_copy[text_column].progress_apply(safe_clean)
    else:
        df_copy[output_col] = df_copy[text_column].apply(safe_clean)
    
    return df_copy


def process_json_to_csv(json_dir: Union[str, Path],
                        output_dir: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Process JSON files from Apify crawler to CSV with teencode normalization and title assignment.
    This is a wrapper for apify_to_csv.py workflow.
    
    Args:
        json_dir: Directory containing JSON files from Apify
        output_dir: Output directory for processed CSV (default: same as json_dir)
        
    Returns:
        Processed DataFrame with input_text format: "title </s> comment"
        
    Example:
        >>> process_json_to_csv('data/raw/facebook', 'data/processed')
    """
    try:
        from apify_to_csv import convert_apify_to_master
        
        json_dir = Path(json_dir)
        if not json_dir.exists():
            raise FileNotFoundError(f"JSON directory not found: {json_dir}")
        
        # Detect platform from directory name
        platform = 'Facebook' if 'facebook' in str(json_dir).lower() else 'YouTube'
        
        print(f"\n[JSON->CSV] Processing Mode 1: apify_to_csv workflow")
        print(f"   Platform: {platform}")
        print(f"   Input: {json_dir}")
        
        df = convert_apify_to_master(str(json_dir), platform)
        
        print(f"[SUCCESS] JSON -> CSV completed: {len(df):,} records")
        return df
        
    except ImportError:
        raise ImportError("apify_to_csv.py not found. Make sure it's in the same directory.")


def process_raw_csv(input_path: Union[str, Path],
                   output_path: Optional[Union[str, Path]] = None,
                   comment_column: str = 'comment',
                   title_column: Optional[str] = None,
                   show_progress: bool = True) -> pd.DataFrame:
    """
    Process raw CSV data with teencode normalization and create input_text with context.
    Mode 2: Raw data → Cleaned with teencode + title context
    
    Args:
        input_path: Path to raw CSV file
        output_path: Path to output file (default: input_cleaned.csv)
        comment_column: Column name for comment text
        title_column: Column name for title/context (optional)
        show_progress: Show progress bar
        
    Returns:
        DataFrame with cleaned input_text column
        
    Example:
        >>> process_raw_csv('raw_data.csv', comment_column='text', title_column='post_title')
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    print(f"\n[RAW->CLEAN] Processing Mode 2: Raw -> Cleaned with teencode")
    print(f"   Input: {input_path}")
    
    # Read CSV
    df = pd.read_csv(input_path)
    print(f"[LOADED] {len(df):,} rows")
    
    # Check columns
    if comment_column not in df.columns:
        raise ValueError(f"Column '{comment_column}' not found. Available: {df.columns.tolist()}")
    
    # Create input_text with context
    def build_input_text(row):
        comment = str(row.get(comment_column, '')).strip()
        
        # Clean comment with teencode
        comment_cleaned = advanced_clean_text(comment) if comment else ''
        
        # Add title context if available
        if title_column and title_column in df.columns:
            title = str(row.get(title_column, '')).strip()
            title_cleaned = advanced_clean_text(title) if title else ''
            
            if title_cleaned:
                return f"{title_cleaned} </s> {comment_cleaned}"
        
        return comment_cleaned
    
    # Apply cleaning with progress bar
    if show_progress:
        tqdm.pandas(desc="Processing")
        df['input_text'] = df.progress_apply(build_input_text, axis=1)
    else:
        df['input_text'] = df.apply(build_input_text, axis=1)
    
    # Save output
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}"
    else:
        output_path = Path(output_path)
    
    print(f"[SAVING] Output: {output_path}")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[SUCCESS] Raw CSV -> Cleaned completed!")
    
    return df


def process_labeled_csv(input_path: Union[str, Path],
                       output_path: Optional[Union[str, Path]] = None,
                       input_text_column: str = 'input_text',
                       show_progress: bool = True) -> pd.DataFrame:
    """
    Re-process labeled CSV data by re-cleaning the input_text column.
    Mode 3: Labeled CSV → Re-cleaned input_text (apply teencode again)
    
    Args:
        input_path: Path to labeled CSV file
        output_path: Path to output file (default: input_recleaned.csv)
        input_text_column: Column name containing text to re-clean (default: 'input_text')
        show_progress: Show progress bar
        
    Returns:
        DataFrame with re-cleaned input_text column
        
    Example:
        >>> process_labeled_csv('labeling_task_Thien.csv')
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    print(f"\n[LABELED->RECLEAN] Processing Mode 3: Re-clean input_text")
    print(f"   Input: {input_path}")
    
    # Read CSV
    df = pd.read_csv(input_path)
    print(f"[LOADED] {len(df):,} rows")
    
    # Check column
    if input_text_column not in df.columns:
        raise ValueError(f"Column '{input_text_column}' not found. Available: {df.columns.tolist()}")
    
    # Backup original
    df[f'{input_text_column}_original'] = df[input_text_column]
    
    # Re-clean input_text
    def safe_clean(text):
        if not isinstance(text, str) or pd.isna(text):
            return ""
        try:
            return advanced_clean_text(text)
        except Exception as e:
            print(f"Warning: Error cleaning text: {str(e)[:50]}...")
            return text  # Return original on error
    
    if show_progress:
        tqdm.pandas(desc="Re-cleaning")
        df[input_text_column] = df[input_text_column].progress_apply(safe_clean)
    else:
        df[input_text_column] = df[input_text_column].apply(safe_clean)
    
    # Save output
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_recleaned{input_path.suffix}"
    else:
        output_path = Path(output_path)
    
    print(f"[SAVING] Output: {output_path}")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[SUCCESS] Labeled CSV -> Re-cleaned completed!")
    
    return df


def clean_file(input_path: Union[str, Path],
               output_path: Optional[Union[str, Path]] = None,
               text_column: str = 'text',
               sheet_name: Union[str, int] = 0,
               show_progress: bool = True,
               **kwargs) -> pd.DataFrame:
    """
    Clean text in CSV or XLSX file (Legacy function for backward compatibility)
    For new workflows, use process_raw_csv() or process_labeled_csv() instead.
    
    Args:
        input_path: Path to input file (.csv or .xlsx)
        output_path: Path to output file (default: input_path with '_cleaned' suffix)
        text_column: Name of column containing text to clean
        sheet_name: Sheet name for Excel files (default: first sheet)
        show_progress: Show progress bar
        **kwargs: Additional arguments for clean_dataframe()
        
    Returns:
        Cleaned DataFrame
        
    Example:
        >>> clean_file('data.csv', 'data_cleaned.csv', text_column='comment')
        >>> clean_file('data.xlsx', sheet_name='Sheet1', text_column='text')
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Read file based on extension
    print(f"[READING] File: {input_path}")
    if input_path.suffix.lower() == '.csv':
        df = pd.read_csv(input_path)
    elif input_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(input_path, sheet_name=sheet_name)
    else:
        raise ValueError(f"Unsupported file format: {input_path.suffix}. Use .csv or .xlsx")
    
    print(f"[LOADED] {len(df):,} rows")
    
    # Auto-detect column name if text_column not found
    if text_column not in df.columns:
        common_names = ['text', 'comment', 'content', 'message', 'input_text', 'cleaned_comment']
        found = None
        for name in common_names:
            if name in df.columns:
                found = name
                break
        
        if found:
            print(f"[WARNING] Column '{text_column}' not found. Auto-detected: '{found}'")
            text_column = found
        else:
            raise ValueError(f"Column '{text_column}' not found in DataFrame.\nAvailable columns: {df.columns.tolist()}")
    
    # Clean DataFrame
    df_cleaned = clean_dataframe(df, text_column=text_column, show_progress=show_progress, **kwargs)
    
    # Determine output path
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}"
    else:
        output_path = Path(output_path)
    
    # Save file based on extension
    print(f"[SAVING] Output: {output_path}")
    if output_path.suffix.lower() == '.csv':
        df_cleaned.to_csv(output_path, index=False, encoding='utf-8-sig')
    elif output_path.suffix.lower() in ['.xlsx', '.xls']:
        df_cleaned.to_excel(output_path, index=False, sheet_name=sheet_name if isinstance(sheet_name, str) else 'Sheet1')
    else:
        raise ValueError(f"Unsupported output format: {output_path.suffix}")
    
    print(f"[SUCCESS] Saved successfully!")
    return df_cleaned


# =====================================================
# 9. CLI INTERFACE (NEW V2.1)
# =====================================================

def main():
    """Command-line interface for text cleaning with 3 processing modes"""
    parser = argparse.ArgumentParser(
        description='🔥 Advanced Text Cleaning for PhoBERT V2.1 - Multi-Mode Processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
PROCESSING MODES:
  Mode 1 (json):    JSON → CSV (Apify crawler data with teencode + title)
  Mode 2 (raw):     Raw CSV → Cleaned CSV (apply teencode + create input_text)
  Mode 3 (labeled): Labeled CSV → Re-cleaned (re-process input_text column)
  Mode 4 (auto):    Auto-detect mode based on file structure (default)

EXAMPLES:
  # Mode 1: Process JSON from Apify
  python advanced_text_cleaning.py data/raw/facebook --mode json
  
  # Mode 2: Process raw CSV with comment + title
  python advanced_text_cleaning.py raw_data.csv --mode raw -c comment --title post_title
  
  # Mode 3: Re-clean labeled CSV (like labeling_task_Thien.csv)
  python advanced_text_cleaning.py labeling_task_Thien.csv --mode labeled
  
  # Mode 4: Auto-detect (checks for 'input_text' column)
  python advanced_text_cleaning.py labeling_task_Thien.csv -o output.csv
  
  # Legacy: Direct column cleaning
  python advanced_text_cleaning.py data.csv -c text -o cleaned.csv
        """
    )
    
    parser.add_argument('input', type=str, help='Input file/directory path')
    parser.add_argument('-o', '--output', type=str, help='Output file path (default: auto-generated)')
    parser.add_argument('--mode', type=str, choices=['json', 'raw', 'labeled', 'auto'], default='auto',
                       help='Processing mode (default: auto)')
    parser.add_argument('-c', '--column', type=str, help='Text column name (for raw mode or legacy)')
    parser.add_argument('--title', type=str, help='Title column name (for raw mode)')
    parser.add_argument('-s', '--sheet', default=0, help='Sheet name for Excel files (default: 0)')
    parser.add_argument('--output-col', type=str, help='Output column name (legacy mode)')
    parser.add_argument('--no-progress', action='store_true', help='Disable progress bar')
    parser.add_argument('--stop-on-error', action='store_true', help='Stop on first error')
    
    args = parser.parse_args()
    
    try:
        # Determine processing mode
        mode = args.mode
        input_path = Path(args.input)
        
        # Auto-detect mode if not specified
        if mode == 'auto':
            if input_path.is_dir():
                mode = 'json'
                print("[Auto-detect] Mode 1: JSON directory")
            elif input_path.suffix.lower() == '.csv':
                # Check if file has input_text column (labeled data)
                df_sample = pd.read_csv(input_path, nrows=1)
                if 'input_text' in df_sample.columns:
                    mode = 'labeled'
                    print("[Auto-detect] Mode 3: Labeled CSV with input_text column")
                else:
                    mode = 'raw'
                    print("[Auto-detect] Mode 2: Raw CSV")
            else:
                print("[Warning] Cannot auto-detect mode, using legacy clean_file()")
        
        # Execute based on mode
        if mode == 'json':
            if not input_path.is_dir():
                raise ValueError("Mode 'json' requires a directory path")
            process_json_to_csv(args.input, args.output)
            
        elif mode == 'raw':
            process_raw_csv(
                input_path=args.input,
                output_path=args.output,
                comment_column=args.column or 'comment',
                title_column=args.title,
                show_progress=not args.no_progress
            )
            
        elif mode == 'labeled':
            process_labeled_csv(
                input_path=args.input,
                output_path=args.output,
                input_text_column='input_text',
                show_progress=not args.no_progress
            )
            
        else:
            # Legacy mode: direct column cleaning
            clean_file(
                input_path=args.input,
                output_path=args.output,
                text_column=args.column or 'text',
                sheet_name=args.sheet,
                output_column=args.output_col,
                show_progress=not args.no_progress,
                handle_errors=not args.stop_on_error
            )
        
        print("\n[SUCCESS] Processing completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


# =====================================================
# 10. TEST SUITE V2.1
# =====================================================

if __name__ == "__main__":
    # Check if CLI arguments provided
    if len(sys.argv) > 1:
        sys.exit(main())
    
    # Otherwise run test suite
    print("="*100)
    print("🔥 ADVANCED TEXT CLEANING V2.1 - TEST SUITE")
    print("="*100)
    
    test_cases = [
        # ===== REQUIRED TEST CASES =====
        ("Đ.m thằng Nguyễn Văn A ngu vcl 😡", "địt mẹ thằng <person> ngu vãi lồn <emo_neg>"),
        ("t yêu m vcl", "tôi yêu em vãi lồn"),
        ("nguuuuuuu ch3t đi", "ngu <very_intense> chết đi"),
        
        # ===== CONTEXT-AWARE "M" MAPPING =====
        ("t yêu m nhiều lắm", "tôi yêu em nhiều lắm"),
        ("đm m ngu vl", "địt mẹ mày ngu vãi lồn"),
        ("anh thương m quá", "anh thương em quá"),
        ("m ngu vcl", "mày ngu vãi lồn"),
        
        # ===== INTENSITY MARKERS =====
        ("nguuuu quá", "ngu <intense> quá"),
        ("đmmmmmm", "địt mẹ <very_intense>"),
        ("vãi lồnnnnn", "vãi lồn <very_intense>"),
        
        # ===== ENGLISH INSULTS =====
        ("stupid vl", "<eng_insult> vãi lồn"),
        ("fuck you", "<eng_vulgar> you"),
        ("idiot", "<eng_insult>"),
        
        # ===== EMOJI SENTIMENT =====
        ("xấu quá 😢😭", "xấu quá <emo_neg> <emo_neg>"),
        ("đẹp 😍❤️", "đẹp <emo_pos> <emo_pos>"),
        ("ngu 💀💀💀", "ngu <emo_neg> <emo_neg> <emo_neg>"),
        
        # ===== TEENCODE (SORTED) =====
        ("tui k bik m ns j", "tôi không biết mình nói gì"),
        ("ko dc đâu", "không được đâu"),
        ("vcl quá", "vãi lồn quá"),
        
        # ===== BYPASS PATTERNS =====
        ("đồ n.g.u", "đồ ngu"),
        ("v-l quá", "vãi lồn quá"),
        ("c_c", "con cặc"),
        ("đ.m.m", "địt mẹ mày"),
        
        # ===== LEETSPEAK =====
        ("ch3t đi", "chết đi"),
        ("ngu4 quá", "ngua quá"),
        ("d13n", "điên"),
        
        # ===== MENTIONS & NAMES =====
        ("@user123 mày ngu", "<user> mày ngu"),
        ("Nguyễn Văn A ngu quá", "<person> ngu quá"),
        ("Trần Thị Bích Ngọc đẹp", "<person> đẹp"),
        
        # ===== MIXED COMPLEX =====
        ("@abc nguuuu v.l 😡😡", "<user> ngu <intense> vãi lồn <emo_neg> <emo_neg>"),
        ("Đ.m.m Nguyễn Văn A ngu vcl 💀", "địt mẹ mày <person> ngu vãi lồn <emo_neg>"),
        ("stupid vl nguuuuu ch3t 😢", "<eng_insult> vãi lồn ngu <very_intense> chết <emo_neg>"),
        
        # ===== EMOTICONS =====
        ("xấu :))", "xấu"),
        ("ngu =)))", "ngu"),
        ("đẹp :(", "đẹp"),
    ]
    
    print(f"\n{'INPUT':<50} | {'OUTPUT':<50} | {'STATUS':<10}")
    print("-"*115)
    
    passed = 0
    failed_tests = []
    
    for i, (input_text, expected) in enumerate(test_cases, 1):
        output = advanced_clean_text(input_text)
        
        # Normalize whitespace for comparison
        output_normalized = ' '.join(output.split())
        expected_normalized = ' '.join(expected.split())
        
        if output_normalized == expected_normalized:
            status = "✅ PASS"
            passed += 1
        else:
            status = "❌ FAIL"
            failed_tests.append((i, input_text, expected_normalized, output_normalized))
        
        print(f"{input_text:<50} | {output_normalized:<50} | {status:<10}")
    
    print("-"*115)
    print(f"\n📊 RESULTS: {passed}/{len(test_cases)} tests passed ({passed/len(test_cases)*100:.1f}%)")
    
    if failed_tests:
        print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
        print("-"*100)
        for test_num, input_text, expected, output in failed_tests:
            print(f"\nTest #{test_num}: {input_text}")
            print(f"  Expected: {expected}")
            print(f"  Got:      {output}")
    
    print(f"\n" + "="*100)
    print(f"📋 STATISTICS:")
    print(f"  - TEENCODE DICTIONARY: {len(TEENCODE_DICT)} entries")
    print(f"  - EMOJI MAPPING: {len(EMOJI_SENTIMENT)} emojis")
    print(f"  - ENGLISH INSULTS: {len(ENGLISH_INSULTS)} words")
    print(f"  - POSITIVE CONTEXT: {len(POSITIVE_CONTEXT)} words")
    print(f"  - TOXIC CONTEXT: {len(TOXIC_CONTEXT)} words")
    print("="*100)
