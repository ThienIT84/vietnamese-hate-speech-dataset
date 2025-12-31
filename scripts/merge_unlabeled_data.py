"""
Script để gộp file Youtube và Master đã xử lý, loại bỏ trùng lặp với Training Data
Tạo file sẵn sàng để nhóm gán nhãn
"""

import pandas as pd
import os
from pathlib import Path

def load_and_prepare_data():
    """Load các file và chuẩn bị dữ liệu"""
    
    # Đường dẫn các file
    base_dir = Path(__file__).parent.parent
    youtube_file = base_dir / "data" / "processing" / "youtube_comment_craw_processed.xlsx"
    master_file = base_dir / "data" / "processed" / "master_combined.csv"
    training_file = base_dir / "data" / "processed" / "training_data_final_merged.csv"
    output_file = base_dir / "data" / "processed" / "unlabeled_data_for_labeling.csv"
    
    print("📂 Đang load các file...")
    
    # Load file Youtube đã xử lý
    print(f"  - Đọc Youtube: {youtube_file}")
    youtube_df = pd.read_excel(youtube_file)
    print(f"    ✓ {len(youtube_df):,} dòng")
    
    # Load file Master
    print(f"  - Đọc Master: {master_file}")
    master_df = pd.read_csv(master_file)
    print(f"    ✓ {len(master_df):,} dòng")
    
    # Load file Training (đã gán nhãn)
    print(f"  - Đọc Training: {training_file}")
    training_df = pd.read_csv(training_file)
    print(f"    ✓ {len(training_df):,} dòng (đã gán nhãn)")
    
    return youtube_df, master_df, training_df, output_file


def standardize_columns(df, source_name):
    """Chuẩn hóa cột để đồng nhất giữa các file"""
    
    # Các cột cần thiết
    required_cols = ['id', 'input_text', 'raw_comment', 'raw_title', 
                     'cleaned_comment', 'cleaned_title', 'source_platform',
                     'source_url', 'post_id', 'video_id', 'timestamp',
                     'username', 'likes', 'replies_count', 'char_length',
                     'word_count', 'has_emoji', 'topic']
    
    # Thêm các cột thiếu với giá trị mặc định
    for col in required_cols:
        if col not in df.columns:
            if col == 'source_platform':
                df[col] = source_name
            elif col in ['likes', 'replies_count', 'char_length', 'word_count']:
                df[col] = 0
            elif col == 'has_emoji':
                df[col] = False
            else:
                df[col] = ''
    
    # Đảm bảo thứ tự cột
    df = df[required_cols]
    
    return df


def remove_duplicates_with_training(combined_df, training_df):
    """Loại bỏ các dòng trùng lặp với training data"""
    
    print("\n🔍 Kiểm tra trùng lặp với Training Data...")
    
    # Tạo set các input_text từ training data
    training_texts = set(training_df['input_text'].dropna().unique())
    print(f"  - Training có {len(training_texts):,} input_text unique")
    
    # Đếm số dòng trước khi lọc
    before_count = len(combined_df)
    
    # Lọc bỏ các dòng có input_text trùng với training
    combined_df['is_duplicate'] = combined_df['input_text'].isin(training_texts)
    duplicates_count = combined_df['is_duplicate'].sum()
    
    print(f"  - Tìm thấy {duplicates_count:,} dòng trùng lặp với Training")
    
    # Giữ lại các dòng không trùng
    combined_df = combined_df[~combined_df['is_duplicate']].copy()
    combined_df.drop('is_duplicate', axis=1, inplace=True)
    
    after_count = len(combined_df)
    print(f"  - Còn lại: {after_count:,} dòng ({after_count/before_count*100:.1f}%)")
    
    return combined_df


def remove_internal_duplicates(df):
    """Loại bỏ trùng lặp nội bộ (trong chính file gộp)"""
    
    print("\n🔍 Loại bỏ trùng lặp nội bộ...")
    
    before_count = len(df)
    
    # Loại bỏ dựa trên input_text (giữ dòng đầu tiên)
    df = df.drop_duplicates(subset=['input_text'], keep='first')
    
    after_count = len(df)
    removed = before_count - after_count
    
    print(f"  - Đã loại bỏ {removed:,} dòng trùng lặp nội bộ")
    print(f"  - Còn lại: {after_count:,} dòng")
    
    return df


def add_labeling_columns(df):
    """Thêm các cột để gán nhãn"""
    
    df['label'] = ''
    df['note'] = ''
    df['labeler'] = ''
    df['confidence'] = ''
    
    return df


def main():
    print("=" * 70)
    print("🔄 GỘP DỮ LIỆU YOUTUBE + MASTER VÀ LOẠI BỎ TRÙNG LẶP")
    print("=" * 70)
    
    # 1. Load dữ liệu
    youtube_df, master_df, training_df, output_file = load_and_prepare_data()
    
    # 2. Chuẩn hóa cột
    print("\n📋 Chuẩn hóa cột...")
    youtube_df = standardize_columns(youtube_df, 'Youtube')
    master_df = standardize_columns(master_df, master_df['source_platform'].iloc[0] if 'source_platform' in master_df.columns else 'Facebook')
    print(f"  ✓ Youtube: {youtube_df.shape[1]} cột")
    print(f"  ✓ Master: {master_df.shape[1]} cột")
    
    # 3. Gộp Youtube + Master
    print("\n🔗 Gộp Youtube + Master...")
    combined_df = pd.concat([youtube_df, master_df], ignore_index=True)
    print(f"  ✓ Tổng: {len(combined_df):,} dòng")
    
    # 4. Loại bỏ trùng lặp nội bộ
    combined_df = remove_internal_duplicates(combined_df)
    
    # 5. Loại bỏ trùng lặp với Training Data
    combined_df = remove_duplicates_with_training(combined_df, training_df)
    
    # 6. Thêm cột để gán nhãn
    print("\n✏️ Thêm cột để gán nhãn...")
    combined_df = add_labeling_columns(combined_df)
    print(f"  ✓ Đã thêm: label, note, labeler, confidence")
    
    # 7. Sắp xếp theo timestamp (mới nhất trước)
    if 'timestamp' in combined_df.columns and combined_df['timestamp'].notna().any():
        print("\n📅 Sắp xếp theo thời gian...")
        combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'], errors='coerce')
        combined_df = combined_df.sort_values('timestamp', ascending=False)
        print("  ✓ Đã sắp xếp (mới nhất → cũ nhất)")
    
    # 8. Reset index
    combined_df = combined_df.reset_index(drop=True)
    
    # 9. Lưu file
    print(f"\n💾 Lưu file output...")
    combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"  ✓ Đã lưu: {output_file}")
    
    # 10. Thống kê
    print("\n" + "=" * 70)
    print("📊 THỐNG KÊ KẾT QUẢ")
    print("=" * 70)
    print(f"✓ Tổng dòng: {len(combined_df):,}")
    print(f"✓ Youtube: {len(combined_df[combined_df['source_platform'] == 'Youtube']):,}")
    print(f"✓ Facebook: {len(combined_df[combined_df['source_platform'] == 'Facebook']):,}")
    
    if 'topic' in combined_df.columns:
        print("\n📌 Phân bố theo Topic:")
        topic_dist = combined_df['topic'].value_counts()
        for topic, count in topic_dist.items():
            print(f"  - {topic}: {count:,}")
    
    print("\n✅ HOÀN TẤT! File sẵn sàng để gán nhãn.")
    print(f"📁 Output: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
