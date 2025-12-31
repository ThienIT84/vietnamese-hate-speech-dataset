# -*- coding: utf-8 -*-
from src.preprocessing.advanced_text_cleaning import EMOJI_SENTIMENT, ENGLISH_INSULTS

print("=== EMOJI_SENTIMENT ===")
for emoji, tag in list(EMOJI_SENTIMENT.items())[:5]:
    print(f"{repr(emoji)}: {repr(tag)}")

print("\n=== ENGLISH_INSULTS ===")
for word, tag in list(ENGLISH_INSULTS.items())[:3]:
    print(f"{repr(word)}: {repr(tag)}")
