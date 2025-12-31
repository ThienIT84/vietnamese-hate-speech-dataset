"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔍 KAGGLE: Export Model Errors to Excel                                     ║
║  Cell này export tất cả các câu model dự đoán SAI ra file Excel             ║
║  Để phân tích lỗi và cải thiện model                                         ║
║                                                                               ║
║  YÊU CẦU: Phải chạy sau CELL 14 (Final Evaluation)                           ║
║  Cần có: final_true, final_preds, final_probs                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CELL: Export Model Errors với Confidence Scores
# ═══════════════════════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
from datetime import datetime
import os

print("="*80)
print("🔍 EXPORTING MODEL ERRORS")
print("="*80)

# Bước 1: Load lại data để lấy validation texts
print("\n📂 Loading data to get validation texts...")

# Tìm data file
data_path = None
if 'Config' in globals() and hasattr(Config, 'DATA_PATH'):
    data_path = Config.DATA_PATH
else:
    # Auto-detect
    input_path = "/kaggle/input"
    if os.path.exists(input_path):
        for dataset in os.listdir(input_path):
            dataset_path = os.path.join(input_path, dataset)
            if os.path.isdir(dataset_path):
                for file in os.listdir(dataset_path):
                    if 'TRUNCATED' in file and (file.endswith('.xlsx') or file.endswith('.csv')):
                        data_path = os.path.join(dataset_path, file)
                        break
                if data_path:
                    break

if not data_path:
    print("❌ ERROR: Cannot find data file!")
    print("   Please set data_path manually:")
    print("   data_path = '/kaggle/input/your-dataset/your-file.xlsx'")
    raise FileNotFoundError("Data file not found")

print(f"✅ Found data: {data_path}")

# Load data
if data_path.endswith('.xlsx'):
    df = pd.read_excel(data_path)
else:
    df = pd.read_csv(data_path)

# Xác định text column
text_col = 'training_text' if 'training_text' in df.columns else 'text'
label_col = 'label'

print(f"✅ Loaded: {len(df)} samples")

# Bước 2: Recreate train/val split (PHẢI GIỐNG CELL 7)
from sklearn.model_selection import train_test_split

texts = df[text_col].fillna('').astype(str).tolist()
labels = df[label_col].astype(int).tolist()

# Split với SEED giống CELL 7
SEED = 42 if 'Config' not in globals() else Config.SEED

train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels,
    test_size=0.15,
    random_state=SEED,
    stratify=labels
)

print(f"✅ Recreated split: Train={len(train_texts)} | Val={len(val_texts)}")

# Kiểm tra xem số lượng có khớp không
if len(val_texts) != len(final_true):
    print(f"⚠️ WARNING: Val size mismatch!")
    print(f"   val_texts: {len(val_texts)} | final_true: {len(final_true)}")
    print(f"   Using first {len(final_true)} samples from val_texts")
    val_texts = val_texts[:len(final_true)]

# Tạo DataFrame với đầy đủ thông tin
label_names = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}

error_data = []
for i, (text, true_label, pred_label, probs) in enumerate(zip(val_texts, final_true, final_preds, final_probs)):
    is_error = true_label != pred_label
    
    error_data.append({
        'id': i + 1,
        'text': text,
        'true_label': int(true_label),
        'true_label_name': label_names[int(true_label)],
        'pred_label': int(pred_label),
        'pred_label_name': label_names[int(pred_label)],
        'is_error': is_error,
        'error_type': f"{int(true_label)}→{int(pred_label)}" if is_error else 'Correct',
        'confidence_clean': float(probs[0]),
        'confidence_toxic': float(probs[1]),
        'confidence_hate': float(probs[2]),
        'max_confidence': float(probs.max()),
        'text_length': len(str(text).split())
    })

df_all = pd.DataFrame(error_data)

# Lọc chỉ lấy các câu SAI
df_errors = df_all[df_all['is_error'] == True].copy()

# Sắp xếp theo confidence (cao nhất trước - model tự tin nhưng sai)
df_errors = df_errors.sort_values('max_confidence', ascending=False)

print(f"\n📊 STATISTICS:")
print(f"   Total validation samples: {len(df_all)}")
print(f"   Correct predictions: {len(df_all) - len(df_errors)} ({(len(df_all) - len(df_errors))/len(df_all)*100:.1f}%)")
print(f"   Wrong predictions: {len(df_errors)} ({len(df_errors)/len(df_all)*100:.1f}%)")

print(f"\n📊 ERROR BREAKDOWN:")
error_types = df_errors['error_type'].value_counts()
for error_type, count in error_types.items():
    true_label = int(error_type.split('→')[0])
    pred_label = int(error_type.split('→')[1])
    print(f"   {label_names[true_label]} → {label_names[pred_label]}: {count} errors")

# Export ra Excel với formatting
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f'/kaggle/working/model_errors_{timestamp}.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Sheet 1: Tất cả các lỗi
    df_errors.to_excel(writer, sheet_name='All_Errors', index=False)
    
    # Sheet 2-7: Chia theo từng loại lỗi
    for error_type in error_types.index:
        sheet_name = f"Error_{error_type.replace('→', '_to_')}"
        df_subset = df_errors[df_errors['error_type'] == error_type]
        df_subset.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Sheet 8: Summary statistics
    summary_data = {
        'Metric': [
            'Total Validation Samples',
            'Correct Predictions',
            'Wrong Predictions',
            'Accuracy',
            'Error Rate'
        ],
        'Value': [
            len(df_all),
            len(df_all) - len(df_errors),
            len(df_errors),
            f"{(len(df_all) - len(df_errors))/len(df_all)*100:.2f}%",
            f"{len(df_errors)/len(df_all)*100:.2f}%"
        ]
    }
    pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

print(f"\n💾 EXPORTED:")
print(f"   File: {output_file}")
print(f"   Total errors: {len(df_errors)}")
print(f"   Sheets: All_Errors + {len(error_types)} error type sheets + Summary")

# Hiển thị 10 lỗi đầu tiên (model tự tin nhất nhưng sai)
print(f"\n🔥 TOP 10 HIGH-CONFIDENCE ERRORS (Model tự tin nhưng SAI):")
print("="*80)
for idx, row in df_errors.head(10).iterrows():
    print(f"\n{row['id']}. [{row['error_type']}] Confidence: {row['max_confidence']:.2%}")
    print(f"   Text: {row['text'][:100]}...")
    print(f"   True: {row['true_label_name']} | Pred: {row['pred_label_name']}")

print("\n" + "="*80)
print("✅ ERROR EXPORT COMPLETE!")
print("="*80)
print(f"\n📥 Download file: {output_file}")
print("   Click 'Output' tab → Download")
