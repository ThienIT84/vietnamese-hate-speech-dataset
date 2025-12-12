# Vietnamese Hate Speech Detection Dataset

Dự án xây dựng bộ dữ liệu phát hiện ngôn từ thù ghét (Hate Speech) tiếng Việt chất lượng cao (~12K mẫu), phục vụ huấn luyện mô hình PhoBERT.

## 📂 Cấu trúc dự án

```
Dataset/
├── data/                    # Quản lý dữ liệu
│   ├── raw/                 # Dữ liệu thô (JSON từ Facebook/YouTube)
│   ├── processed/           # Dữ liệu đã qua xử lý sơ bộ
│   ├── labeled/             # Dữ liệu đã gán nhãn thủ công
│   └── final/               # Dataset hoàn chỉnh (Final version)
│
├── notebooks/               # Jupyter Notebooks phân tích & trình bày
│   ├── 01_Data_Journey_Presentation.ipynb  # Báo cáo hành trình dữ liệu
│   └── ...
│
├── scripts/                 # Các script tiện ích (Utility scripts)
│   ├── analyze_coverage.py
│   ├── auto_label_samples.py
│   └── ...
│
├── src/                     # Source code chính
│   ├── preprocessing/       # Pipeline tiền xử lý (Clean text, normalize)
│   ├── labeling/            # Logic gán nhãn, Active Learning
│   ├── training/            # Code huấn luyện mô hình
│   └── utils/               # Các hàm tiện ích chung
│
├── docs/                    # Tài liệu hướng dẫn (Guideline, Plan)
├── models/                  # Nơi lưu trữ models (đã train)
└── configs/                 # File cấu hình
```

## 🚀 Cài đặt

1. Clone repository:
```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

2. Cài đặt môi trường:
```bash
pip install -r requirements.txt
```

## 📊 Dataset Overview
- **Tổng số mẫu:** ~12,695
- **Labels:**
  - `0`: Clean (Sạch)
  - `1`: Offensive (Xúc phạm nhưng không thù ghét)
  - `2`: Hate Speech (Ngôn từ thù ghét)
- **Nguồn dữ liệu:** Facebook & YouTube comments

## 🛠 Usage
### 1. Tiền xử lý dữ liệu
```bash
python src/preprocessing/apply_advanced_cleaning.py
```

### 2. Chạy Active Learning
```bash
python src/labeling/active_learning.py
```

### 3. Xem báo cáo dữ liệu
Mở `notebooks/01_Data_Journey_Presentation.ipynb` để xem phân tích chi tiết.

## 📝 License

### Dataset License
Bộ dữ liệu này được phát hành dưới **Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**.

#### ✅ Bạn được phép:
- **Sử dụng thương mại** - Sử dụng dataset cho mục đích thương mại
- **Chỉnh sửa** - Biến đổi, cải tiến dataset
- **Phân phối** - Sao chép, chia sẻ dataset
- **Cấp phép lại** - Sử dụng dataset trong các tác phẩm phái sinh

#### 📋 Yêu cầu:
- **Ghi nhận** - Phải trích dẫn nguồn gốc của dataset
- **Chia sẻ tương tự** - Nếu có biến đổi, phải chia sẻ dưới cùng điều khoản

### Source Code License
Mã nguồn trong dự án được cấp phép theo **MIT License**.

### Citation
Nếu sử dụng dataset này trong nghiên cứu hoặc sản phẩm, vui lòng trích dẫn:

```bibtex
@misc{thien2025vietnamese,
  author = {Trần Thanh Thiện},
  title = {Vietnamese Hate Speech Detection Dataset},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{[https://github.com/ThienIT84/vietnamese-hate-speech-dataset](https://github.com/ThienIT84/vietnamese-hate-speech-dataset)}}
}