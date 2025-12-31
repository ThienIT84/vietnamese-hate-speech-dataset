"""
Analyze class balance after adding strategic samples
"""
import pandas as pd
import numpy as np

print("="*80)
print("📊 CLASS BALANCE ANALYSIS")
print("="*80)

# Load original training data
print("\n📂 Loading original training data...")
original_df = pd.read_excel('final_train_data_v3_TRUNCATED_20251229.xlsx')
print(f"   Original: {len(original_df)} samples")

# Load strategic samples (after your review)
print("\n📂 Loading strategic samples (after review)...")
strategic_df = pd.read_excel('STRATEGIC_SAMPLES_PROCESSED_FINAL_20251229_173802.xlsx')
print(f"   Strategic: {len(strategic_df)} samples")

# Original distribution
print("\n" + "="*80)
print("📊 ORIGINAL TRAINING DATA")
print("="*80)
orig_dist = original_df['label'].value_counts().sort_index()
print(f"\nLabel distribution:")
for label, count in orig_dist.items():
    print(f"   Label {label}: {count:>5} ({count/len(original_df)*100:>5.1f}%)")

print(f"\nTotal: {len(original_df)}")
print(f"Balance ratio (max/min): {orig_dist.max() / orig_dist.min():.2f}x")

# Strategic samples distribution
print("\n" + "="*80)
print("📊 STRATEGIC SAMPLES (AFTER YOUR REVIEW)")
print("="*80)
strat_dist = strategic_df['label'].value_counts().sort_index()
print(f"\nLabel distribution:")
for label, count in strat_dist.items():
    print(f"   Label {label}: {count:>5} ({count/len(strategic_df)*100:>5.1f}%)")

print(f"\nTotal: {len(strategic_df)}")
print(f"Balance ratio (max/min): {strat_dist.max() / strat_dist.min():.2f}x")

# Combined distribution
print("\n" + "="*80)
print("📊 COMBINED (ORIGINAL + STRATEGIC)")
print("="*80)

# Simulate merge
combined_labels = pd.concat([original_df['label'], strategic_df['label']], ignore_index=True)
combined_dist = combined_labels.value_counts().sort_index()

print(f"\nLabel distribution:")
for label in sorted(combined_dist.index):
    orig_count = orig_dist.get(label, 0)
    strat_count = strat_dist.get(label, 0)
    total_count = combined_dist[label]
    growth = ((total_count - orig_count) / orig_count * 100) if orig_count > 0 else 0
    
    print(f"   Label {label}: {orig_count:>5} + {strat_count:>4} = {total_count:>5} ({total_count/len(combined_labels)*100:>5.1f}%) [+{growth:>5.1f}%]")

print(f"\nTotal: {len(original_df)} + {len(strategic_df)} = {len(combined_labels)}")
print(f"Growth: +{len(strategic_df)/len(original_df)*100:.1f}%")

# Balance analysis
print("\n" + "="*80)
print("⚖️ BALANCE ANALYSIS")
print("="*80)

orig_ratio = orig_dist.max() / orig_dist.min()
combined_ratio = combined_dist.max() / combined_dist.min()

print(f"\nBalance ratio (max/min):")
print(f"   Original:  {orig_ratio:.2f}x")
print(f"   Combined:  {combined_ratio:.2f}x")
print(f"   Change:    {combined_ratio - orig_ratio:+.2f}x")

if combined_ratio < orig_ratio:
    print(f"\n✅ BETTER BALANCE! Ratio decreased by {orig_ratio - combined_ratio:.2f}x")
elif combined_ratio > orig_ratio:
    print(f"\n⚠️ WORSE BALANCE! Ratio increased by {combined_ratio - orig_ratio:.2f}x")
else:
    print(f"\n➡️ SAME BALANCE")

# Imbalance severity assessment
print("\n" + "="*80)
print("📈 IMBALANCE SEVERITY")
print("="*80)

def assess_imbalance(ratio):
    if ratio < 1.5:
        return "EXCELLENT", "Perfectly balanced"
    elif ratio < 2.0:
        return "GOOD", "Slightly imbalanced but acceptable"
    elif ratio < 3.0:
        return "MODERATE", "Moderately imbalanced - consider class weights"
    elif ratio < 5.0:
        return "HIGH", "Highly imbalanced - MUST use class weights/focal loss"
    else:
        return "SEVERE", "Severely imbalanced - consider resampling"

orig_severity, orig_desc = assess_imbalance(orig_ratio)
combined_severity, combined_desc = assess_imbalance(combined_ratio)

print(f"\nOriginal:")
print(f"   Severity: {orig_severity}")
print(f"   {orig_desc}")

print(f"\nCombined:")
print(f"   Severity: {combined_severity}")
print(f"   {combined_desc}")

# Recommendations
print("\n" + "="*80)
print("💡 RECOMMENDATIONS")
print("="*80)

if combined_ratio < 2.0:
    print("\n✅ Class balance is GOOD!")
    print("   - Can train with standard cross-entropy loss")
    print("   - Class weights optional but recommended")
    print("   - No need for special techniques")
elif combined_ratio < 3.0:
    print("\n⚠️ Class balance is MODERATE")
    print("   - RECOMMENDED: Use class weights")
    print("   - Consider: Focal loss with gamma=2.0")
    print("   - Monitor: Per-class F1 scores")
else:
    print("\n🚨 Class balance is POOR")
    print("   - MUST USE: Class weights")
    print("   - MUST USE: Focal loss with gamma=2.0-3.0")
    print("   - CONSIDER: Oversampling minority class")
    print("   - CONSIDER: Undersampling majority class")

# Class weights calculation
print("\n" + "="*80)
print("⚖️ RECOMMENDED CLASS WEIGHTS")
print("="*80)

from sklearn.utils.class_weight import compute_class_weight

# Compute class weights
classes = np.array([0, 1, 2])  # Fixed: use integer labels
combined_labels_clean = combined_labels.dropna().astype(int)  # Remove NaN and convert to int
weights = compute_class_weight(
    class_weight='balanced',
    classes=classes,
    y=combined_labels_clean
)

print(f"\nBalanced class weights:")
for label, weight in zip(classes, weights):
    print(f"   Label {label}: {weight:.3f}")

print(f"\nWeight ratio (max/min): {weights.max() / weights.min():.2f}x")

# Training config recommendation
print("\n" + "="*80)
print("🎯 TRAINING CONFIG RECOMMENDATION")
print("="*80)

print(f"""
Config.USE_CLASS_WEIGHTS = True
Config.LABEL_SMOOTHING = 0.1

# Class weights (copy to training script)
class_weights = torch.tensor([{weights[0]:.3f}, {weights[1]:.3f}, {weights[2]:.3f}], dtype=torch.float).to(device)

# Loss function
""")

if combined_ratio < 2.0:
    print("criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.1)")
else:
    print("# Use Focal Loss for better handling of imbalance")
    print("Config.USE_FOCAL_LOSS = True")
    print("Config.FOCAL_GAMMA = 2.0")
    print("criterion = FocalLoss(alpha=class_weights, gamma=2.0)")

print("\n✅ ANALYSIS COMPLETE!")
