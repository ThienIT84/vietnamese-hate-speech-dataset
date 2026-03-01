#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Chuẩn bị dữ liệu training cho PhoBERT-base-v2
- Lowercase toàn bộ training_text
- Loại bỏ null values
- Loại bỏ trùng lặp
- Shuffle data
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

def prepare_phobert_training_data(
    input_file: str,
    output_file: str = None,
    random_seed: int = 42
):
    """
    Chuẩn bị dữ liệu training cho PhoBERT
    
    Args:
        input_file: Đường dẫn file input (.xlsx)
        output_file: Đường dẫn file output (optional)
        random_seed: Random seed cho shuffle
    """
    print("="*80)
    print("🔥 CHUẨN BỊ DỮ LIỆU TRAINING CHO PHOBERT-BASE-V2")
    print("="*80)
    
    # Read file
    print(f"\n📂 Đọc file: {input_file}")
    try:
        df = pd.read_excel(input_file)
        print(f"   ✅ Đọc thành công: {len(df):,} dòng")
    except Exception as e:
        print(f"   ❌ Lỗi đọc file: {e}")
        return
    
    # Show columns
    print(f"\n📋 Các cột trong file: {list(df.columns)}")
    
    # Check required columns
    required_cols = ['training_text', 'label']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"   ❌ Thiếu các cột: {missing_cols}")
        return
    
    print(f"\n📊 Thống kê ban đầu:")
    print(f"   - Tổng số dòng: {len(df):,}")
    print(f"   - Null training_text: {df['training_text'].isna().sum():,}")
    print(f"   - Null label: {df['label'].isna().sum():,}")
    print(f"   - Phân bố label:")
    # Convert label to numeric to avoid mixed type issues
    try:
        print(df['label'].value_counts().sort_index())
    except TypeError:
        # Mixed types - show without sorting
        print(df['label'].value_counts())
    
    # Step 1: Loại bỏ null values
    print(f"\n🧹 Bước 1: Loại bỏ null values...")
    before_count = len(df)
    df = df.dropna(subset=['training_text', 'label'])
    after_count = len(df)
    removed = before_count - after_count
    print(f"   ✅ Đã loại bỏ {removed:,} dòng null")
    print(f"   📊 Còn lại: {after_count:,} dòng")
    
    # Convert label to int (clean up any string labels)
    print(f"\n🔢 Bước 1.5: Chuẩn hóa label về integer...")
    df['label'] = pd.to_numeric(df['label'], errors='coerce')
    # Remove any rows where label couldn't be converted
    invalid_labels = df['label'].isna().sum()
    if invalid_labels > 0:
        print(f"   ⚠️  Tìm thấy {invalid_labels:,} label không hợp lệ, đang loại bỏ...")
        df = df.dropna(subset=['label'])
    df['label'] = df['label'].astype(int)
    print(f"   ✅ Label đã được chuẩn hóa về integer")
    print(f"   📊 Còn lại: {len(df):,} dòng")
    
    # Step 2: Lowercase training_text
    print(f"\n🔤 Bước 2: Lowercase toàn bộ training_text...")
    df['training_text'] = df['training_text'].astype(str).str.lower()
    print(f"   ✅ Đã lowercase {len(df):,} dòng")
    
    # Step 3: Loại bỏ trùng lặp
    print(f"\n🔍 Bước 3: Loại bỏ trùng lặp...")
    before_count = len(df)
    # Giữ lại dòng đầu tiên khi trùng lặp
    df = df.drop_duplicates(subset=['training_text', 'label'], keep='first')
    after_count = len(df)
    removed = before_count - after_count
    print(f"   ✅ Đã loại bỏ {removed:,} dòng trùng lặp")
    print(f"   📊 Còn lại: {after_count:,} dòng unique")
    
    # Step 4: Shuffle data
    print(f"\n🔀 Bước 4: Shuffle data (random_seed={random_seed})...")
    df = df.sample(frac=1, random_state=random_seed).reset_index(drop=True)
    print(f"   ✅ Đã shuffle {len(df):,} dòng")
    
    # Final statistics
    print(f"\n📊 Thống kê cuối cùng:")
    print(f"   - Tổng số dòng: {len(df):,}")
    print(f"   - Phân bố label:")
    label_counts = df['label'].value_counts().sort_index()
    for label, count in label_counts.items():
        percentage = (count / len(df)) * 100
        print(f"     Label {label}: {count:,} ({percentage:.2f}%)")
    
    # Check for empty strings
    empty_count = (df['training_text'].str.strip() == '').sum()
    if empty_count > 0:
        print(f"\n⚠️  Cảnh báo: Có {empty_count:,} dòng training_text rỗng (chỉ có khoảng trắng)")
        print(f"   Đang loại bỏ...")
        df = df[df['training_text'].str.strip() != '']
        print(f"   ✅ Đã loại bỏ. Còn lại: {len(df):,} dòng")
    
    # Generate output filename if not provided
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_PHOBERT_{timestamp}.xlsx"
    
    # Save to file
    print(f"\n💾 Lưu file output: {output_file}")
    try:
        df.to_excel(output_file, index=False)
        print(f"   ✅ Đã lưu thành công!")
    except Exception as e:
        print(f"   ❌ Lỗi lưu file: {e}")
        return
    
    # Sample preview
    print(f"\n👀 Preview 5 dòng đầu tiên:")
    print(df[['training_text', 'label']].head())
    
    print("\n" + "="*80)
    print("✅ HOÀN THÀNH!")
    print("="*80)
    print(f"\n📁 File output: {output_file}")
    print(f"📊 Tổng số dòng: {len(df):,}")
    print(f"🎯 Sẵn sàng cho training với PhoBERT-base-v2!")
    
    return df, output_file


if __name__ == "__main__":
    # Input file
    input_file = r"C:\Học sâu\Dataset\data\final\final_train_data_v3_READY.xlsx"
    
    # Process
    df, output_file = prepare_phobert_training_data(
        input_file=input_file,
        random_seed=42
    )
    
    print(f"\n🚀 Bạn có thể sử dụng file này để train PhoBERT:")
    print(f"   {output_file}")
