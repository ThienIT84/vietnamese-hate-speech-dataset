"""
🧪 TEST SUITE: Teencode Intensity Preservation (V7.2)
Author: Senior AI Engineer
Date: 2025-12-27
Purpose: Verify that TEENCODE_INTENSITY_SENSITIVE words are preserved correctly

Test Philosophy:
- Preserve "đm" (slang) to distinguish from "địt mẹ" (explicit)
- Maintain morphology for PhoBERT to learn intensity gradient
- Improve F1-Macro for Label 0 (Khẩu ngữ) vs Label 1 (Dung tục)
"""

import sys
sys.path.append('c:\\Học sâu\\Dataset')

from src.preprocessing.advanced_text_cleaning import clean_text, normalize_teencode

# =====================================================
# TEST CASES
# =====================================================

test_cases = [
    # ===== CASE 1: Positive Slang (Label 0) - "đm" preserved =====
    {
        'id': 1,
        'input': "Đẹp đm luôn á, xinh quá",
        'expected_keywords': ["đm"],  # Should preserve "đm"
        'should_not_contain': ["địt mẹ"],  # Should NOT expand to "địt mẹ"
        'label': 0,
        'reason': "đm in positive context = slang, not insult"
    },
    
    # ===== CASE 2: Positive Slang with vcl =====
    {
        'id': 2,
        'input': "Giỏi vcl, tài năng thật",
        'expected_keywords': ["vcl"],  # Should preserve "vcl"
        'should_not_contain': ["vãi lồn"],
        'label': 0,
        'reason': "vcl in praise context = slang intensifier"
    },
    
    # ===== CASE 3: Explicit Insult (Label 1) - already explicit =====
    {
        'id': 3,
        'input': "Địt mẹ mày ngu vl",
        'expected_keywords': ["địt mẹ", "mày", "ngu", "vl"],
        'should_not_contain': [],
        'label': 1,
        'reason': "Explicit form already present, preserve all toxic words"
    },
    
    # ===== CASE 4: Neutral normalization still works =====
    {
        'id': 4,
        'input': "Ko biết j hết, cx bthg thôi",
        'expected_keywords': ["không", "gì", "cũng", "bình thường"],
        'should_not_contain': ["ko", "j", "cx", "bthg"],
        'label': 0,
        'reason': "Neutral words normalized correctly"
    },
    
    # ===== CASE 5: Mixed - neutral + intensity =====
    {
        'id': 5,
        'input': "Ko hiểu sao mày ngu vl",
        'expected_keywords': ["không", "hiểu", "sao", "mày", "ngu", "vl"],
        'should_not_contain': ["ko"],  # "ko" should be normalized
        'label': 1,
        'reason': "Neutral words normalized, toxic words preserved"
    },
    
    # ===== CASE 6: Regional discrimination preserved =====
    {
        'id': 6,
        'input': "Mấy thằng parky về Bắc đi",
        'expected_keywords': ["mấy", "thằng", "parky"],  # parky preserved
        'should_not_contain': ["bắc kỳ"],  # Should NOT expand
        'label': 2,
        'reason': "parky preserved for hate speech detection"
    },
    
    # ===== CASE 7: Death metaphor preserved =====
    {
        'id': 7,
        'input': "Đăng xuất đi mày",
        'expected_keywords': ["đăng xuất", "mày"],
        'should_not_contain': [],
        'label': 1,
        'reason': "Death metaphor preserved for threat detection"
    },
    
    # ===== CASE 8: Complex positive slang =====
    {
        'id': 8,
        'input': "Đẹp đm, xinh vcl, yêu quá đi",
        'expected_keywords': ["đẹp", "đm", "xinh", "vcl", "yêu", "quá"],
        'should_not_contain': ["địt mẹ", "vãi lồn"],
        'label': 0,
        'reason': "Multiple slang intensifiers in positive context"
    },
    
    # ===== CASE 9: Neutral with context =====
    {
        'id': 9,
        'input': "T ko biết m là ai",
        'expected_keywords': ["tôi", "không", "biết"],
        'should_not_contain': ["t", "ko"],
        'label': 0,
        'reason': "Neutral pronouns and negation normalized"
    },
    
    # ===== CASE 10: Body parts preserved =====
    {
        'id': 10,
        'input': "Cái lồn gì vậy",
        'expected_keywords': ["cái", "lồn", "gì", "vậy"],
        'should_not_contain': [],
        'label': 1,
        'reason': "Body parts preserved for vulgarity detection"
    },
]

# =====================================================
# TEST RUNNER
# =====================================================

def run_tests():
    """Run all test cases and report results"""
    print("=" * 70)
    print("🧪 TEENCODE INTENSITY PRESERVATION TEST SUITE")
    print("=" * 70)
    print()
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        print(f"Test #{test['id']}: {test['reason']}")
        print(f"  Input:  {test['input']}")
        
        # Clean text
        output = clean_text(test['input'])
        print(f"  Output: {output}")
        
        # Check expected keywords
        success = True
        for keyword in test['expected_keywords']:
            if keyword.lower() not in output.lower():
                print(f"  ❌ FAIL: Expected keyword '{keyword}' not found")
                success = False
        
        # Check should_not_contain
        for keyword in test['should_not_contain']:
            if keyword.lower() in output.lower():
                print(f"  ❌ FAIL: Unwanted keyword '{keyword}' found")
                success = False
        
        if success:
            print(f"  ✅ PASS (Label {test['label']})")
            passed += 1
        else:
            failed += 1
        
        print()
    
    # Summary
    print("=" * 70)
    print(f"📊 TEST SUMMARY")
    print("=" * 70)
    print(f"Total: {len(test_cases)} tests")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {passed/len(test_cases)*100:.1f}%")
    print()
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Intensity preservation is working correctly.")
    else:
        print("⚠️ Some tests failed. Please review the implementation.")
    
    return passed, failed

# =====================================================
# DETAILED ANALYSIS
# =====================================================

def analyze_intensity_preservation():
    """Analyze how intensity preservation affects different contexts"""
    print("=" * 70)
    print("📊 INTENSITY PRESERVATION ANALYSIS")
    print("=" * 70)
    print()
    
    examples = [
        ("Đẹp đm", "Positive Slang"),
        ("Địt mẹ mày", "Explicit Insult"),
        ("Giỏi vcl", "Positive Slang"),
        ("Ngu vcl", "Negative Insult"),
        ("Ko biết", "Neutral"),
    ]
    
    for text, context in examples:
        output = clean_text(text)
        print(f"{context:20s} | {text:20s} → {output}")
    
    print()
    print("Key Insight:")
    print("- 'đm' preserved → PhoBERT learns context dependency")
    print("- 'vcl' preserved → Distinguishes praise vs insult by surrounding words")
    print("- Neutral words normalized → Reduces vocabulary size without losing signal")
    print()

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    # Run tests
    passed, failed = run_tests()
    
    # Run analysis
    analyze_intensity_preservation()
    
    # Exit code
    sys.exit(0 if failed == 0 else 1)
