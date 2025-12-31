"""
Truncate long titles in training data - keep last 50 words
"""
import pandas as pd
from datetime import datetime

# Load data
df = pd.read_csv('final_train_data_v3_AUGMENTED_20251229_112040.csv')
print(f"✅ Loaded: {len(df)} rows")

# Backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'backup_before_truncate_{timestamp}.csv'
df.to_csv(backup_file, index=False, encoding='utf-8-sig')
print(f"💾 Backup: {backup_file}")

# Function to truncate title
def truncate_title(text, max_words=50):
    """Keep last max_words of title before </s>"""
    if pd.isna(text) or '</s>' not in text:
        return text
    
    parts = text.split('</s>', 1)
    title = parts[0].strip()
    comment = parts[1].strip() if len(parts) > 1 else ''
    
    words = title.split()
    if len(words) > max_words:
        # Keep last 50 words (most important context)
        truncated_title = ' '.join(words[-max_words:])
        return f"{truncated_title} </s> {comment}"
    
    return text

# Count before
titles_before = df['training_text'].str.split('</s>').str[0]
word_counts_before = titles_before.str.split().str.len()
long_titles_before = (word_counts_before > 50).sum()

print(f"\n📊 BEFORE:")
print(f"   Titles > 50 words: {long_titles_before}")
print(f"   Max words: {word_counts_before.max():.0f}")
print(f"   Mean words: {word_counts_before.mean():.1f}")

# Truncate
df['training_text'] = df['training_text'].apply(truncate_title)

# Count after
titles_after = df['training_text'].str.split('</s>').str[0]
word_counts_after = titles_after.str.split().str.len()
long_titles_after = (word_counts_after > 50).sum()

print(f"\n📊 AFTER:")
print(f"   Titles > 50 words: {long_titles_after}")
print(f"   Max words: {word_counts_after.max():.0f}")
print(f"   Mean words: {word_counts_after.mean():.1f}")

# Save
output_csv = 'final_train_data_v3_TRUNCATED_20251229.csv'
output_xlsx = 'final_train_data_v3_TRUNCATED_20251229.xlsx'

df.to_csv(output_csv, index=False, encoding='utf-8-sig')
df.to_excel(output_xlsx, index=False, engine='openpyxl')

print(f"\n💾 Saved:")
print(f"   {output_csv}")
print(f"   {output_xlsx}")
print(f"\n✅ DONE! Reduced {long_titles_before} long titles to {long_titles_after}")
