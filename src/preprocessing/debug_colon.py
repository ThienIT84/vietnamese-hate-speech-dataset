import sys
sys.stdout.reconfigure(encoding='utf-8')

from advanced_text_cleaning import *

test = "Thạch Trang my20s: Bộ Mặt Thật"
print(f"Original: [{test}]")
print()

# Step by step
text = test

text = normalize_unicode_nfc(text)
print(f"After normalize_unicode_nfc: [{text}]")

text = remove_urls(text)
print(f"After remove_urls: [{text}]")

text = remove_html(text)
print(f"After remove_html: [{text}]")

text = remove_hashtags(text)
print(f"After remove_hashtags: [{text}]")

text = remove_mentions(text)
print(f"After remove_mentions: [{text}]")

text = replace_person_names(text)
print(f"After replace_person_names: [{text}]")

text = text.replace('<user>', '___USER___')
text = text.replace('<person>', '___PERSON___')
print(f"After protect tags: [{text}]")

text = text.lower()
print(f"After lowercase: [{text}]")

text = text.replace('___user___', '<user>')
text = text.replace('___person___', '<person>')
print(f"After restore tags: [{text}]")

text = remove_emojis(text)
print(f"After remove_emojis: [{text}]")

text = remove_text_emoticons(text)
print(f"After remove_text_emoticons: [{text}]")

text = map_english_insults(text)
print(f"After map_english_insults: [{text}]")

text = normalize_unicode(text)
print(f"After normalize_unicode: [{text}]")

text = remove_bypass_patterns(text)
print(f"After remove_bypass_patterns: [{text}]")

text = convert_leetspeak(text)
print(f"After convert_leetspeak: [{text}]")

text = remove_repeated_chars(text)
print(f"After remove_repeated_chars: [{text}]")

text = context_aware_m_mapping(text)
print(f"After context_aware_m_mapping: [{text}]")

text = normalize_teencode(text)
print(f"After normalize_teencode: [{text}]")

text = normalize_punctuation(text)
print(f"After normalize_punctuation: [{text}]")

text = normalize_whitespace(text)
print(f"After normalize_whitespace: [{text}]")

print()
print(f"Final: [{text}]")
