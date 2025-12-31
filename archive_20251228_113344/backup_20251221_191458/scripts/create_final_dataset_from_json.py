import pandas as pd 
import json 
import re 

def create_final_dataset(): 
    print("🚀 BẮT ĐẦU TẠO DATASET TỪ FILE GỐC (JSON)...") 
    
    # 1. Đọc file JSON gốc (Nơi icon vẫn còn nguyên vẹn) 
    # Thay đường dẫn tới file json gốc của bạn 
    json_path = 'c:\\Học sâu\\Dataset\\data\\raw\\facebook\\topiclgbt.json' 
    
    try: 
        with open(json_path, 'r', encoding='utf-8') as f: 
            data = json.load(f) 
        df = pd.DataFrame(data) 
        print(f"✅ Đã load {len(df)} dòng từ JSON.") 
    except Exception as e: 
        print(f"❌ Lỗi đọc file JSON: {e}") 
        return 
    
    # 2. Hàm xử lý text chuẩn (Giữ icon quan trọng) 
    def clean_and_contextualize(row): 
        # Lấy text và title 
        text = str(row.get('text', '')) 
        title = str(row.get('postTitle', '')) 
        
        # --- A. XỬ LÝ EMOJI QUAN TRỌNG (DEMOJIZING) --- 
        # Phải làm bước này ĐẦU TIÊN khi icon còn nguyên 
        emoji_map = { 
            '🏳️‍🌈': ' đồng tính ', 
            '🏳️‍⚧️': ' chuyển giới ', 
            '🌈': ' lgbt ', 
            '👨‍❤️‍💋‍👨': ' nam yêu nam ', 
            '👩‍❤️‍💋‍👩': ' nữ yêu nữ ', 
            '👬': ' nam yêu nam ', 
            '👭': ' nữ yêu nữ ', 
            '❤️': ' yêu ', 
            '💔': ' chia tay ' 
        } 
        
        # Quét và thay thế trong cả Title và Comment 
        for icon, mean in emoji_map.items(): 
            text = text.replace(icon, mean) 
            title = title.replace(icon, mean) 
        
        # --- B. XỬ LÝ HASHTAG --- 
        # Xóa hashtag rác 
        spam_tags = ['#xuhuong', '#fyp', '#viral', '#reels', '#trending', '#shorts'] 
        for tag in spam_tags: 
            text = re.sub(tag, '', text, flags=re.IGNORECASE) 
            title = re.sub(tag, '', title, flags=re.IGNORECASE) 
            
        # Hashtag còn lại -> Bỏ dấu #, giữ chữ (ví dụ #lgbt -> lgbt) 
        text = text.replace('#', ' ') 
        title = title.replace('#', ' ') 

        # --- C. XỬ LÝ TITLE DÀI --- 
        # Cắt title nếu quá dài (lấy 50 từ đầu) để tránh chiếm hết chỗ của comment 
        title_words = title.split() 
        if len(title_words) > 50: 
            title = ' '.join(title_words[:50]) 
            
        # --- D. TẠO INPUT CONTEXT --- 
        # Cấu trúc: Title </s> Comment 
        # PhoBERT dùng </s> làm token ngăn cách 
        if title.strip(): 
            final_input = f"{title.strip()} </s> {text.strip()}" 
        else: 
            final_input = text.strip() 
            
        # --- E. LÀM SẠCH KÝ TỰ LẠ CUỐI CÙNG --- 
        # Lúc này icon đã thành chữ rồi, các icon vô nghĩa khác có thể xóa 
        # Xóa ký tự @@ (nếu có sót) 
        final_input = re.sub(r'@@+', '', final_input) 
        # Chuẩn hóa khoảng trắng 
        final_input = re.sub(r'\s+', ' ', final_input).strip() 
        
        return final_input 
    
    # 3. Áp dụng vào DataFrame 
    df['input_text'] = df.apply(clean_and_contextualize, axis=1) 
    
    # 4. Xuất file kết quả 
    output_path = 'c:\\Học sâu\\Dataset\\TOXIC_COMMENT\\training_data_final_phobert.csv' 
    # Chỉ giữ lại các cột cần thiết (ví dụ giữ lại id để đối chiếu nhãn cũ nếu cần) 
    df_final = df[['id', 'input_text']] 
    
    df_final.to_csv(output_path, index=False, encoding='utf-8-sig') 
    
    print(f"\n🎉 XONG! File chuẩn đã lưu tại: {output_path}") 
    print("👀 Ví dụ 3 dòng đầu tiên:") 
    print(df_final['input_text'].head(3)) 

if __name__ == "__main__": 
    create_final_dataset()