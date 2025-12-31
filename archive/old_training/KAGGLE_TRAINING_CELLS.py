"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔥 SafeSense-VI: PhoBERT-v2 Toxic Comment Classification                    ║
║  Complete Training Notebook for KAGGLE                                        ║
║                                                                               ║
║  Copy từng CELL vào Kaggle notebook                                           ║
║  Mỗi CELL được đánh dấu bằng: # ═══ CELL X: Title ═══                        ║
║                                                                               ║
║  KAGGLE SETUP:                                                                ║
║  1. Create new notebook                                                       ║
║  2. Settings → Accelerator → GPU T4 x2 hoặc P100                             ║
║  3. Add dataset: Upload file xlsx lên Kaggle Datasets                        ║
║  4. Internet: ON (để download model)                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 1: Install Dependencies (Kaggle)
# ═══════════════════════════════════════════════════════════════════════════════

# Kaggle đã có sẵn nhiều thư viện, chỉ cần install thêm transformers và underthesea
!pip install transformers accelerate underthesea -q

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
# CELL 3: Configuration (Kaggle optimized)
# ═══════════════════════════════════════════════════════════════════════════════

class Config:
    # Model
    MODEL_NAME = "vinai/phobert-base-v2"
    NUM_LABELS = 3
    MAX_LENGTH = 256
    
    # Training - Kaggle có GPU mạnh hơn, có thể tăng batch size
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
    
    # Kaggle Paths - QUAN TRỌNG: Thay đổi theo dataset của bạn
    # Khi upload dataset lên Kaggle, nó sẽ nằm trong /kaggle/input/[dataset-name]/
    DATA_PATH = "/kaggle/input/safesense-training-data/final_train_data_v3_TRUNCATED_20251229.xlsx"
    
    # Output path - Kaggle cho phép ghi vào /kaggle/working/
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
# CELL 4: Check Kaggle Input Data
# ═══════════════════════════════════════════════════════════════════════════════

# List all input datasets
print("📂 KAGGLE INPUT DATASETS:")
print("="*60)

input_path = "/kaggle/input"
if os.path.exists(input_path):
    for dataset in os.listdir(input_path):
        dataset_path = os.path.join(input_path, dataset)
        print(f"\n📁 {dataset}/")
        if os.path.isdir(dataset_path):
            for file in os.listdir(dataset_path):
                file_path = os.path.join(dataset_path, file)
                size = os.path.getsize(file_path) / 1024 / 1024  # MB
                print(f"   📄 {file} ({size:.2f} MB)")
else:
    print("⚠️ No input datasets found!")
    print("   Please add your dataset in Kaggle notebook settings")

# Auto-detect data file
print("\n🔍 AUTO-DETECTING DATA FILE...")
for dataset in os.listdir(input_path) if os.path.exists(input_path) else []:
    dataset_path = os.path.join(input_path, dataset)
    if os.path.isdir(dataset_path):
        for file in os.listdir(dataset_path):
            if file.endswith('.xlsx') or file.endswith('.csv'):
                Config.DATA_PATH = os.path.join(dataset_path, file)
                print(f"✅ Found: {Config.DATA_PATH}")
                break


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 5: Load & Explore Data
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("📊 LOADING & EXPLORING DATA")
print("="*80)

# Load data
if Config.DATA_PATH.endswith('.xlsx'):
    df = pd.read_excel(Config.DATA_PATH)
else:
    df = pd.read_csv(Config.DATA_PATH)
    
print(f"\n📂 Loaded: {len(df)} samples")
print(f"📂 Columns: {df.columns.tolist()}")

# Check for required columns
text_col = 'training_text' if 'training_text' in df.columns else 'text'
label_col = 'label'

print(f"\n📝 Text column: {text_col}")
print(f"📝 Label column: {label_col}")

# Basic stats
print(f"\n📊 DATASET STATISTICS:")
print(f"   Total samples: {len(df)}")
print(f"   Missing text: {df[text_col].isna().sum()}")
print(f"   Missing labels: {df[label_col].isna().sum()}")

# Label distribution
print(f"\n📊 LABEL DISTRIBUTION:")
label_counts = df[label_col].value_counts().sort_index()
label_names = {0: 'Clean', 1: 'Toxic', 2: 'Hate'}
for label, count in label_counts.items():
    pct = count / len(df) * 100
    print(f"   Label {int(label)} ({label_names.get(int(label), 'Unknown')}): {count} ({pct:.1f}%)")

# Balance ratio
balance_ratio = label_counts.max() / label_counts.min()
print(f"\n⚖️ Balance ratio: {balance_ratio:.2f}x")

# Text length analysis
df['text_length'] = df[text_col].astype(str).str.split().str.len()
print(f"\n📏 TEXT LENGTH:")
print(f"   Mean: {df['text_length'].mean():.1f} | Max: {df['text_length'].max()} | Min: {df['text_length'].min()}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 6: Visualize Data Distribution
# ═══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Label distribution
ax1 = axes[0]
colors = ['#2ecc71', '#e74c3c', '#9b59b6']
bars = ax1.bar(label_counts.index, label_counts.values, color=colors)
ax1.set_xlabel('Label')
ax1.set_ylabel('Count')
ax1.set_title('Label Distribution')
ax1.set_xticks([0, 1, 2])
ax1.set_xticklabels(['Clean (0)', 'Toxic (1)', 'Hate (2)'])

# Text length distribution
ax2 = axes[1]
ax2.hist(df['text_length'], bins=50, color='steelblue', edgecolor='white')
ax2.axvline(df['text_length'].mean(), color='red', linestyle='--', label=f'Mean: {df["text_length"].mean():.1f}')
ax2.set_xlabel('Text Length (words)')
ax2.set_ylabel('Count')
ax2.set_title('Text Length Distribution')
ax2.legend()

# Text length by label
ax3 = axes[2]
for label in sorted(df[label_col].unique()):
    subset = df[df[label_col] == label]['text_length']
    ax3.hist(subset, bins=30, alpha=0.5, label=f'Label {int(label)}')
ax3.set_xlabel('Text Length (words)')
ax3.set_ylabel('Count')
ax3.set_title('Text Length by Label')
ax3.legend()

plt.tight_layout()
plt.savefig(f'{Config.OUTPUT_DIR}/data_distribution.png', dpi=150)
plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 7: Prepare Data
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🔧 PREPARING DATA")
print("="*80)

# Extract texts and labels
texts = df[text_col].fillna('').astype(str).tolist()
labels = df[label_col].astype(int).tolist()

# Train/Val split (85/15)
train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels,
    test_size=0.15,
    random_state=Config.SEED,
    stratify=labels
)

print(f"📊 Train: {len(train_texts)} | Val: {len(val_texts)}")
print("✅ Data prepared!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 8: Load Tokenizer & Create Dataset (WITH WORD SEGMENTATION)
# ═══════════════════════════════════════════════════════════════════════════════

print("📥 Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
print(f"✅ Tokenizer loaded: {Config.MODEL_NAME}")

# Import word segmentation
from underthesea import word_tokenize

def segment_text(text):
    """Apply word segmentation for PhoBERT"""
    if not text or pd.isna(text):
        return ""
    try:
        # word_tokenize with format="text" returns segmented string
        # Example: "học sinh giỏi" → "học_sinh giỏi"
        return word_tokenize(str(text), format="text")
    except:
        return str(text)

print("✅ Word segmentation function loaded")

class ToxicDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length, use_segmentation=True):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.use_segmentation = use_segmentation
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        # Apply word segmentation BEFORE tokenization
        if self.use_segmentation:
            text = segment_text(text)
        
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

# Create datasets WITH word segmentation
train_dataset = ToxicDataset(train_texts, train_labels, tokenizer, Config.MAX_LENGTH, use_segmentation=True)
val_dataset = ToxicDataset(val_texts, val_labels, tokenizer, Config.MAX_LENGTH, use_segmentation=True)

print(f"✅ Train dataset: {len(train_dataset)} | Val dataset: {len(val_dataset)}")
print(f"✅ Word segmentation: ENABLED")

# Test segmentation
print(f"\n🔍 SEGMENTATION TEST:")
test_text = "học sinh giỏi bú fame"
segmented = segment_text(test_text)
print(f"   Original: {test_text}")
print(f"   Segmented: {segmented}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 9: Create DataLoaders & Class Weights
# ═══════════════════════════════════════════════════════════════════════════════

# DataLoaders - Set num_workers=0 to avoid multiprocessing issues in Kaggle notebook
train_loader = DataLoader(
    train_dataset,
    batch_size=Config.BATCH_SIZE,
    shuffle=True,
    num_workers=0,  # Must be 0 in Kaggle notebook to avoid multiprocessing errors
    pin_memory=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=Config.BATCH_SIZE * 2,
    shuffle=False,
    num_workers=0,  # Must be 0 in Kaggle notebook
    pin_memory=True
)

print(f"✅ Train batches: {len(train_loader)} | Val batches: {len(val_loader)}")

# Class weights
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
print("📥 LOADING MODEL & SETUP")
print("="*80)

# Load model
model = AutoModelForSequenceClassification.from_pretrained(
    Config.MODEL_NAME,
    num_labels=Config.NUM_LABELS
)
model.to(Config.DEVICE)

total_params = sum(p.numel() for p in model.parameters())
print(f"✅ Model loaded: {total_params:,} parameters")

# Loss function
criterion = nn.CrossEntropyLoss(
    weight=class_weights,
    label_smoothing=Config.LABEL_SMOOTHING
)

# Optimizer
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=Config.LEARNING_RATE,
    weight_decay=Config.WEIGHT_DECAY
)

# Scheduler
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
    
    # Train
    train_loss, train_f1 = train_epoch(
        model, train_loader, optimizer, scheduler, criterion,
        Config.DEVICE, Config.GRADIENT_ACCUMULATION_STEPS
    )
    
    # Evaluate
    val_metrics, val_preds, val_true, val_probs = eval_epoch(
        model, val_loader, criterion, Config.DEVICE
    )
    
    # Save history
    history['train_loss'].append(train_loss)
    history['train_f1'].append(train_f1)
    history['val_loss'].append(val_metrics['loss'])
    history['val_f1'].append(val_metrics['f1_macro'])
    history['val_accuracy'].append(val_metrics['accuracy'])
    
    # Print metrics
    print(f"\n📊 Train Loss: {train_loss:.4f} | Train F1: {train_f1:.4f}")
    print(f"📊 Val Loss: {val_metrics['loss']:.4f} | Val F1: {val_metrics['f1_macro']:.4f} | Val Acc: {val_metrics['accuracy']:.4f}")
    
    # Check improvement
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

# Load best model
if best_model_state:
    model.load_state_dict(best_model_state)

print(f"\n{'='*60}")
print(f"🏆 TRAINING COMPLETE! Best F1: {best_f1:.4f} at epoch {best_epoch}")
print(f"{'='*60}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 13: Plot Training History
# ═══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Loss
axes[0].plot(history['train_loss'], label='Train', marker='o')
axes[0].plot(history['val_loss'], label='Val', marker='s')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Loss')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# F1
axes[1].plot(history['train_f1'], label='Train', marker='o')
axes[1].plot(history['val_f1'], label='Val', marker='s')
axes[1].axhline(y=0.72, color='r', linestyle='--', label='Target')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('F1 (macro)')
axes[1].set_title('F1 Score')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Accuracy
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

# Confusion matrix
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
# CELL 15: Error Analysis
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🔍 ERROR ANALYSIS")
print("="*80)

error_df = pd.DataFrame({
    'text': val_texts,
    'true_label': final_true,
    'pred_label': final_preds
})
error_df['is_error'] = error_df['true_label'] != error_df['pred_label']
error_df['error_type'] = error_df.apply(
    lambda x: f"{x['true_label']}→{x['pred_label']}" if x['is_error'] else 'Correct', axis=1
)

total_errors = error_df['is_error'].sum()
print(f"\n📊 Errors: {total_errors} / {len(error_df)} ({total_errors/len(error_df)*100:.1f}%)")

print(f"\n📊 ERROR BREAKDOWN:")
for et, cnt in error_df[error_df['is_error']]['error_type'].value_counts().items():
    print(f"   {et}: {cnt}")

# Save errors
errors_only = error_df[error_df['is_error']]
errors_only.to_csv(f'{Config.OUTPUT_DIR}/model_errors.csv', index=False)
print(f"\n💾 Errors saved: {Config.OUTPUT_DIR}/model_errors.csv")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 16: Save Model (Kaggle Output)
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("💾 SAVING MODEL")
print("="*80)

os.makedirs(Config.MODEL_SAVE_PATH, exist_ok=True)

# Save model & tokenizer
model.save_pretrained(Config.MODEL_SAVE_PATH)
tokenizer.save_pretrained(Config.MODEL_SAVE_PATH)

# Save config
import json
config_dict = {
    'model_name': Config.MODEL_NAME,
    'num_labels': Config.NUM_LABELS,
    'max_length': Config.MAX_LENGTH,
    'best_f1': best_f1,
    'best_epoch': best_epoch,
    'final_metrics': final_metrics
}
with open(f'{Config.MODEL_SAVE_PATH}/training_config.json', 'w') as f:
    json.dump(config_dict, f, indent=2, default=str)

# Save history
pd.DataFrame(history).to_csv(f'{Config.MODEL_SAVE_PATH}/training_history.csv', index=False)

print(f"\n✅ Model saved to: {Config.MODEL_SAVE_PATH}")
print(f"   Files: pytorch_model.bin, config.json, tokenizer files")

# List output files
print(f"\n📁 OUTPUT FILES:")
for f in os.listdir(Config.OUTPUT_DIR):
    size = os.path.getsize(os.path.join(Config.OUTPUT_DIR, f)) / 1024 / 1024
    print(f"   {f} ({size:.2f} MB)")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 17: Test Inference (WITH WORD SEGMENTATION)
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🧪 TEST INFERENCE")
print("="*80)

def predict(text, model, tokenizer, device):
    model.eval()
    # Apply word segmentation before tokenization
    segmented_text = segment_text(text)
    encoding = tokenizer(segmented_text, max_length=Config.MAX_LENGTH, padding='max_length', 
                        truncation=True, return_tensors='pt')
    with torch.no_grad():
        outputs = model(encoding['input_ids'].to(device), encoding['attention_mask'].to(device))
        probs = torch.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    return pred, probs[0].cpu().numpy(), segmented_text

test_samples = [
    "video hay quá, cảm ơn bạn",
    "thằng ngu, mày biết gì",
    "đồ con chó, cút đi",
    "sản phẩm chất vcl",
    "bọn bắc kỳ toàn lừa đảo",
    "học sinh giỏi bú fame"
]

label_names = ['Clean', 'Toxic', 'Hate']
print("\n🔮 PREDICTIONS:")
for text in test_samples:
    pred, probs, segmented = predict(text, model, tokenizer, Config.DEVICE)
    print(f"\n📝 Original: {text}")
    print(f"   Segmented: {segmented}")
    print(f"   → {label_names[pred]} ({probs[pred]:.2%})")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 18: Summary
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("🏆 TRAINING SUMMARY")
print("="*80)

print(f"""
📊 DATASET: {len(texts)} samples (Train: {len(train_texts)} | Val: {len(val_texts)})

🔧 MODEL: {Config.MODEL_NAME}
   Parameters: {total_params:,}
   Max Length: {Config.MAX_LENGTH}

📈 TRAINING:
   Epochs: {len(history['train_loss'])} (best at {best_epoch})
   Batch: {Config.BATCH_SIZE} x {Config.GRADIENT_ACCUMULATION_STEPS}

🎯 RESULTS:
   Best F1 (macro): {best_f1:.4f}
   Final Accuracy: {final_metrics['accuracy']:.4f}
   Errors: {total_errors} ({total_errors/len(error_df)*100:.1f}%)

💾 OUTPUT: {Config.OUTPUT_DIR}
   - phobert_toxic_model/
   - training_history.png
   - confusion_matrix.png
   - model_errors.csv

{'✅ TARGET ACHIEVED!' if best_f1 >= 0.72 else '⚠️ Target (0.72) not reached'}
""")

print("="*80)
print("✅ NOTEBOOK COMPLETE!")
print("="*80)
print("\n📥 To download model: Click 'Output' tab → Download files")
