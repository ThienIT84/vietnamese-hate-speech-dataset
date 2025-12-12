"""
Active Learning: Model predict, bạn chỉ label những mẫu khó
Tiết kiệm 80% thời gian labeling
"""

import pandas as pd
import joblib
import numpy as np

print("="*80)
print("🎯 ACTIVE LEARNING - CHỈ LABEL MẪU KHÓ")
print("="*80)

# Load model
model = joblib.load('models/baseline_model.pkl')
vectorizer = joblib.load('models/baseline_vectorizer.pkl')

print("✅ Loaded model & vectorizer")

# Load full dataset
df_full = pd.read_csv('final_dataset/master_combined.csv')
print(f"\n📊 Full dataset: {len(df_full):,} samples")

# Load samples đã gắn nhãn
df_labeled = pd.read_csv('labeling/dataset_labeled_tran_20251127.csv')
labeled_ids = set(df_labeled['id'])

# Lọc samples chưa gắn nhãn
df_unlabeled = df_full[~df_full['id'].isin(labeled_ids)].copy()
print(f"   Chưa gắn nhãn: {len(df_unlabeled):,} samples")

# Predict
print(f"\n🤖 Predicting với model...")
X_unlabeled = df_unlabeled['text']
X_vec = vectorizer.transform(X_unlabeled)

# Predict với probability
y_pred = model.predict(X_vec)
y_proba = model.predict_proba(X_vec)

# Tính confidence (max probability)
confidence = y_proba.max(axis=1)

# Thêm vào dataframe
df_unlabeled['predicted_label'] = y_pred
df_unlabeled['confidence'] = confidence

# Sắp xếp theo confidence (thấp nhất = khó nhất)
df_uncertain = df_unlabeled.sort_values('confidence').head(1000)

print(f"\n📋 KẾT QUẢ:")
print(f"   Predicted distribution:")
print(df_unlabeled['predicted_label'].value_counts())

print(f"\n💡 ACTIVE LEARNING STRATEGY:")
print(f"   Model đã tự động gắn nhãn {len(df_unlabeled):,} samples")
print(f"   Nhưng có {len(df_uncertain)} samples có confidence THẤP (<0.6)")
print(f"\n   → BẠN CHỈ CẦN XEM LẠI {len(df_uncertain)} mẫu khó này!")

# Export uncertain samples
uncertain_file = f'labeling/uncertain_samples_to_review_{pd.Timestamp.now().strftime("%Y%m%d")}.csv'
export = df_uncertain[['id', 'text', 'topic', 'predicted_label', 'confidence']].copy()
export['corrected_label'] = None  # Bạn sửa ở đây nếu sai
export['notes'] = None

export.to_csv(uncertain_file, index=False, encoding='utf-8-sig')

print(f"\n💾 EXPORTED: {uncertain_file}")
print(f"   {len(export)} samples cần review")
print(f"\n📌 HƯỚNG DẪN:")
print(f"   1. Mở file {uncertain_file}")
print(f"   2. Kiểm tra cột 'predicted_label'")
print(f"   3. Nếu SAI: Ghi nhãn đúng vào 'corrected_label'")
print(f"   4. Nếu ĐÚNG: Để trống")
print(f"   5. Import lại để cập nhật model")

# Export auto-labeled (high confidence)
df_confident = df_unlabeled[df_unlabeled['confidence'] > 0.8].copy()
confident_file = f'labeling/auto_labeled_high_confidence_{pd.Timestamp.now().strftime("%Y%m%d")}.csv'
df_confident[['id', 'text', 'topic', 'predicted_label', 'confidence']].to_csv(
    confident_file, index=False, encoding='utf-8-sig'
)

print(f"\n✅ AUTO-LABELED (high confidence > 0.8): {confident_file}")
print(f"   {len(df_confident)} samples tự động gắn nhãn")

print("\n" + "="*80)
print("🎯 TIẾT KIỆM THỜI GIAN:")
print(f"   Tổng cần label: {len(df_unlabeled):,}")
print(f"   Model tự làm: {len(df_confident):,} ({len(df_confident)/len(df_unlabeled)*100:.1f}%)")
print(f"   Bạn chỉ cần review: {len(df_uncertain):,} ({len(df_uncertain)/len(df_unlabeled)*100:.1f}%)")
print("="*80)
