"""
🔥 SafeSense-VI: PhoBERT-base-v2 Training V5 (FINAL)
Vietnamese Toxic Comment Classification - IT Got Talent 2025

✅ Cải tiến V5:
- Data Split chuẩn: 80% Train / 10% Val / 10% Test
- Test Set độc lập: Đánh giá cuối cùng trên tập chưa từng thấy
- Classification Report đầy đủ
- Confusion Matrix visualization

📋 HƯỚNG DẪN SỬ DỤNG TRÊN GOOGLE COLAB:
1. Upload file này lên Colab
2. Thay đổi DATA_PATH trong Config
3. Chạy: !python COLAB_PHOBERT_V5_FINAL.py
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
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

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class Config:
    # Model
    MODEL_NAME = "vinai/phobert-base-v2"
    NUM_LABELS = 3
    MAX_LENGTH = 256

    # Training
    BATCH_SIZE = 16
    GRADIENT_ACCUMULATION_STEPS = 2  # Effective batch = 32
    EPOCHS = 7
    LEARNING_RATE = 3e-5
    WEIGHT_DECAY = 0.01
    WARMUP_RATIO = 0.15

    # Optimization
    USE_CLASS_WEIGHTS = True
    LABEL_SMOOTHING = 0.1

    # Early stopping
    PATIENCE = 2

    # ⭐ DATA SPLIT - CHUẨN KHOA HỌC
    TRAIN_RATIO = 0.80  # 80% for training
    VAL_RATIO = 0.10    # 10% for validation (early stopping)
    TEST_RATIO = 0.10   # 10% for final evaluation (NEVER SEEN DURING TRAINING)

    # Seed
    SEED = 42

    # Device
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # ⚠️ THAY ĐỔI ĐƯỜNG DẪN NÀY
    DATA_PATH = "/content/drive/MyDrive/Deep_Learning_hate_speech_V3/final_train_data_v3_READY_PHOBERT_20260102_053035_SEGMENTED_20260102_053456.csv"
    OUTPUT_DIR = "/content/drive/MyDrive/SafeSense-VI/output_v5"
    MODEL_SAVE_PATH = "/content/drive/MyDrive/SafeSense-VI/phobert_toxic_model_v5_final"


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True


# ═══════════════════════════════════════════════════════════════════════════════
# DATASET CLASS
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


# ═══════════════════════════════════════════════════════════════════════════════
# TRAINING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

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

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits

        loss = criterion(logits, labels)
        loss = loss / accumulation_steps
        loss.backward()

        total_loss += loss.item() * accumulation_steps

        preds = torch.argmax(logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

        if (step + 1) % accumulation_steps == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

        progress_bar.set_postfix({'loss': f'{loss.item() * accumulation_steps:.4f}'})

    avg_loss = total_loss / len(dataloader)
    f1 = f1_score(all_labels, all_preds, average='macro')
    acc = accuracy_score(all_labels, all_preds)

    return avg_loss, f1, acc


def evaluate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Evaluating"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits

            loss = criterion(logits, labels)
            total_loss += loss.item()

            preds = torch.argmax(logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / len(dataloader)
    f1 = f1_score(all_labels, all_preds, average='macro')
    acc = accuracy_score(all_labels, all_preds)

    return avg_loss, f1, acc, all_preds, all_labels


# ═══════════════════════════════════════════════════════════════════════════════
# VISUALIZATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def plot_confusion_matrix(y_true, y_pred, save_path=None):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    
    labels = ['Clean (0)', 'Offensive (1)', 'Hate (2)']
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels,
                annot_kws={'size': 16})
    
    plt.title('Confusion Matrix - Test Set\n(Final Evaluation)', fontsize=16, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=14)
    plt.ylabel('True Label', fontsize=14)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Confusion matrix saved to: {save_path}")
    
    plt.show()


def plot_training_history(history, save_path=None):
    """Plot training history"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Loss
    axes[0].plot(history['train_loss'], label='Train Loss', marker='o')
    axes[0].plot(history['val_loss'], label='Val Loss', marker='s')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training & Validation Loss')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # F1-Score
    axes[1].plot(history['train_f1'], label='Train F1', marker='o')
    axes[1].plot(history['val_f1'], label='Val F1', marker='s')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('F1-Score (Macro)')
    axes[1].set_title('Training & Validation F1-Score')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"💾 Training history saved to: {save_path}")
    
    plt.show()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN TRAINING PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("="*80)
    print("🔥 SafeSense-VI: PhoBERT Training V5 (FINAL)")
    print("   Vietnamese Toxic Comment Classification")
    print("   IT Got Talent 2025")
    print("="*80)
    
    # Set seed
    set_seed(Config.SEED)
    
    print(f"\n🔧 Configuration:")
    print(f"   Device: {Config.DEVICE}")
    print(f"   Model: {Config.MODEL_NAME}")
    print(f"   Batch Size: {Config.BATCH_SIZE} x {Config.GRADIENT_ACCUMULATION_STEPS} = {Config.BATCH_SIZE * Config.GRADIENT_ACCUMULATION_STEPS}")
    print(f"   Data Split: Train {Config.TRAIN_RATIO*100:.0f}% / Val {Config.VAL_RATIO*100:.0f}% / Test {Config.TEST_RATIO*100:.0f}%")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LOAD DATA
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*80)
    print("📊 LOADING DATA")
    print("="*80)
    
    if Config.DATA_PATH.endswith('.xlsx'):
        df = pd.read_excel(Config.DATA_PATH)
    else:
        df = pd.read_csv(Config.DATA_PATH)
    
    print(f"📂 Loaded: {len(df):,} samples")
    
    # Identify columns
    text_col = 'training_text' if 'training_text' in df.columns else 'text'
    label_col = 'label'
    
    # Clean data
    df[label_col] = pd.to_numeric(df[label_col], errors='coerce')
    df = df.dropna(subset=[text_col, label_col])
    df[label_col] = df[label_col].astype(int)
    
    print(f"📂 After cleaning: {len(df):,} samples")
    
    # Label distribution
    print(f"\n📊 LABEL DISTRIBUTION:")
    label_names = {0: 'Clean', 1: 'Offensive', 2: 'Hate'}
    for label in sorted(df[label_col].unique()):
        count = (df[label_col] == label).sum()
        pct = count / len(df) * 100
        print(f"   Label {label} ({label_names.get(label, 'Unknown')}): {count:,} ({pct:.2f}%)")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ⭐ DATA SPLIT: 80% TRAIN / 10% VAL / 10% TEST
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*80)
    print("📊 DATA SPLIT (80/10/10)")
    print("="*80)
    
    X = df[text_col].values
    y = df[label_col].values
    
    # First split: 80% train, 20% temp (val + test)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y,
        test_size=0.20,  # 20% for val + test
        random_state=Config.SEED,
        stratify=y
    )
    
    # Second split: 50% val, 50% test (from temp) = 10% each of total
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp,
        test_size=0.50,  # 50% of 20% = 10% of total
        random_state=Config.SEED,
        stratify=y_temp
    )
    
    print(f"✅ Train set: {len(X_train):,} samples ({len(X_train)/len(df)*100:.1f}%)")
    print(f"✅ Val set:   {len(X_val):,} samples ({len(X_val)/len(df)*100:.1f}%)")
    print(f"✅ Test set:  {len(X_test):,} samples ({len(X_test)/len(df)*100:.1f}%)")
    print(f"   Total:     {len(X_train) + len(X_val) + len(X_test):,} samples")
    
    # Verify stratification
    print(f"\n📊 Label distribution per split:")
    for name, y_split in [("Train", y_train), ("Val", y_val), ("Test", y_test)]:
        dist = {label: (y_split == label).sum() / len(y_split) * 100 for label in [0, 1, 2]}
        print(f"   {name}: Clean {dist[0]:.1f}% | Offensive {dist[1]:.1f}% | Hate {dist[2]:.1f}%")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # PREPARE DATALOADERS
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*80)
    print("📦 PREPARING DATALOADERS")
    print("="*80)
    
    tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
    print(f"✅ Tokenizer loaded: {Config.MODEL_NAME}")
    
    train_dataset = ToxicDataset(X_train, y_train, tokenizer, Config.MAX_LENGTH)
    val_dataset = ToxicDataset(X_val, y_val, tokenizer, Config.MAX_LENGTH)
    test_dataset = ToxicDataset(X_test, y_test, tokenizer, Config.MAX_LENGTH)
    
    train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE * 2, shuffle=False, num_workers=0, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=Config.BATCH_SIZE * 2, shuffle=False, num_workers=0, pin_memory=True)
    
    print(f"✅ DataLoaders created!")
    print(f"   Train batches: {len(train_loader)}")
    print(f"   Val batches: {len(val_loader)}")
    print(f"   Test batches: {len(test_loader)}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # LOAD MODEL & SETUP
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*80)
    print("🤖 LOADING MODEL")
    print("="*80)
    
    model = AutoModelForSequenceClassification.from_pretrained(
        Config.MODEL_NAME,
        num_labels=Config.NUM_LABELS
    )
    model.to(Config.DEVICE)
    print(f"✅ Model loaded and moved to {Config.DEVICE}")
    
    # Class weights (computed on TRAIN SET ONLY!)
    if Config.USE_CLASS_WEIGHTS:
        class_weights = compute_class_weight(
            class_weight='balanced',
            classes=np.unique(y_train),
            y=y_train
        )
        class_weights = torch.tensor(class_weights, dtype=torch.float).to(Config.DEVICE)
        print(f"⚖️ Class weights (from train set): {class_weights.tolist()}")
    else:
        class_weights = None
    
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
    
    print(f"📈 Total steps: {total_steps} | Warmup: {warmup_steps}")


    # ═══════════════════════════════════════════════════════════════════════════
    # TRAINING LOOP
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*80)
    print("🚀 STARTING TRAINING")
    print("="*80)
    
    best_f1 = 0
    patience_counter = 0
    history = {'train_loss': [], 'val_loss': [], 'train_f1': [], 'val_f1': []}
    
    for epoch in range(Config.EPOCHS):
        print(f"\n{'='*60}")
        print(f"📌 EPOCH {epoch + 1}/{Config.EPOCHS}")
        print(f"{'='*60}")
        
        # Train
        train_loss, train_f1, train_acc = train_epoch(
            model, train_loader, optimizer, scheduler, criterion,
            Config.DEVICE, Config.GRADIENT_ACCUMULATION_STEPS
        )
        
        # Validate
        val_loss, val_f1, val_acc, _, _ = evaluate(
            model, val_loader, criterion, Config.DEVICE
        )
        
        # Log
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        history['train_f1'].append(train_f1)
        history['val_f1'].append(val_f1)
        
        print(f"\n📊 Results:")
        print(f"   Train - Loss: {train_loss:.4f} | F1: {train_f1:.4f} | Acc: {train_acc:.4f}")
        print(f"   Val   - Loss: {val_loss:.4f} | F1: {val_f1:.4f} | Acc: {val_acc:.4f}")
        
        # Save best model
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
        
        # Early stopping
        if patience_counter >= Config.PATIENCE:
            print(f"\n⚠️ Early stopping triggered!")
            break
    
    print(f"\n{'='*80}")
    print(f"✅ TRAINING COMPLETED!")
    print(f"🏆 Best Validation F1: {best_f1:.4f}")
    print(f"{'='*80}")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ⭐ FINAL EVALUATION ON TEST SET (NEVER SEEN DURING TRAINING!)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*80)
    print("🎯 FINAL EVALUATION ON TEST SET")
    print("   (This data was NEVER seen during training or validation!)")
    print("="*80)
    
    # Load best model
    print("\n📂 Loading best model...")
    model = AutoModelForSequenceClassification.from_pretrained(Config.MODEL_SAVE_PATH)
    model.to(Config.DEVICE)
    
    # Evaluate on test set
    test_loss, test_f1, test_acc, test_preds, test_labels = evaluate(
        model, test_loader, criterion, Config.DEVICE
    )
    
    print(f"\n{'='*60}")
    print(f"📊 TEST SET RESULTS (Final Evaluation)")
    print(f"{'='*60}")
    print(f"   Loss:     {test_loss:.4f}")
    print(f"   F1-Score: {test_f1:.4f}")
    print(f"   Accuracy: {test_acc:.4f}")
    
    # Classification Report
    print(f"\n{'='*60}")
    print("📋 CLASSIFICATION REPORT:")
    print(f"{'='*60}")
    target_names = ['Clean (0)', 'Offensive (1)', 'Hate (2)']
    print(classification_report(test_labels, test_preds, target_names=target_names, digits=4))
    
    # Confusion Matrix
    print(f"\n{'='*60}")
    print("📊 CONFUSION MATRIX:")
    print(f"{'='*60}")
    cm = confusion_matrix(test_labels, test_preds)
    print(f"\n              Predicted")
    print(f"           Clean  Off   Hate")
    print(f"Actual")
    for i, label in enumerate(['Clean', 'Off  ', 'Hate ']):
        print(f"  {label}   {cm[i][0]:4d}  {cm[i][1]:4d}  {cm[i][2]:4d}")
    
    # Save results
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
    
    # Plot and save confusion matrix
    plot_confusion_matrix(
        test_labels, test_preds,
        save_path=os.path.join(Config.OUTPUT_DIR, 'confusion_matrix_test.png')
    )
    
    # Plot and save training history
    plot_training_history(
        history,
        save_path=os.path.join(Config.OUTPUT_DIR, 'training_history.png')
    )
    
    # Save results to file
    results = {
        'test_loss': test_loss,
        'test_f1': test_f1,
        'test_accuracy': test_acc,
        'best_val_f1': best_f1,
        'train_samples': len(X_train),
        'val_samples': len(X_val),
        'test_samples': len(X_test),
        'epochs_trained': len(history['train_loss']),
        'classification_report': classification_report(test_labels, test_preds, target_names=target_names, output_dict=True)
    }
    
    import json
    with open(os.path.join(Config.OUTPUT_DIR, 'results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {Config.OUTPUT_DIR}/results.json")
    
    # ═══════════════════════════════════════════════════════════════════════════
    # SUMMARY
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*80)
    print("🏆 TRAINING SUMMARY - IT GOT TALENT 2025")
    print("="*80)
    print(f"""
📊 DATA SPLIT (Chuẩn khoa học):
   - Train: {len(X_train):,} samples (80%)
   - Val:   {len(X_val):,} samples (10%) - Used for early stopping
   - Test:  {len(X_test):,} samples (10%) - Final evaluation (NEVER seen during training)

🎯 FINAL RESULTS (on Test Set):
   - F1-Score (Macro): {test_f1:.4f}
   - Accuracy:         {test_acc:.4f}
   - Best Val F1:      {best_f1:.4f}

📁 OUTPUT FILES:
   - Model: {Config.MODEL_SAVE_PATH}
   - Results: {Config.OUTPUT_DIR}/results.json
   - Confusion Matrix: {Config.OUTPUT_DIR}/confusion_matrix_test.png
   - Training History: {Config.OUTPUT_DIR}/training_history.png

✅ Model is ready for IT Got Talent 2025 presentation!
""")
    print("="*80)
    
    return results


if __name__ == "__main__":
    results = main()
