# 🛡️ SafeSense-VI — Vietnamese Hate Speech Detection

> **IT Got Talent 2025** | PhoBERT-base-v2 | F1 Macro ≥ 0.85 (Target)

Dự án xây dựng hệ thống phát hiện ngôn từ thù ghét (Hate Speech) tiếng Việt end-to-end, từ thu thập dữ liệu → gán nhãn → tiền xử lý → huấn luyện PhoBERT → demo extension.

---

## 📋 Mục lục

- [Tổng quan](#-tổng-quan)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Dataset](#-dataset)
- [Pipeline tiền xử lý](#-pipeline-tiền-xử-lý--advanced_text_cleaningpy)
- [Huấn luyện mô hình](#-huấn-luyện-mô-hình)
- [Kết quả](#-kết-quả)
- [Demo](#-demo)
- [Cài đặt](#-cài-đặt)
- [Sử dụng nhanh](#-sử-dụng-nhanh)
- [Tài liệu](#-tài-liệu)
- [License](#-license)

---

## 🎯 Tổng quan

| Hạng mục | Chi tiết |
|---|---|
| **Model** | `vinai/phobert-base-v2` (135M parameters) |
| **Task** | 3-class classification: Clean / Offensive / Hate Speech |
| **Dataset** | 7,626 mẫu tiếng Việt (gold-standard, gán nhãn thủ công) |
| **Nguồn dữ liệu** | Facebook & YouTube comments (crawled via Apify) |
| **Ngôn ngữ** | Python 3.9+ |
| **Framework** | HuggingFace Transformers, PyTorch |
| **Hardware** | Google Colab T4 GPU (fp16) |

### Nhãn phân loại

| Label | Tên | Mô tả |
|---|---|---|
| `0` | **Clean** | Bình thường, không có vấn đề |
| `1` | **Offensive** | Xúc phạm cá nhân, chửi bới nhưng không thù ghét nhóm |
| `2` | **Hate Speech** | Thù ghét dựa trên danh tính (vùng miền, giới tính, LGBT, chủng tộc...) |

---

## 📂 Cấu trúc dự án

```
SafeSense-VI/
│
├── 📁 src/                          # Source code chính
│   ├── preprocessing/
│   │   ├── advanced_text_cleaning.py    # ⭐ Pipeline 18 bước (2,000+ lines)
│   │   ├── apply_advanced_cleaning.py   # Script chạy pipeline trên CSV
│   │   └── apify_to_csv.py              # Chuyển đổi dữ liệu Apify → CSV
│   ├── labeling/                        # Active Learning, label logic
│   ├── training/                        # Training scripts (local)
│   └── utils/                           # Hàm tiện ích chung
│
├── 📁 src_submission/               # Code đóng gói nộp thi
│   ├── preprocessing/
│   ├── training/
│   └── utils/
│
├── 📁 notebooks/                    # Jupyter Notebooks
│   ├── COLAB_PHOBERT_IT_GOT_TALENT_Final.ipynb   # ⭐ Training notebook (Colab)
│   ├── KAGGLE_PHOBERT_IT_GOT_TALENT.ipynb        # Kaggle version
│   ├── ViDeBERTa_Training_Colab.ipynb             # ViDeBERTa experiments
│   └── PhoBERT_Training_Colab.ipynb               # PhoBERT baseline
│
├── 📁 scripts/                      # Utility scripts
│   ├── analyze_coverage.py          # Phân tích độ phủ dữ liệu
│   ├── auto_label_samples.py        # Auto-labeling với model đã train
│   ├── chia_du_lieu.py              # Chia train/val/test
│   └── ...
│
├── 📁 data/                         # Dữ liệu (⚠️ không đẩy lên Git — xem .gitignore)
│   ├── raw/                         # Dữ liệu thô từ Apify (JSON)
│   ├── processed/                   # Dữ liệu qua bước làm sạch ban đầu
│   ├── labeled/                     # Dữ liệu đã gán nhãn thủ công
│   ├── final/                       # Dataset hoàn chỉnh (CSV/XLSX)
│   └── gold/                        # Gold standard samples
│
├── 📁 TOXIC_COMMENT/                # Module demo & submission
│   ├── demo/                        # Demo scripts
│   ├── models/                      # ⚠️ Model weights (dùng Git LFS)
│   └── notebooks/                   # Training notebooks
│
├── 📁 safesense-kids-extension/     # Chrome Extension (Manifest V3)
│   ├── manifest.json
│   ├── content.js
│   ├── popup.html / popup.js
│   └── background.js
│
├── 📁 safesense-youtube-demo/       # Web Demo (Node.js / Vanilla JS)
│   ├── app.js / duel_app.js
│   ├── index.html / the_duel.html
│   └── mock-data.js
│
├── 📁 docs/                         # Tài liệu chi tiết
├── 📁 configs/                      # File cấu hình (YAML/JSON)
├── 📁 EDA/                          # Exploratory Data Analysis
├── 📁 models/                       # Model checkpoints (local, không push)
├── 📁 archive/                      # Code cũ, backup
│
├── requirements.txt                 # Python dependencies
├── .gitignore
└── LICENSE
```

---

## 📊 Dataset

### Thống kê

| Tập | Số mẫu | Tỷ lệ |
|---|---|---|
| Train | 6,101 | 80% |
| Validation | 762 | 10% |
| Test | 763 | 10% |
| **Tổng** | **7,626** | 100% |

### Phân bố nhãn

| Label | Tên | Số mẫu | Tỷ lệ |
|---|---|---|---|
| `0` | Clean | ~3,355 | ~44% |
| `1` | Offensive | ~1,942 | ~25.5% |
| `2` | Hate Speech | ~2,149 | ~28.2% |

> Dataset có **lớp mất cân bằng nhẹ** — nhóm dùng class weights [0.75, 1.27, 1.14] để bù trừ khi training.

### Nguồn dữ liệu

Thu thập từ các nền tảng mạng xã hội Việt Nam via **Apify**:

| Nền tảng | Chủ đề |
|---|---|
| Facebook | Drama influencer, Regional discrimination, Body shaming, LGBTQ, Social issues |
| YouTube | IT Got Talent, Rap Việt, Tin tức |
| VOZ/Forum | Confession, Phản biện |

### Cấu trúc CSV cuối

```
text,label,topic,source
"nội dung bình luận",0,"Drama","facebook"
```

> ⚠️ **Lưu ý:** Dữ liệu thô chứa thông tin người dùng, **không được phép phân phối công khai**. Chỉ chia sẻ dataset đã ẩn danh hóa với giấy phép CC BY-SA 4.0.

---

## ⚙️ Pipeline tiền xử lý — `advanced_text_cleaning.py`

Module cốt lõi với **18 bước xử lý tuần tự**, tối ưu cho PhoBERT:

```
Input Text
    │
    ▼
 1. Unicode NFC normalization
 2. Apify/HTML artifact removal
 3. URL & Social link removal
 4. Mention @user → <user>
 5. Person name masking → <person>   (Rule-based NER: 50+ họ, 63 tỉnh thành)
 6. Special emoji mapping (LGBT 🏳️‍🌈 → "lgbt")
 7. Standard emoji → sentiment tags (<emo_pos> / <emo_neg>)
 8. ASCII emoticons removal (:))) → "")
 9. Hashtag removal
10. Bypass pattern detection (d.ị.t → địt)
11. Leetspeak conversion (3 → ê, @ → a...)
12. English insult mapping (fuck → <eng_vulgar>)
13. Teencode normalization (1,000+ variants, 2-tier)
14. Context-aware "m" disambiguation (mày vs em/anh)
15. Repeated character normalization (vllllll → vl)
16. Punctuation normalization
17. Whitespace normalization
18. PhoBERT token-aware truncation (max_length=256)
    │
    ▼
Cleaned Text
```

### Thiết kế 2-tier Teencode

| Tier | Loại | Ví dụ | Xử lý |
|---|---|---|---|
| `TEENCODE_NEUTRAL` | An toàn chuẩn hóa | `ko` → `không` | Thay thế |
| `TEENCODE_INTENSITY_SENSITIVE` | Bảo tồn hình thái | `đm`, `vcl`, `parky` | Giữ nguyên |

> **Triết lý thiết kế:** "Bảo toàn nồng độ" — Giữ nguyên các biến thể viết tắt tục tĩu để PhoBERT học được intensity gradient (phân biệt giữa casual slang và hate speech nghiêm trọng).

### Sử dụng API

```python
from src.preprocessing.advanced_text_cleaning import (
    clean_text,           # Làm sạch 1 text
    clean_dataframe,      # Làm sạch DataFrame
    clean_file,           # Làm sạch file CSV/XLSX
    build_input_text_with_context  # Xây dựng "title </s> comment"
)

# Single text
cleaned = clean_text("k0 phải thế đmm")
# → "không phải thế đmm"

# DataFrame
df_clean = clean_dataframe(df, text_column='comment')

# File
df_result = clean_file('data/raw/input.csv', 'data/processed/output.csv', text_column='comment')

# Context format (title + comment)
text = build_input_text_with_context(
    title="Video âm nhạc",
    comment="bài này hay vl",
    max_total_length=256
)
# → "Video âm nhạc </s> bài này hay vl"
```

### CLI

```bash
python src/preprocessing/advanced_text_cleaning.py input.csv -o output.csv -c comment
```

---

## 🚀 Huấn luyện mô hình

### Môi trường: Google Colab / Kaggle

**Notebook chính:** `notebooks/COLAB_PHOBERT_IT_GOT_TALENT_Final.ipynb`

#### Cấu hình training

```python
CONFIG = {
    'model_name':     'vinai/phobert-base-v2',
    'num_labels':     3,
    'max_length':     256,
    'batch_size':     16,
    'learning_rate':  2e-5,
    'num_epochs':     5,
    'warmup_ratio':   0.1,
    'weight_decay':   0.01,
    'test_size':      0.10,
    'val_size':       0.10,
    'random_state':   42,
}
```

#### Các bước chạy trên Colab

```python
# 1. Mount Drive và upload dataset
from google.colab import drive
drive.mount('/content/drive')

# 2. Cập nhật đường dẫn dataset
CONFIG['data_path'] = '/content/drive/MyDrive/dataset_hate_speech_Vietnamese_KAGGLE_V2.csv'

# 3. Chạy toàn bộ notebook (Runtime > Run All)
```

#### Input format

Dataset CSV phải có 2 cột bắt buộc:

| Cột | Kiểu | Mô tả |
|---|---|---|
| `text` | string | Văn bản đã qua tiền xử lý, format: `"title </s> comment"` |
| `label` | int | 0 (Clean), 1 (Offensive), 2 (Hate Speech) |

### Tính năng Training

- ✅ **Stratified split** (80/10/10) — giữ tỷ lệ label đều
- ✅ **Early stopping** (patience=2)
- ✅ **FP16** mixed precision (tiết kiệm VRAM)
- ✅ **Best model checkpoint** theo `f1_macro`
- ✅ **Confusion matrix** & classification report tự động

---

## 📈 Kết quả

### PhoBERT-base-v2 (Final — IT Got Talent 2025)

| Metric | Score |
|---|---|
| **Accuracy** | **80.87%** |
| **F1 Macro** | **0.7995** |
| **Val F1 (Best epoch)** | 0.7960 (Epoch 4) |
| **Inference Speed** | < 100ms / sample |
| **Inter-annotator Agreement** | Cohen's Kappa = 0.77 (Substantial) |

### Per-class F1 (Test Set)

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Clean | ~0.85 | ~0.85 | ~0.85 |
| Offensive | ~0.73 | ~0.72 | ~0.72 |
| Hate Speech | ~0.82 | ~0.78 | ~0.80 |

> Kết quả đầy đủ được lưu tự động vào `results_summary.json` sau training.

---

## 🌐 Demo

### Chrome Extension — SafeSense Kids

```
safesense-kids-extension/
├── manifest.json      # Manifest V3
├── content.js         # Inject script → detect hate speech
├── popup.html/js      # Extension popup UI
└── background.js      # Service worker
```

Cài đặt:
1. Mở Chrome → `chrome://extensions`
2. Bật **Developer mode**
3. Chọn **Load unpacked** → chọn thư mục `safesense-kids-extension/`

### Web Demo — YouTube Duel

```bash
cd safesense-youtube-demo
node app.js
# Truy cập: http://localhost:3000
```

---

## 🛠 Cài đặt

### Yêu cầu

- Python 3.9+
- CUDA 11.3+ (khuyến nghị để training)
- Node.js 16+ (cho web demo)

### Chạy Streamlit Demo

```bash
# Demo phát hiện toxic (cần model đã train)
cd TOXIC_COMMENT/demo
streamlit run Safesense_VI.py

# Demo preprocessing pipeline (không cần model)
streamlit run preprocessing_demo.py
```

### Cài đặt môi trường Python

```bash
# Clone repo
git clone https://github.com/<your-username>/safesense-vi.git
cd safesense-vi

# Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt
```

### Kiểm tra cài đặt

```python
from src.preprocessing.advanced_text_cleaning import clean_text

result = clean_text("bọn này ngu vl đm")
print(result)
```

---

## 💻 Sử dụng nhanh

### 1. Tiền xử lý dataset

```bash
# Xử lý file CSV
python src/preprocessing/apply_advanced_cleaning.py

# Hoặc xử lý JSON từ Apify
python src/preprocessing/apify_to_csv.py \
    --input data/raw/facebook/ \
    --output data/processed/facebook_cleaned.csv
```

### 2. Training (local)

```bash
python src/training/train_phobert.py \
    --data data/final/dataset_hate_speech_Vietnamese_KAGGLE_V2.csv \
    --output models/phobert-v2
```

### 3. Inference

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_path = "TOXIC_COMMENT/models/phobert-hate-speech-final"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def predict(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        logits = model(**inputs).logits
    label = torch.argmax(logits, dim=1).item()
    labels = {0: "Clean", 1: "Offensive", 2: "Hate Speech"}
    return labels[label]

print(predict("bài hát hay quá"))        # → Clean
print(predict("đồ ngu, bắc kỳ cút đi")) # → Hate Speech
```

---

## 📚 Tài liệu

| File | Mô tả |
|---|---|
| [docs/GUIDELINE_GAN_NHAN_V3.md](docs/GUIDELINE_GAN_NHAN_V3.md) | Hướng dẫn gán nhãn chi tiết |
| [docs/PREPROCESSING_DOCUMENTATION.md](docs/PREPROCESSING_DOCUMENTATION.md) | Tài liệu pipeline tiền xử lý |
| [docs/TEXT_CLEANING_GUIDE.md](docs/TEXT_CLEANING_GUIDE.md) | Hướng dẫn làm sạch văn bản |
| [docs/WORD_SEGMENTATION_GUIDE.md](docs/WORD_SEGMENTATION_GUIDE.md) | Hướng dẫn tách từ tiếng Việt |
| [docs/TRAINING_IMPROVEMENT_GUIDE.md](docs/TRAINING_IMPROVEMENT_GUIDE.md) | Các hướng cải thiện mô hình |
| [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) | Trạng thái dự án hiện tại |
| [src/preprocessing/README_APIFY_TO_CSV.md](src/preprocessing/README_APIFY_TO_CSV.md) | Hướng dẫn chuyển đổi Apify data |

---

## 🤝 Đóng góp

1. Fork repo
2. Tạo branch mới: `git checkout -b feature/ten-tinh-nang`
3. Commit: `git commit -m "feat: mô tả ngắn gọn"`
4. Push: `git push origin feature/ten-tinh-nang`
5. Tạo Pull Request

---

## ⚖️ License

- **Source Code:** [MIT License](LICENSE)
- **Dataset:** [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — Chỉ áp dụng cho phần dữ liệu đã ẩn danh hóa

---

## 📧 Liên hệ

- **Tác giả:** SafeSense-VI Team — IT Got Talent 2025
- **Email:** Thientran805954@gmail.com

---

*Dự án được phát triển phục vụ mục đích nghiên cứu học thuật và bảo vệ trẻ em trên môi trường mạng.*
