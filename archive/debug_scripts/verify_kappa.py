"""
Verification script to calculate Kappa inter-annotator agreement
"""

import pandas as pd
from sklearn.metrics import cohen_kappa_score

def verify_kappa(file_prefix=""):
    """Calculate Kappa scores from the three annotator files"""
    
    suffix = "_adjusted" if file_prefix else ""
    
    print(f"\n{'='*60}")
    print(f"VERIFYING KAPPA SCORES{' (ADJUSTED FILES)' if suffix else ' (ORIGINAL FILES)'}")
    print(f"{'='*60}\n")
    
    # Load files
    huy_df = pd.read_csv(f'data/gold/kappa_huy_final{suffix}.csv')
    kiet_df = pd.read_excel(f'data/gold/kappa_kiet_final{suffix}.xlsx')
    thien_df = pd.read_excel(f'data/gold/kappa_thien_final{suffix}.xlsx')
    
    print(f"Loaded files:")
    print(f"  Huy:   {len(huy_df)} samples")
    print(f"  Kiệt:  {len(kiet_df)} samples")
    print(f"  Thiện: {len(thien_df)} samples")
    
    # Find common samples
    common_ids = set(huy_df['id']) & set(kiet_df['id']) & set(thien_df['id'])
    print(f"\nCommon samples: {len(common_ids)}")
    
    # Filter and sort
    huy_common = huy_df[huy_df['id'].isin(common_ids)].sort_values('id').reset_index(drop=True)
    kiet_common = kiet_df[kiet_df['id'].isin(common_ids)].sort_values('id').reset_index(drop=True)
    thien_common = thien_df[thien_df['id'].isin(common_ids)].sort_values('id').reset_index(drop=True)
    
    # Extract labels
    huy_labels = huy_common['label'].values
    kiet_labels = kiet_common['label'].values
    thien_labels = thien_common['label'].values
    
    # Calculate pairwise Kappa
    kappa_huy_kiet = cohen_kappa_score(huy_labels, kiet_labels)
    kappa_huy_thien = cohen_kappa_score(huy_labels, thien_labels)
    kappa_kiet_thien = cohen_kappa_score(kiet_labels, thien_labels)
    
    # Average Kappa
    avg_kappa = (kappa_huy_kiet + kappa_huy_thien + kappa_kiet_thien) / 3
    
    print(f"\n{'='*60}")
    print("KAPPA SCORES")
    print(f"{'='*60}")
    print(f"\nPairwise Kappa:")
    print(f"  Huy vs Kiệt:   {kappa_huy_kiet:.4f}")
    print(f"  Huy vs Thiện:  {kappa_huy_thien:.4f}")
    print(f"  Kiệt vs Thiện: {kappa_kiet_thien:.4f}")
    print(f"\n{'='*60}")
    print(f"AVERAGE KAPPA: {avg_kappa:.4f}")
    print(f"{'='*60}\n")
    
    # Agreement statistics
    import numpy as np
    full_agreement = np.sum((huy_labels == kiet_labels) & (kiet_labels == thien_labels))
    total = len(common_ids)
    
    print(f"Agreement Statistics:")
    print(f"  Full agreement (3/3): {full_agreement}/{total} ({full_agreement/total*100:.1f}%)")
    print(f"  Disagreements:        {total-full_agreement}/{total} ({(total-full_agreement)/total*100:.1f}%)")
    
    return avg_kappa

if __name__ == "__main__":
    print("\n" + "="*60)
    print("KAPPA INTER-ANNOTATOR AGREEMENT VERIFICATION")
    print("="*60)
    
    # Verify original files
    print("\n1. ORIGINAL FILES:")
    original_kappa = verify_kappa()
    
    # Verify adjusted files
    print("\n2. ADJUSTED FILES (After Team Consensus):")
    adjusted_kappa = verify_kappa("_adjusted")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Original Kappa: {original_kappa:.4f}")
    print(f"Adjusted Kappa: {adjusted_kappa:.4f}")
    print(f"Improvement:    {adjusted_kappa - original_kappa:.4f}")
    print("\nThe adjusted files reflect team consensus after meeting")
    print("to resolve disagreements through discussion.")
    print("="*60 + "\n")
