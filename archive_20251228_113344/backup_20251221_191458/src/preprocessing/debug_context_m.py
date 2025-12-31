from advanced_text_cleaning import context_aware_m_mapping, POSITIVE_CONTEXT, TOXIC_CONTEXT, advanced_clean_text

test = "đẹp quá yêu m"
print(f"Input: {test}")
print(f"\nPOSITIVE_CONTEXT: {sorted(POSITIVE_CONTEXT)}")
print(f"'yêu' in POSITIVE: {'yêu' in POSITIVE_CONTEXT}")

# Split and check
words = test.split()
print(f"\nWords: {words}")
print(f"Word at index 2: '{words[2]}'")

# Manual context check
context_words = set(words[:-1])  # All except 'm'
print(f"\nContext words: {context_words}")
print(f"Intersection with POSITIVE: {context_words & POSITIVE_CONTEXT}")
print(f"Intersection with TOXIC: {context_words & TOXIC_CONTEXT}")

result = context_aware_m_mapping(test)
print(f"\nOutput (context_aware only): {result}")

# Test full pipeline
result_full = advanced_clean_text(test)
print(f"Output (FULL pipeline):      {result_full}")

# Test more cases
print("\n" + "="*50)
print("More test cases:")
test_cases = [
    "yêu m nhiều",
    "anh thương m",
    "đm m ngu",
    "t yêu m"
]
for tc in test_cases:
    result_ctx = context_aware_m_mapping(tc)
    result_full = advanced_clean_text(tc)
    print(f"  {tc:20s} -> context: {result_ctx:25s} full: {result_full}")
