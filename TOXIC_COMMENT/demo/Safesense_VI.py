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
    # Force reimport to avoid cache issues
    import importlib
    import src.preprocessing.advanced_text_cleaning
    importlib.reload(src.preprocessing.advanced_text_cleaning)
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
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS THEME ---
st.markdown("""
<style>
    /* Main gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main content area */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Header banner */
    .header-banner {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Quick example buttons */
    .example-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: transform 0.2s;
        border-left: 4px solid #667eea;
    }
    
    .example-card:hover {
        transform: translateX(5px);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Override Streamlit metric styling for better visibility */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #1a1a1a !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    
    /* Result cards with colored borders */
    .result-clean {
        border-left: 5px solid #2ecc71;
        background: #e8f8f5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .result-offensive {
        border-left: 5px solid #f1c40f;
        background: #fef9e7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .result-hate {
        border-left: 5px solid #e74c3c;
        background: #fadbd8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Preprocessing preview box */
    .preprocessing-box {
        background: #ffffff;
        border: 2px dashed #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-family: monospace;
        color: #2c3e50;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Info boxes - đồng bộ màu */
    .stAlert {
        border-radius: 10px;
    }
    
    div[data-baseweb="notification"] {
        border-radius: 10px;
    }
    
    /* Streamlit info boxes */
    .element-container div[data-testid="stMarkdownContainer"] > div[data-testid="stMarkdown"] > div {
        border-radius: 8px;
    }
    
    /* Text areas and inputs */
    .stTextArea textarea {
        border: 2px solid #667eea;
        border-radius: 8px;
        font-size: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #764ba2;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eaf6 100%);
        border-radius: 8px;
        border: 1px solid #667eea;
        color: #667eea;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border: 2px solid #667eea;
        border-radius: 8px;
        background: #f8f9fa;
    }
    
    code {
        color: #667eea;
        background: #f0f2f6;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. TẢI MODEL ---
# Load PhoBERT model đã fine-tune cho phân loại Hate Speech
@st.cache_resource
def load_model():
    # Đường dẫn tới model đã fine-tune
    model_path = "C:\\Học sâu\\Dataset\\TOXIC_COMMENT\\models\\phobert-hate-speech-final"
    
    # Load tokenizer và model từ checkpoint đã train
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=3)
    
    return tokenizer, model

# Load resources
try:
    tokenizer, model = load_model()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
except Exception as e:
    st.error(f"Lỗi tải model: {e}")

# --- 2. HÀM TIỀN XỬ LÝ (PIPELINE 18 BƯỚC CHUẨN) ---
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

# Header Banner
st.markdown("""
<div class="header-banner">
    <div class="header-title">🛡️ SafeSense-Vi</div>
    <div class="header-subtitle">
        Hệ thống phát hiện ngôn ngữ độc hại đa tầng (Context-Aware Toxicity Detection)
    </div>
    <div style="margin-top: 1rem; font-size: 0.9rem;">
        🏆 IT Got Talent 2025 | 🤖 Powered by PhoBERT-v2 | 🎯 F1-Score: 0.7995
    </div>
</div>
""", unsafe_allow_html=True)

# Model Performance Metrics
st.markdown("### 📊 Model Performance")
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="🎯 F1-Score (Macro)", value="0.7995", delta="+11% vs target")
with col_m2:
    st.metric(label="✅ Accuracy", value="80.87%", delta="+7.8% vs target")
with col_m3:
    st.metric(label="📚 Training Samples", value="7,626")
with col_m4:
    st.metric(label="⚡ Inference Speed", value="<100ms")

st.markdown("---")

# Quick Test Examples
with st.expander("💡 Quick Test Examples - Nhấp để dùng mẫu", expanded=False):
    st.markdown("**Chọn một ví dụ để test nhanh:**")
    
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    
    with ex_col1:
        if st.button("✅ CLEAN Example", use_container_width=True):
            st.session_state.example_title = "Cải cách giáo dục ở Việt Nam"
            st.session_state.example_comment = "Tôi ủng hộ chương trình đào tạo mới này. Hi vọng sẽ cải thiện chất lượng giảng dạy."
            st.rerun()
    
    with ex_col2:
        if st.button("⚠️ OFFENSIVE Example", use_container_width=True):
            st.session_state.example_title = "Vụ án tham nhũng lớn"
            st.session_state.example_comment = "Mấy thằng này ngu vcl, đáng đi tù hết. Chính phủ làm việc gì cũng kém."
            st.rerun()
    
    with ex_col3:
        if st.button("🚫 HATE SPEECH Example", use_container_width=True):
            st.session_state.example_title = "Xung đột sắc tộc tại Hà Nội"
            st.session_state.example_comment = "Bọn người miền Nam thì chỉ biết lừa đảo. Nên đuổi hết về quê đi. Chúng nó đáng bị đánh chết."
            st.rerun()

st.markdown("---")

# Khu vực nhập liệu
col1, col2 = st.columns([1, 2])
# Initialize session state for examples
if 'example_title' not in st.session_state:
    st.session_state.example_title = ""
if 'example_comment' not in st.session_state:
    st.session_state.example_comment = ""

with col1:
    st.markdown("""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 padding: 0.75rem; border-radius: 8px; color: white; margin-bottom: 0.5rem;'>
                 📝 <b>Nhập ngữ cảnh (Tiêu đề bài viết)</b></div>""", unsafe_allow_html=True)
    title_input = st.text_area(
        "Tiêu đề (Title)", 
        height=120, 
        placeholder="Ví dụ: Vụ án tham nhũng...",
        value=st.session_state.example_title,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 padding: 0.75rem; border-radius: 8px; color: white; margin-bottom: 0.5rem;'>
                 💬 <b>Nhập nội dung cần kiểm tra</b></div>""", unsafe_allow_html=True)
    comment_input = st.text_area(
        "Bình luận (Comment)", 
        height=120, 
        placeholder="Ví dụ: Đáng bị tử hình...",
        value=st.session_state.example_comment,
        label_visibility="collapsed"
    )

# Clear examples button
if st.button("🗑️ Xóa nội dung", type="secondary"):
    st.session_state.example_title = ""
    st.session_state.example_comment = ""
    st.rerun()

# Nút phân tích
if st.button("🔍 PHÂN TÍCH ĐỘC HẠI", type="primary", use_container_width=True):
    if not comment_input:
        st.warning("Vui lòng nhập nội dung bình luận!")
    else:
        with st.spinner("⚙️ Đang xử lý qua PhoBERT..."):
            # A. Tiền xử lý
            processed_text = preprocess_input(title_input, comment_input)
            
            # Show preprocessing preview
            with st.expander("🔍 Xem quá trình tiền xử lý (Preprocessing Preview)", expanded=False):
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;
                     box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);'>
                    <b>📥 INPUT GỐC</b>
                </div>
                """, unsafe_allow_html=True)
                st.code(f"Title: {title_input}\nComment: {comment_input}", language="text")
                
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     padding: 1rem; border-radius: 10px; color: white; margin: 1rem 0 0.5rem 0;
                     box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);'>
                    <b>🔧 SAU KHI CLEANING (18-STEP PIPELINE)</b>
                </div>
                """, unsafe_allow_html=True)
                
                # Escape special tags để hiển thị đúng (không bị HTML render)
                highlighted_text = processed_text
                # Special tags mapping với màu sắc đẹp mắt
                tag_styles = {
                    "</s>": ("#ffd54f", "#f57c00"),           # Vàng cam - Separator
                    "<person>": ("#e3f2fd", "#1976d2"),       # Xanh nhạt - Person
                    "<user>": ("#f3e5f5", "#7b1fa2"),         # Tím nhạt - User
                    "<eng_insult>": ("#ffebee", "#c62828"),   # Đỏ nhạt - English insult
                    "<eng_vulgar>": ("#ef5350", "#ffffff"),   # Đỏ đậm - English vulgar
                    "<emo_pos>": ("#e8f5e9", "#2e7d32"),      # Xanh lá - Positive emoji
                    "<emo_neg>": ("#fce4ec", "#c2185b"),      # Hồng - Negative emoji
                    "<emo_neutral>": ("#f5f5f5", "#616161"),  # Xám - Neutral emoji
                    "<intense>": ("#fff3e0", "#ef6c00"),      # Cam nhạt - Intensity
                    "<very_intense>": ("#ff6f00", "#ffffff"), # Cam đậm - Very intense
                }
                
                for tag, (bg_color, text_color) in tag_styles.items():
                    escaped_tag = tag.replace("<", "&lt;").replace(">", "&gt;")
                    highlighted_text = highlighted_text.replace(
                        tag, 
                        f"<span style='background: {bg_color}; color: {text_color}; padding: 2px 6px; border-radius: 4px; font-weight: bold;'>{escaped_tag}</span>"
                    )
                
                st.markdown(f"<div class='preprocessing-box'>{highlighted_text}</div>", unsafe_allow_html=True)
                
                st.markdown("""
                <div style='background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                     padding: 0.75rem; border-radius: 8px; border-left: 4px solid #4caf50;
                     color: #2e7d32; font-size: 0.9rem; margin-top: 0.75rem; font-weight: 500;'>
                    ✓ Teencode normalized &nbsp;|&nbsp; ✓ Emoji → sentiment tags &nbsp;|&nbsp; ✓ Named entities masked
                </div>
                """, unsafe_allow_html=True)
            
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

            # C. Hiển thị kết quả
            st.markdown("### 🎯 Kết quả phân tích")
            
            labels_map = {
                0: ("✅ SẠCH (CLEAN)", "success", "Nội dung an toàn hoặc tường thuật khách quan.", "#2ecc71"),
                1: ("⚠️ PHẢN CẢM (OFFENSIVE)", "warning", "Có từ ngữ thô tục hoặc công kích cá nhân nhẹ.", "#f1c40f"),
                2: ("🚫 THÙ GHÉT (HATE SPEECH)", "error", "Vi phạm nghiêm trọng: Kích động bạo lực, thù ghét danh tính.", "#e74c3c")
            }
            
            label_text, color, description, color_hex = labels_map[pred_label]
            
            # Hiển thị kết quả với styling đẹp
            result_col1, result_col2 = st.columns([2, 1])
            
            with result_col1:
                # Hiển thị thẻ kết quả lớn
                if color == "success":
                    st.success(f"**{label_text}**")
                elif color == "warning":
                    st.warning(f"**{label_text}**")
                else:
                    st.error(f"**{label_text}**")
                
                st.markdown(f"**📊 Độ tin cậy:** {probs_np[pred_label]:.2%}")
                st.caption(f"💡 {description}")
            
            with result_col2:
                # Confidence meter
                st.markdown(f"**Confidence Score**")
                st.progress(float(probs_np[pred_label]))
                
                # Risk level indicator
                if pred_label == 0:
                    st.markdown("🟢 **Low Risk**")
                elif pred_label == 1:
                    st.markdown("🟡 **Medium Risk**")
                else:
                    st.markdown("🔴 **High Risk**")

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
# ----------------------------------------------------
# Enhanced Sidebar
with st.sidebar:
    st.markdown("# 🛡️ SafeSense-Vi")
    st.markdown("---")
    
    # Model Information
    st.markdown("### 🤖 Model Information")
    st.markdown("""
    **🏗️ Architecture:**  
    PhoBERT-base-v2  
    (vinai/phobert-base-v2)
    
    **📥 Input Format:**  
    `Title </s> Comment`
    
    **🎯 Task:**  
    Multi-class Text Classification
    
    **⚙️ Parameters:**  
    135M parameters
    
    **📊 Classes:**
    - 🟢 Class 0: Clean
    - 🟡 Class 1: Offensive  
    - 🔴 Class 2: Hate Speech
    """)
    
    st.markdown("---")
    
    # Dataset Statistics
    st.markdown("### 📚 Dataset Statistics")
    st.markdown("""
    **Total Dataset:** 7,626 samples  
    **Training Set:** 6,100 samples (80%)  
    **Validation Set:** 763 samples (10%)  
    **Test Set:** 763 samples (10%)
    
    **Distribution:**
    - Clean (Label 0): 44.3%
    - Offensive (Label 1): 27.0%
    - Hate (Label 2): 28.6%
    
    **Quality:**
    - Inter-annotator agreement: 70-75%
    - Multiple rounds of review
    - Guideline V7.2 compliant
    """)
    
    st.markdown("---")
    
    # Performance Metrics
    st.markdown("### 📈 Performance Metrics")
    st.markdown("""
    **Overall (Test Set - 763 samples):**
    - F1-Score (Macro): **0.7995**
    - Accuracy: **80.87%**
    - Precision (Macro): **0.8018**
    - Recall (Macro): **0.7978**
    
    **Per-Class Performance:**
    - Clean F1: **0.85** (Precision: 0.84, Recall: 0.86)
    - Offensive F1: **0.73** (Precision: 0.72, Recall: 0.74)
    - Hate F1: **0.82** (Precision: 0.84, Recall: 0.79)
    
    **Training Details:**
    - Best Epoch: 5/5
    - Training Time: ~30 minutes
    - Hardware: Kaggle T4 GPU
    - Model Size: ~500MB
    """)
    
    st.markdown("---")
    
    # Preprocessing Pipeline
    st.markdown("### 🔧 Preprocessing Pipeline")
    st.markdown("""
    **18-Step Advanced Pipeline:**
    1. ✓ Lowercase normalization
    2. ✓ Emoji extraction & sentiment mapping
    3. ✓ URL & HTML tag removal
    4. ✓ Teencode normalization (vcl, đm, etc.)
    5. ✓ Bypass pattern removal (v.c.l → vcl)
    6. ✓ Repeated character detection (<intense>)
    7. ✓ Context-aware 'm' mapping
    8. ✓ Named entity recognition & masking
    9. ✓ Special character normalization
    10. ✓ Whitespace optimization
    11. ✓ Vietnamese diacritics handling
    12. ✓ Slang & abbreviation expansion
    13. ✓ Punctuation normalization
    14. ✓ Number & digit handling
    15. ✓ Intensity marker injection
    16. ✓ Profanity pattern detection
    17. ✓ Context separator (</s>)
    18. ✓ Final validation & cleanup
    """)
    
    st.markdown("---")
    
    # Project Info
    st.markdown("### 👥 Project Team")
    st.markdown("""
    **Project:** SafeSense-Vi  
    **Event:** IT Got Talent 2025  
    **University:** [Your University]
    
    **Team Members:**
    - Student 1
    - Student 2
    - Student 3
    
    **Supervisor:**
    - [Supervisor Name]
    """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <small>🏆 IT Got Talent 2025</small><br>
        <small>🇻🇳 Made with ❤️ in Vietnam</small>
    </div>
    """, unsafe_allow_html=True)