"""
🔥 ADVANCED TEXT CLEANING DEMO
Interactive interface to test preprocessing pipeline step-by-step

Features:
- Real-time text cleaning
- Step-by-step pipeline visualization
- Batch processing from CSV/Text
- Export results
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import re
from io import StringIO


# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from src.preprocessing.advanced_text_cleaning import (
    clean_text,
    normalize_unicode_nfc,
    remove_urls,
    remove_html,
    remove_hashtags,
    remove_mentions,
    normalize_teencode,
    replace_person_names,
    remove_emojis,
    remove_text_emoticons,
    map_english_insults,
    normalize_unicode,
    remove_bypass_patterns,
    convert_leetspeak,
    remove_repeated_chars,
    context_aware_m_mapping,
    normalize_punctuation,
    normalize_whitespace
)
except ImportError as e:
    st.error(f"❌ Lỗi import preprocessing module: {e}")
    st.info(f"💡 Project root: {project_root}")
    st.info("💡 Hãy chạy: streamlit run preprocessing_demo.py từ thư mục demo")
    st.stop()

# Page config
st.set_page_config(
    page_title="Advanced Text Cleaning Demo",
    page_icon="🔥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .step-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 4px solid #1f77b4;
    }
    .input-box {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .output-box {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .changed {
        background-color: #fff3cd;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🔥 Advanced Text Cleaning Demo")
st.markdown("**Interactive Preprocessing Pipeline for Vietnamese Text**")
st.markdown("---")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    show_steps = st.checkbox("Show Step-by-Step", value=True)
    show_stats = st.checkbox("Show Statistics", value=True)
    
    st.markdown("---")
    st.markdown("### 📚 Pipeline Steps")
    st.markdown("""
    1. Unicode Normalize
    2. Remove URLs/HTML
    3. Remove Hashtags
    4. Remove Mentions
    5. **Teencode Normalize**
    6. **Person Name Masking**
    7. Lowercase
    8. **Emoji → Tags**
    9. **English Insults**
    10. Bypass Patterns
    11. Leetspeak
    12. **Repeated Chars**
    13. **Context "m"**
    14. Punctuation & Space
    """)

# Tab selection
tab1, tab2, tab3 = st.tabs(["🔍 Single Text", "📊 Batch Processing", "📖 Examples"])

# ===== TAB 1: SINGLE TEXT =====
with tab1:
    st.header("Single Text Processing")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Input")
        input_text = st.text_area(
            "Enter text to clean:",
            height=200,
            placeholder="Ví dụ: Đ.m nguuuu vcl 😡 ko biết ns gì luôn ạ"
        )
        
        col_a, col_b = st.columns(2)
        with col_a:
            process_btn = st.button("🚀 Process", type="primary", use_container_width=True)
        with col_b:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)
    
    with col2:
        st.subheader("✨ Output")
        if process_btn and input_text:
            cleaned = clean_text(input_text)
            st.markdown(f'<div class="output-box">{cleaned}</div>', unsafe_allow_html=True)
            
            # Copy button
            st.code(cleaned, language=None)
        elif clear_btn:
            st.info("Enter text and click Process")
        else:
            st.info("Enter text and click Process")
    
    # Step-by-step visualization
    if show_steps and process_btn and input_text:
        st.markdown("---")
        st.header("🔬 Step-by-Step Pipeline")
        
        steps = []
        text = input_text
        
        # Step 1: Unicode Normalize
        text_step = normalize_unicode_nfc(text)
        steps.append(("1. Unicode Normalize (NFC)", text, text_step))
        text = text_step
        
        # Step 2: Remove URLs
        text_step = remove_urls(text)
        steps.append(("2. Remove URLs", text, text_step))
        text = text_step
        
        # Step 3: Remove HTML
        text_step = remove_html(text)
        steps.append(("3. Remove HTML", text, text_step))
        text = text_step
        
        # Step 4: Remove Hashtags
        text_step = remove_hashtags(text)
        steps.append(("4. Remove Hashtags", text, text_step))
        text = text_step
        
        # Step 5: Remove Mentions
        text_step = remove_mentions(text)
        steps.append(("5. Remove Mentions → <user>", text, text_step))
        text = text_step
        
        # Step 6: Teencode Normalize
        text_step = normalize_teencode(text)
        steps.append(("6. 🔥 Teencode Normalize", text, text_step))
        text = text_step
        
        # Step 7: Person Names
        text_step = replace_person_names(text)
        steps.append(("7. 🔥 Person Names → <person>", text, text_step))
        text = text_step
        
        # Step 8: Lowercase (with tag protection)
        text_step = text.replace('<user>', '___USER___').replace('<person>', '___PERSON___')
        text_step = text_step.lower()
        text_step = text_step.replace('___user___', '<user>').replace('___person___', '<person>')
        steps.append(("8. Lowercase", text, text_step))
        text = text_step
        
        # Step 9: Emoji
        text_step = remove_emojis(text)
        text_step = remove_text_emoticons(text_step)
        steps.append(("9. 🔥 Emoji → Tags", text, text_step))
        text = text_step
        
        # Step 10: English Insults
        text_step = map_english_insults(text)
        steps.append(("10. 🔥 English Insults", text, text_step))
        text = text_step
        
        # Step 11: Unicode tricks
        text_step = normalize_unicode(text)
        steps.append(("11. Unicode Tricks", text, text_step))
        text = text_step
        
        # Step 12: Bypass patterns
        text_step = remove_bypass_patterns(text)
        steps.append(("12. Bypass Patterns (đ.m→đm)", text, text_step))
        text = text_step
        
        # Step 13: Leetspeak
        text_step = convert_leetspeak(text)
        steps.append(("13. Leetspeak (ch3t→chết)", text, text_step))
        text = text_step
        
        # Step 14: Repeated chars
        text_step = remove_repeated_chars(text)
        steps.append(("14. 🔥 Repeated Chars + Intensity", text, text_step))
        text = text_step
        
        # Step 15: Context "m"
        text_step = context_aware_m_mapping(text)
        steps.append(("15. 🔥 Context-aware 'm'", text, text_step))
        text = text_step
        
        # Step 16: Punctuation
        text_step = normalize_punctuation(text)
        steps.append(("16. Punctuation", text, text_step))
        text = text_step
        
        # Step 17: Whitespace
        text_step = normalize_whitespace(text)
        steps.append(("17. Whitespace", text, text_step))
        
        # Display steps
        for step_name, before, after in steps:
            if before != after:
                with st.expander(f"✅ {step_name} - **CHANGED**", expanded=False):
                    col_before, col_after = st.columns(2)
                    with col_before:
                        st.markdown("**Before:**")
                        st.code(before, language=None)
                    with col_after:
                        st.markdown("**After:**")
                        st.code(after, language=None)
            else:
                st.markdown(f"⏭️ {step_name} - No change")
    
    # Statistics
    if show_stats and process_btn and input_text:
        st.markdown("---")
        st.header("📊 Statistics")
        
        cleaned = clean_text(input_text)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Original Length", len(input_text))
        with col2:
            st.metric("Cleaned Length", len(cleaned))
        with col3:
            reduction = len(input_text) - len(cleaned)
            st.metric("Reduction", reduction, delta=f"-{reduction}")
        with col4:
            tag_count = cleaned.count('<')
            st.metric("Tags Added", tag_count)
        
        # Detailed stats
        st.markdown("### Detected Features:")
        features = []
        
        if '<emo_neg>' in cleaned:
            features.append("😡 Negative Emotion")
        if '<emo_pos>' in cleaned:
            features.append("😊 Positive Emotion")
        if '<intense>' in cleaned or '<very_intense>' in cleaned:
            features.append("⚡ Intensity Markers")
        if '<person>' in cleaned:
            features.append("👤 Person Names")
        if '<user>' in cleaned:
            features.append("@ Mentions")
        if '<eng_vulgar>' in cleaned or '<eng_insult>' in cleaned:
            features.append("🌐 English Insults")
        
        if features:
            for feature in features:
                st.markdown(f"- {feature}")
        else:
            st.info("No special features detected")

# ===== TAB 2: BATCH PROCESSING =====
with tab2:
    st.header("📊 Batch Processing")
    
    st.markdown("Upload a text file or CSV to process multiple texts at once")
    
    upload_type = st.radio("Input Type:", ["Text File (.txt)", "CSV File (.csv)"])
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['txt', 'csv'] if upload_type == "CSV File (.csv)" else ['txt']
    )
    
    if uploaded_file is not None:
        try:
            if upload_type == "Text File (.txt)":
                # Process text file (one text per line)
                content = uploaded_file.read().decode('utf-8')
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                
                st.info(f"Found {len(lines)} texts to process")
                
                if st.button("🚀 Process All Texts", type="primary"):
                    with st.spinner("Processing..."):
                        results = []
                        for i, line in enumerate(lines, 1):
                            cleaned = clean_text(line)
                            results.append({
                                'ID': i,
                                'Original': line,
                                'Cleaned': cleaned,
                                'Length_Before': len(line),
                                'Length_After': len(cleaned)
                            })
                        
                        df_results = pd.DataFrame(results)
                        
                        st.success(f"✅ Processed {len(results)} texts!")
                        
                        # Display results
                        st.dataframe(df_results, use_container_width=True)
                        
                        # Download button
                        csv = df_results.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Results (CSV)",
                            data=csv,
                            file_name="cleaned_results.csv",
                            mime="text/csv"
                        )
            
            else:  # CSV File
                df = pd.read_csv(uploaded_file)
                st.write("Preview of uploaded data:")
                st.dataframe(df.head(), use_container_width=True)
                
                text_column = st.selectbox(
                    "Select column to clean:",
                    options=df.columns.tolist()
                )
                
                if st.button("🚀 Process Column", type="primary"):
                    with st.spinner("Processing..."):
                        df['cleaned'] = df[text_column].apply(
                            lambda x: clean_text(str(x)) if pd.notna(x) else ""
                        )
                        
                        st.success("✅ Processing complete!")
                        
                        # Display results
                        st.dataframe(df, use_container_width=True)
                        
                        # Download button
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Results (CSV)",
                            data=csv,
                            file_name="cleaned_dataset.csv",
                            mime="text/csv"
                        )
        
        except Exception as e:
            st.error(f"Error processing file: {e}")

# ===== TAB 3: EXAMPLES =====
with tab3:
    st.header("📖 Example Use Cases")
    
    examples = {
        "Teencode Normalization": {
            "input": "ko biết ns gì luôn ạ đc rồi m ơi",
            "expected": "không biết nói gì luôn ạ được rồi em ơi",
            "description": "Chuyển đổi teencode thành tiếng Việt chuẩn"
        },
        "Bypass Pattern": {
            "input": "Đ.m n.g.u vcl đ-é-o biết gì",
            "expected": "đm ngu vcl đéo biết gì",
            "description": "Xử lý bypass patterns (dấu chấm, gạch giữa chữ)"
        },
        "Emoji & Intensity": {
            "input": "Nguuuuuu quáaaaa 😡😤🤬",
            "expected": "ngu <very_intense> quá <very_intense> <emo_neg> <emo_neg> <emo_neg>",
            "description": "Emoji → sentiment tags và intensity markers"
        },
        "Context-aware 'm' (Positive)": {
            "input": "yêu m nhiều lắm nhớ m quá",
            "expected": "yêu em nhiều lắm nhớ em quá",
            "description": "Ngữ cảnh tích cực: m → em"
        },
        "Context-aware 'm' (Toxic)": {
            "input": "m ngu vcl đéo biết gì hết",
            "expected": "mày ngu vcl đéo biết gì hết",
            "description": "Ngữ cảnh độc hại: m → mày"
        },
        "Person Name Masking": {
            "input": "Anh Tuấn và chị Hoa đi Hà Nội",
            "expected": "anh tuấn và <person> đi hà nội",
            "description": "Mask tên người thành <person>"
        },
        "English Insults": {
            "input": "stupid idiot fuck you shit",
            "expected": "<eng_insult> <eng_insult> <eng_vulgar> you <eng_vulgar>",
            "description": "Phát hiện từ xúc phạm tiếng Anh"
        },
        "Leetspeak": {
            "input": "ch3t di con ngu4",
            "expected": "chết đi con ngua",
            "description": "Chuyển đổi số thành chữ trong từ"
        },
        "Mixed Features": {
            "input": "@nguyenvana Đ.m Trần Ngọc nguuuu vcl 😡 ko biết gì",
            "expected": "<user> đm <person> ngu <very_intense> vcl <emo_neg> không biết gì",
            "description": "Kết hợp nhiều tính năng"
        }
    }
    
    st.markdown("Click on any example to test it:")
    
    for title, example in examples.items():
        with st.expander(f"✨ {title}"):
            st.markdown(f"**Description:** {example['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Input:**")
                st.code(example['input'], language=None)
            with col2:
                st.markdown("**Expected Output:**")
                st.code(example['expected'], language=None)
            
            if st.button(f"Test '{title}'", key=f"btn_{title}"):
                actual = clean_text(example['input'])
                
                st.markdown("**Actual Output:**")
                st.code(actual, language=None)
                
                if actual == example['expected']:
                    st.success("✅ Output matches expected!")
                else:
                    st.warning("⚠️ Output differs from expected")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**Expected:**")
                        st.text(example['expected'])
                    with col_b:
                        st.markdown("**Got:**")
                        st.text(actual)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🔥 Advanced Text Cleaning Demo | Built with Streamlit</p>
    <p>Pipeline: 14 steps | Dictionary: 300+ teencode entries</p>
</div>
""", unsafe_allow_html=True)
