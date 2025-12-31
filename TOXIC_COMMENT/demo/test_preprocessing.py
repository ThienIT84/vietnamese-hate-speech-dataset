"""
Test script để kiểm tra preprocessing với teencode
"""
import sys
import os
from pathlib import Path

# Fix encoding for Windows terminal
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.preprocessing.advanced_text_cleaning import clean_text

# Test cases với teencode
test_cases = [
    {
        "input": "Đ.m nguuuu vcl 😡",
        "description": "Bypass pattern + repeated chars + emoji"
    },
    {
        "input": "chị ak Trần Ngọc đẹp quá 😍",
        "description": "Teencode + person name + positive emoji"
    },
    {
        "input": "Thằng parky đó ngu vl khốn nạn",
        "description": "Regional discrimination + insult"
    },
    {
        "input": "ko biết ns gì luôn ạ",
        "description": "Neutral teencode normalization"
    },
    {
        "input": "m yêu t k?",
        "description": "Context-aware 'm' mapping (positive context)"
    },
    {
        "input": "m ngu vcl đéo biết gì",
        "description": "Context-aware 'm' mapping (toxic context)"
    },
    {
        "input": "Anh Tuấn và chị Hoa đi du lịch Hà Nội",
        "description": "Person names with titles + location"
    },
    {
        "input": "Đáng bị tử hình hết bọn đồ khốn nạn",
        "description": "Death reference + insult"
    },
    {
        "input": "LGBT là người bình thường mà",
        "description": "Identity group mention"
    },
    {
        "input": "Stupid idiot fuck you 🖕",
        "description": "English insults + negative emoji"
    },
]

def test_preprocessing():
    """Run test cases and display results"""
    print("=" * 80)
    print("TEST PREPROCESSING WITH TEENCODE NORMALIZATION")
    print("=" * 80)
    
    for i, test in enumerate(test_cases, 1):
        input_text = test["input"]
        description = test["description"]
        
        print(f"\n[TEST {i}] {description}")
        print(f"INPUT:  {input_text}")
        
        cleaned = clean_text(input_text)
        print(f"OUTPUT: {cleaned}")
        print("-" * 80)
    
    print("\n✅ All tests completed!")
    
    # Test with title + comment format
    print("\n" + "=" * 80)
    print("TEST TITLE + COMMENT FORMAT")
    print("=" * 80)
    
    title = "Vụ án tham nhũng nghiêm trọng"
    comment = "Đáng bị tử hình hết bọn tham nhũng vcl"
    
    cleaned_title = clean_text(title)
    cleaned_comment = clean_text(comment)
    combined = f"{cleaned_title} </s> {cleaned_comment}"
    
    print(f"\nTitle:   {title}")
    print(f"Cleaned: {cleaned_title}")
    print(f"\nComment: {comment}")
    print(f"Cleaned: {cleaned_comment}")
    print(f"\nCombined Input for PhoBERT:")
    print(f"{combined}")
    print("=" * 80)

if __name__ == "__main__":
    test_preprocessing()
