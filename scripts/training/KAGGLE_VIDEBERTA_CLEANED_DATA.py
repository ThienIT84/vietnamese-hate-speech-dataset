"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  🔥 SafeSense-VI: ViDeBERTa with CLEANED Data (Same as PhoBERT)             ║
║  Using final_train_data_v3_CLEANED.xlsx - Expected F1: 0.75-0.80            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CELL 1: Install & Import
# ═══════════════════════════════════════════════════════════════════════════════

!pip install pyarrow==14.0.2 -q
!pip install transformers datasets accelerate -q

import os
import torch
import pandas as pd
import numpy as np
from datasets import Dataset, ClassLabel, Features, Value
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
    EarlyStoppingCallback
)
from sklearn.metrics import f1_score, accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

print(f"✅ PyTorch: {torch.__version__}")
print(f"✅ CUDA: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 2: Configuration
# ═══════════════════════════════════════════════════════════════════════════════

class Config:
    MODEL_NAME = "Fsoft-AIC/videberta-base"
    NUM_LABELS = 3
    MAX_LENGTH = 256
    
    BATCH_SIZE = 8
    GRADIENT_ACCUMULATION = 4
    EPOCHS = 7
    LEARNING_RATE = 2e-5
    WEIGHT_DECAY = 0.01
    WARMUP_RATIO = 0.1
    
    SEED = 42
    OUTPUT_DIR = "./videberta_cleaned_output"
    
    # NO custom tokens needed - using native [SEP]
    SPECIAL_TOKENS = []
    
    # PhoBERT uses </s> as separator
    SEP_TOKEN = "</s>"

torch.manual_seed(Config.SEED)
np.random.seed(Config.SEED)

print("="*60)
print("CONFIGURATION (CLEANED DATA)")
print("="*60)
print(f"Model: {Config.MODEL_NAME}")
print(f"Data: final_train_data_v3_CLEANED.xlsx (SAME AS PHOBERT)")
print(f"Separator: {Config.SEP_TOKEN}")
print(f"Batch Size: {Config.BATCH_SIZE} x {Config.GRADIENT_ACCUMULATION}")
print(f"Learning Rate: {Config.LEARNING_RATE}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 3: Load Data
# ═══════════════════════════════════════════════════════════════════════════════

print("="*60)
print("LOADING DATA")
print("="*60)

# Find CLEANED data file
input_path = "/kaggle/input"
data_path = None

for dataset in os.listdir(input_path):
    dataset_path = os.path.join(input_path, dataset)
    if os.path.isdir(dataset_path):
        for file in os.listdir(dataset_path):
            if 'CLEANED' in file and file.endswith('.xlsx'):
                data_path = os.path.join(dataset_path, file)
                break
            elif file.endswith('.xlsx') and data_path is None:
                data_path = os.path.join(dataset_path, file)

print(f"📂 Using: {data_path}")

# Load data
df = pd.read_excel(data_path)
df.columns = df.columns.str.strip()

# Use training_text column
if 'training_text' not in df.columns:
    raise ValueError("Column 'training_text' not found!")

df = df[['training_text', 'label']].dropna()
df["label"] = df["label"].astype(int)

print(f"✅ Loaded: {len(df)} samples")
print(f"\n📊 Label distribution:")
print(df['label'].value_counts().sort_index())

# Check separator
sample = df['training_text'].iloc[0]
print(f"\n📝 Sample:")
print(sample[:150])
print(f"\n✅ Has </s>: {'</s>' in sample}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 4: Load Tokenizer
# ═══════════════════════════════════════════════════════════════════════════════

print("="*60)
print("LOADING TOKENIZER")
print("="*60)

tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME, use_fast=True)
print(f"✅ Tokenizer loaded: {Config.MODEL_NAME}")
print(f"   Vocab size: {len(tokenizer)}")
print(f"   Native SEP token: {tokenizer.sep_token}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 5: Tokenization Function
# ═══════════════════════════════════════════════════════════════════════════════

def tokenize_function(examples):
    """
    Split by </s> and use text_pair
    """
    raw_texts = examples["training_text"]
    
    contexts = []
    comments = []
    
    for text in raw_texts:
        text = str(text)
        
        # Split by </s> (PhoBERT separator)
        if Config.SEP_TOKEN in text:
            parts = text.split(Config.SEP_TOKEN, 1)
            context = parts[0].strip()
            comment = parts[1].strip() if len(parts) > 1 else ""
            
            contexts.append(context if context else "")
            comments.append(comment if comment else "")
        else:
            contexts.append(text.strip())
            comments.append("")
    
    # Tokenize with text_pair (uses native [SEP])
    return tokenizer(
        text=contexts,
        text_pair=comments,
        truncation=True,
        max_length=Config.MAX_LENGTH,
        padding=False
    )

print("✅ Tokenization function defined")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 6: Create Dataset
# ═══════════════════════════════════════════════════════════════════════════════

print("="*60)
print("CREATING DATASET")
print("="*60)

features = Features({
    'training_text': Value('string'),
    'label': ClassLabel(num_classes=Config.NUM_LABELS, names=['Clean', 'Toxic', 'Hate'])
})

dataset = Dataset.from_pandas(df[['training_text', 'label']], features=features)
print(f"✅ Dataset created: {len(dataset)} samples")

# Split
dataset = dataset.train_test_split(test_size=0.15, seed=Config.SEED, stratify_by_column='label')
train_dataset = dataset['train']
val_dataset = dataset['test']

print(f"✅ Train: {len(train_dataset)} samples")
print(f"✅ Val: {len(val_dataset)} samples")

# Tokenize
print("\n🔄 Tokenizing...")
train_dataset = train_dataset.map(tokenize_function, batched=True, remove_columns=['training_text'])
val_dataset = val_dataset.map(tokenize_function, batched=True, remove_columns=['training_text'])

print(f"✅ Tokenization complete")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 7: Load Model
# ═══════════════════════════════════════════════════════════════════════════════

print("="*60)
print("LOADING MODEL")
print("="*60)

model = AutoModelForSequenceClassification.from_pretrained(
    Config.MODEL_NAME,
    num_labels=Config.NUM_LABELS,
    id2label={0: "Clean", 1: "Toxic", 2: "Hate"},
    label2id={"Clean": 0, "Toxic": 1, "Hate": 2}
)

print(f"✅ Model loaded: {Config.MODEL_NAME}")
print(f"   Parameters: {sum(p.numel() for p in model.parameters()):,}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 8: Metrics
# ═══════════════════════════════════════════════════════════════════════════════

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1_macro": f1_score(labels, preds, average='macro'),
        "f1_weighted": f1_score(labels, preds, average='weighted')
    }

print("✅ Metrics function defined")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 9: Training Arguments
# ═══════════════════════════════════════════════════════════════════════════════

print("="*60)
print("SETTING UP TRAINING")
print("="*60)

training_args = TrainingArguments(
    output_dir=Config.OUTPUT_DIR,
    num_train_epochs=Config.EPOCHS,
    per_device_train_batch_size=Config.BATCH_SIZE,
    per_device_eval_batch_size=Config.BATCH_SIZE * 2,
    gradient_accumulation_steps=Config.GRADIENT_ACCUMULATION,
    learning_rate=Config.LEARNING_RATE,
    weight_decay=Config.WEIGHT_DECAY,
    warmup_ratio=Config.WARMUP_RATIO,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1_macro",
    greater_is_better=True,
    logging_steps=50,
    fp16=True,
    dataloader_num_workers=0,
    save_total_limit=2,
    seed=Config.SEED,
    report_to="none"
)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

print(f"✅ Training setup complete")
print(f"   Expected F1: 0.75-0.80 (same data as PhoBERT)")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 10: Train
# ═══════════════════════════════════════════════════════════════════════════════

print("="*60)
print("🏋️ STARTING TRAINING")
print("="*60)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)

train_result = trainer.train()

print("\n" + "="*60)
print("🏆 TRAINING COMPLETE!")
print("="*60)


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 11: Evaluate
# ═══════════════════════════════════════════════════════════════════════════════

print("="*60)
print("📊 FINAL EVALUATION")
print("="*60)

eval_results = trainer.evaluate()

print(f"\n📊 Results:")
print(f"   Loss: {eval_results['eval_loss']:.4f}")
print(f"   Accuracy: {eval_results['eval_accuracy']:.4f}")
print(f"   F1 (macro): {eval_results['eval_f1_macro']:.4f}")
print(f"   F1 (weighted): {eval_results['eval_f1_weighted']:.4f}")

predictions = trainer.predict(val_dataset)
preds = np.argmax(predictions.predictions, axis=1)
labels = predictions.label_ids

print(f"\n📋 Classification Report:")
print(classification_report(labels, preds, target_names=['Clean', 'Toxic', 'Hate']))

f1_macro = eval_results['eval_f1_macro']
print(f"\n{'='*60}")
print(f"🎯 COMPARISON:")
print(f"   PhoBERT F1: 0.792")
print(f"   ViDeBERTa F1: {f1_macro:.4f}")
print(f"   Difference: {(f1_macro - 0.792):.4f}")
print(f"{'='*60}")


# ═══════════════════════════════════════════════════════════════════════════════
# CELL 12: Save
# ═══════════════════════════════════════════════════════════════════════════════

save_path = "./videberta_toxic_final"
trainer.save_model(save_path)
tokenizer.save_pretrained(save_path)

print(f"✅ Model saved to: {save_path}")
