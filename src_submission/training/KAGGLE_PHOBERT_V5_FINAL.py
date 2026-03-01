"""
🔥 SafeSense-VI: PhoBERT Training V5 - KAGGLE VERSION
Vietnamese Toxic Comment Classification - IT Got Talent 2025

✅ Data Split: 80% Train / 10% Val / 10% Test
✅ Test Set độc lập cho đánh giá cuối cùng

📋 KAGGLE SETUP:
1. Upload dataset lên Kaggle Datasets
2. Add dataset vào notebook
3. Copy code này vào notebook và chạy
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 1: Install & Imports
# ═══════════════════════════════════════════════════════════════════════════════
import os
import random
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_cosine_schedule_with_warmup
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print('✅ Libraries imported!')
print(f'🔧 PyTorch: {torch.__version__}')
print(f'🔧 CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'🔧 GPU: {torch.cuda.get_device_name(0)}')

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 2: Configuration
# ═══════════════════════════════════════════════════════════════════════════════
class Config:
    MODEL_NAME = "vinai/phobert-base-v2"
    NUM_LABELS = 3
    MAX_LENGTH = 256
    BATCH_SIZE = 16
    GRADIENT_ACCUMULATION_STEPS = 2  # Effective batch = 32
    EPOCHS = 7
    LEARNING_RATE = 3e-5
    WEIGHT_DECAY = 0.01
    WARMUP_RATIO = 0.15
    USE_CLASS_WEIGHTS = True
    LABEL_SMOOTHING = 0.1
    PATIENCE = 2
    SEED = 42
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # ⚠️ KAGGLE PATHS - Thay đổi theo dataset của bạn
    DATA_PATH = "/kaggle/input/safesense-training-data/final_train_data_v3_READY_PHOBERT_SEGMENTED.csv"
    OUTPUT_DIR = "/kaggle/working/output"
    MODEL_SAVE_PATH = "/kaggle/working/phobert_toxic_v5"

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

set_seed(Config.SEED)
print(f'✅ Config set! Device: {Config.DEVICE}')

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 3: Dataset Class
# ═══════════════════════════════════════════════════════════════════════════════
class ToxicDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            str(self.texts[idx]),
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[idx], dtype=torch.long)
        }

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 4: Training Functions
# ═══════════════════════════════════════════════════════════════════════════════
def train_epoch(model, dataloader, optimizer, scheduler, criterion, device, accum_steps):
    model.train()
    total_loss = 0
    all_preds, all_labels = [], []
    pbar = tqdm(dataloader, desc="Training")
    optimizer.zero_grad()
    
    for step, batch in enumerate(pbar):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = criterion(outputs.logits, labels) / accum_steps
        loss.backward()
        total_loss += loss.item() * accum_steps
        
        preds = torch.argmax(outputs.logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        
        if (step + 1) % accum_steps == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
        
        pbar.set_postfix({'loss': f'{loss.item() * accum_steps:.4f}'})
    
    return total_loss/len(dataloader), f1_score(all_labels, all_preds, average='macro'), accuracy_score(all_labels, all_preds)

def evaluate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    all_preds, all_labels = [], []
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = criterion(outputs.logits, labels)
            total_loss += loss.item()
            
            preds = torch.argmax(outputs.logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    return total_loss/len(dataloader), f1_score(all_labels, all_preds, average='macro'), accuracy_score(all_labels, all_preds), all_preds, all_labels

print('✅ Functions defined!')


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 5: Load Data & Split 80/10/10
# ═══════════════════════════════════════════════════════════════════════════════
print("="*60)
print("📊 LOADING DATA & SPLITTING 80/10/10")
print("="*60)

# Check available files
import glob
print("\n📂 Available files in /kaggle/input:")
for f in glob.glob("/kaggle/input/**/*", recursive=True):
    if f.endswith(('.csv', '.xlsx')):
        print(f"   {f}")

# Load data
if Config.DATA_PATH.endswith('.xlsx'):
    df = pd.read_excel(Config.DATA_PATH)
else:
    df = pd.read_csv(Config.DATA_PATH)

print(f"\n📂 Loaded: {len(df):,} samples")

# Identify columns
text_col = 'training_text' if 'training_text' in df.columns else 'text'
label_col = 'label'
print(f"📝 Text column: {text_col}")

# Clean
df[label_col] = pd.to_numeric(df[label_col], errors='coerce')
df = df.dropna(subset=[text_col, label_col])
df[label_col] = df[label_col].astype(int)
print(f"📂 After cleaning: {len(df):,} samples")

X = df[text_col].values
y = df[label_col].values

# ⭐ SPLIT: 80% Train / 10% Val / 10% Test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.20, random_state=Config.SEED, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=Config.SEED, stratify=y_temp
)

print(f"\n{'='*50}")
print(f"📊 DATA SPLIT RESULTS:")
print(f"{'='*50}")
print(f"✅ Train: {len(X_train):,} samples ({len(X_train)/len(df)*100:.1f}%)")
print(f"✅ Val:   {len(X_val):,} samples ({len(X_val)/len(df)*100:.1f}%)")
print(f"✅ Test:  {len(X_test):,} samples ({len(X_test)/len(df)*100:.1f}%)")

# Label distribution per split
print(f"\n📊 Label distribution per split:")
for name, y_split in [("Train", y_train), ("Val", y_val), ("Test", y_test)]:
    dist = {l: (y_split == l).sum() for l in [0, 1, 2]}
    pct = {l: (y_split == l).sum() / len(y_split) * 100 for l in [0, 1, 2]}
    print(f"   {name}: Clean {dist[0]} ({pct[0]:.1f}%) | Off {dist[1]} ({pct[1]:.1f}%) | Hate {dist[2]} ({pct[2]:.1f}%)")

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 6: Create DataLoaders
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("📦 CREATING DATALOADERS")
print("="*60)

tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
print(f"✅ Tokenizer loaded: {Config.MODEL_NAME}")

train_dataset = ToxicDataset(X_train, y_train, tokenizer, Config.MAX_LENGTH)
val_dataset = ToxicDataset(X_val, y_val, tokenizer, Config.MAX_LENGTH)
test_dataset = ToxicDataset(X_test, y_test, tokenizer, Config.MAX_LENGTH)

train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)
val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE*2, shuffle=False, num_workers=2, pin_memory=True)
test_loader = DataLoader(test_dataset, batch_size=Config.BATCH_SIZE*2, shuffle=False, num_workers=2, pin_memory=True)

print(f"✅ Train batches: {len(train_loader)}")
print(f"✅ Val batches: {len(val_loader)}")
print(f"✅ Test batches: {len(test_loader)}")

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 7: Load Model & Setup
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("🤖 LOADING MODEL")
print("="*60)

model = AutoModelForSequenceClassification.from_pretrained(Config.MODEL_NAME, num_labels=Config.NUM_LABELS)
model.to(Config.DEVICE)
print(f"✅ Model loaded on {Config.DEVICE}")

# Class weights (from TRAIN set only!)
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights = torch.tensor(class_weights, dtype=torch.float).to(Config.DEVICE)
print(f"⚖️ Class weights: {[f'{w:.4f}' for w in class_weights.tolist()]}")

criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=Config.LABEL_SMOOTHING)
optimizer = torch.optim.AdamW(model.parameters(), lr=Config.LEARNING_RATE, weight_decay=Config.WEIGHT_DECAY)

total_steps = len(train_loader) * Config.EPOCHS // Config.GRADIENT_ACCUMULATION_STEPS
warmup_steps = int(total_steps * Config.WARMUP_RATIO)
scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_steps, num_training_steps=total_steps)

print(f"📈 Total steps: {total_steps} | Warmup: {warmup_steps}")

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 8: Training Loop
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("🚀 STARTING TRAINING")
print("="*60)

best_f1 = 0
patience_counter = 0
history = {'train_loss': [], 'val_loss': [], 'train_f1': [], 'val_f1': []}

for epoch in range(Config.EPOCHS):
    print(f"\n{'='*50}")
    print(f"📌 EPOCH {epoch + 1}/{Config.EPOCHS}")
    print(f"{'='*50}")
    
    train_loss, train_f1, train_acc = train_epoch(
        model, train_loader, optimizer, scheduler, criterion,
        Config.DEVICE, Config.GRADIENT_ACCUMULATION_STEPS
    )
    
    val_loss, val_f1, val_acc, _, _ = evaluate(model, val_loader, criterion, Config.DEVICE)
    
    history['train_loss'].append(train_loss)
    history['val_loss'].append(val_loss)
    history['train_f1'].append(train_f1)
    history['val_f1'].append(val_f1)
    
    print(f"\n📊 Results:")
    print(f"   Train - Loss: {train_loss:.4f} | F1: {train_f1:.4f} | Acc: {train_acc:.4f}")
    print(f"   Val   - Loss: {val_loss:.4f} | F1: {val_f1:.4f} | Acc: {val_acc:.4f}")
    
    if val_f1 > best_f1:
        best_f1 = val_f1
        patience_counter = 0
        os.makedirs(Config.MODEL_SAVE_PATH, exist_ok=True)
        model.save_pretrained(Config.MODEL_SAVE_PATH)
        tokenizer.save_pretrained(Config.MODEL_SAVE_PATH)
        print(f"   💾 Best model saved! (Val F1: {best_f1:.4f})")
    else:
        patience_counter += 1
        print(f"   ⏳ No improvement ({patience_counter}/{Config.PATIENCE})")
    
    if patience_counter >= Config.PATIENCE:
        print(f"\n⚠️ Early stopping!")
        break

print(f"\n{'='*60}")
print(f"✅ TRAINING COMPLETED!")
print(f"🏆 Best Validation F1: {best_f1:.4f}")
print(f"{'='*60}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 9: ⭐ FINAL EVALUATION ON TEST SET
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*60)
print("🎯 FINAL EVALUATION ON TEST SET")
print("   (Data NEVER seen during training!)")
print("="*60)

# Load best model
model = AutoModelForSequenceClassification.from_pretrained(Config.MODEL_SAVE_PATH)
model.to(Config.DEVICE)
print("✅ Best model loaded!")

# Evaluate on TEST set
test_loss, test_f1, test_acc, test_preds, test_labels = evaluate(model, test_loader, criterion, Config.DEVICE)

print(f"\n{'='*50}")
print(f"📊 TEST SET RESULTS (FINAL)")
print(f"{'='*50}")
print(f"   Loss:     {test_loss:.4f}")
print(f"   F1-Score: {test_f1:.4f}")
print(f"   Accuracy: {test_acc:.4f}")

# Classification Report
print(f"\n{'='*50}")
print("📋 CLASSIFICATION REPORT:")
print(f"{'='*50}")
target_names = ['Clean (0)', 'Offensive (1)', 'Hate (2)']
print(classification_report(test_labels, test_preds, target_names=target_names, digits=2))

# Confusion Matrix
cm = confusion_matrix(test_labels, test_preds)
print(f"\n📊 CONFUSION MATRIX:")
print(f"              Predicted")
print(f"           Clean  Off   Hate")
for i, label in enumerate(['Clean ', 'Off   ', 'Hate  ']):
    print(f"  {label}  {cm[i][0]:4d}  {cm[i][1]:4d}  {cm[i][2]:4d}")

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 10: Visualizations
# ═══════════════════════════════════════════════════════════════════════════════
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

# Confusion Matrix Plot
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Clean', 'Offensive', 'Hate'],
            yticklabels=['Clean', 'Offensive', 'Hate'],
            annot_kws={'size': 16})
plt.title('Confusion Matrix - TEST SET\n(Final Evaluation - IT Got Talent 2025)', fontsize=16, fontweight='bold')
plt.xlabel('Predicted', fontsize=14)
plt.ylabel('Actual', fontsize=14)
plt.tight_layout()
plt.savefig(f'{Config.OUTPUT_DIR}/confusion_matrix_test.png', dpi=300)
plt.show()

# Training History
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(range(1, len(history['train_loss'])+1), history['train_loss'], 'o-', label='Train', linewidth=2)
axes[0].plot(range(1, len(history['val_loss'])+1), history['val_loss'], 's-', label='Val', linewidth=2)
axes[0].set_xlabel('Epoch', fontsize=12)
axes[0].set_ylabel('Loss', fontsize=12)
axes[0].set_title('Training & Validation Loss', fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)

axes[1].plot(range(1, len(history['train_f1'])+1), history['train_f1'], 'o-', label='Train', linewidth=2)
axes[1].plot(range(1, len(history['val_f1'])+1), history['val_f1'], 's-', label='Val', linewidth=2)
axes[1].set_xlabel('Epoch', fontsize=12)
axes[1].set_ylabel('F1-Score (Macro)', fontsize=12)
axes[1].set_title('Training & Validation F1-Score', fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{Config.OUTPUT_DIR}/training_history.png', dpi=300)
plt.show()

print(f"\n💾 Visualizations saved to: {Config.OUTPUT_DIR}")

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 11: Save Results & Summary
# ═══════════════════════════════════════════════════════════════════════════════
import json

results = {
    'test_f1': float(test_f1),
    'test_accuracy': float(test_acc),
    'test_loss': float(test_loss),
    'best_val_f1': float(best_f1),
    'train_samples': int(len(X_train)),
    'val_samples': int(len(X_val)),
    'test_samples': int(len(X_test)),
    'total_samples': int(len(df)),
    'epochs_trained': len(history['train_loss']),
    'classification_report': classification_report(test_labels, test_preds, target_names=target_names, output_dict=True)
}

with open(f'{Config.OUTPUT_DIR}/results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*60)
print("🏆 TRAINING SUMMARY - IT GOT TALENT 2025")
print("="*60)
print(f"""
📊 DATA SPLIT (Chuẩn khoa học):
   ├─ Train: {len(X_train):,} samples (80%)
   ├─ Val:   {len(X_val):,} samples (10%) - Early stopping
   └─ Test:  {len(X_test):,} samples (10%) - Final evaluation

🎯 TEST SET RESULTS (Final - Chưa từng thấy khi training):
   ├─ F1-Score (Macro): {test_f1:.4f}
   ├─ Accuracy:         {test_acc:.4f}
   └─ Best Val F1:      {best_f1:.4f}

📁 OUTPUT FILES:
   ├─ Model: {Config.MODEL_SAVE_PATH}
   ├─ Results: {Config.OUTPUT_DIR}/results.json
   ├─ Confusion Matrix: {Config.OUTPUT_DIR}/confusion_matrix_test.png
   └─ Training History: {Config.OUTPUT_DIR}/training_history.png

✅ Ready for IT Got Talent 2025 presentation!
""")
print("="*60)

# Download model (optional)
print("\n📥 To download model, run:")
print(f"   from kaggle_secrets import UserSecretsClient")
print(f"   # Or use Kaggle Output to download")
