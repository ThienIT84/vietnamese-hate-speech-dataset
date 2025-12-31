# ═══════════════════════════════════════════════════════════════════════════════
# CELL 3: Configuration (COMPLETE - FIX ALL ERRORS)
# ═══════════════════════════════════════════════════════════════════════════════

import torch
import random
import numpy as np
import os

class Config:
    # Model - ViDeBERTa
    MODEL_NAME = "Fsoft-AIC/videberta-base"
    NUM_LABELS = 3
    MAX_LENGTH = 512  # ViDeBERTa supports longer context!
    
    # Training
    BATCH_SIZE = 8  # ← REDUCED for memory (was 16)
    GRADIENT_ACCUMULATION_STEPS = 4  # ← INCREASED (was 2) - effective batch = 32
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
    DATA_PATH = None  # Will be set automatically
    OUTPUT_DIR = 'videberta_toxic_model'
    MODEL_SAVE_PATH = 'videberta_toxic_model'
    
    # Special tokens (CRITICAL for ViDeBERTa!)
    SPECIAL_TOKENS = [
        '<sep>',      # Semantic separator (title/comment boundary)
        '<emo_pos>',  # Positive emoji
        '<emo_neg>',  # Negative emoji
        '<person>',   # Person mention
        '<user>'      # User mention
    ]

# Set random seed for reproducibility
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

set_seed(Config.SEED)

# Create output directory
import os
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

print('='*80)
print('CONFIGURATION')
print('='*80)
print(f'🔧 Device: {Config.DEVICE}')
print(f'🔧 Model: {Config.MODEL_NAME}')
print(f'🔧 Max Length: {Config.MAX_LENGTH} tokens (2x PhoBERT!)')
print(f'🔧 Batch Size: {Config.BATCH_SIZE} x {Config.GRADIENT_ACCUMULATION_STEPS} = {Config.BATCH_SIZE * Config.GRADIENT_ACCUMULATION_STEPS}')
print(f'🔧 Epochs: {Config.EPOCHS}')
print(f'🔧 Learning Rate: {Config.LEARNING_RATE}')
print(f'🔧 Output Dir: {Config.OUTPUT_DIR}')
print(f'🔧 Special Tokens: {len(Config.SPECIAL_TOKENS)}')
print('✅ Configuration set!')
