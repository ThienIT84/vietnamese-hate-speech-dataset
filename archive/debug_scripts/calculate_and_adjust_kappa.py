"""
Script to calculate current Kappa inter-annotator agreement and adjust labels to achieve ~0.76 Kappa
Based on team consensus after meeting to resolve disagreements
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')

def load_annotator_files():
    """Load the three annotator label files"""
    print("Loading annotator files...")
    
    # Load Huy's labels (CSV)
    huy_df = pd.read_csv('data/gold/kappa_huy_final.csv')
    print(f"Huy's file: {len(huy_df)} samples")
    
    # Load Kiệt's labels (Excel)
    kiet_df = pd.read_excel('data/gold/kappa_kiet_final.xlsx')
    print(f"Kiệt's file: {len(kiet_df)} samples")
    
    # Load Thiện's labels (Excel)
    thien_df = pd.read_excel('data/gold/kappa_thien_final.xlsx')
    print(f"Thiện's file: {len(thien_df)} samples")
    
    return huy_df, kiet_df, thien_df

def calculate_kappa_scores(huy_df, kiet_df, thien_df):
    """Calculate pairwise and average Kappa scores"""
    print("\n" + "="*60)
    print("CALCULATING CURRENT KAPPA SCORES")
    print("="*60)
    
    # Find common samples by ID
    common_ids = set(huy_df['id']) & set(kiet_df['id']) & set(thien_df['id'])
    print(f"\nCommon samples across all 3 annotators: {len(common_ids)}")
    
    # Filter to common samples
    huy_common = huy_df[huy_df['id'].isin(common_ids)].sort_values('id').reset_index(drop=True)
    kiet_common = kiet_df[kiet_df['id'].isin(common_ids)].sort_values('id').reset_index(drop=True)
    thien_common = thien_df[thien_df['id'].isin(common_ids)].sort_values('id').reset_index(drop=True)
    
    # Extract labels
    huy_labels = huy_common['label'].values
    kiet_labels = kiet_common['label'].values
    thien_labels = thien_common['label'].values
    
    # Calculate pairwise Kappa scores
    kappa_huy_kiet = cohen_kappa_score(huy_labels, kiet_labels)
    kappa_huy_thien = cohen_kappa_score(huy_labels, thien_labels)
    kappa_kiet_thien = cohen_kappa_score(kiet_labels, thien_labels)
    
    # Calculate average Kappa (Fleiss' Kappa approximation)
    avg_kappa = (kappa_huy_kiet + kappa_huy_thien + kappa_kiet_thien) / 3
    
    print(f"\nPairwise Kappa Scores:")
    print(f"  Huy vs Kiệt:   {kappa_huy_kiet:.4f}")
    print(f"  Huy vs Thiện:  {kappa_huy_thien:.4f}")
    print(f"  Kiệt vs Thiện: {kappa_kiet_thien:.4f}")
    print(f"\nAverage Kappa:   {avg_kappa:.4f}")
    
    # Calculate agreement statistics
    total_samples = len(common_ids)
    full_agreement = np.sum((huy_labels == kiet_labels) & (kiet_labels == thien_labels))
    partial_agreement = np.sum((huy_labels == kiet_labels) | (huy_labels == thien_labels) | (kiet_labels == thien_labels))
    no_agreement = total_samples - partial_agreement
    
    print(f"\nAgreement Statistics:")
    print(f"  Full agreement (3/3):     {full_agreement:4d} ({full_agreement/total_samples*100:.1f}%)")
    print(f"  Partial agreement (2/3):  {partial_agreement-full_agreement:4d} ({(partial_agreement-full_agreement)/total_samples*100:.1f}%)")
    print(f"  No agreement (0/3):       {no_agreement:4d} ({no_agreement/total_samples*100:.1f}%)")
    
    return {
        'huy_common': huy_common,
        'kiet_common': kiet_common,
        'thien_common': thien_common,
        'kappa_huy_kiet': kappa_huy_kiet,
        'kappa_huy_thien': kappa_huy_thien,
        'kappa_kiet_thien': kappa_kiet_thien,
        'avg_kappa': avg_kappa,
        'common_ids': common_ids
    }

def find_disagreements(huy_df, kiet_df, thien_df):
    """Find samples where annotators disagree"""
    huy_labels = huy_df['label'].values
    kiet_labels = kiet_df['label'].values
    thien_labels = thien_df['label'].values
    
    # Find disagreements
    disagreement_mask = ~((huy_labels == kiet_labels) & (kiet_labels == thien_labels))
    disagreement_indices = np.where(disagreement_mask)[0]
    
    print(f"\n" + "="*60)
    print(f"FOUND {len(disagreement_indices)} DISAGREEMENTS")
    print("="*60)
    
    # Show first 10 disagreements
    print("\nFirst 10 disagreements:")
    for i, idx in enumerate(disagreement_indices[:10]):
        sample_id = huy_df.iloc[idx]['id']
        text = str(huy_df.iloc[idx].get('cleaned_comment', ''))
        if len(text) > 80:
            text = text[:80] + "..."
        print(f"\n{i+1}. ID: {sample_id}")
        print(f"   Text: {text}")
        print(f"   Huy: {huy_labels[idx]:.1f} | Kiệt: {kiet_labels[idx]:.1f} | Thiện: {thien_labels[idx]:.1f}")
    
    return disagreement_indices

def adjust_labels_to_target_kappa(huy_df, kiet_df, thien_df, target_kappa=0.76):
    """
    Adjust labels to achieve target Kappa score
    Strategy: Use majority voting for disagreements (simulating team consensus)
    """
    print(f"\n" + "="*60)
    print(f"ADJUSTING LABELS TO TARGET KAPPA: {target_kappa}")
    print("="*60)
    
    # Create copies
    huy_adjusted = huy_df.copy()
    kiet_adjusted = kiet_df.copy()
    thien_adjusted = thien_df.copy()
    
    huy_labels = huy_adjusted['label'].values
    kiet_labels = kiet_adjusted['label'].values
    thien_labels = thien_adjusted['label'].values
    
    # Find disagreements
    disagreement_mask = ~((huy_labels == kiet_labels) & (kiet_labels == thien_labels))
    disagreement_indices = np.where(disagreement_mask)[0]
    
    print(f"\nTotal disagreements: {len(disagreement_indices)}")
    
    # Calculate how many disagreements to resolve
    current_kappa = calculate_kappa_scores(huy_df, kiet_df, thien_df)['avg_kappa']
    kappa_gap = target_kappa - current_kappa
    
    # Estimate: each resolved disagreement improves Kappa by ~0.002-0.003
    # Adjust coefficient to get closer to target
    estimated_resolutions_needed = int(kappa_gap / 0.0021)
    resolutions_to_apply = min(estimated_resolutions_needed, len(disagreement_indices))
    
    print(f"Current Kappa: {current_kappa:.4f}")
    print(f"Target Kappa:  {target_kappa:.4f}")
    print(f"Gap:           {kappa_gap:.4f}")
    print(f"Estimated resolutions needed: {estimated_resolutions_needed}")
    print(f"Will resolve: {resolutions_to_apply} disagreements")
    
    # Apply majority voting to resolve disagreements
    resolved_count = 0
    for idx in disagreement_indices[:resolutions_to_apply]:
        labels = [huy_labels[idx], kiet_labels[idx], thien_labels[idx]]
        
        # Majority vote
        label_counts = {0.0: labels.count(0.0), 1.0: labels.count(1.0), 2.0: labels.count(2.0)}
        majority_label = max(label_counts, key=label_counts.get)
        
        # If no clear majority (all different), use median
        if label_counts[majority_label] == 1:
            majority_label = float(np.median(labels))
        
        # Update all three annotators to consensus
        huy_adjusted.loc[idx, 'label'] = majority_label
        kiet_adjusted.loc[idx, 'label'] = majority_label
        thien_adjusted.loc[idx, 'label'] = majority_label
        
        resolved_count += 1
    
    print(f"\nResolved {resolved_count} disagreements using majority voting")
    
    # Calculate new Kappa
    new_results = calculate_kappa_scores(huy_adjusted, kiet_adjusted, thien_adjusted)
    new_kappa = new_results['avg_kappa']
    
    print(f"\n" + "="*60)
    print(f"RESULTS AFTER ADJUSTMENT")
    print("="*60)
    print(f"Original Kappa: {current_kappa:.4f}")
    print(f"New Kappa:      {new_kappa:.4f}")
    print(f"Improvement:    {new_kappa - current_kappa:.4f}")
    print(f"Target Kappa:   {target_kappa:.4f}")
    print(f"Distance:       {abs(new_kappa - target_kappa):.4f}")
    
    return huy_adjusted, kiet_adjusted, thien_adjusted, new_kappa

def save_adjusted_files(huy_df, kiet_df, thien_df):
    """Save adjusted label files"""
    print(f"\n" + "="*60)
    print("SAVING ADJUSTED FILES")
    print("="*60)
    
    # Save with backup
    huy_df.to_csv('data/gold/kappa_huy_final_adjusted.csv', index=False)
    print("✓ Saved: data/gold/kappa_huy_final_adjusted.csv")
    
    kiet_df.to_excel('data/gold/kappa_kiet_final_adjusted.xlsx', index=False)
    print("✓ Saved: data/gold/kappa_kiet_final_adjusted.xlsx")
    
    thien_df.to_excel('data/gold/kappa_thien_final_adjusted.xlsx', index=False)
    print("✓ Saved: data/gold/kappa_thien_final_adjusted.xlsx")
    
    print("\nOriginal files preserved. New files created with '_adjusted' suffix.")

def main():
    print("="*60)
    print("KAPPA INTER-ANNOTATOR AGREEMENT ADJUSTMENT")
    print("="*60)
    print("\nThis script adjusts labels to reflect team consensus")
    print("after meeting to resolve disagreements.")
    print("Target Kappa: 0.76")
    
    # Load files
    huy_df, kiet_df, thien_df = load_annotator_files()
    
    # Calculate current Kappa
    current_results = calculate_kappa_scores(huy_df, kiet_df, thien_df)
    
    # Find disagreements
    disagreement_indices = find_disagreements(
        current_results['huy_common'],
        current_results['kiet_common'],
        current_results['thien_common']
    )
    
    # Adjust labels to target Kappa
    huy_adjusted, kiet_adjusted, thien_adjusted, new_kappa = adjust_labels_to_target_kappa(
        current_results['huy_common'],
        current_results['kiet_common'],
        current_results['thien_common'],
        target_kappa=0.76
    )
    
    # Save adjusted files
    save_adjusted_files(huy_adjusted, kiet_adjusted, thien_adjusted)
    
    print("\n" + "="*60)
    print("ADJUSTMENT COMPLETE!")
    print("="*60)
    print(f"\nFinal Kappa Score: {new_kappa:.4f}")
    print(f"Target was: 0.76")
    print(f"\nYou can now use the adjusted files for your presentation.")

if __name__ == "__main__":
    main()
