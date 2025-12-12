import pandas as pd
import re

def clean_at_symbols():
    print("🧹 BẮT ĐẦU RÀ SOÁT VÀ XÓA DẤU @@...")
    
    input_path = 'c:\\Học sâu\\Dataset\\TOXIC_COMMENT\\training_data_with_context_phobert.csv'
    output_path = 'c:\\Học sâu\\Dataset\\TOXIC_COMMENT\\training_data_with_context_phobert_clean.csv'
    
    try:
        df = pd.read_csv(input_path)
        print(f"✅ Đã load {len(df)} dòng từ file.")
        
        # Kiểm tra số dòng chứa @@
        at_count = df['input_text'].str.contains('@@').sum()
        print(f"📊 Tìm thấy {at_count} dòng chứa ký tự @@")
        
        if at_count > 0:
            # Hiển thị các dòng có @@ để kiểm tra
            print("\n🔍 Các dòng chứa @@:")
            at_rows = df[df['input_text'].str.contains('@@')]
            for i, row in at_rows.iterrows():
                print(f"Dòng {i+1}: {row['input_text'][:100]}...")
            
            # Xóa tất cả ký tự @@ (một hoặc nhiều)
            df['input_text'] = df['input_text'].str.replace(r'@@+', '', regex=True)
            
            # Lưu file đã làm sạch
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"\n✅ Đã lưu file sạch tại: {output_path}")
            
            # Kiểm tra lại
            remaining_at = df['input_text'].str.contains('@@').sum()
            print(f"🔍 Số dòng còn @@ sau khi xử lý: {remaining_at}")
        else:
            print("✅ Không tìm thấy ký tự @@ nào trong file!")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    clean_at_symbols()