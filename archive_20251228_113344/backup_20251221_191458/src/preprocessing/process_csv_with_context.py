"""
Process CSV/XLSX file với context và teencode normalization
Tương tự apify_to_csv.py nhưng input là CSV/XLSX thay vì JSON

Input CSV/XLSX có thể có các cột:
- text/comment: Nội dung comment (BẮT BUỘC)
- title/postTitle/post_title: Tiêu đề/ngữ cảnh (TÙY CHỌN)
- label: Nhãn có sẵn (TÙY CHỌN)
- note: Ghi chú (TÙY CHỌN)
- id: ID (TÙY CHỌN, tự tạo nếu không có)

Output CSV/XLSX:
- input_text: Format "title </s> comment" hoặc chỉ "comment"
- label: Giữ nguyên nếu có, để trống nếu chưa có
- note: Giữ nguyên nếu có, để trống nếu chưa có

Hỗ trợ: .csv, .xlsx, .xls
"""

import pandas as pd
import hashlib
import sys
import os
from transformers import AutoTokenizer

# Import advanced cleaning
sys.path.append(os.path.dirname(__file__))
from advanced_text_cleaning import advanced_clean_text, TEENCODE_DICT

# Load PhoBERT tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
    print("✓ Loaded PhoBERT tokenizer")
except:
    print("⚠️ Không load được PhoBERT tokenizer, sử dụng word split")
    tokenizer = None

# ===================== EMOJI MAPPING =====================
EMOJI_MAP = {
    '🏳️‍🌈': ' đồng tính ',
    '🏳️‍⚧️': ' chuyển giới ',
    '🌈': ' lgbt ',
    '👨‍❤️‍💋‍👨': ' nam yêu nam ',
    '👩‍❤️‍💋‍👩': ' nữ yêu nữ ',
    '👬': ' nam yêu nam ',
    '👭': ' nữ yêu nữ ',
    '❤️': ' yêu ',
    '💕': ' thương ',
    '💖': ' tình yêu ',
    '😘': ' hôn ',
    '😍': ' thích ',
    '🥰': ' yêu thương ',
    '💔': ' chia tay ',
}

# ===================== FUNCTIONS =====================
def clean_text_with_emoji(text):
    """
    Bước 1: Thay emoji thành text TRƯỚC khi clean
    Bước 2: Xóa hashtags spam
    Bước 3: Apply advanced_clean_text (bao gồm teencode normalization)
    """
    if not text or pd.isna(text):
        return ''
    
    text = str(text)
    
    # 1. Thay emoji TRƯỚC
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    
    # 2. Xóa TOÀN BỘ hashtags
    import re
    text = re.sub(r'#[a-zA-Z0-9_àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ]+', ' ', text)
    
    # 3. Apply advanced cleaning (teencode + tất cả)
    text = advanced_clean_text(text)
    
    return text

def build_input_text(title, comment, max_total_length=256):
    """
    Format: title </s> comment
    Truncate hierarchical: title tối đa 50 tokens, tổng ≤256 tokens
    """
    if pd.isna(title) or not title:
        title = ''
    if pd.isna(comment) or not comment:
        comment = ''
    
    title = str(title).strip()
    comment = str(comment).strip()
    
    # Nếu không có title, chỉ trả về comment
    if not title:
        if tokenizer:
            comment_tokens = tokenizer.tokenize(comment)
            if len(comment_tokens) > max_total_length:
                comment_tokens = comment_tokens[:max_total_length]
                comment = tokenizer.convert_tokens_to_string(comment_tokens)
        return comment
    
    # Có title: tokenize và truncate
    if tokenizer:
        title_tokens = tokenizer.tokenize(title)
        comment_tokens = tokenizer.tokenize(comment)
        
        # Truncate title nếu > 50 tokens
        max_title_len = 50
        if len(title_tokens) > max_title_len:
            title_tokens = title_tokens[:max_title_len]
            title = tokenizer.convert_tokens_to_string(title_tokens)
        
        # Separator: </s>
        sep = ' </s> '
        sep_tokens = tokenizer.tokenize(sep)
        
        # Tính comment max length
        available_for_comment = max_total_length - len(title_tokens) - len(sep_tokens)
        
        # Truncate comment nếu cần
        if len(comment_tokens) > available_for_comment and available_for_comment > 0:
            comment_tokens = comment_tokens[:available_for_comment]
            comment = tokenizer.convert_tokens_to_string(comment_tokens)
        
        # Combine
        input_text = f"{title}{sep}{comment}"
    else:
        # Fallback: dùng word count
        title_words = title.split()
        if len(title_words) > 50:
            title = ' '.join(title_words[:50])
        
        input_text = f"{title} </s> {comment}"
        
        # Simple truncate by words
        words = input_text.split()
        if len(words) > max_total_length:
            input_text = ' '.join(words[:max_total_length])
    
    return input_text

def detect_columns(df):
    """Tự động detect các cột trong CSV"""
    cols = df.columns.tolist()
    
    # Detect comment column
    comment_col = None
    for possible in ['text', 'comment', 'cleaned_text', 'raw_comment', 'content', 'message']:
        if possible in cols:
            comment_col = possible
            break
    
    # Detect title column
    title_col = None
    for possible in ['title', 'postTitle', 'post_title', 'cleaned_title', 'raw_title', 'videoTitle']:
        if possible in cols:
            title_col = possible
            break
    
    # Detect label column
    label_col = 'label' if 'label' in cols else None
    
    # Detect note column
    note_col = 'note' if 'note' in cols else None
    
    # Detect id column
    id_col = 'id' if 'id' in cols else None
    
    return {
        'comment': comment_col,
        'title': title_col,
        'label': label_col,
        'note': note_col,
        'id': id_col
    }

def process_csv(input_path, output_path=None):
    """
    Xử lý file CSV/XLSX với context và teencode normalization
    """
    print("="*80)
    print("XỬ LÝ CSV/XLSX VỚI CONTEXT & TEENCODE NORMALIZATION")
    print("="*80)
    print(f"📂 Input: {input_path}")
    
    # Detect file format và read
    file_ext = os.path.splitext(input_path)[1].lower()
    
    if file_ext in ['.xlsx', '.xls']:
        print(f"📊 Phát hiện file Excel ({file_ext})")
        try:
            df = pd.read_excel(input_path, engine='openpyxl' if file_ext == '.xlsx' else None)
            print(f"✓ Đọc được {len(df):,} dòng từ Excel")
        except ImportError:
            print("❌ Cần cài đặt openpyxl để đọc file Excel:")
            print("   pip install openpyxl")
            return None
    elif file_ext == '.csv':
        print(f"📄 Phát hiện file CSV")
        df = pd.read_csv(input_path)
        print(f"✓ Đọc được {len(df):,} dòng từ CSV")
    else:
        print(f"❌ Format không hỗ trợ: {file_ext}")
        print("   Chỉ hỗ trợ: .csv, .xlsx, .xls")
        return None
    
    # Detect columns
    cols = detect_columns(df)
    print(f"\n🔍 Phát hiện cột:")
    print(f"   - Comment: {cols['comment']}")
    print(f"   - Title: {cols['title']}")
    print(f"   - Label: {cols['label']}")
    print(f"   - Note: {cols['note']}")
    print(f"   - ID: {cols['id']}")
    
    if not cols['comment']:
        print("\n❌ KHÔNG TÌM THẤY CỘT COMMENT!")
        print("   File CSV phải có một trong các cột: text, comment, cleaned_text, content")
        return
    
    print(f"\n⏳ Đang xử lý...")
    
    # Process
    results = []
    for idx, row in df.iterrows():
        # Get comment
        comment_raw = row[cols['comment']]
        if pd.isna(comment_raw) or len(str(comment_raw).strip()) < 3:
            continue
        
        # Get title (nếu có)
        title_raw = row[cols['title']] if cols['title'] else ''
        
        # Clean với emoji mapping
        comment_cleaned = clean_text_with_emoji(comment_raw)
        title_cleaned = clean_text_with_emoji(title_raw)
        
        # Skip nếu cleaned comment rỗng
        if len(comment_cleaned.strip()) < 3:
            continue
        
        # Build input_text
        input_text = build_input_text(title_cleaned, comment_cleaned)
        
        # Get label và note (nếu có)
        label = row[cols['label']] if cols['label'] and cols['label'] in row.index else None
        note = row[cols['note']] if cols['note'] and cols['note'] in row.index else ''
        
        # Get or generate ID
        if cols['id'] and cols['id'] in row.index:
            record_id = row[cols['id']]
        else:
            record_id = hashlib.md5(comment_raw.encode('utf-8')).hexdigest()[:12]
        
        results.append({
            'id': record_id,
            'input_text': input_text,
            'label': label if pd.notna(label) else None,
            'note': note if pd.notna(note) else '',
            'raw_comment': comment_raw,
            'raw_title': title_raw,
        })
    
    # Create output DataFrame
    output_df = pd.DataFrame(results)
    
    print(f"\n✓ Xử lý xong {len(output_df):,} dòng")
    print(f"   (Loại bỏ {len(df) - len(output_df):,} dòng rỗng/ngắn)")
    
    # Determine output path
    if not output_path:
        base_name = os.path.splitext(input_path)[0]
        input_ext = os.path.splitext(input_path)[1].lower()
        output_path = f"{base_name}_processed{input_ext}"
    
    # Save theo format
    output_ext = os.path.splitext(output_path)[1].lower()
    
    if output_ext in ['.xlsx', '.xls']:
        try:
            output_df.to_excel(output_path, index=False, engine='openpyxl')
            print(f"\n💾 Đã lưu Excel: {output_path}")
        except ImportError:
            print("⚠️ Không có openpyxl, lưu thành CSV thay thế")
            output_path = output_path.replace(output_ext, '.csv')
            output_df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"💾 Đã lưu CSV: {output_path}")
    else:
        output_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\n💾 Đã lưu CSV: {output_path}")
    
    # Statistics
    print(f"\n📊 THỐNG KÊ:")
    print(f"   - Tổng dòng: {len(output_df):,}")
    print(f"   - Có title: {output_df['raw_title'].notna().sum():,} ({100*output_df['raw_title'].notna().sum()/len(output_df):.1f}%)")
    print(f"   - Có label: {output_df['label'].notna().sum():,} ({100*output_df['label'].notna().sum()/len(output_df):.1f}%)")
    
    # Hiển thị mẫu
    print(f"\n📌 MẪU DỮ LIỆU (3 dòng đầu):")
    for i in range(min(3, len(output_df))):
        row = output_df.iloc[i]
        print(f"\n[{i+1}]")
        print(f"   Raw: {str(row['raw_comment'])[:80]}...")
        print(f"   Processed: {row['input_text'][:80]}...")
        if pd.notna(row['label']):
            print(f"   Label: {row['label']}")
    
    print("\n" + "="*80)
    print("✅ HOÀN TẤT!")
    print("="*80)
    
    return output_df

# ===================== MAIN =====================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Xử lý CSV/XLSX với context và teencode normalization')
    parser.add_argument('input', help='Đường dẫn file CSV/XLSX input')
    parser.add_argument('-o', '--output', help='Đường dẫn file output (optional, giữ nguyên format input)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ File không tồn tại: {args.input}")
        sys.exit(1)
    
    print(f"📋 Teencode dictionary: {len(TEENCODE_DICT)} từ")
    print(f"🔧 Emoji mapping: {len(EMOJI_MAP)} emojis")
    print()
    
    process_csv(args.input, args.output)
