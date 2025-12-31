"""
🔥 SAFESENSE-VI: PhoBERT Training Script for Kaggle
Vietnamese Toxic Comment Classification with Intensity Preservation

Author: Thanh Thien
Date: 28/12/2025
Model: vinai/phobert-base
Task: Multi-class classification (3 labels)
    - Label 0: Clean/Positive Slang
    - Label 1: Toxic/Offensive
    - Label 2: Hate Speech/Discrimination

Optimizations for Best F1:
    1. Class weights for imbalanced data
    2. Focal Loss option
    3. Learning rate scheduling with warmup
    4. Early stopping with F1 monitoring
    5. Stratified K-Fold cross-validation
    6. Label smoothing
    7. Gradient accumulation for larger effective batch size
"""

# ============================================================
# 1. INSTALL & IMPORTS
# ============================================================

# !pip install transformers datasets accelerate -q
# !pip install scikit-learn pandas numpy -q

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
    get_linear_schedule_with_warmup,
    get_cosine_schedule_with_warmup
)
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import (
    f1_score, accuracy_score, precision_score, recall_score,
    classification_report, confusion_matrix
)
from sklearn.utils.class_weight import compute_class_weight
from tqdm.auto import tqdm
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 2. CONFIGURATION
# ============================================================

class Config:
    # Model
    MODEL_NAME = "vinai/phobert-base"
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
    USE_FOCAL_LOSS = False  # Set True if class imbalance is severe
    FOCAL_GAMMA = 2.0
    LABEL_SMOOTHING = 0.1
    
    # Cross-validation
    USE_KFOLD = False  # Set True for K-Fold CV
    N_FOLDS = 5
    
    # Early stopping
    PATIENCE = 2
    
    # Seed
    SEED = 42
    
    # Device
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

set_seed(Config.SEED)
print(f"🔧 Device: {Config.DEVICE}")
print(f"🔧 Model: {Config.MODEL_NAME}")

# ============================================================
# 3. LOAD DATA
# ============================================================

# For Kaggle: Upload your CSV file and update path
DATA_PATH = "/kaggle/input/your-dataset/final_train_data_v2.csv"
# For local testing:
# DATA_PATH = "final_train_data_v2.csv"


def load_data(path):
    """Load and prepare data"""
    df = pd.read_csv(path)
    
    # Use training_text column
    texts = df['training_text'].fillna('').astype(str).tolist()
    labels = df['label'].tolist()
    
    print(f"📊 Dataset loaded: {len(texts)} samples")
    print(f"📊 Label distribution:")
    for label, count in df['label'].value_counts().sort_index().items():
        print(f"   Label {label}: {count} ({count/len(df)*100:.1f}%)")
    
    return texts, labels

# ============================================================
# 4. DATASET CLASS
# ============================================================

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

# ============================================================
# 5. FOCAL LOSS (Optional - for severe class imbalance)
# ============================================================

class FocalLoss(nn.Module):
    def __init__(self, alpha=None, gamma=2.0, reduction='mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
    
    def forward(self, inputs, targets):
        ce_loss = nn.functional.cross_entropy(
            inputs, targets, weight=self.alpha, reduction='none'
        )
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss

# ============================================================
# 6. TRAINING FUNCTIONS
# ============================================================

def train_epoch(model, dataloader, optimizer, scheduler, criterion, device, accumulation_steps):
    model.train()
    total_loss = 0
    all_preds = []
    all_labels = []
    
    progress_bar = tqdm(dataloader, desc="Training")
    optimizer.zero_grad()
    
    for step, batch in enumerate(progress_bar):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
        
        logits = outputs.logits
        loss = criterion(logits, labels)
        loss = loss / accumulation_steps
        
        loss.backward()
        
        if (step + 1) % accumulation_steps == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
        
        total_loss += loss.item() * accumulation_steps
        
        preds = torch.argmax(logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        
        progress_bar.set_postfix({'loss': f'{loss.item() * accumulation_steps:.4f}'})
    
    avg_loss = total_loss / len(dataloader)
    f1 = f1_score(all_labels, all_preds, average='macro')
    
    return avg_loss, f1

def eval_epoch(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
            
            logits = outputs.logits
            loss = criterion(logits, labels)
            
            total_loss += loss.item()
            
            preds = torch.argmax(logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    avg_loss = total_loss / len(dataloader)
    
    # Calculate metrics
    f1_macro = f1_score(all_labels, all_preds, average='macro')
    f1_weighted = f1_score(all_labels, all_preds, average='weighted')
    accuracy = accuracy_score(all_labels, all_preds)
    
    return avg_loss, f1_macro, f1_weighted, accuracy, all_preds, all_labels


# ============================================================
# 7. MAIN TRAINING FUNCTION
# ============================================================

def train_model(texts, labels, config=Config):
    """Main training function with all optimizations"""
    
    print("\n" + "="*60)
    print("🚀 STARTING TRAINING")
    print("="*60)
    
    # Split data
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, 
        test_size=0.15, 
        random_state=config.SEED,
        stratify=labels
    )
    
    print(f"\n📊 Train size: {len(train_texts)}")
    print(f"📊 Val size: {len(val_texts)}")
    
    # Load tokenizer
    print(f"\n📥 Loading tokenizer: {config.MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME)
    
    # Create datasets
    train_dataset = ToxicDataset(train_texts, train_labels, tokenizer, config.MAX_LENGTH)
    val_dataset = ToxicDataset(val_texts, val_labels, tokenizer, config.MAX_LENGTH)
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset, 
        batch_size=config.BATCH_SIZE, 
        shuffle=True,
        num_workers=2,
        pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset, 
        batch_size=config.BATCH_SIZE * 2,
        shuffle=False,
        num_workers=2,
        pin_memory=True
    )
    
    # Load model
    print(f"📥 Loading model: {config.MODEL_NAME}")
    model = AutoModelForSequenceClassification.from_pretrained(
        config.MODEL_NAME,
        num_labels=config.NUM_LABELS
    )
    model.to(config.DEVICE)
    
    # Calculate class weights
    class_weights = None
    if config.USE_CLASS_WEIGHTS:
        class_weights = compute_class_weight(
            class_weight='balanced',
            classes=np.unique(train_labels),
            y=train_labels
        )
        class_weights = torch.tensor(class_weights, dtype=torch.float).to(config.DEVICE)
        print(f"\n⚖️ Class weights: {class_weights.cpu().numpy()}")
    
    # Loss function
    if config.USE_FOCAL_LOSS:
        criterion = FocalLoss(alpha=class_weights, gamma=config.FOCAL_GAMMA)
        print("📉 Using Focal Loss")
    else:
        criterion = nn.CrossEntropyLoss(
            weight=class_weights,
            label_smoothing=config.LABEL_SMOOTHING
        )
        print(f"📉 Using CrossEntropyLoss with label_smoothing={config.LABEL_SMOOTHING}")
    
    # Optimizer
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.LEARNING_RATE,
        weight_decay=config.WEIGHT_DECAY
    )
    
    # Scheduler
    total_steps = len(train_loader) * config.EPOCHS // config.GRADIENT_ACCUMULATION_STEPS
    warmup_steps = int(total_steps * config.WARMUP_RATIO)
    
    scheduler = get_cosine_schedule_with_warmup(
        optimizer,
        num_warmup_steps=warmup_steps,
        num_training_steps=total_steps
    )
    print(f"📈 Total steps: {total_steps}, Warmup steps: {warmup_steps}")
    
    # Training loop
    best_f1 = 0
    patience_counter = 0
    best_model_state = None
    
    print("\n" + "="*60)
    print("🏋️ TRAINING STARTED")
    print("="*60)
    
    for epoch in range(config.EPOCHS):
        print(f"\n📅 Epoch {epoch + 1}/{config.EPOCHS}")
        print("-" * 40)
        
        # Train
        train_loss, train_f1 = train_epoch(
            model, train_loader, optimizer, scheduler, 
            criterion, config.DEVICE, config.GRADIENT_ACCUMULATION_STEPS
        )
        
        # Evaluate
        val_loss, val_f1_macro, val_f1_weighted, val_acc, val_preds, val_true = eval_epoch(
            model, val_loader, criterion, config.DEVICE
        )
        
        print(f"\n📊 Train Loss: {train_loss:.4f} | Train F1: {train_f1:.4f}")
        print(f"📊 Val Loss: {val_loss:.4f} | Val F1 (macro): {val_f1_macro:.4f} | Val F1 (weighted): {val_f1_weighted:.4f}")
        print(f"📊 Val Accuracy: {val_acc:.4f}")
        
        # Early stopping check
        if val_f1_macro > best_f1:
            best_f1 = val_f1_macro
            patience_counter = 0
            best_model_state = model.state_dict().copy()
            print(f"✅ New best F1: {best_f1:.4f} - Model saved!")
        else:
            patience_counter += 1
            print(f"⚠️ No improvement. Patience: {patience_counter}/{config.PATIENCE}")
        
        if patience_counter >= config.PATIENCE:
            print(f"\n🛑 Early stopping triggered at epoch {epoch + 1}")
            break
    
    # Load best model
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
    
    # Final evaluation
    print("\n" + "="*60)
    print("📊 FINAL EVALUATION")
    print("="*60)
    
    val_loss, val_f1_macro, val_f1_weighted, val_acc, val_preds, val_true = eval_epoch(
        model, val_loader, criterion, config.DEVICE
    )
    
    print(f"\n🎯 Best F1 (macro): {best_f1:.4f}")
    print(f"🎯 Final F1 (macro): {val_f1_macro:.4f}")
    print(f"🎯 Final F1 (weighted): {val_f1_weighted:.4f}")
    print(f"🎯 Final Accuracy: {val_acc:.4f}")
    
    # Classification report
    print("\n📋 Classification Report:")
    print(classification_report(
        val_true, val_preds,
        target_names=['Label 0 (Clean)', 'Label 1 (Toxic)', 'Label 2 (Hate)']
    ))
    
    # Confusion matrix
    print("\n📋 Confusion Matrix:")
    cm = confusion_matrix(val_true, val_preds)
    print(cm)
    
    return model, tokenizer, best_f1

