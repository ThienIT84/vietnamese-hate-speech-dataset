# 🔬 Semantic Separator vs Removed Separator

**Date**: 2024-12-30  
**Question**: Nên xóa `</s>` hay thay bằng `<sep>`?

---

## 🎯 TL;DR - Recommendation

**✅ SỬ DỤNG `<sep>` (SEMANTIC APPROACH) - TỐT HƠN!**

Lý do:
- ✅ Model học được boundary giữa title và comment
- ✅ Giữ nguyên cấu trúc semantic của data
- ✅ Tăng khả năng hiểu context
- ✅ F1 score kỳ vọng cao hơn 1-2%

---

## 📊 So Sánh 2 Approaches

### Approach 1: Remove `</s>` (FIXED version)
```
BEFORE: boy phố gãy cánh <emo_pos> </s> <person> hôm sau
AFTER:  boy phố gãy cánh <emo_pos> <person> hôm sau

❌ Mất thông tin: Không biết đâu là title, đâu là comment
❌ Model không học được structure
✅ Đơn giản, không cần config tokenizer
```

**File**: `data/final/final_train_data_v3_RAW_FIXED.xlsx`

### Approach 2: Replace `</s>` → `<sep>` (SEMANTIC version)
```
BEFORE: boy phố gãy cánh <emo_pos> </s> <person> hôm sau
AFTER:  boy phố gãy cánh <emo_pos> <sep> <person> hôm sau

✅ Giữ thông tin: Biết rõ boundary title/comment
✅ Model học được structure
✅ Semantic understanding tốt hơn
⚠️ Cần add <sep> vào tokenizer special tokens
```

**File**: `data/final/final_train_data_v3_SEMANTIC.xlsx`

---

## 🔬 Chi Tiết Kỹ Thuật

### Data Structure

Dữ liệu gốc có cấu trúc:
```
[POST_TITLE] </s> [COMMENT_TEXT]
```

Ví dụ:
```
"awai x <user> - body shaming ? ( ft . trà bông ) | visualizer mv </s> tôi cũng hỏi thế"
                                                                    ^^^^
                                                                    Separator
```

### Approach 1: Remove Separator

**Kết quả**:
```
"awai x <user> - body shaming ? ( ft . trà bông ) | visualizer mv tôi cũng hỏi thế"
```

**Vấn đề**:
- Model không biết "mv" là kết thúc title
- Model không biết "tôi" là bắt đầu comment
- Mất context về cấu trúc post + comment

**Khi nào dùng**:
- Khi data không có cấu trúc rõ ràng
- Khi muốn đơn giản hóa tối đa
- Khi không quan tâm đến structure

### Approach 2: Semantic Separator

**Kết quả**:
```
"awai x <user> - body shaming ? ( ft . trà bông ) | visualizer mv <sep> tôi cũng hỏi thế"
                                                                   ^^^^^
                                                                   Semantic boundary
```

**Lợi ích**:
- Model học: "Trước `<sep>` là title, sau `<sep>` là comment"
- Attention mechanism có thể focus khác nhau cho title vs comment
- Toxic words trong title vs comment có thể có ý nghĩa khác

**Khi nào dùng**:
- Khi data có cấu trúc rõ ràng (title + comment)
- Khi muốn model hiểu semantic structure
- Khi muốn F1 score cao nhất

---

## 🎯 Ví Dụ Cụ Thể

### Example 1: Toxic in Title vs Comment

**Case 1**: Toxic trong title
```
"thằng ngu vcl <sep> video hay quá"
 ^^^^^^^^^^^^         ^^^^^^^^^^^^
 Title (toxic)        Comment (clean)
 
Label: 1 (Toxic) - vì title toxic
```

**Case 2**: Toxic trong comment
```
"video hay quá <sep> thằng ngu vcl"
 ^^^^^^^^^^^^        ^^^^^^^^^^^^
 Title (clean)       Comment (toxic)
 
Label: 1 (Toxic) - vì comment toxic
```

**Với `<sep>`**: Model học được toxic ở đâu (title hay comment)  
**Không có `<sep>`**: Model chỉ thấy "thằng ngu vcl" và "video hay quá" - không biết context

### Example 2: Sarcasm Detection

```
"học sinh giỏi bú fame <sep> tương lai đấy có tương lai"
 ^^^^^^^^^^^^^^^^^^^^         ^^^^^^^^^^^^^^^^^^^^^^^^^^
 Title (neutral)              Comment (sarcastic/toxic)
```

**Với `<sep>`**: Model hiểu comment đang châm biếm title  
**Không có `<sep>`**: Model khó hiểu mối quan hệ sarcastic

---

## 📈 Expected Performance

### Approach 1: Remove `</s>`
```
Expected F1: 0.75-0.78
Pros:
  ✅ Simple
  ✅ No tokenizer config needed
Cons:
  ❌ Lost structure information
  ❌ Lower F1 potential
```

### Approach 2: Semantic `<sep>`
```
Expected F1: 0.76-0.80 (+1-2%)
Pros:
  ✅ Better semantic understanding
  ✅ Model learns structure
  ✅ Higher F1 potential
  ✅ Better for edge cases
Cons:
  ⚠️ Need to add <sep> to tokenizer
```

---

## 🛠️ Implementation

### Approach 1: Remove (Already Done)
```python
# File: final_train_data_v3_RAW_FIXED.xlsx
# No special config needed

tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")
# Works out of the box
```

### Approach 2: Semantic (Recommended)
```python
# File: final_train_data_v3_SEMANTIC.xlsx
# Need to add <sep> to tokenizer

tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")

# Add <sep> as special token
special_tokens_dict = {
    'additional_special_tokens': [
        '<sep>',
        '<emo_pos>',
        '<emo_neg>',
        '<person>',
        '<user>'
    ]
}
tokenizer.add_special_tokens(special_tokens_dict)

# Resize model embeddings
model.resize_token_embeddings(len(tokenizer))

# Now tokenizer understands <sep>
```

---

## 📊 Conversion Statistics

### Approach 1: Remove
```
Input:  44,647 underscores, 5,721 </s>
Output: 1,496 underscores (in special tokens), 0 </s>
Result: Clean text, no separator
```

### Approach 2: Semantic
```
Input:  44,647 underscores, 5,721 </s>
Output: 1,496 underscores (in special tokens), 5,721 <sep>
Result: Clean text, semantic separator preserved
```

---

## 🎯 Recommendation

### Use Semantic `<sep>` If:
- ✅ Bạn muốn F1 score cao nhất
- ✅ Data có cấu trúc title + comment
- ✅ Sẵn sàng config tokenizer (5 dòng code)
- ✅ Muốn model hiểu structure

### Use Remove If:
- ✅ Muốn đơn giản tối đa
- ✅ Không quan tâm structure
- ✅ Không muốn config tokenizer
- ✅ F1 0.75-0.78 là đủ

---

## 📁 Files Available

### Approach 1: Remove
```
data/final/final_train_data_v3_RAW_FIXED.xlsx
data/final/final_train_data_v3_RAW_FIXED.csv
Script: scripts/preprocessing/convert_segmented_to_raw_FIXED_V2.py
```

### Approach 2: Semantic (Recommended)
```
data/final/final_train_data_v3_SEMANTIC.xlsx
data/final/final_train_data_v3_SEMANTIC.csv
Script: scripts/preprocessing/convert_with_semantic_tokens.py
```

---

## 🚀 Next Steps

### If Using Semantic (Recommended):

1. **Upload data**:
   ```
   File: final_train_data_v3_SEMANTIC.xlsx
   ```

2. **Training script changes**:
   ```python
   # Add to training script
   special_tokens_dict = {
       'additional_special_tokens': [
           '<sep>', '<emo_pos>', '<emo_neg>', 
           '<person>', '<user>'
       ]
   }
   tokenizer.add_special_tokens(special_tokens_dict)
   model.resize_token_embeddings(len(tokenizer))
   ```

3. **Train & evaluate**:
   - Expected F1: 0.76-0.80
   - Compare with PhoBERT baseline

### If Using Remove:

1. **Upload data**:
   ```
   File: final_train_data_v3_RAW_FIXED.xlsx
   ```

2. **Training script**:
   ```python
   # No special config needed
   tokenizer = AutoTokenizer.from_pretrained("Fsoft-AIC/videberta-base")
   ```

3. **Train & evaluate**:
   - Expected F1: 0.75-0.78

---

## 💡 Expert Opinion

**Khuyến nghị**: Dùng **Semantic `<sep>`**

Lý do:
1. **Tăng F1**: +1-2% improvement expected
2. **Better understanding**: Model học được structure
3. **Edge cases**: Xử lý tốt hơn các trường hợp phức tạp
4. **Cost**: Chỉ cần thêm 5 dòng code
5. **Competition**: Mỗi 1% F1 rất quan trọng!

**Trade-off**: Phải config tokenizer, nhưng đáng giá!

---

## 📚 References

- [BERT Special Tokens](https://huggingface.co/docs/transformers/preprocessing#special-tokens)
- [Adding Special Tokens](https://huggingface.co/docs/transformers/main_classes/tokenizer#transformers.PreTrainedTokenizer.add_special_tokens)
- [Semantic Separators in NLP](https://arxiv.org/abs/1810.04805)

---

**Recommendation**: Use `final_train_data_v3_SEMANTIC.xlsx` for best results! 🚀

---

**Last Updated**: 2024-12-30  
**Status**: ✅ Both approaches ready, Semantic recommended
