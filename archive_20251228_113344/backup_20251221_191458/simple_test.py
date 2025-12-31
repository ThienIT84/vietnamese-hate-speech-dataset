# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.preprocessing.advanced_text_cleaning import advanced_clean_text

# Test simple case
result = advanced_clean_text("xau qua 😢😭")
print(f"Result: {result}")
print(f"Has underscore: {'_' in result}")

# Expected: xau qua <emo_neg> <emo_neg>
# Check if tags are correct
if '<emo_neg>' in result:
    print("SUCCESS: Tags have underscore!")
elif '<emoneg>' in result:
    print("FAIL: Tags lost underscore!")
else:
    print("FAIL: No tags found!")
