"""
PhoBERT-v2 Training Script with Built-in Error Analysis
Automatically analyzes and exports model errors after training
"""
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
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================
class Config:
    MODEL_NAME = "vinai/phobert-base-v2"
    NUM_LABELS = 3
    MAX_LENGTH = 256
    BATCH_SIZE = 16
    GRADIENT_ACCUMULATION_STEPS = 2
    EPOCHS = 5
    LEARNING_RATE = 2e-5
    WEIGHT_DECAY = 0.01
    WARMUP_RATIO = 0.1
    USE_CLASS_WEIGHTS = True
    LABEL_SMOOTHING = 0.1
    PATIENCE = 2
    SEED = 42
    DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

set_seed(Config.SEED)

# ============================================================
# DATASET
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
# TRAINING FUNCTIONS
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
        
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
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
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            loss = criterion(logits, labels)
            
            total_loss += loss.item()
            preds = torch.argmax(logits, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    avg_loss = total_loss / len(dataloader)
    f1_macro = f1_score(all_labels, all_preds, average='macro')
    f1_weighted = f1_score(all_labels, all_preds, average='weighted')
    accuracy = accuracy_score(all_labels, all_preds)
    
    return avg_loss, f1_macro, f1_weighted, accuracy, all_preds, all_labels

# ============================================================
# ERROR ANALYSIS
# ============================================================
def detect_patterns(texts):
    """Detect common patterns in texts"""
    patterns = {
        'vcl_vl_positive': ['vcl', 'vl', 'vãi', 'chất vl', 'hay vl', 'đẹp vl', 'peak vcl'],
        'technical_nang': ['nặng khung', 'mv nặng', 'video nặng', 'lag', 'render'],
        'justice_call': ['pháp luật', 'luật', 'tù', 'giam', 'bắt', 'phạt', 'xử lý'],
        'mv_description': ['official', 'visualizer', 'lyrics', 'mv', 'music video'],
        'family_attack': ['mẹ', 'ba', 'cha', 'chết mẹ', 'đụ mẹ', 'địt mẹ'],
        'animal_words': ['chó', 'lợn', 'heo', 'bò', 'trâu', 'khỉ', 'súc vật'],
        'violence_call': ['đánh', 'đập', 'giết', 'chém', 'tát', 'bạo hành'],
        'positive_slang': ['xịn', 'chất', 'đỉnh', 'pro', 'ngon', 'hay', 'đẹp']
    }
    
    results = {k: 0 for k in patterns.keys()}
    results['long_title'] = 0
    
    for text in texts:
        text_lower = text.lower()
        
        for pattern_name, keywords in patterns.items():
            if any(kw in text_lower for kw in keywords):
                results[pattern_name] += 1
        
        # Check long title
        if '</s>' in text:
            title = text.split('</s>')[0]
            if len(title.split()) > 50:
                results['long_title'] += 1
    
    return results

def analyze_errors(val_texts, val_labels, val_preds, output_path='/content/drive/MyDrive/'):
    """Analyze and export model errors"""
    print("\n" + "="*80)
    print("🔍 PHÂN TÍCH LỖI DỰ ĐOÁN")
    print("="*80)
    
    df = pd.DataFrame({
        'text': val_texts,
        'true_label': val_labels,
        'pred_label': val_preds
    })
    
    df['is_error'] = df['true_label'] != df['pred_label']
    df['error_type'] = df.apply(
        lambda x: f"{x['true_label']}→{x['pred_label']}" if x['is_error'] else 'Correct',
        axis=1
    )
    
    total = len(df)
    errors = df['is_error'].sum()
    
    print(f"\n📊 TỔNG QUAN:")
    print(f"   Total: {total}")
    print(f"   Correct: {total - errors} ({(1-errors/total)*100:.1f}%)")
    print(f"   Errors: {errors} ({errors/total*100:.1f}%)")
    
    if errors == 0:
        print("\n✅ Không có lỗi!")
        return
    
    print(f"\n📊 PHÂN LOẠI LỖI:")
    error_counts = df[df['is_error']]['error_type'].value_counts()
    for error_type, count in error_counts.items():
        print(f"   {error_type}: {count} ({count/errors*100:.1f}%)")
    
    # Analyze patterns for each error type
    for error_type in error_counts.index:
        error_df = df[df['error_type'] == error_type]
        patterns = detect_patterns(error_df['text'].tolist())
        
        print(f"\n🔍 {error_type}:")
        for pattern, count in patterns.items():
            if count > 0:
                print(f"   {pattern}: {count}")
    
    # Save files
    print(f"\n💾 LƯU FILE:")
    
    # All errors
    errors_df = df[df['is_error']].sort_values('error_type')
    all_file = output_path + 'MODEL_ERRORS_ALL.xlsx'
    errors_df.to_excel(all_file, index=False)
    print(f"   ✅ {all_file}")
    
    # By error type
    for error_type in error_counts.index():
        error_df = df[df['error_type'] == error_type]
        filename = output_path + f'MODEL_ERRORS_{error_type.replace("→", "_to_")}.xlsx'
        error_df.to_excel(filename, index=False)
        print(f"   ✅ {filename}")
    
    # Summary
    summary = []
    for error_type in error_counts.index:
        error_df = df[df['error_type'] == error_type]
        patterns = detect_patterns(error_df['text'].tolist())
        top_patterns = [k for k, v in sorted(patterns.items(), key=lambda x: -x[1]) if v > 0][:3]
        
        summary.append({
            'error_type': error_type,
            'count': error_counts[error_type],
            'percentage': f"{error_counts[error_type]/errors*100:.1f}%",
            'top_patterns': ', '.join(top_patterns)
        })
    
    summary_df = pd.DataFrame(summary)
    summary_file = output_path + 'MODEL_ERRORS_SUMMARY.xlsx'
    summary_df.to_excel(summary_file, index=False)
    print(f"   ✅ {summary_file}")
    
    print("\n✅ PHÂN TÍCH HOÀN TẤT!")

# ============================================================
# MAIN TRAINING
# ============================================================
def train_model(data_path, output_path='/content/drive/MyDrive/'):
    """Main training function with error analysis"""
    print("="*80)
    print("🔥 PHOBERT-V2 TRAINING WITH ERROR ANALYSIS")
    print("="*80)
    
    # Mount Drive
    from google.colab import drive
    drive.mount('/content/drive')
    
    # Load data
    print(f"\n📂 Loading: {data_path}")
    df = pd.read_excel(data_path)
    texts = df['training_text'].fillna('').astype(str).tolist()
    labels = df['label'].tolist()
    
    print(f"📊 Dataset: {len(texts)} samples")
    for label, count in df['label'].value_counts().sort_index().items():
        print(f"   Label {label}: {count} ({count/len(df)*100:.1f}%)")
    
    # Split
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.15, random_state=Config.SEED, stratify=labels
    )
    
    print(f"\n📊 Train: {len(train_texts)} | Val: {len(val_texts)}")
    
    # Tokenizer & Model
    print(f"\n📥 Loading: {Config.MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        Config.MODEL_NAME, num_labels=Config.NUM_LABELS
    )
    model.to(Config.DEVICE)
    
    # Datasets
    train_dataset = ToxicDataset(train_texts, train_labels, tokenizer, Config.MAX_LENGTH)
    val_dataset = ToxicDataset(val_texts, val_labels, tokenizer, Config.MAX_LENGTH)
    
    train_loader = DataLoader(train_dataset, batch_size=Config.BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=Config.BATCH_SIZE*2, shuffle=False, num_workers=0)
    
    # Class weights
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(train_labels),
        y=train_labels
    )
    class_weights = torch.tensor(class_weights, dtype=torch.float).to(Config.DEVICE)
    print(f"\n⚖️ Class weights: {class_weights.cpu().numpy()}")
    
    # Loss & Optimizer
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=Config.LABEL_SMOOTHING)
    optimizer = torch.optim.AdamW(model.parameters(), lr=Config.LEARNING_RATE, weight_decay=Config.WEIGHT_DECAY)
    
    total_steps = len(train_loader) * Config.EPOCHS // Config.GRADIENT_ACCUMULATION_STEPS
    warmup_steps = int(total_steps * Config.WARMUP_RATIO)
    scheduler = get_cosine_schedule_with_warmup(optimizer, warmup_steps, total_steps)
    
    # Training loop
    best_f1 = 0
    patience_counter = 0
    best_model_state = None
    
    print("\n" + "="*80)
    print("🏋️ TRAINING")
    print("="*80)
    
    for epoch in range(Config.EPOCHS):
        print(f"\n📅 Epoch {epoch + 1}/{Config.EPOCHS}")
        
        train_loss, train_f1 = train_epoch(
            model, train_loader, optimizer, scheduler, criterion,
            Config.DEVICE, Config.GRADIENT_ACCUMULATION_STEPS
        )
        
        val_loss, val_f1_macro, val_f1_weighted, val_acc, val_preds, val_true = eval_epoch(
            model, val_loader, criterion, Config.DEVICE
        )
        
        print(f"\n📊 Train Loss: {train_loss:.4f} | Train F1: {train_f1:.4f}")
        print(f"📊 Val Loss: {val_loss:.4f} | Val F1: {val_f1_macro:.4f}")
        
        if val_f1_macro > best_f1:
            best_f1 = val_f1_macro
            patience_counter = 0
            best_model_state = model.state_dict().copy()
            best_val_preds = val_preds
            print(f"✅ New best F1: {best_f1:.4f}")
        else:
            patience_counter += 1
            if patience_counter >= Config.PATIENCE:
                print(f"\n🛑 Early stopping at epoch {epoch + 1}")
                break
    
    # Load best model
    if best_model_state:
        model.load_state_dict(best_model_state)
    
    # Final evaluation
    print("\n" + "="*80)
    print("📊 FINAL EVALUATION")
    print("="*80)
    
    val_loss, val_f1_macro, val_f1_weighted, val_acc, val_preds, val_true = eval_epoch(
        model, val_loader, criterion, Config.DEVICE
    )
    
    print(f"\n🎯 Best F1: {best_f1:.4f}")
    print(f"🎯 Final F1 (macro): {val_f1_macro:.4f}")
    print(f"🎯 Final Accuracy: {val_acc:.4f}")
    print("\n📋 Classification Report:")
    print(classification_report(val_true, val_preds,
                                target_names=['Label 0', 'Label 1', 'Label 2']))
    
    # Save model
    model_path = output_path + 'phobert_toxic_model'
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    print(f"\n💾 Model saved: {model_path}")
    
    # ERROR ANALYSIS
    analyze_errors(val_texts, val_true, val_preds, output_path)
    
    print("\n" + "="*80)
    print("✅ HOÀN TẤT!")
    print("="*80)
    
    return model, tokenizer, best_f1

# ============================================================
# MAIN EXECUTION
# ============================================================
if __name__ == "__main__":
    DATA_PATH = "/content/final_train_data_v3_TRUNCATED_20251229.xlsx"
    OUTPUT_PATH = "/content/drive/MyDrive/"
    
    model, tokenizer, best_f1 = train_model(DATA_PATH, OUTPUT_PATH)
