"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔥 SafeSense-VI: PhoBERT-v2 Toxic Comment Classification                    ║
║  Complete Training Notebook for Google Colab                                  ║
║                                                                               ║
║  Copy từng CELL vào Google Colab notebook                                     ║
║  Mỗi CELL được đánh dấu bằng: # ═══ CELL X: Title ═══                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 1: Mount Google Drive & Install Dependencies
# ═══════════════════════════════════════════════════════════════════════════════

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Install dependencies
!pip install transformers datasets accelerate -q
!pip install scikit-learn pandas openpyxl -q

print('✅ Dependencies installed!')


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

print('✅ Libraries imported!')
print(f'🔧 PyTorch version: {torch.__version__}')
print(f'🔧 CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'🔧 GPU: {torch.cuda.get_device_name(0)}')


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
    
    # Paths
    DATA_PATH = "/content/final_train_data_v3_TRUNCATED_20251229.xlsx"
    MODEL_SAVE_PATH = "/content/drive/MyDrive/phobert_toxic_model"

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
print(f'🔧 Max Length: {Config.MAX_LENGTH}')
print(f'🔧 Batch Size: {Config.BATCH_SIZE} x {Config.GRADIENT_ACCUMULATION_STEPS} = {Config.BATCH_SIZE * Config.GRADIENT_ACCUMULATION_STEPS}')


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 4: Upload Data File
# ═══════════════════════════════════════════════════════════════════════════════

# Option 1: Upload from local machine
from google.colab import files
print("📂 Please upload: final_train_data_v3_TRUNCATED_20251229.xlsx")
uploaded = files.upload()

# Move to content folder
import shutil
for filename in uploaded.keys():
    if filename.endswith('.xlsx'):
        Config.DATA_PATH = f"/content/{filename}"
        print(f"✅ File uploaded: {Config.DATA_PATH}")

# Option 2: If file is already in Google Drive, uncomment below:
# Config.DATA_PATH = "/content/drive/MyDrive/your_folder/final_train_data_v3_TRUNCATED_20251229.xlsx"


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 5: Load & Explore Data
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("📊 LOADING & EXPLORING DATA")
print("="*80)

# Load data
df = pd.read_excel(Config.DATA_PATH)
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
if balance_ratio < 2.0:
    print("   ✅ Good balance!")
elif balance_ratio < 3.0:
    print("   ⚠️ Moderate imbalance - using class weights")
else:
    print("   🚨 High imbalance - consider focal loss")

# Text length analysis
df['text_length'] = df[text_col].astype(str).str.split().str.len()
print(f"\n📏 TEXT LENGTH STATISTICS:")
print(f"   Mean: {df['text_length'].mean():.1f} words")
print(f"   Max: {df['text_length'].max()} words")
print(f"   Min: {df['text_length'].min()} words")
print(f"   Median: {df['text_length'].median():.1f} words")


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
for bar, count in zip(bars, label_counts.values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
             f'{count}', ha='center', va='bottom', fontsize=10)

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
plt.show()

print("✅ Visualization complete!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 7: Prepare Data
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🔧 PREPARING DATA")
print("="*80)

# Extract texts and labels
texts = df[text_col].fillna('').astype(str).tolist()
labels = df[label_col].astype(int).tolist()

print(f"\n📊 Total samples: {len(texts)}")

# Train/Val split (85/15)
train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts, labels,
    test_size=0.15,
    random_state=Config.SEED,
    stratify=labels
)

print(f"📊 Train size: {len(train_texts)} ({len(train_texts)/len(texts)*100:.1f}%)")
print(f"📊 Val size: {len(val_texts)} ({len(val_texts)/len(texts)*100:.1f}%)")

# Check stratification
print(f"\n📊 Train label distribution:")
train_label_counts = pd.Series(train_labels).value_counts().sort_index()
for label, count in train_label_counts.items():
    print(f"   Label {label}: {count} ({count/len(train_labels)*100:.1f}%)")

print(f"\n📊 Val label distribution:")
val_label_counts = pd.Series(val_labels).value_counts().sort_index()
for label, count in val_label_counts.items():
    print(f"   Label {label}: {count} ({count/len(val_labels)*100:.1f}%)")

print("\n✅ Data prepared!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 8: Load Tokenizer
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("📥 LOADING TOKENIZER")
print("="*80)

tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)

print(f"✅ Tokenizer loaded: {Config.MODEL_NAME}")
print(f"📝 Vocab size: {tokenizer.vocab_size}")

# Test tokenization
test_text = "video hay vcl, chất vl luôn </s> đỉnh quá"
tokens = tokenizer.tokenize(test_text)
print(f"\n🧪 Test tokenization:")
print(f"   Input: {test_text}")
print(f"   Tokens: {tokens[:20]}...")
print(f"   Token count: {len(tokens)}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 9: Create Dataset Class
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
        text = str(self.texts[idx])
        label = self.labels[idx]
        
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

# Create datasets
train_dataset = ToxicDataset(train_texts, train_labels, tokenizer, Config.MAX_LENGTH)
val_dataset = ToxicDataset(val_texts, val_labels, tokenizer, Config.MAX_LENGTH)

print(f"✅ Datasets created!")
print(f"   Train dataset: {len(train_dataset)} samples")
print(f"   Val dataset: {len(val_dataset)} samples")

# Test dataset
sample = train_dataset[0]
print(f"\n🧪 Sample check:")
print(f"   input_ids shape: {sample['input_ids'].shape}")
print(f"   attention_mask shape: {sample['attention_mask'].shape}")
print(f"   label: {sample['labels']}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 10: Create DataLoaders
# ═══════════════════════════════════════════════════════════════════════════════

train_loader = DataLoader(
    train_dataset,
    batch_size=Config.BATCH_SIZE,
    shuffle=True,
    num_workers=2,
    pin_memory=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=Config.BATCH_SIZE * 2,  # Larger batch for validation
    shuffle=False,
    num_workers=2,
    pin_memory=True
)

print(f"✅ DataLoaders created!")
print(f"   Train batches: {len(train_loader)}")
print(f"   Val batches: {len(val_loader)}")
print(f"   Steps per epoch: {len(train_loader)}")
print(f"   Total training steps: {len(train_loader) * Config.EPOCHS}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 11: Calculate Class Weights
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("⚖️ CALCULATING CLASS WEIGHTS")
print("="*80)

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.array([0, 1, 2]),
    y=train_labels
)

class_weights = torch.tensor(class_weights, dtype=torch.float).to(Config.DEVICE)

print(f"\n⚖️ Class weights:")
for i, w in enumerate(class_weights.cpu().numpy()):
    print(f"   Label {i}: {w:.4f}")

print(f"\n⚖️ Weight ratio: {class_weights.max().item() / class_weights.min().item():.2f}x")
print("✅ Class weights calculated!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 12: Load Model
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("📥 LOADING MODEL")
print("="*80)

model = AutoModelForSequenceClassification.from_pretrained(
    Config.MODEL_NAME,
    num_labels=Config.NUM_LABELS
)

model.to(Config.DEVICE)

# Count parameters
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

print(f"\n✅ Model loaded: {Config.MODEL_NAME}")
print(f"📊 Total parameters: {total_params:,}")
print(f"📊 Trainable parameters: {trainable_params:,}")
print(f"📊 Model size: ~{total_params * 4 / 1024 / 1024:.1f} MB")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 13: Setup Optimizer, Scheduler & Loss
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🔧 SETTING UP TRAINING COMPONENTS")
print("="*80)

# Loss function with class weights and label smoothing
criterion = nn.CrossEntropyLoss(
    weight=class_weights,
    label_smoothing=Config.LABEL_SMOOTHING
)
print(f"✅ Loss: CrossEntropyLoss (label_smoothing={Config.LABEL_SMOOTHING})")

# Optimizer
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=Config.LEARNING_RATE,
    weight_decay=Config.WEIGHT_DECAY
)
print(f"✅ Optimizer: AdamW (lr={Config.LEARNING_RATE}, weight_decay={Config.WEIGHT_DECAY})")

# Scheduler
total_steps = len(train_loader) * Config.EPOCHS // Config.GRADIENT_ACCUMULATION_STEPS
warmup_steps = int(total_steps * Config.WARMUP_RATIO)

scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=warmup_steps,
    num_training_steps=total_steps
)
print(f"✅ Scheduler: Cosine with warmup")
print(f"   Total steps: {total_steps}")
print(f"   Warmup steps: {warmup_steps}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 14: Training Functions
# ═══════════════════════════════════════════════════════════════════════════════

def train_epoch(model, dataloader, optimizer, scheduler, criterion, device, accumulation_steps):
    """Train for one epoch"""
    model.train()
    total_loss = 0
    all_preds = []
    all_labels = []
    
    progress_bar = tqdm(dataloader, desc="Training", leave=False)
    optimizer.zero_grad()
    
    for step, batch in enumerate(progress_bar):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        
        # Forward pass
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        loss = criterion(logits, labels)
        
        # Scale loss for gradient accumulation
        loss = loss / accumulation_steps
        loss.backward()
        
        # Update weights
        if (step + 1) % accumulation_steps == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
        
        total_loss += loss.item() * accumulation_steps
        
        # Predictions
        preds = torch.argmax(logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        
        # Update progress bar
        progress_bar.set_postfix({'loss': f'{loss.item() * accumulation_steps:.4f}'})
    
    avg_loss = total_loss / len(dataloader)
    f1 = f1_score(all_labels, all_preds, average='macro')
    
    return avg_loss, f1


def eval_epoch(model, dataloader, criterion, device):
    """Evaluate model"""
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []
    all_probs = []
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating", leave=False):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            loss = criterion(logits, labels)
            
            total_loss += loss.item()
            
            probs = torch.softmax(logits, dim=1)
            preds = torch.argmax(probs, dim=1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    
    avg_loss = total_loss / len(dataloader)
    
    # Metrics
    f1_macro = f1_score(all_labels, all_preds, average='macro')
    f1_weighted = f1_score(all_labels, all_preds, average='weighted')
    accuracy = accuracy_score(all_labels, all_preds)
    precision = precision_score(all_labels, all_preds, average='macro')
    recall = recall_score(all_labels, all_preds, average='macro')
    
    metrics = {
        'loss': avg_loss,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall
    }
    
    return metrics, all_preds, all_labels, all_probs

print("✅ Training functions defined!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 15: Training Loop
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🏋️ STARTING TRAINING")
print("="*80)

# Training history
history = {
    'train_loss': [],
    'train_f1': [],
    'val_loss': [],
    'val_f1': [],
    'val_accuracy': []
}

# Best model tracking
best_f1 = 0
best_epoch = 0
patience_counter = 0
best_model_state = None

# Training loop
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
    print(f"📊 Val Loss: {val_metrics['loss']:.4f} | Val F1 (macro): {val_metrics['f1_macro']:.4f}")
    print(f"📊 Val Accuracy: {val_metrics['accuracy']:.4f} | Val Precision: {val_metrics['precision']:.4f} | Val Recall: {val_metrics['recall']:.4f}")
    
    # Check for improvement
    if val_metrics['f1_macro'] > best_f1:
        best_f1 = val_metrics['f1_macro']
        best_epoch = epoch + 1
        patience_counter = 0
        best_model_state = model.state_dict().copy()
        print(f"✅ New best F1: {best_f1:.4f} - Model saved!")
    else:
        patience_counter += 1
        print(f"⚠️ No improvement. Patience: {patience_counter}/{Config.PATIENCE}")
    
    # Early stopping
    if patience_counter >= Config.PATIENCE:
        print(f"\n🛑 Early stopping triggered at epoch {epoch + 1}")
        break

# Load best model
if best_model_state is not None:
    model.load_state_dict(best_model_state)
    print(f"\n✅ Loaded best model from epoch {best_epoch}")

print(f"\n{'='*60}")
print(f"🏆 TRAINING COMPLETE!")
print(f"{'='*60}")
print(f"🎯 Best F1 (macro): {best_f1:.4f} at epoch {best_epoch}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 16: Plot Training History
# ═══════════════════════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Loss
ax1 = axes[0]
ax1.plot(history['train_loss'], label='Train Loss', marker='o')
ax1.plot(history['val_loss'], label='Val Loss', marker='s')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.set_title('Training & Validation Loss')
ax1.legend()
ax1.grid(True, alpha=0.3)

# F1 Score
ax2 = axes[1]
ax2.plot(history['train_f1'], label='Train F1', marker='o')
ax2.plot(history['val_f1'], label='Val F1', marker='s')
ax2.axhline(y=0.72, color='r', linestyle='--', label='Target (0.72)')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('F1 Score (macro)')
ax2.set_title('Training & Validation F1')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Accuracy
ax3 = axes[2]
ax3.plot(history['val_accuracy'], label='Val Accuracy', marker='s', color='green')
ax3.set_xlabel('Epoch')
ax3.set_ylabel('Accuracy')
ax3.set_title('Validation Accuracy')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/content/training_history.png', dpi=150, bbox_inches='tight')
plt.show()

print("✅ Training history plotted!")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 17: Final Evaluation
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("📊 FINAL EVALUATION")
print("="*80)

# Final evaluation on validation set
final_metrics, final_preds, final_true, final_probs = eval_epoch(
    model, val_loader, criterion, Config.DEVICE
)

print(f"\n🎯 FINAL METRICS:")
print(f"   F1 (macro): {final_metrics['f1_macro']:.4f}")
print(f"   F1 (weighted): {final_metrics['f1_weighted']:.4f}")
print(f"   Accuracy: {final_metrics['accuracy']:.4f}")
print(f"   Precision: {final_metrics['precision']:.4f}")
print(f"   Recall: {final_metrics['recall']:.4f}")

# Classification report
print(f"\n📋 CLASSIFICATION REPORT:")
print(classification_report(
    final_true, final_preds,
    target_names=['Clean (0)', 'Toxic (1)', 'Hate (2)']
))

# Confusion matrix
print(f"\n📋 CONFUSION MATRIX:")
cm = confusion_matrix(final_true, final_preds)
print(cm)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Clean', 'Toxic', 'Hate'],
            yticklabels=['Clean', 'Toxic', 'Hate'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.savefig('/content/confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 18: Error Analysis
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🔍 ERROR ANALYSIS")
print("="*80)

# Create error dataframe
error_df = pd.DataFrame({
    'text': val_texts,
    'true_label': final_true,
    'pred_label': final_preds
})

error_df['is_error'] = error_df['true_label'] != error_df['pred_label']
error_df['error_type'] = error_df.apply(
    lambda x: f"{x['true_label']}→{x['pred_label']}" if x['is_error'] else 'Correct',
    axis=1
)

# Error statistics
total_errors = error_df['is_error'].sum()
print(f"\n📊 ERROR STATISTICS:")
print(f"   Total samples: {len(error_df)}")
print(f"   Correct: {len(error_df) - total_errors} ({(1 - total_errors/len(error_df))*100:.1f}%)")
print(f"   Errors: {total_errors} ({total_errors/len(error_df)*100:.1f}%)")

# Error breakdown
print(f"\n📊 ERROR BREAKDOWN:")
error_counts = error_df[error_df['is_error']]['error_type'].value_counts()
for error_type, count in error_counts.items():
    print(f"   {error_type}: {count} ({count/total_errors*100:.1f}%)")

# Save errors for review
errors_only = error_df[error_df['is_error']][['text', 'true_label', 'pred_label', 'error_type']]
errors_only.to_excel('/content/model_errors.xlsx', index=False)
print(f"\n💾 Errors saved to: /content/model_errors.xlsx")

# Show sample errors
print(f"\n📋 SAMPLE ERRORS (first 5):")
for i, row in errors_only.head(5).iterrows():
    print(f"\n{row['error_type']} | True: {row['true_label']} → Pred: {row['pred_label']}")
    print(f"   {row['text'][:100]}...")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 19: Save Model
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("💾 SAVING MODEL")
print("="*80)

# Create save directory
import os
os.makedirs(Config.MODEL_SAVE_PATH, exist_ok=True)

# Save model and tokenizer
model.save_pretrained(Config.MODEL_SAVE_PATH)
tokenizer.save_pretrained(Config.MODEL_SAVE_PATH)

# Save training config
config_dict = {
    'model_name': Config.MODEL_NAME,
    'num_labels': Config.NUM_LABELS,
    'max_length': Config.MAX_LENGTH,
    'best_f1': best_f1,
    'best_epoch': best_epoch,
    'final_metrics': final_metrics
}

import json
with open(f'{Config.MODEL_SAVE_PATH}/training_config.json', 'w') as f:
    json.dump(config_dict, f, indent=2, default=str)

# Save training history
history_df = pd.DataFrame(history)
history_df.to_csv(f'{Config.MODEL_SAVE_PATH}/training_history.csv', index=False)

print(f"\n✅ Model saved to: {Config.MODEL_SAVE_PATH}")
print(f"   - pytorch_model.bin")
print(f"   - config.json")
print(f"   - tokenizer files")
print(f"   - training_config.json")
print(f"   - training_history.csv")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 20: Test Inference
# ═══════════════════════════════════════════════════════════════════════════════

print("="*80)
print("🧪 TEST INFERENCE")
print("="*80)

def predict_single(text, model, tokenizer, device):
    """Predict label for a single text"""
    model.eval()
    
    encoding = tokenizer(
        text,
        add_special_tokens=True,
        max_length=Config.MAX_LENGTH,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        probs = torch.softmax(outputs.logits, dim=1)
        pred = torch.argmax(probs, dim=1).item()
    
    label_names = ['Clean', 'Toxic', 'Hate']
    
    return {
        'text': text[:100] + '...' if len(text) > 100 else text,
        'prediction': pred,
        'label': label_names[pred],
        'confidence': probs[0][pred].item(),
        'probabilities': {
            'Clean': probs[0][0].item(),
            'Toxic': probs[0][1].item(),
            'Hate': probs[0][2].item()
        }
    }

# Test samples
test_samples = [
    "video hay quá, cảm ơn bạn đã chia sẻ",
    "thằng ngu, mày biết cái gì mà nói",
    "đồ con chó, cút đi",
    "sản phẩm chất vcl, mua về dùng thích lắm",
    "bài hát này hay quá đi",
    "bọn bắc kỳ toàn lừa đảo",
    "pháp luật sẽ xử lý nghiêm minh"
]

print("\n🔮 PREDICTIONS:")
print("-" * 80)

for text in test_samples:
    result = predict_single(text, model, tokenizer, Config.DEVICE)
    
    print(f"\n📝 Text: {result['text']}")
    print(f"🏷️ Prediction: {result['prediction']} ({result['label']})")
    print(f"📊 Confidence: {result['confidence']:.2%}")
    print(f"   Clean: {result['probabilities']['Clean']:.2%} | Toxic: {result['probabilities']['Toxic']:.2%} | Hate: {result['probabilities']['Hate']:.2%}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 21: Summary
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("🏆 TRAINING SUMMARY")
print("="*80)

print(f"""
📊 DATASET:
   - Total samples: {len(texts)}
   - Train: {len(train_texts)} | Val: {len(val_texts)}
   - Labels: Clean (0), Toxic (1), Hate (2)

🔧 MODEL:
   - Architecture: {Config.MODEL_NAME}
   - Max length: {Config.MAX_LENGTH}
   - Parameters: {total_params:,}

📈 TRAINING:
   - Epochs: {len(history['train_loss'])} (early stopped at {best_epoch})
   - Batch size: {Config.BATCH_SIZE} x {Config.GRADIENT_ACCUMULATION_STEPS}
   - Learning rate: {Config.LEARNING_RATE}
   - Class weights: {class_weights.cpu().numpy()}

🎯 RESULTS:
   - Best F1 (macro): {best_f1:.4f}
   - Final Accuracy: {final_metrics['accuracy']:.4f}
   - Final Precision: {final_metrics['precision']:.4f}
   - Final Recall: {final_metrics['recall']:.4f}

💾 SAVED:
   - Model: {Config.MODEL_SAVE_PATH}
   - Errors: /content/model_errors.xlsx
   - History: {Config.MODEL_SAVE_PATH}/training_history.csv

{'✅ TARGET ACHIEVED!' if best_f1 >= 0.72 else '⚠️ Target not reached (0.72). Consider:'}
{'   - More training data' if best_f1 < 0.72 else ''}
{'   - Focal loss for hard examples' if best_f1 < 0.72 else ''}
{'   - Longer training with lower LR' if best_f1 < 0.72 else ''}
""")

print("="*80)
print("✅ NOTEBOOK COMPLETE!")
print("="*80)
