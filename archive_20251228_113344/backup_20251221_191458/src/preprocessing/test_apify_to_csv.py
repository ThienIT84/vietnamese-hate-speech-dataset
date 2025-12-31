"""
Test script để kiểm tra apify_to_csv.py

Chạy test này để đảm bảo:
1. Emoji mapping hoạt động đúng
2. Context building đúng format
3. Truncation hoạt động
"""

import sys
import os

# Add path để import
sys.path.append(os.path.dirname(__file__))

from apify_to_csv import (
    clean_text_with_emoji, 
    build_input_text,
    EMOJI_MAP
)

def test_emoji_mapping():
    """Test emoji được chuyển thành text"""
    print("="*80)
    print("TEST 1: EMOJI MAPPING")
    print("="*80)
    
    test_cases = [
        ("Tôi yêu bạn ❤️", "Tôi yêu bạn  yêu "),
        ("🏳️‍🌈 pride month", " đồng tính  pride month"),
        ("💔 chia tay rồi", " chia tay  chia tay rồi"),
    ]
    
    for input_text, expected_contains in test_cases:
        result = clean_text_with_emoji(input_text)
        print(f"\nInput:  {input_text}")
        print(f"Output: {result}")
        print(f"✓ Pass" if expected_contains.lower() in result.lower() else "✗ Fail")

def test_hashtag_removal():
    """Test hashtag được xóa"""
    print("\n" + "="*80)
    print("TEST 2: HASHTAG REMOVAL")
    print("="*80)
    
    test_cases = [
        "#fyp #xuhuong mày béo vậy",
        "#confession tôi thích bạn",
        "Video hay #viral #trending",
    ]
    
    for text in test_cases:
        result = clean_text_with_emoji(text)
        print(f"\nInput:  {text}")
        print(f"Output: {result}")
        has_hashtag = '#' in result
        print(f"{'✗ Fail - vẫn còn hashtag' if has_hashtag else '✓ Pass - đã xóa hashtag'}")

def test_context_building():
    """Test build input_text với context"""
    print("\n" + "="*80)
    print("TEST 3: CONTEXT BUILDING")
    print("="*80)
    
    test_cases = [
        {
            "title": "Hằng Du Mục về Việt Nam",
            "comment": "Cảm ơn chị đã chia sẻ",
            "expected_format": "title </s> comment"
        },
        {
            "title": "",
            "comment": "Comment không có title",
            "expected_format": "comment only"
        },
        {
            "title": "Title dài " * 20,  # Title rất dài
            "comment": "Comment ngắn",
            "expected_format": "truncated title </s> comment"
        },
    ]
    
    for idx, case in enumerate(test_cases, 1):
        title = case["title"]
        comment = case["comment"]
        result = build_input_text(title, comment)
        
        print(f"\n--- Test case {idx} ---")
        print(f"Title:   {title[:50]}..." if len(title) > 50 else f"Title:   {title}")
        print(f"Comment: {comment[:50]}...")
        print(f"Result:  {result[:100]}...")
        
        # Kiểm tra format
        if case["expected_format"] == "comment only":
            has_separator = "</s>" in result
            print(f"{'✗ Fail - không nên có </s>' if has_separator else '✓ Pass - comment only'}")
        else:
            has_separator = "</s>" in result
            print(f"{'✓ Pass - có separator' if has_separator else '✗ Fail - thiếu </s>'}")

def test_teencode_normalization():
    """Test teencode được normalize"""
    print("\n" + "="*80)
    print("TEST 4: TEENCODE NORMALIZATION")
    print("="*80)
    
    test_cases = [
        "vcl bạn ơi",
        "đcm mày làm gì vậy",
        "tml biết gì không",
    ]
    
    for text in test_cases:
        result = clean_text_with_emoji(text)
        print(f"\nInput:  {text}")
        print(f"Output: {result}")
        print("✓ Normalized" if result != text else "✗ No change")

def test_full_pipeline():
    """Test full pipeline như trong thực tế"""
    print("\n" + "="*80)
    print("TEST 5: FULL PIPELINE")
    print("="*80)
    
    # Giả lập data từ JSON
    mock_facebook_comment = {
        "postTitle": "Hằng Du Mục về Việt Nam 🏳️‍🌈",
        "text": "#fyp mày béo như lợn vcl 💔",
    }
    
    print("\nMock Facebook Comment:")
    print(f"  Title: {mock_facebook_comment['postTitle']}")
    print(f"  Text:  {mock_facebook_comment['text']}")
    
    # Process
    title_cleaned = clean_text_with_emoji(mock_facebook_comment['postTitle'])
    comment_cleaned = clean_text_with_emoji(mock_facebook_comment['text'])
    input_text = build_input_text(title_cleaned, comment_cleaned)
    
    print("\nProcessed:")
    print(f"  Title cleaned:   {title_cleaned}")
    print(f"  Comment cleaned: {comment_cleaned}")
    print(f"  Input text:      {input_text}")
    
    # Kiểm tra
    checks = {
        "Emoji converted": "đồng tính" in input_text.lower() or "chia tay" in input_text.lower(),
        "Hashtag removed": "#" not in input_text,
        "Has separator": "</s>" in input_text,
        "Title first": input_text.index("hằng") < input_text.index("mày") if "hằng" in input_text.lower() and "mày" in input_text.lower() else False,
    }
    
    print("\nChecks:")
    for check_name, passed in checks.items():
        print(f"  {check_name}: {'✓ Pass' if passed else '✗ Fail'}")

def main():
    """Run all tests"""
    print("\n")
    print("🧪 TESTING apify_to_csv.py")
    print("="*80)
    print(f"Emoji mapping: {len(EMOJI_MAP)} emojis")
    print("="*80)
    
    try:
        test_emoji_mapping()
        test_hashtag_removal()
        test_context_building()
        test_teencode_normalization()
        test_full_pipeline()
        
        print("\n" + "="*80)
        print("✅ TẤT CẢ TESTS HOÀN TẤT")
        print("="*80)
        print("\nNếu tất cả đều PASS, script đã sẵn sàng sử dụng!")
        print("Chạy: python apify_to_csv.py")
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
