import streamlit as st
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Verify path exists
if not (project_root / "src" / "preprocessing" / "advanced_text_cleaning.py").exists():
    st.error(f"❌ Không tìm thấy module preprocessing tại: {project_root / 'src'}")
    st.info("💡 Hãy chạy từ thư mục gốc project hoặc kiểm tra cấu trúc thư mục")
    st.stop()

# Import text cleaning module
try:
    from src.preprocessing.advanced_text_cleaning import clean_text
except ImportError as e:
    st.error(f"❌ Lỗi import: {e}")
    st.info(f"💡 Project root: {project_root}")
    st.info("💡 Hãy đảm bảo file advanced_text_cleaning.py tồn tại trong src/preprocessing/")
    st.stop()

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="SafeSense-Vi Demo",
    page_icon="🛡️",
    layout="centered"
)

# --- 1. TẢI MODEL (MÔ PHỎNG) ---
# Lưu ý: Đây là hàm để load model của bạn. 
# Khi chạy thật, bạn thay 'vinai/phobert-base-v2' bằng đường dẫn đến file checkpoint của bạn (ví dụ: './saved_models/epoch_3')
@st.cache_resource
def load_model():
    # Sử dụng PhoBERT chuẩn làm tokenizer nền tảng [cite: 64]
    tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base-v2")
    
    # HƯỚNG DẪN THAY THẾ:
    # Thay dòng dưới bằng: model = AutoModelForSequenceClassification.from_pretrained("./path_to_your_trained_model")
    # Hiện tại tôi dùng model gốc chưa fine-tune để code chạy được giao diện ngay lập tức.
    model = AutoModelForSequenceClassification.from_pretrained("C:\\Học sâu\\Dataset\\TOXIC_COMMENT\\models", num_labels=3)
    
    return tokenizer, model

# Load resources
try:
    tokenizer, model = load_model()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
except Exception as e:
    st.error(f"Lỗi tải model: {e}")

# --- 2. HÀM TIỀN XỬ LÝ (PIPELINE 14 BƯỚC CHUẨN) ---
def preprocess_input(title, comment):
    """
    Tiền xử lý theo pipeline chuẩn với teencode normalization.
    
    Pipeline bao gồm:
    - Chuẩn hóa teencode (k→không, đm→địt mẹ, vcl→vãi lồn)
    - Xử lý emoji → sentiment tags
    - Xử lý repeated chars (nguuuu → ngu <intense>)
    - Context-aware "m" mapping
    - Named entity masking (<PERSON>, <USER>)
    """
    # Clean title and comment using advanced pipeline
    cleaned_title = clean_text(title) if title.strip() else ""
    cleaned_comment = clean_text(comment)
    
    # Ghép Tiêu đề và Bình luận theo format PhoBERT
    input_text = f"{cleaned_title} </s> {cleaned_comment}" if cleaned_title else f"</s> {cleaned_comment}"
    
    return input_text

# --- 3. GIAO DIỆN NGƯỜI DÙNG (UI) ---

st.title("🛡️ SafeSense-Vi Demo")
st.markdown("**Hệ thống phát hiện ngôn ngữ độc hại đa tầng (Context-Aware Toxicity Detection)**")
st.markdown("---")

# Khu vực nhập liệu
col1, col2 = st.columns([1, 2])
with col1:
    st.info("Nhập ngữ cảnh (Tiêu đề bài viết)")
    title_input = st.text_area("Tiêu đề (Title)", height=100, placeholder="Ví dụ: Vụ án tham nhũng...")

with col2:
    st.info("Nhập nội dung cần kiểm tra")
    comment_input = st.text_area("Bình luận (Comment)", height=100, placeholder="Ví dụ: Đáng bị tử hình...")

# Nút phân tích
if st.button("🔍 PHÂN TÍCH ĐỘC HẠI", type="primary", use_container_width=True):
    if not comment_input:
        st.warning("Vui lòng nhập nội dung bình luận!")
    else:
        with st.spinner("Đang xử lý qua PhoBERT..."):
            # A. Tiền xử lý
            processed_text = preprocess_input(title_input, comment_input)
            
            # B. Tokenize & Inference
            inputs = tokenizer(processed_text, return_tensors="pt", truncation=True, max_length=256, padding=True)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(**inputs)
                probs = F.softmax(outputs.logits, dim=1)
                confidence, predicted_class = torch.max(probs, dim=1)
                
                # Convert to numpy for display
                probs_np = probs.cpu().numpy()[0]
                pred_label = predicted_class.item()
                conf_score = confidence.item()

            # --- MÔ PHỎNG KẾT QUẢ (DEMO LOGIC) ---
            # (Vì chưa có file model fine-tuned của bạn, tôi viết logic giả lập dựa trên từ khóa 
            # để bạn test giao diện. Khi lắp model thật vào, hãy XÓA đoạn logic if/else này đi)
            
            # --- BẮT ĐẦU LOGIC GIẢ LẬP (XÓA KHI CÓ MODEL THẬT) ---
            keywords_hate = ["giết", "tử hình", "ngu", "chết"]
            if any(k in comment_input.lower() for k in keywords_hate):
                if "vụ án" in title_input.lower() and "tử hình" in comment_input.lower():
                     # Mô phỏng ngữ cảnh tường thuật 
                    pred_label = 0 
                    probs_np = [0.85, 0.10, 0.05]
                else:
                    pred_label = 2
                    probs_np = [0.05, 0.15, 0.80]
            # --- KẾT THÚC LOGIC GIẢ LẬP ---

            # C. Hiển thị kết quả [cite: 60-62]
            st.markdown("### Kết quả phân tích:")
            
            labels_map = {
                0: ("SẠCH (CLEAN)", "success", "Nội dung an toàn hoặc tường thuật khách quan."),
                1: ("PHẢN CẢM (OFFENSIVE)", "warning", "Có từ ngữ thô tục hoặc công kích cá nhân nhẹ."),
                2: ("THÙ GHÉT (HATE SPEECH)", "error", "Vi phạm nghiêm trọng: Kích động bạo lực, thù ghét danh tính.")
            }
            
            label_text, color, description = labels_map[pred_label]
            
            # Hiển thị thẻ kết quả lớn
            if color == "success":
                st.success(f"Dự đoán: {label_text} | Độ tin cậy: {probs_np[pred_label]:.2%}")
            elif color == "warning":
                st.warning(f"Dự đoán: {label_text} | Độ tin cậy: {probs_np[pred_label]:.2%}")
            else:
                st.error(f"Dự đoán: {label_text} | Độ tin cậy: {probs_np[pred_label]:.2%}")
                
            st.caption(f"Lý giải: {description}")

            # D. Biểu đồ xác suất
            st.markdown("#### Phân phối xác suất lớp:")
            chart_data = {
                "Nhãn": ["Clean (0)", "Offensive (1)", "Hate (2)"],
                "Xác suất": probs_np
            }
            # --- Thay thế đoạn st.bar_chart cũ bằng đoạn này ---
            import altair as alt
            import pandas as pd

            # Tạo DataFrame cho biểu đồ
            df_chart = pd.DataFrame({
                "Nhãn": ["Clean (0)", "Offensive (1)", "Hate (2)"],
                "Xác suất": probs_np,
                "Màu": ["#2ecc71", "#f1c40f", "#e74c3c"]  # Định nghĩa màu tương ứng
            })

            # Vẽ biểu đồ bằng Altair
            c = alt.Chart(df_chart).mark_bar().encode(
                x=alt.X('Nhãn', sort=None),
                y='Xác suất',
                color=alt.Color('Nhãn', scale=alt.Scale(
                    domain=["Clean (0)", "Offensive (1)", "Hate (2)"],
                    range=["#2ecc71", "#f1c40f", "#e74c3c"]
                )),
                tooltip=['Nhãn', alt.Tooltip('Xác suất', format='.1%')]
            ).properties(
                height=300
            )

            st.altair_chart(c, use_container_width=True)
# ----------------------------------------------------r
# Sidebar thông tin
with st.sidebar:
    st.header("Thông tin Model")
    st.markdown("**Kiến trúc:** PhoBERT-base-v2")
    st.markdown("**Input:** `Title </s> Comment`")
    st.markdown("**Labels:**")
    st.markdown("- 0: Clean (Không độc hại)")
    st.markdown("- 1: Offensive (Phản cảm)")
    st.markdown("- 2: Hate (Thù ghét)")
    st.info("Demo phục vụ Hội thi Tài năng CNTT 2025")