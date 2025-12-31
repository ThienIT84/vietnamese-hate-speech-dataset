"""
Smart teencode expansion - chỉ expand khi cần thiết
Giữ nguyên các từ viết tắt nhẹ, chỉ expand khi có ngữ cảnh toxic rõ ràng
"""

import re

class SmartTeencodeExpander:
    """
    Expand teencode một cách thông minh dựa vào ngữ cảnh
    """
    
    def __init__(self):
        # Các từ viết tắt CÓ THỂ là thán từ nhẹ hoặc toxic tùy ngữ cảnh
        self.context_sensitive = {
            'đm': 'địt mẹ',
            'dm': 'địt mẹ', 
            'đcm': 'địt con mẹ',
            'dcm': 'địt con mẹ',
            'dmm': 'địt mẹ mày',
            'dkm': 'đéo kệ mày',
            'đkm': 'đéo kệ mày',
        }
        
        # Các từ LUÔN expand (rõ ràng toxic)
        self.always_expand = {
            'đcmm': 'địt con mẹ mày',
            'dcmm': 'địt con mẹ mày',
            'clm': 'cái lồn mẹ',
            'đmmm': 'địt mẹ mày mẹ',
            'vl': 'vãi lồn',
            'vcl': 'vãi cái lồn',
            'cc': 'cặc',
            'đb': 'đéo biết',
            'db': 'đéo biết',
        }
        
        # Các từ KHÔNG expand (thán từ nhẹ, slang bình thường)
        self.never_expand = {
            'oke': 'oke',
            'ok': 'ok',
            'tks': 'thanks',
            'thks': 'thanks',
            'ad': 'admin',
            'mn': 'mọi người',
        }
        
        # Ngữ cảnh toxic - nếu có các từ này thì expand
        self.toxic_context_words = [
            'chửi', 'mắng', 'đánh', 'giết', 'chết', 'thối', 'ngu', 'đần', 
            'khốn', 'súc vật', 'con chó', 'đồ', 'thằng', 'con', 'bọn'
        ]
        
        # Ngữ cảnh neutral/positive - nếu có các từ này thì KHÔNG expand
        self.neutral_context_words = [
            'hay', 'đẹp', 'tốt', 'giỏi', 'pro', 'xịn', 'ngon', 'vui', 
            'haha', 'hihi', 'game', 'phim', 'nhạc', 'video'
        ]
    
    def detect_context(self, text):
        """
        Phát hiện ngữ cảnh của câu
        Returns: 'toxic', 'neutral', 'positive'
        """
        text_lower = text.lower()
        
        toxic_score = sum(1 for word in self.toxic_context_words if word in text_lower)
        neutral_score = sum(1 for word in self.neutral_context_words if word in text_lower)
        
        if toxic_score > neutral_score:
            return 'toxic'
        elif neutral_score > 0:
            return 'neutral'
        else:
            return 'unknown'
    
    def expand(self, text, force_expand=False):
        """
        Expand teencode dựa vào ngữ cảnh
        
        Args:
            text: Text cần expand
            force_expand: Nếu True, expand tất cả (dùng cho data đã labeled toxic)
        
        Returns:
            expanded_text, was_expanded
        """
        if force_expand:
            # Expand tất cả
            result = text
            for short, full in {**self.context_sensitive, **self.always_expand}.items():
                result = re.sub(r'\b' + re.escape(short) + r'\b', full, result, flags=re.IGNORECASE)
            return result, True
        
        # Detect context
        context = self.detect_context(text)
        
        result = text
        was_expanded = False
        
        # Always expand
        for short, full in self.always_expand.items():
            if re.search(r'\b' + re.escape(short) + r'\b', result, re.IGNORECASE):
                result = re.sub(r'\b' + re.escape(short) + r'\b', full, result, flags=re.IGNORECASE)
                was_expanded = True
        
        # Context-sensitive expand
        if context == 'toxic':
            for short, full in self.context_sensitive.items():
                if re.search(r'\b' + re.escape(short) + r'\b', result, re.IGNORECASE):
                    result = re.sub(r'\b' + re.escape(short) + r'\b', full, result, flags=re.IGNORECASE)
                    was_expanded = True
        elif context == 'neutral':
            # Không expand, giữ nguyên
            pass
        else:
            # Unknown context - expand một phần (conservative)
            # Chỉ expand nếu có nhiều teencode trong câu
            teencode_count = sum(1 for short in self.context_sensitive.keys() 
                               if re.search(r'\b' + re.escape(short) + r'\b', result, re.IGNORECASE))
            if teencode_count >= 2:  # Nếu có >= 2 teencode thì expand
                for short, full in self.context_sensitive.items():
                    if re.search(r'\b' + re.escape(short) + r'\b', result, re.IGNORECASE):
                        result = re.sub(r'\b' + re.escape(short) + r'\b', full, result, flags=re.IGNORECASE)
                        was_expanded = True
        
        return result, was_expanded


# Demo usage
if __name__ == "__main__":
    expander = SmartTeencodeExpander()
    
    test_cases = [
        "đm game này hay vãi",  # Neutral context - không expand
        "địt mẹ thằng ngu này",  # Toxic context - expand
        "dm đồ ngu",  # Toxic context - expand
        "đm đm đm",  # Nhiều teencode - expand
        "game này đm pro",  # Neutral - không expand
    ]
    
    print("=== DEMO SMART TEENCODE EXPANSION ===\n")
    for text in test_cases:
        expanded, was_expanded = expander.expand(text)
        context = expander.detect_context(text)
        print(f"Original: {text}")
        print(f"Context: {context}")
        print(f"Expanded: {expanded}")
        print(f"Was expanded: {was_expanded}")
        print()
