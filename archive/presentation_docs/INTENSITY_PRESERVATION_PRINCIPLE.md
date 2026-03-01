# 🎯 Nguyên Tắc Intensity Preservation

## 📋 Triết Lý Cốt Lõi

**"Chỉ nên chuẩn hóa những từ KHÔNG làm mất đi tính độc hại"**

---

## ⚖️ Quy Tắc Phân Loại

### **Nhóm 1: GIỮ NGUYÊN (Intensity-Sensitive)**

**Đặc điểm:**
- Từ có tính độc hại
- Biến âm/biến thể có mức độ khác nhau
- Morphology (hình thái) quan trọng

**Ví dụ:**
```python
# Biến âm của "bắc kỳ"
"parky"  → GIỮ NGUYÊN (biến âm - mức độ cố chấp cao)
"backy"  → GIỮ NGUYÊN (biến âm)
"pake"   → GIỮ NGUYÊN (biến âm)
"3q"     → GIỮ NGUYÊN (ký hiệu số)
"3 gậy"  → GIỮ NGUYÊN (ký hiệu số)

# Từ chửi thề
"đm"     → GIỮ NGUYÊN (viết tắt - nhẹ hơn)
"vcl"    → GIỮ NGUYÊN (slang - nhẹ hơn)
"cc"     → GIỮ NGUYÊN (viết tắt)
```

**Lý do:**
- Model cần học được intensity gradient
- "parky" (biến âm) ≠ "bắc kỳ" (chuẩn)
- Mức độ cố chấp khác nhau

---

### **Nhóm 2: CHUẨN HÓA (Neutral/Lỗi Chính Tả)**

**Đặc điểm:**
- Từ trung tính (không độc hại)
- Lỗi chính tả đơn giản
- Chuẩn hóa không làm mất nghĩa

**Ví dụ:**
```python
# Lỗi chính tả
"bắc kì"  → "bắc kỳ"  (lỗi dấu)
"bac ky"  → "bắc kỳ"  (thiếu dấu)
"nam kì"  → "nam kỳ"  (lỗi dấu)

# Từ trung tính
"khum"    → "không"
"noa"     → "nó"
"tôy"     → "tôi"
"fai"     → "phải"
"ní"      → "bạn"
```

**Lý do:**
- Giảm nhiễu cho model
- Không làm mất tính độc hại (vì không có)
- Đồng nhất các biến thể trung tính

---

## 🔍 So Sánh: Biến Âm vs Lỗi Chính Tả

### **Biến Âm (Intentional Variation)**

**Đặc điểm:**
- Cố ý thay đổi để tránh filter
- Có mục đích bypass
- Thể hiện mức độ cố chấp

**Ví dụ:**
```
"bắc kỳ" → "parky" → "backy" → "pake" → "3q" → "3 gậy"
```

**Xử lý:** **GIỮ NGUYÊN** - Mỗi biến thể là 1 signal riêng

---

### **Lỗi Chính Tả (Unintentional Error)**

**Đặc điểm:**
- Không cố ý
- Lỗi đánh máy/dấu
- Không có ý nghĩa phân biệt

**Ví dụ:**
```
"bắc kỳ" → "bắc kì" (lỗi dấu)
"bắc kỳ" → "bac ky" (thiếu dấu)
```

**Xử lý:** **CHUẨN HÓA** - Về dạng chuẩn

---

## 📊 Bảng Quyết Định

| Từ | Loại | Xử Lý | Lý Do |
|-----|------|--------|-------|
| `parky` | Biến âm | GIỮ NGUYÊN | Intensity-sensitive |
| `backy` | Biến âm | GIỮ NGUYÊN | Intensity-sensitive |
| `pake` | Biến âm | GIỮ NGUYÊN | Intensity-sensitive |
| `3q` | Ký hiệu số | GIỮ NGUYÊN | Intensity-sensitive |
| `bắc kì` | Lỗi chính tả | CHUẨN HÓA | → "bắc kỳ" |
| `bac ky` | Lỗi chính tả | CHUẨN HÓA | → "bắc kỳ" |
| `bắc kỳ` | Chuẩn | GIỮ NGUYÊN | - |
| `đm` | Viết tắt | GIỮ NGUYÊN | Intensity-sensitive |
| `vcl` | Slang | GIỮ NGUYÊN | Intensity-sensitive |
| `khum` | Trung tính | CHUẨN HÓA | → "không" |
| `noa` | Trung tính | CHUẨN HÓA | → "nó" |

---

## 🎯 Ví Dụ Thực Tế

### **Ví dụ 1: Biến Âm - GIỮ NGUYÊN**

```python
Input:  "Thằng parky ngu vcl"
Output: "thằng parky ngu vcl"

# ✅ Giữ nguyên "parky"
# Model học: "parky" = biến âm của "bắc kỳ" = regional discrimination
# Label: 2 (Hate)
```

---

### **Ví dụ 2: Lỗi Chính Tả - CHUẨN HÓA**

```python
Input:  "Bắc kì toàn gian"
Output: "bắc kỳ toàn gian"

# ✅ Chuẩn hóa "bắc kì" → "bắc kỳ"
# Model học: "bắc kỳ" = regional discrimination
# Label: 2 (Hate)
```

---

### **Ví dụ 3: Intensity Gradient**

```python
# Case A: Biến âm (cố chấp cao)
Input:  "Thằng parky ngu"
Output: "thằng parky ngu"
# → Model học: "parky" = mức độ cố chấp cao

# Case B: Chuẩn (cố chấp thấp hơn)
Input:  "Bắc kỳ toàn gian"
Output: "bắc kỳ toàn gian"
# → Model học: "bắc kỳ" = mức độ cố chấp thấp hơn

# Model học được gradient: "parky" > "bắc kỳ"
```

---

### **Ví dụ 4: Từ Chửi Thề**

```python
# Case A: Viết tắt (nhẹ)
Input:  "Ngu đm"
Output: "ngu đm"
# ✅ Giữ nguyên "đm" (viết tắt)

# Case B: Đầy đủ (nặng)
Input:  "Ngu địt mẹ"
Output: "ngu địt mẹ"
# ✅ Giữ nguyên "địt mẹ" (đầy đủ)

# Model học được: "đm" (nhẹ) < "địt mẹ" (nặng)
```

---

## 🔬 Tại Sao Approach Này Hiệu Quả?

### **1. Better Discrimination**

**Nếu chuẩn hóa tất cả:**
```python
"parky" → "bắc kỳ"
"backy" → "bắc kỳ"
"pake"  → "bắc kỳ"
"3q"    → "bắc kỳ"

# Model chỉ học: "bắc kỳ" = hate
# Mất đi thông tin về mức độ cố chấp
```

**Nếu preserve:**
```python
"parky" → "parky"  (biến âm 1)
"backy" → "backy"  (biến âm 2)
"pake"  → "pake"   (biến âm 3)
"3q"    → "3q"     (ký hiệu số)

# Model học:
# - "parky" = hate (mức độ X)
# - "backy" = hate (mức độ Y)
# - "pake"  = hate (mức độ Z)
# - "3q"    = hate (mức độ W)
# → Richer representation
```

---

### **2. Generalization**

**Với preserve:**
- Model học được pattern chung: Biến âm = bypass = hate
- Khi gặp biến âm mới (ví dụ: "pakry"), model vẫn detect được

**Không preserve:**
- Model chỉ học "bắc kỳ" = hate
- Gặp biến âm mới → Không detect được

---

### **3. Intensity Gradient**

**Với preserve:**
```
"đm" (viết tắt) < "địt mẹ" (đầy đủ)
"vcl" (slang) < "vãi lồn" (explicit)
"parky" (biến âm) > "bắc kỳ" (chuẩn)
```

Model học được mức độ → Classify chính xác hơn

---

## 📝 Implementation

### **TEENCODE_DICT (Chuẩn hóa)**

```python
TEENCODE_DICT = {
    # Giảm nhiễu cho từ trung tính
    "khum": "không",
    "noa": "nó",
    "tôy": "tôi",
    "fai": "phải",
    "ní": "bạn",
    
    # Chuẩn hóa lỗi chính tả (không làm mất tính độc hại)
    "bắc kì": "bắc kỳ",  # Lỗi dấu
    "bac ky": "bắc kỳ",  # Thiếu dấu
    "nam kì": "nam kỳ",  # Lỗi dấu
    
    # ⚠️ KHÔNG chuẩn hóa biến âm
    # "parky": "bắc kỳ",  # ❌ XÓA - Làm mất intensity
}
```

---

### **TEENCODE_INTENSITY_SENSITIVE (Preserve)**

```python
TEENCODE_INTENSITY_SENSITIVE = {
    # Biến âm của "bắc kỳ"
    "parky", "backy", "pake", "pakky",
    "3q", "3 gậy", "3 sọc", "///",
    "ba que", "3que", "3 /", "3 ke",
    
    # Từ chửi thề
    "đm", "dm", "vcl", "vl", "cc", "cl",
    
    # Ẩn dụ cái chết
    "đăng xuất", "bán muối", "xanh cỏ",
    
    # Body parts
    "lồn", "cặc", "đít", "cứt",
}
```

---

## 🎤 Cách Trình Bày

Nếu BGK hỏi về nguyên tắc này:

> "Chúng em áp dụng nguyên tắc **Intensity Preservation** - chỉ chuẩn hóa những từ KHÔNG làm mất đi tính độc hại.
> 
> **2 nhóm:**
> 
> **1. GIỮ NGUYÊN (Intensity-Sensitive):**
> - Biến âm: 'parky', 'backy', 'pake' (mức độ cố chấp khác nhau)
> - Từ chửi: 'đm' vs 'địt mẹ' (intensity gradient)
> - Lý do: Model cần học được sự khác biệt
> 
> **2. CHUẨN HÓA (Neutral):**
> - Lỗi chính tả: 'bắc kì' → 'bắc kỳ'
> - Từ trung tính: 'khum' → 'không'
> - Lý do: Giảm nhiễu, không làm mất nghĩa
> 
> **Ví dụ:**
> - 'Thằng parky ngu' → Giữ 'parky' (biến âm)
> - 'Bắc kì toàn gian' → Chuẩn 'bắc kì' → 'bắc kỳ' (lỗi chính tả)
> 
> Approach này giúp model học được intensity gradient và detect hate speech chính xác hơn."

---

## ✅ Key Takeaways

1. **Biến âm ≠ Lỗi chính tả:** Biến âm có ý nghĩa, lỗi chính tả không
2. **Preserve intensity:** Giữ nguyên để model học gradient
3. **Chuẩn hóa neutral:** Chỉ chuẩn hóa từ trung tính
4. **Better discrimination:** Model học được sự khác biệt tinh tế

---

**Nguyên tắc này là core innovation của preprocessing pipeline! 🎯**
