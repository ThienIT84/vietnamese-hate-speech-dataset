#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Apply word segmentation cho PhoBERT training data
Sử dụng pyvi (RDRSegmenter) - nhanh và không cần Java
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

# Try to import pyvi
try:
    from pyvi import ViTokenizer
    SEGMENTER_AVAILABLE = True
except ImportError:
    print("⚠️  pyvi chưa được cài đặt!")
    print("   Cài đặt bằng: pip install pyvi")
    SEGMENTER_AVAILABLE = False


def is_segmented(text):
    """
    Kiểm tra xem text đã được segment chưa
    Dựa vào việc có underscore _ giữa các từ
    """
    if not isinstance(text, str):
        return False
    
    # Nếu có ít nhất 2 underscore và không phải URL/email
    underscore_count = text.count('_')
    if underscore_count >= 2 and 'http' not in text and '@' not in text:
        return True
    return False


def segment_text(text):
    """Apply word segmentation using pyvi"""
    if not isinstance(text, str) or not text.strip():
        return text
    
    try:
        return ViTokenizer.tokenize(text)
    except Exception as e:
        print(f"   ⚠️  Lỗi segment: {e}")
        return text


def apply_word_segmentation(
    input_file: str,
    output_file: str = None,
    force_resegment: bool = False
):
    """
    Apply word segmentation cho training data
    
    Args:
        input_file: File input (.xlsx)
        output_file: File output (optional)
        force_resegment: Nếu True, segment lại tất cả (kể cả đã segment)
    """
    if not SEGMENTER_AVAILABLE:
        print("❌ Không thể chạy - pyvi chưa được cài đặt")
        return
    
    print("="*80)
    print("🔪 APPLY WORD SEGMENTATION CHO PHOBERT")
    print("="*80)
    
    # Read file
    print(f"\n📂 Đọc file: {input_file}")
    try:
        df = pd.read_excel(input_file)
        print(f"   ✅ Đọc thành công: {len(df):,} dòng")
    except Exception as e:
        print(f"   ❌ Lỗi đọc file: {e}")
        return
    
    # Check column
    if 'training_text' not in df.columns:
        print("   ❌ Không tìm thấy cột 'training_text'")
        return
    
    # Analyze segmentation status
    print(f"\n🔍 Phân tích trạng thái segmentation...")
    segmented_count = df['training_text'].apply(is_segmented).sum()
    not_segmented_count = len(df) - segmented_count
    
    print(f"   - Đã segment: {segmented_count:,} ({segmented_count/len(df)*100:.1f}%)")
    print(f"   - Chưa segment: {not_segmented_count:,} ({not_segmented_count/len(df)*100:.1f}%)")
    
    if not force_resegment and not_segmented_count == 0:
        print(f"\n✅ Tất cả câu đã được segment!")
        print(f"   Nếu muốn segment lại, dùng force_resegment=True")
        return df, input_file
    
    # Apply segmentation
    if force_resegment:
        print(f"\n🔪 Đang segment lại TẤT CẢ {len(df):,} câu...")
        to_segment = df.index
    else:
        print(f"\n🔪 Đang segment {not_segmented_count:,} câu chưa được segment...")
        to_segment = df[~df['training_text'].apply(is_segmented)].index
    
    # Apply with progress bar
    tqdm.pandas(desc="Segmenting")
    
    if force_resegment:
        df['training_text'] = df['training_text'].progress_apply(segment_text)
    else:
        # Only segment rows that need it
        for idx in tqdm(to_segment, desc="Segmenting"):
            df.at[idx, 'training_text'] = segment_text(df.at[idx, 'training_text'])
    
    print(f"   ✅ Hoàn thành!")
    
    # Verify
    print(f"\n✅ Kiểm tra lại...")
    segmented_count_after = df['training_text'].apply(is_segmented).sum()
    print(f"   - Đã segment: {segmented_count_after:,} ({segmented_count_after/len(df)*100:.1f}%)")
    
    # Generate output filename
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_path = Path(input_file)
        output_file = input_path.parent / f"{input_path.stem}_SEGMENTED_{timestamp}.xlsx"
    
    # Save
    print(f"\n💾 Lưu file: {output_file}")
    try:
        df.to_excel(output_file, index=False)
        print(f"   ✅ Đã lưu thành công!")
    except Exception as e:
        print(f"   ❌ Lỗi lưu file: {e}")
        return
    
    # Preview
    print(f"\n👀 Preview 5 câu sau khi segment:")
    for i, row in df.head(5).iterrows():
        text = row['training_text']
        # Truncate if too long
        if len(text) > 100:
            text = text[:100] + "..."
        print(f"   {i+1}. {text}")
    
    print("\n" + "="*80)
    print("✅ HOÀN THÀNH!")
    print("="*80)
    print(f"\n📁 File output: {output_file}")
    print(f"📊 Tổng số dòng: {len(df):,}")
    print(f"🎯 Sẵn sàng cho PhoBERT training!")
    
    return df, output_file


if __name__ == "__main__":
    import sys
    
    # Check if pyvi is installed
    if not SEGMENTER_AVAILABLE:
        print("\n" + "="*80)
        print("📦 HƯỚNG DẪN CÀI ĐẶT PYVI")
        print("="*80)
        print("\nChạy lệnh sau để cài đặt:")
        print("   pip install pyvi")
        print("\nHoặc:")
        print("   python -m pip install pyvi")
        print("\n" + "="*80)
        sys.exit(1)
    
    # Input file (file vừa tạo)
    input_file = r"C:\Học sâu\Dataset\data\final\final_train_data_v3_READY_PHOBERT_20260102_053035.xlsx"
    
    # Check if file exists
    if not Path(input_file).exists():
        print(f"❌ File không tồn tại: {input_file}")
        print("\nVui lòng cập nhật đường dẫn file trong script!")
        sys.exit(1)
    
    # Process
    df, output_file = apply_word_segmentation(
        input_file=input_file,
        force_resegment=False  # Chỉ segment câu chưa được segment
    )
    
    print(f"\n🚀 File đã sẵn sàng cho PhoBERT training:")
    print(f"   {output_file}")
