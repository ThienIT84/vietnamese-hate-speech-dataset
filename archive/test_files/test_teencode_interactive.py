"""
🧪 TEENCODE TESTER - Interactive
Giao diện đơn giản để test teencode cleaning

Author: Senior AI Engineer
Date: 2025-12-28
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from preprocessing.advanced_text_cleaning import advanced_clean_text

def print_header():
    """In header"""
    print("\n" + "=" * 70)
    print("🧪 TEENCODE TESTER - Interactive Mode")
    print("=" * 70)
    print("\n✨ Features:")
    print("  ✅ Intensity Preservation: Giữ nguyên vcl, đm, cc...")
    print("  ✅ Time Format: Giữ nguyên 12:30, 14:00...")
    print("  ✅ Separator: Bảo tồn </s>")
    print("  ✅ Emoji → Tags: 😂 → <emo_pos>")
    print("\n💡 Nhập 'exit' hoặc 'quit' để thoát")
    print("💡 Nhập 'examples' để xem ví dụ")
    print("=" * 70)


def show_examples():
    """Hiển thị ví dụ"""
    examples = [
        ("nguoi ta ko biet gi ca", "Teencode neutral"),
        ("dm game nay hay vcl", "Intensity preservation"),
        ("Video lúc 12:30 rất hay", "Time format"),
        ("Boy pho moi </s> Te nan xa hoi", "Separator + teencode"),
        ("Thật tuyệt vời 😂😂", "Emoji to tags"),
        ("Nguyen Van A di hoc", "Person name masking"),
    ]
    
    print("\n" + "=" * 70)
    print("📝 VÍ DỤ:")
    print("=" * 70)
    
    for i, (text, desc) in enumerate(examples, 1):
        result = advanced_clean_text(text)
        print(f"\n[{i}] {desc}")
        print(f"  Input:  {text}")
        print(f"  Output: {result}")
    
    print("\n" + "=" * 70)


def test_interactive():
    """Interactive testing mode"""
    print_header()
    
    while True:
        try:
            # Get input
            print("\n" + "-" * 70)
            user_input = input("\n📝 Nhập text để test (hoặc 'exit'/'examples'): ").strip()
            
            # Check commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Tạm biệt!")
                break
            
            if user_input.lower() in ['examples', 'ex', 'e']:
                show_examples()
                continue
            
            if not user_input:
                print("⚠️  Vui lòng nhập text!")
                continue
            
            # Clean
            print("\n🔧 Processing...")
            result = advanced_clean_text(user_input)
            
            # Display result
            print("\n" + "=" * 70)
            print("📊 RESULT:")
            print("=" * 70)
            print(f"\n📥 Input:")
            print(f"  {user_input}")
            print(f"\n📤 Output:")
            print(f"  {result}")
            
            # Analysis
            print(f"\n🔍 Analysis:")
            
            # Check changes
            if result == user_input.lower():
                print("  ✅ Chỉ lowercase (không có thay đổi khác)")
            else:
                # Check specific features
                features = []
                
                if '</s>' in result:
                    features.append("Có separator </s>")
                
                if any(tag in result for tag in ['<emo_pos>', '<emo_neg>', '<person>', '<user>']):
                    tags = [tag for tag in ['<emo_pos>', '<emo_neg>', '<person>', '<user>'] if tag in result]
                    features.append(f"Tags: {', '.join(tags)}")
                
                if any(slang in result for slang in ['vcl', 'vl', 'đm', 'dm', 'cc']):
                    slangs = [s for s in ['vcl', 'vl', 'đm', 'dm', 'cc'] if s in result]
                    features.append(f"Slang preserved: {', '.join(slangs)}")
                
                import re
                if re.search(r'\d+:\d+', result):
                    times = re.findall(r'\d+:\d+', result)
                    features.append(f"Time format: {', '.join(times)}")
                
                if features:
                    for f in features:
                        print(f"  ✨ {f}")
                else:
                    print("  ✅ Text đã được chuẩn hóa")
            
            # Length comparison
            print(f"\n📏 Length: {len(user_input)} → {len(result)} chars")
            
            print("\n" + "=" * 70)
            
        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


def test_batch():
    """Batch testing mode"""
    test_cases = [
        # Teencode neutral
        "nguoi ta ko biet gi ca",
        "mh di hoc roi nha",
        "t yeu m nhieu lam",
        
        # Intensity preservation
        "dm game nay hay vcl",
        "vl thang nay ngu vl",
        "cc gi vay troi",
        
        # Time format
        "Video lúc 12:30 rất hay",
        "Họp lúc 14:00 nhé",
        "Từ 9:00 đến 17:30",
        
        # Separator
        "Title here </s> Comment here",
        "Boy pho moi </s> Te nan xa hoi",
        
        # Emoji
        "Thật tuyệt vời 😂😂",
        "Buồn quá 😭😭",
        
        # Person names
        "Nguyen Van A di hoc",
        "Tran Thi B rat xinh",
        
        # Mixed
        "dm 12:30 roi ma ko den vcl 😂",
    ]
    
    print("\n" + "=" * 70)
    print("🧪 BATCH TESTING MODE")
    print("=" * 70)
    
    for i, text in enumerate(test_cases, 1):
        result = advanced_clean_text(text)
        print(f"\n[{i}]")
        print(f"  Input:  {text}")
        print(f"  Output: {result}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    import sys
    
    # Check mode
    if len(sys.argv) > 1 and sys.argv[1] == '--batch':
        test_batch()
    else:
        test_interactive()
