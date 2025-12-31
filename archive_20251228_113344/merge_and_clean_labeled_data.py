"""
Script để merge 3 file đã gán nhãn và xử lý text cleaning
cho semi-supervised learning

Files input:
1. final_1k_thien_gold_sample.json (Label Studio format)
2. final_thien_gold_sample.json (Label Studio format)  
3. labeling_task_Quang.csv (CSV format)

Output:
- merged_cleaned_labeled_data.csv: File CSV đã merge và cleaned
- merged_cleaned_labeled_data.json: File JSON đã merge và cleaned
"""

import pandas as pd
import json
import sys
from pathlib import Path
from datetime import datetime

# Import text cleaning module
from src.preprocessing.advanced_text_cleaning import clean_text

def extract_label_from_labelstudio_json(task):
    """
    Trích xuất label từ format Label Studio JSON
    
    Returns:
        dict với keys: comment, context, label, note
    """
    result = {
        'comment': '',
        'context': '',
        'label': None,
        'note': ''
    }
    
    # Lấy comment và context từ data
    if 'data' in task:
        result['comment'] = task['data'].get('comment', '')
        result['context'] = task['data'].get('context', '')
    
    # Lấy label từ annotations
    if 'annotations' in task and len(task['annotations']) > 0:
        annotation = task['annotations'][0]
        if 'result' in annotation:
            for item in annotation['result']:
                # Tìm label (choices)
                if item.get('from_name') == 'label' and item.get('type') == 'choices':
                    choices = item.get('value', {}).get('choices', [])
                    if choices:
                        # Extract số từ label (0, 1, 2)
                        label_str = choices[0]
                        if '0' in label_str:
                            result['label'] = 0
                        elif '1' in label_str:
                            result['label'] = 1
                        elif '2' in label_str:
                            result['label'] = 2
                
                # Tìm note (textarea)
                if item.get('from_name') == 'note' and item.get('type') == 'textarea':
                    text_list = item.get('value', {}).get('text', [])
                    if text_list:
                        result['note'] = ' '.join(text_list)
    
    return result

def load_json_labelstudio(json_path):
    """
    Load file JSON từ Label Studio và chuyển sang DataFrame
    """
    print(f"\nĐang đọc file: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    records = []
    for task in data:
        extracted = extract_label_from_labelstudio_json(task)
        
        # Chỉ lấy những task đã được gán nhãn
        if extracted['label'] is not None:
            record = {
                'comment': extracted['comment'],
                'context': extracted['context'],
                'label': extracted['label'],
                'note': extracted['note'],
                'task_id': task.get('id', ''),
                'source': 'labelstudio'
            }
            records.append(record)
    
    df = pd.DataFrame(records)
    print(f"  - Số lượng records đã gán nhãn: {len(df)}")
    print(f"  - Phân bố label: {df['label'].value_counts().to_dict()}")
    
    return df

def load_csv_quang(csv_path):
    """
    Load file CSV từ Quang và chuyển về format chuẩn
    Sử dụng raw_comment và raw_title để giữ emoji và tags
    """
    print(f"\nĐang đọc file: {csv_path}")
    
    df = pd.read_csv(csv_path, encoding='utf-8')
    print(f"  - Tổng số dòng: {len(df)}")
    print(f"  - Columns: {df.columns.tolist()}")
    
    # Lọc những dòng đã gán nhãn
    df_labeled = df[df['label'].notna()].copy()
    
    # Chuẩn hóa format - SỬ DỤNG RAW DATA
    df_output = pd.DataFrame({
        'comment': df_labeled['raw_comment'].fillna(''),  # Dùng raw_comment
        'context': df_labeled['raw_title'].fillna(''),     # Dùng raw_title
        'label': df_labeled['label'].astype(int),
        'note': df_labeled['note'].fillna(''),
        'task_id': df_labeled['id'].fillna(''),
        'source': 'quang_csv'
    })
    
    print(f"  - Số lượng records đã gán nhãn: {len(df_output)}")
    print(f"  - Phân bố label: {df_output['label'].value_counts().to_dict()}")
    
    return df_output

def merge_dataframes(dfs):
    """
    Merge nhiều DataFrames
    """
    print("\n" + "="*60)
    print("MERGE CÁC FILE")
    print("="*60)
    
    merged_df = pd.concat(dfs, ignore_index=True)
    
    print(f"\nTổng số records sau khi merge: {len(merged_df)}")
    print(f"Phân bố label:")
    print(merged_df['label'].value_counts().sort_index())
    
    # Kiểm tra duplicates
    duplicates = merged_df.duplicated(subset=['comment'], keep=False).sum()
    print(f"\nSố comment trùng lặp: {duplicates}")
    
    return merged_df

def apply_text_cleaning(df):
    """
    Áp dụng text cleaning cho comment
    """
    print("\n" + "="*60)
    print("ÁP DỤNG TEXT CLEANING")
    print("="*60)
    
    print("\nĐang clean text...")
    
    # Clean comment
    df['cleaned_comment'] = df['comment'].apply(lambda x: clean_text(str(x)) if pd.notna(x) else '')
    
    # Clean context (nếu có)
    df['cleaned_context'] = df['context'].apply(lambda x: clean_text(str(x)) if pd.notna(x) else '')
    
    print("✓ Hoàn thành text cleaning!")
    
    # Hiển thị một vài ví dụ
    print("\n--- VÍ DỤ TEXT CLEANING ---")
    for idx in range(min(3, len(df))):
        print(f"\nSample {idx+1}:")
        print(f"  Original: {df.iloc[idx]['comment'][:100]}...")
        print(f"  Cleaned:  {df.iloc[idx]['cleaned_comment'][:100]}...")
        print(f"  Label:    {df.iloc[idx]['label']}")
    
    return df

def save_outputs(df, output_dir):
    """
    Lưu kết quả ra CSV và JSON
    """
    print("\n" + "="*60)
    print("LƯU KẾT QUẢ")
    print("="*60)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Lưu CSV đầy đủ (tất cả columns)
    csv_full_path = output_dir / f"merged_cleaned_labeled_full_{timestamp}.csv"
    df.to_csv(csv_full_path, index=False, encoding='utf-8')
    print(f"\n✓ Đã lưu CSV đầy đủ: {csv_full_path}")
    
    # 2. Lưu CSV cho training - MERGE context và text
    df_training = df[['cleaned_context', 'cleaned_comment', 'label', 'note']].copy()
    
    # Combine context và text với separator </s>
    df_training['full_text'] = df_training.apply(
        lambda row: f"{row['cleaned_context']} </s> {row['cleaned_comment']}" 
        if row['cleaned_context'] and len(row['cleaned_context'].strip()) > 0 
        else row['cleaned_comment'],
        axis=1
    )
    
    # Tạo DataFrame final với full_text
    df_final = pd.DataFrame({
        'text': df_training['full_text'],
        'label': df_training['label'],
        'note': df_training['note'],
        'comment_only': df_training['cleaned_comment'],
        'context_only': df_training['cleaned_context']
    })
    
    csv_train_path = output_dir / f"merged_cleaned_for_training_{timestamp}.csv"
    df_final.to_csv(csv_train_path, index=False, encoding='utf-8')
    print(f"✓ Đã lưu CSV for training (với context merged): {csv_train_path}")
    
    # 3. Lưu JSON
    json_path = output_dir / f"merged_cleaned_labeled_{timestamp}.json"
    
    json_data = []
    for _, row in df.iterrows():
        # Merge context và text
        full_text = f"{row['cleaned_context']} </s> {row['cleaned_comment']}" \
            if row['cleaned_context'] and len(row['cleaned_context'].strip()) > 0 \
            else row['cleaned_comment']
        
        json_data.append({
            'text': full_text,
            'label': int(row['label']),
            'note': row['note'],
            'comment_only': row['cleaned_comment'],
            'context_only': row['cleaned_context'],
            'original_text': row['comment'],
            'source': row['source']
        })
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Đã lưu JSON: {json_path}")
    
    # 4. Tạo báo cáo thống kê
    stats_path = output_dir / f"merge_statistics_{timestamp}.txt"
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("THỐNG KÊ MERGE & CLEAN DATA\n")
        f.write("="*60 + "\n\n")
        
        f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"Tổng số records: {len(df)}\n\n")
        
        f.write("Phân bố label:\n")
        for label, count in df['label'].value_counts().sort_index().items():
            percentage = count / len(df) * 100
            f.write(f"  Label {label}: {count} ({percentage:.1f}%)\n")
        
        f.write("\nPhân bố theo source:\n")
        for source, count in df['source'].value_counts().items():
            f.write(f"  {source}: {count}\n")
        
        f.write("\nThống kê độ dài text (sau cleaning):\n")
        text_lengths = df['cleaned_comment'].str.len()
        f.write(f"  Min: {text_lengths.min()}\n")
        f.write(f"  Max: {text_lengths.max()}\n")
        f.write(f"  Mean: {text_lengths.mean():.1f}\n")
        f.write(f"  Median: {text_lengths.median():.1f}\n")
    
    print(f"✓ Đã lưu báo cáo thống kê: {stats_path}")
    
    return csv_train_path

def main():
    """
    Main function
    """
    print("="*60)
    print("MERGE & CLEAN LABELED DATA FOR SEMI-SUPERVISED LEARNING")
    print("="*60)
    
    # Đường dẫn files
    base_dir = Path(r"c:\Học sâu\Dataset\TOXIC_COMMENT\datasets\final")
    
    json_1k_path = base_dir / "final_1k_thien_gold_sample.json"
    json_full_path = base_dir / "final_thien_gold_sample.json"
    csv_quang_path = base_dir / "labeling_task_Quang.csv"
    
    # Output directory
    output_dir = Path(r"c:\Học sâu\Dataset\data\processed")
    
    # 1. Load các files
    dfs = []
    
    # Load JSON 1k
    if json_1k_path.exists():
        df1 = load_json_labelstudio(json_1k_path)
        dfs.append(df1)
    else:
        print(f"⚠ Không tìm thấy file: {json_1k_path}")
    
    # Load JSON full
    if json_full_path.exists():
        df2 = load_json_labelstudio(json_full_path)
        dfs.append(df2)
    else:
        print(f"⚠ Không tìm thấy file: {json_full_path}")
    
    # Load CSV Quang
    if csv_quang_path.exists():
        df3 = load_csv_quang(csv_quang_path)
        dfs.append(df3)
    else:
        print(f"⚠ Không tìm thấy file: {csv_quang_path}")
    
    if not dfs:
        print("\n❌ Không có file nào để xử lý!")
        return
    
    # 2. Merge
    merged_df = merge_dataframes(dfs)
    
    # 3. Remove duplicates (giữ lại first occurrence)
    print("\nXóa duplicates...")
    before = len(merged_df)
    merged_df = merged_df.drop_duplicates(subset=['comment'], keep='first')
    after = len(merged_df)
    print(f"  Đã xóa {before - after} duplicates")
    
    # 4. Apply text cleaning
    cleaned_df = apply_text_cleaning(merged_df)
    
    # 5. Lọc bỏ những text quá ngắn sau khi clean
    print("\nLọc text quá ngắn...")
    before = len(cleaned_df)
    cleaned_df = cleaned_df[cleaned_df['cleaned_comment'].str.len() >= 5]
    after = len(cleaned_df)
    print(f"  Đã lọc bỏ {before - after} text quá ngắn")
    
    # 6. Save outputs
    output_path = save_outputs(cleaned_df, output_dir)
    
    print("\n" + "="*60)
    print("✓ HOÀN THÀNH!")
    print("="*60)
    print(f"\nFile training chính: {output_path}")
    print(f"Tổng số samples: {len(cleaned_df)}")
    print("\nBạn có thể sử dụng file này để train semi-supervised learning model!")

if __name__ == "__main__":
    main()
