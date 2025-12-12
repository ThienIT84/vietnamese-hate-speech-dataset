"""
Script train baseline model với 500 samples đã gắn nhãn
Sử dụng: Logistic Regression hoặc Random Forest
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

print("="*80)
print("🤖 TRAIN BASELINE MODEL - TOXIC COMMENT CLASSIFICATION")
print("="*80)

# Đọc data đã gắn nhãn
labeled_file = input("Nhập tên file đã gắn nhãn (vd: dataset_labeled_tran_20251127.csv): ")
df = pd.read_csv(f'labeling/{labeled_file}')

# Lọc những mẫu đã gắn nhãn
df = df[df['label'].notna()].copy()

print(f"\n📊 DỮ LIỆU:")
print(f"   Tổng samples đã gắn nhãn: {len(df)}")
print(f"\n   Phân bố nhãn:")
print(df['label'].value_counts())

# Kiểm tra minimum samples per class
min_samples = df['label'].value_counts().min()
if min_samples < 10:
    print(f"\n⚠️  WARNING: Nhãn '{df['label'].value_counts().idxmin()}' chỉ có {min_samples} samples!")
    print("   Nên có ít nhất 20 samples/nhãn để train tốt")
    cont = input("\n   Tiếp tục? (y/n): ")
    if cont.lower() != 'y':
        exit()

# Chuẩn bị data
X = df['text']
y = df['label']

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n📊 SPLIT DATA:")
print(f"   Train: {len(X_train)} samples")
print(f"   Test: {len(X_test)} samples")

# Vectorization
print(f"\n🔄 VECTORIZING TEXT...")
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
print(f"\n🤖 TRAINING MODEL...")
print("   Model: Logistic Regression")

model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
model.fit(X_train_vec, y_train)

# Evaluate
print(f"\n📈 EVALUATION:")
y_pred = model.predict(X_test_vec)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Accuracy per class
from sklearn.metrics import accuracy_score
acc = accuracy_score(y_test, y_pred)
print(f"\n✅ Overall Accuracy: {acc:.2%}")

# Save model
model_file = 'models/baseline_model.pkl'
vectorizer_file = 'models/baseline_vectorizer.pkl'

import os
os.makedirs('models', exist_ok=True)

joblib.dump(model, model_file)
joblib.dump(vectorizer, vectorizer_file)

print(f"\n💾 SAVED MODEL:")
print(f"   Model: {model_file}")
print(f"   Vectorizer: {vectorizer_file}")

print("\n" + "="*80)
print("✅ HOÀN TẤT! Model baseline đã sẵn sàng")
print("="*80)
print("\n💡 BƯỚC TIẾP THEO:")
print("   1. Nếu accuracy < 60%: Gắn thêm 500 samples nữa")
print("   2. Nếu accuracy 60-80%: Tiếp tục gắn đến 2,000 samples")
print("   3. Nếu accuracy > 80%: Chuyển sang active learning")
print("="*80)
