"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔥 SafeSense-VI: PhoBERT-v2 Toxic Comment Classification                    ║
║  Complete Training Notebook for KAGGLE - VERSION 2                           ║
║                                                                               ║
║  📌 DATA: final_train_data_v3_READY.xlsx (ĐÃ SEGMENT SẴN!)                   ║
║  📌 KHÔNG CẦN segment trong training vì data đã được xử lý                   ║
║                                                                               ║
║  Copy từng CELL vào Kaggle notebook                                           ║
║  Mỗi CELL được đánh dấu bằng: # ═══ CELL X: Title ═══                        ║
║                                                                               ║
║  KAGGLE SETUP:                                                                ║
║  1. Create new notebook                                                       ║
║  2. Settings → Accelerator → GPU T4 x2 hoặc P100                             ║
║  3. Add dataset: Upload file final_train_data_v3_READY.xlsx                  ║
║  4. Internet: ON (để download model)                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 1: Install Dependencies
# ═══════════════════════════════════════════════════════════════════════════════

!pip install transformers accelerate -q

import torch
print(f'✅ PyTorch: {torch.__version__}')
print(f'✅ CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'✅ GPU: {torch.cuda.get_device_name(0)}')
    print(f'✅ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 2: Import Libraries
# ═══════════════════════════════════════════════════════════════════════════════

import os
import random
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    get_cosine_schedule_with_warmup
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    f1_score, accuracy_score, precision_score, recall_score,
    classification_report, confusion_matrix
)
from sklearn.utils.class_weight import compute_class_weight
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print('✅ All libraries imported!')


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 3: Configuration
# ═══════════════════════════════════════════════════════════════════════════════

class Config:
    # Model
    MODEL_NAME = "vinai/phobert-base-v2"
    NUM_LABELS = 3
    MAX_LENGTH = 256
    
    # Training
    BATCH_SIZE = 16
    GRADIENT_ACCUMULATION_STEPS = 2  # Effective batch = 32
    EPOCHS = 5
    LEARNING_RATE = 2e-5
    WEIGHT_DECAY = 0.01
    WARMUP_RATIO = 0.1
    
    # Optimization
    USE_CLASS_WEIGHTS = True
    LABEL_SMOOTHING = 0.1
    
    # Early stopping
    PATIENCE = 2
    
    # Seed
    SEED = 42
    
    # Device
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Kaggle Paths
    DATA_PATH = "/kaggle/input/safesense-training-data/final_train_data_v3_READY.xlsx"
    OUTPUT_DIR = "/kaggle/working"
    MODEL_SAVE_PATH = "/kaggle/working/phobert_toxic_model"

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

set_seed(Config.SEED)

print('✅ Configuration set!')
print(f'🔧 Device: {Config.DEVICE}')
print(f'🔧 Model: {Config.MODEL_NAME}')
print(f'🔧 Batch Size: {Config.BATCH_SIZE} x {Config.GRADIENT_ACCUMULATION_STEPS} = {Config.BATCH_SIZE * Config.GRADIENT_ACCUMULATION_STEPS}')


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 4: Find & Load Data
# ═══════════════════════════════════════════════════════════════════════════════

print("📂 FINDING DATA FILE...")
print("="*60)

input_path = "/kaggle/input"
data_path = None

if os.path.exists(input_path):
    for dataset in os.listdir(input_path):
        dataset_path = os.path.join(input_path, dataset)
        print(f"\n📁 {dataset}/")
        if os.path.isdir(dataset_path):
            for file in os.listdir(dataset_path):
                file_path = os.path.join(dataset_path, file)
                size = os.path.getsize(file_path) / 1024 / 1024
                print(f"   📄 {file} ({size:.2f} MB)")
                if 'READY' in file and file.endswith('.xlsx'):
                    data_path = file_path
                elif file.endswith('.xlsx') and data_path is None:
                    data_path = file_path

if data_path:
    Config.DATA_PATH = data_path
    print(f"\n✅ Using: {data_path}")
else:
    print("❌ No data file found!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 5: Load & Explore Data
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("📊 LOADING DATA")
print("="*80)

if Config.DATA_PATH.endswith('.xlsx'):
    df = pd.read_excel(Config.DATA_PATH)
else:
    df = pd.read_csv(Config.DATA_PATH)
    
print(f"\n📂 Loaded: {len(df)} samples")
print(f"📂 Columns: {df.columns.tolist()}")

text_col = 'training_text' if 'training_text' in df.columns else 'text'
label_col = 'label'

print(f"\n📝 Text column: {text_col}")
print(f"📝 Label column: {label_col}")

# Check word segmentation
sample_text = df[text_col].iloc[0]
underscore_count = str(sample_text).count('_')
print(f"\n🔍 WORD SEGMENTATION CHECK:")
print(f"   Sample text: {str(sample_text)[:100]}...")
print(f"   Underscores (compound words): {underscore_count}")
if underscore_count > 0:
    print(f"   ✅ Data is PRE-SEGMENTED! No need to segment during training.")
else:
    print(f"   ⚠️ Data may not be segmented!")

# Label distribution
print(f"\n📊 LABEL DISTRIBUTION:")
label_counts = df[label_col].value_counts().sort_index()
label_names = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}
for label, count in label_counts.items():
    pct = count / len(df) * 100
    print(f"   Label {int(label)} ({label_names.get(int(label), 'Unknown')}): {count} ({pct:.1f}%)")

balance_ratio = label_counts.max() / label_counts.min()
print(f"\n⚖️ Balance ratio: {balance_ratio:.2f}x")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 6: Visualize Data
# ═══════════════════════════════════════════════════════════════════════════════

df['text_length'] = df[text_col].astype(str).str.split().str.len()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

colors = ['#2ecc71', '#e74c3c', '#9b59b6']
axes[0].bar(label_counts.index, label_counts.values, color=colors)
axes[0].set_xlabel('Label')
axes[0].set_ylabel('Count')
axes[0].set_title('Label Distribution')
axes[0].set_xticks([0, 1, 2])
axes[0].set_xticklabels(['Clean (0)', 'Toxic (1)', 'Hate (2)'])

axes[1].hist(df['text_length'], bins=50, color='steelblue', edgecolor='white')
axes[1].axvline(df['text_length'].mean(), color='red', linestyle='--', label=f'Mean: {df["text_length"].mean():.1f}')
axes[1].set_xlabel('Text Length (words)')
axes[1].set_ylabel('Count')
axes[1].set_title('Text Length Distribution')
axes[1].legend()

for label in sorted(df[label_col].unique()):
    subset = df[df[label_col] == label]['text_length']
    axes[2].hist(subset, bins=30, alpha=0.5, label=f'Label {int(label)}')
axes[2].set_xlabel('Text Length (words)')
axes[2].set_ylabel('Count')
axes[2].set_title('Text Length by Label')
axes[2].legend()

plt.tight_layout()
plt.savefig(f'{Config.OUTPUT_DIR}/data_distribution.png', dpi=150)
plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 7: Prepare Data
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🔧 PREPARING DATA")
print("="*80)

texts = df[text_col].fillna('').astype(str).tolist()
labels = df[label_col].astype(int).tolist()

train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels,
    test_size=0.15,
    random_state=Config.SEED,
    stratify=labels
)

print(f"📊 Train: {len(train_texts)} | Val: {len(val_texts)}")
print("✅ Data prepared!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 8: Load Tokenizer & Create Dataset (NO SEGMENTATION NEEDED!)
# ═══════════════════════════════════════════════════════════════════════════════

print("📥 Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
print(f"✅ Tokenizer loaded: {Config.MODEL_NAME}")

# NOTE: Data đã được segment sẵn trong file READY
# KHÔNG CẦN segment trong Dataset class!

class ToxicDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        # Text đã được segment sẵn, chỉ cần tokenize
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

train_dataset = ToxicDataset(train_texts, train_labels, tokenizer, Config.MAX_LENGTH)
val_dataset = ToxicDataset(val_texts, val_labels, tokenizer, Config.MAX_LENGTH)

print(f"✅ Train dataset: {len(train_dataset)} | Val dataset: {len(val_dataset)}")
print(f"✅ Word segmentation: PRE-APPLIED (no runtime segmentation needed)")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 9: Create DataLoaders & Class Weights
# ═══════════════════════════════════════════════════════════════════════════════

# DataLoaders - num_workers=0 để tránh lỗi multiprocessing trên Kaggle
train_loader = DataLoader(
    train_dataset,
    batch_size=Config.BATCH_SIZE,
    shuffle=True,
    num_workers=0,
    pin_memory=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=Config.BATCH_SIZE * 2,
    shuffle=False,
    num_workers=0,
    pin_memory=True
)

print(f"✅ Train batches: {len(train_loader)} | Val batches: {len(val_loader)}")

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.array([0, 1, 2]),
    y=train_labels
)
class_weights = torch.tensor(class_weights, dtype=torch.float).to(Config.DEVICE)

print(f"⚖️ Class weights: {class_weights.cpu().numpy()}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 10: Load Model & Setup Training
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("📥 LOADING MODEL")
print("="*80)

model = AutoModelForSequenceClassification.from_pretrained(
    Config.MODEL_NAME,
    num_labels=Config.NUM_LABELS
)
model.to(Config.DEVICE)

total_params = sum(p.numel() for p in model.parameters())
print(f"✅ Model loaded: {total_params:,} parameters")

criterion = nn.CrossEntropyLoss(
    weight=class_weights,
    label_smoothing=Config.LABEL_SMOOTHING
)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=Config.LEARNING_RATE,
    weight_decay=Config.WEIGHT_DECAY
)

total_steps = len(train_loader) * Config.EPOCHS // Config.GRADIENT_ACCUMULATION_STEPS
warmup_steps = int(total_steps * Config.WARMUP_RATIO)

scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=warmup_steps,
    num_training_steps=total_steps
)

print(f"✅ Optimizer: AdamW (lr={Config.LEARNING_RATE})")
print(f"✅ Scheduler: Cosine warmup ({warmup_steps}/{total_steps} steps)")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 11: Training Functions
# ═══════════════════════════════════════════════════════════════════════════════

def train_epoch(model, dataloader, optimizer, scheduler, criterion, device, accumulation_steps):
    model.train()
    total_loss = 0
    all_preds, all_labels = [], []
    
    progress_bar = tqdm(dataloader, desc="Training", leave=False)
    optimizer.zero_grad()
    
    for step, batch in enumerate(progress_bar):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        loss = criterion(outputs.logits, labels) / accumulation_steps
        loss.backward()
        
        if (step + 1) % accumulation_steps == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
        
        total_loss += loss.item() * accumulation_steps
        preds = torch.argmax(outputs.logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        
        progress_bar.set_postfix({'loss': f'{loss.item() * accumulation_steps:.4f}'})
    
    return total_loss / len(dataloader), f1_score(all_labels, all_preds, average='macro')


def eval_epoch(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    all_preds, all_labels, all_probs = [], [], []
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating", leave=False):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            loss = criterion(outputs.logits, labels)
            
            total_loss += loss.item()
            probs = torch.softmax(outputs.logits, dim=1)
            preds = torch.argmax(probs, dim=1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    
    metrics = {
        'loss': total_loss / len(dataloader),
        'f1_macro': f1_score(all_labels, all_preds, average='macro'),
        'f1_weighted': f1_score(all_labels, all_preds, average='weighted'),
        'accuracy': accuracy_score(all_labels, all_preds),
        'precision': precision_score(all_labels, all_preds, average='macro'),
        'recall': recall_score(all_labels, all_preds, average='macro')
    }
    
    return metrics, all_preds, all_labels, all_probs

print("✅ Training functions defined!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 12: Training Loop
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🏋️ STARTING TRAINING")
print("="*80)

history = {'train_loss': [], 'train_f1': [], 'val_loss': [], 'val_f1': [], 'val_accuracy': []}
best_f1 = 0
best_epoch = 0
patience_counter = 0
best_model_state = None

for epoch in range(Config.EPOCHS):
    print(f"\n{'='*60}")
    print(f"📅 Epoch {epoch + 1}/{Config.EPOCHS}")
    print(f"{'='*60}")
    
    train_loss, train_f1 = train_epoch(
        model, train_loader, optimizer, scheduler, criterion,
        Config.DEVICE, Config.GRADIENT_ACCUMULATION_STEPS
    )
    
    val_metrics, val_preds, val_true, val_probs = eval_epoch(
        model, val_loader, criterion, Config.DEVICE
    )
    
    history['train_loss'].append(train_loss)
    history['train_f1'].append(train_f1)
    history['val_loss'].append(val_metrics['loss'])
    history['val_f1'].append(val_metrics['f1_macro'])
    history['val_accuracy'].append(val_metrics['accuracy'])
    
    print(f"\n📊 Train Loss: {train_loss:.4f} | Train F1: {train_f1:.4f}")
    print(f"📊 Val Loss: {val_metrics['loss']:.4f} | Val F1: {val_metrics['f1_macro']:.4f} | Val Acc: {val_metrics['accuracy']:.4f}")
    
    if val_metrics['f1_macro'] > best_f1:
        best_f1 = val_metrics['f1_macro']
        best_epoch = epoch + 1
        patience_counter = 0
        best_model_state = model.state_dict().copy()
        print(f"✅ New best F1: {best_f1:.4f}")
    else:
        patience_counter += 1
        print(f"⚠️ No improvement. Patience: {patience_counter}/{Config.PATIENCE}")
    
    if patience_counter >= Config.PATIENCE:
        print(f"\n🛑 Early stopping at epoch {epoch + 1}")
        break

if best_model_state:
    model.load_state_dict(best_model_state)

print(f"\n{'='*60}")
print(f"🏆 TRAINING COMPLETE! Best F1: {best_f1:.4f} at epoch {best_epoch}")
print(f"{'='*60}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 13: Plot Training History
# ═══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].plot(history['train_loss'], label='Train', marker='o')
axes[0].plot(history['val_loss'], label='Val', marker='s')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Loss')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(history['train_f1'], label='Train', marker='o')
axes[1].plot(history['val_f1'], label='Val', marker='s')
axes[1].axhline(y=0.72, color='r', linestyle='--', label='Target')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('F1 (macro)')
axes[1].set_title('F1 Score')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

axes[2].plot(history['val_accuracy'], label='Val', marker='s', color='green')
axes[2].set_xlabel('Epoch')
axes[2].set_ylabel('Accuracy')
axes[2].set_title('Accuracy')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{Config.OUTPUT_DIR}/training_history.png', dpi=150)
plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 14: Final Evaluation & Confusion Matrix
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("📊 FINAL EVALUATION")
print("="*80)

final_metrics, final_preds, final_true, final_probs = eval_epoch(
    model, val_loader, criterion, Config.DEVICE
)

print(f"\n🎯 FINAL METRICS:")
print(f"   F1 (macro): {final_metrics['f1_macro']:.4f}")
print(f"   F1 (weighted): {final_metrics['f1_weighted']:.4f}")
print(f"   Accuracy: {final_metrics['accuracy']:.4f}")
print(f"   Precision: {final_metrics['precision']:.4f}")
print(f"   Recall: {final_metrics['recall']:.4f}")

print(f"\n📋 CLASSIFICATION REPORT:")
print(classification_report(final_true, final_preds, target_names=['Clean', 'Toxic', 'Hate']))

cm = confusion_matrix(final_true, final_preds)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Clean', 'Toxic', 'Hate'],
            yticklabels=['Clean', 'Toxic', 'Hate'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.savefig(f'{Config.OUTPUT_DIR}/confusion_matrix.png', dpi=150)
plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 15: Error Analysis & Export
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🔍 ERROR ANALYSIS")
print("="*80)

label_names_map = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}

error_data = []
for i, (text, true_label, pred_label, probs) in enumerate(zip(val_texts, final_true, final_preds, final_probs)):
    is_error = true_label != pred_label
    error_data.append({
        'id': i + 1,
        'text': text,
        'true_label': int(true_label),
        'true_label_name': label_names_map[int(true_label)],
        'pred_label': int(pred_label),
        'pred_label_name': label_names_map[int(pred_label)],
        'is_error': is_error,
        'error_type': f"{int(true_label)}→{int(pred_label)}" if is_error else 'Correct',
        'confidence': float(probs[pred_label]),
        'conf_clean': float(probs[0]),
        'conf_toxic': float(probs[1]),
        'conf_hate': float(probs[2])
    })

df_results = pd.DataFrame(error_data)
df_errors = df_results[df_results['is_error'] == True].copy()

total_errors = len(df_errors)
print(f"\n📊 Errors: {total_errors} / {len(df_results)} ({total_errors/len(df_results)*100:.1f}%)")

print(f"\n📊 ERROR BREAKDOWN:")
for et, cnt in df_errors['error_type'].value_counts().items():
    print(f"   {et}: {cnt}")

# Save errors to Excel
error_file = f'{Config.OUTPUT_DIR}/model_errors.xlsx'
df_errors.to_excel(error_file, index=False)
print(f"\n💾 Errors saved: {error_file}")

# Show top errors
print(f"\n🔥 TOP 10 HIGH-CONFIDENCE ERRORS:")
high_conf_errors = df_errors.sort_values('confidence', ascending=False).head(10)
for idx, row in high_conf_errors.iterrows():
    print(f"\n[{row['error_type']}] Conf: {row['confidence']:.2%}")
    print(f"   {row['text'][:80]}...")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 16: Save Model
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("💾 SAVING MODEL")
print("="*80)

os.makedirs(Config.MODEL_SAVE_PATH, exist_ok=True)

model.save_pretrained(Config.MODEL_SAVE_PATH)
tokenizer.save_pretrained(Config.MODEL_SAVE_PATH)

import json
config_dict = {
    'model_name': Config.MODEL_NAME,
    'num_labels': Config.NUM_LABELS,
    'max_length': Config.MAX_LENGTH,
    'best_f1': best_f1,
    'best_epoch': best_epoch,
    'final_metrics': final_metrics,
    'data_file': Config.DATA_PATH,
    'word_segmentation': 'PRE-APPLIED'
}
with open(f'{Config.MODEL_SAVE_PATH}/training_config.json', 'w') as f:
    json.dump(config_dict, f, indent=2, default=str)

pd.DataFrame(history).to_csv(f'{Config.MODEL_SAVE_PATH}/training_history.csv', index=False)

print(f"\n✅ Model saved to: {Config.MODEL_SAVE_PATH}")

print(f"\n📁 OUTPUT FILES:")
for f in os.listdir(Config.OUTPUT_DIR):
    fpath = os.path.join(Config.OUTPUT_DIR, f)
    if os.path.isfile(fpath):
        size = os.path.getsize(fpath) / 1024 / 1024
        print(f"   {f} ({size:.2f} MB)")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 17: Test Inference
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🧪 TEST INFERENCE")
print("="*80)

# NOTE: Khi inference với text MỚI, cần segment trước!
# Nhưng với test samples đơn giản, có thể bỏ qua

def predict(text, model, tokenizer, device):
    model.eval()
    encoding = tokenizer(text, max_length=Config.MAX_LENGTH, padding='max_length', 
                        truncation=True, return_tensors='pt')
    with torch.no_grad():
        outputs = model(encoding['input_ids'].to(device), encoding['attention_mask'].to(device))
        probs = torch.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    return pred, probs[0].cpu().numpy()

test_samples = [
    "video hay quá, cảm_ơn bạn",
    "thằng ngu, mày biết gì",
    "đồ con chó, cút đi",
    "sản_phẩm chất vcl",
    "bọn bắc_kỳ toàn lừa_đảo",
    "học_sinh giỏi bú_fame"
]

label_names_list = ['Clean', 'Toxic', 'Hate']
print("\n🔮 PREDICTIONS:")
for text in test_samples:
    pred, probs = predict(text, model, tokenizer, Config.DEVICE)
    print(f"\n📝 {text}")
    print(f"   → {label_names_list[pred]} ({probs[pred]:.2%})")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 18: Summary
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("🏆 TRAINING SUMMARY")
print("="*80)

print(f"""
📊 DATASET: {len(texts)} samples (Train: {len(train_texts)} | Val: {len(val_texts)})
   Word Segmentation: PRE-APPLIED ✅

🔧 MODEL: {Config.MODEL_NAME}
   Parameters: {total_params:,}
   Max Length: {Config.MAX_LENGTH}

📈 TRAINING:
   Epochs: {len(history['train_loss'])} (best at {best_epoch})
   Batch: {Config.BATCH_SIZE} x {Config.GRADIENT_ACCUMULATION_STEPS}

🎯 RESULTS:
   Best F1 (macro): {best_f1:.4f}
   Final Accuracy: {final_metrics['accuracy']:.4f}
   Errors: {total_errors} ({total_errors/len(df_results)*100:.1f}%)

💾 OUTPUT: {Config.OUTPUT_DIR}
   - phobert_toxic_model/
   - training_history.png
   - confusion_matrix.png
   - model_errors.xlsx

{'✅ TARGET ACHIEVED!' if best_f1 >= 0.72 else '⚠️ Target (0.72) not reached'}
""")

print("="*80)
print("✅ NOTEBOOK COMPLETE!")
print("="*80)
print("\n📥 To download model: Click 'Output' tab → Download files")
print("\n⚠️ LƯU Ý: Khi inference với text MỚI, cần segment trước bằng underthesea!")
print("   from underthesea import word_tokenize")
print("   segmented_text = word_tokenize(text, format='text')")
