#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MÔ TẢ DỰ ÁN: PHÁT HIỆN NGÔN TỪ THÙ GHÉT ĐA NGỮ CẢNH TRÊN MXH VIỆT NAM 2025

Tổng quan dự án dựa trên notebook presentaion_data_pipeline.ipynb
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def print_project_description():
    """In mô tả chi tiết về dự án"""
    
    print("=" * 80)
    print("🔍 PHÁT HIỆN NGÔN TỪ THÙ GHÉT ĐA NGỮ CẢNH TRÊN MẠNG XÃ HỘI VIỆT NAM 2025")
    print("=" * 80)
    
    print("\n📋 TÓM TẮT DỰ ÁN:")
    print("-" * 40)
    print("Mục tiêu: Xây dựng model AI phát hiện ngôn từ thù ghét (hate speech) và")
    print("ngôn từ xúc phạm (offensive) trên mạng xã hội Việt Nam với khả năng")
    print("hiểu ngữ cảnh đa chiều.")
    
    print("\n🎯 CÁC THÀNH PHỐ CHÍNH:")
    print("-" * 40)
    
    # 1. Thu thập dữ liệu
    print("\n1️⃣ THU THẬP DỮ LIỆU:")
    print("   • Nguồn: Facebook (15,468 comments) + YouTube (4,246 comments)")
    print("   • Tổng: 19,714 raw samples")
    print("   • Platform: Apify (chuyển từ Selenium do vấn đề anti-bot)")
    print("   • Điểm nổi bật: Có cả Post Title + Comment (quan trọng cho context)")
    
    # 2. Tiền xử lý
    print("\n2️⃣ TIỀN XỬ LÝ ('Very Strict' Preprocessing):")
    print("   • Mục tiêu: Chuẩn hóa cho PhoBERT")
    print("   • 8 bước xử lý:")
    print("     - Emoji → Text (🏳️‍🌈 → 'đồng tính')")
    print("     - Remove Hashtags, URLs")
    print("     - Teencode Dictionary (251+ rules: ko→không, h→giờ)")
    print("     - Leetspeak (g4y→gay)")
    print("     - Repeated chars normalization")
    print("     - Person names → <person>")
    print("     - Unicode normalization")
    
    # 3. Gán nhãn
    print("\n3️⃣ CHIẾN LƯỢC GÁN NHÃN (3 giai đoạn):")
    print("   • Hệ thống nhãn:")
    print("     - Label 0: Clean (Sạch)")
    print("     - Label 1: Offensive (Xúc phạm)")
    print("     - Label 2: Hate Speech (Kỳ thị)")
    print("   • 6 Topics: Regional, Body Shaming, Gender/LGBT, Family, Disability, Violence")
    print("   • Giai đoạn 1: Thất bại (không có context)")
    print("   • Giai đoạn 2: Context-aware labeling (có Post Title)")
    print("   • Giai đoạn 2.5: Active Learning để cân bằng dataset")
    
    # 4. Dataset
    print("\n4️⃣ DATASET FINAL:")
    print("   • Gold Standard: 1,127 samples (balanced)")
    print("   • Final Dataset: 12,695 samples (sau semi-supervised learning)")
    print("   • Phân bố cân bằng: 41.4% / 25.7% / 32.9%")
    print("   • 96.1% có Post Title (context-aware)")
    
    # 5. Technology
    print("\n5️⃣ CÔNG NGHỆ:")
    print("   • Model: PhoBERT (Pre-trained Vietnamese BERT)")
    print("   • Approach: Teacher-Student + Semi-Supervised Learning")
    print("   • Quality Control: Majority Voting (3 annotators)")
    
    # 6. Kết quả
    print("\n6️⃣ KẾT QUẢ ĐẠT ĐƯỢC:")
    print("   • ✅ Dataset chất lượng cao với context")
    print("   • ✅ Balanced labels")
    print("   • ✅ Context-aware hate speech detection")
    print("   • ✅ Robust preprocessing pipeline")
    
    print("\n💡 ĐIỂM NHẤN CÔNG NGHỆ:")
    print("-" * 40)
    print("• Context-aware labeling: Hate speech phụ thuộc hoàn toàn vào ngữ cảnh")
    print("• 'Very Strict' preprocessing: Tối ưu cho PhoBERT")
    print("• Active Learning: Giải quyết vấn đề imbalanced dataset")
    print("• Majority Voting: Đảm bảo chất lượng gán nhãn")
    
    print("\n🚀 HƯỚNG PHÁT TRIỂN:")
    print("-" * 40)
    print("• Mở rộng dataset với nhiều nguồn hơn")
    print("• Real-time hate speech detection")
    print("• Multi-modal analysis (text + image)")
    print("• Deployment cho social media platforms")

def print_data_statistics():
    """In thống kê dữ liệu"""
    
    print("\n📊 THỐNG KÊ DỮ LIỆU:")
    print("-" * 40)
    
    # Raw data
    print(f"• Raw Data Collection: {19714:,} samples")
    print(f"  - Facebook: {15468:,} comments")
    print(f"  - YouTube: {4246:,} comments")
    
    # Gold Standard
    print(f"\n• Gold Standard Dataset: {1127:,} samples")
    print(f"  - Label 0 (Clean): 467 samples (41.4%)")
    print(f"  - Label 1 (Offensive): 289 samples (25.7%)")
    print(f"  - Label 2 (Hate Speech): 371 samples (32.9%)")
    
    # Final Dataset
    print(f"\n• Final Dataset: {12695:,} samples")
    print(f"  - Sau semi-supervised learning")
    print(f"  - 96.1% có Post Title (context-aware)")
    
    # Preprocessing stats
    print(f"\n• Preprocessing Pipeline:")
    print(f"  - 251+ teencode rules")
    print(f"  - 8-step normalization")
    print(f"  - Optimized for PhoBERT")

def print_technical_architecture():
    """In kiến trúc kỹ thuật"""
    
    print("\n🏗️ KIẾN TRÚC KỸ THUẬT:")
    print("-" * 40)
    
    print("1. Data Collection Layer:")
    print("   - Apify Platform")
    print("   - Anti-bot handling")
    print("   - Proxy rotation")
    
    print("\n2. Preprocessing Layer:")
    print("   - Text normalization")
    print("   - Teencode conversion")
    print("   - Emoji-to-text mapping")
    print("   - Person name anonymization")
    
    print("\n3. Labeling Layer:")
    print("   - Context-aware approach")
    print("   - Majority voting system")
    print("   - Active learning")
    print("   - Quality control")
    
    print("\n4. Model Layer:")
    print("   - PhoBERT base")
    print("   - Teacher-Student framework")
    print("   - Semi-supervised learning")
    print("   - Multi-label classification")

def main():
    """Main function"""
    print(f"\n🕒 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Based on: presentaion_data_pipeline.ipynb")
    
    print_project_description()
    print_data_statistics()
    print_technical_architecture()
    
    print("\n" + "=" * 80)
    print("🎉 DỰ ÁN PHÁT HIỆN NGÔN TỪ THÙ GHÉT ĐA NGỮ CẢNH VIỆT NAM 2025")
    print("=" * 80)

if __name__ == "__main__":
    main()