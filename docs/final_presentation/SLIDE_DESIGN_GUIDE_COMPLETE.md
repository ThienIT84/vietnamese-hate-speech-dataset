# 🎨 HƯỚNG DẪN THIẾT KẾ SLIDE CHI TIẾT
## SafeSense-VI - IT Got Talent 2025
**Complete Visual Design Guide for 15-minute Presentation**

---

## 📋 TỔNG QUAN

### Thông tin cơ bản:
- **Số slide:** 1 title + 15 content slides + 1 Q&A = **17 slides total**
- **Thời gian:** 15 phút
- **Công cụ đề xuất:** PowerPoint / Google Slides / Canva
- **Tỷ lệ:** 16:9 (widescreen)
- **Theme:** Professional, Modern, Tech-focused
- **Cấu trúc:** MỖI nội dung là 1 slide riêng biệt, KHÔNG gộp

### Color Palette:
```
Primary:   #2C3E50 (Dark Blue-Grey) - Chủ đạo, tiêu đề
Secondary: #E74C3C (Red) - Toxic/Warning
Accent 1:  #3498DB (Blue) - Clean/Positive
Accent 2:  #F39C12 (Orange) - Highlight/Important
Success:   #27AE60 (Green) - Success metrics
Text:      #34495E (Dark Grey) - Body text
Light BG:  #ECF0F1 (Light Grey) - Background
```

---

## 🎯 SLIDE-BY-SLIDE DESIGN

---

## SLIDE 0: TITLE SLIDE (30 giây)

### Layout:
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│         [LOGO HUTECH - Góc trái trên]              │
│                                                     │
│                                                     │
│              🔥 SAFESENSE-VI                       │
│    HỆ THỐNG PHÁT HIỆN BÌNH LUẬN ĐỘC HẠI          │
│              TIẾNG VIỆT                            │
│                                                     │
│         Sử dụng PhoBERT & Intensity Preservation   │
│                                                     │
│                                                     │
│  Trần Thanh Thiện - 2280603068                    │
│  Nguyễn Đan Huy - 2280601170                      │
│  Lớp 22DTHG2 - HUTECH                             │
│                                                     │
│         IT Got Talent 2025                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Design Details:
**Title:**
- Font: Montserrat Bold, 60pt
- Color: #2C3E50
- Center aligned
- Add flame emoji 🔥 for attention

**Subtitle:**
- Font: Montserrat Regular, 32pt
- Color: #7F8C8D
- Italic

**Student Info:**
- Font: Open Sans Regular, 18pt
- Color: #34495E
- Left aligned, bottom section

**Background:**
- Gradient: #ECF0F1 → White (top to bottom)
- Subtle tech pattern (circuits, nodes) at 5% opacity

---

## SLIDE 1: BỐI CẢNH & BÀI TOÁN (1 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  BỐI CẢNH & BÀI TOÁN                                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📊 BỐI CẢNH THỰC TẾ                               │
│  ┌──────────────┐  ┌──────────────┐               │
│  │   77.9M      │  │   6.5M       │               │
│  │   Users      │  │   Comments   │               │
│  │   🧑‍🤝‍🧑        │  │   💬         │               │
│  └──────────────┘  └──────────────┘               │
│                                                     │
│  ⚠️ 12-18% Toxic Content                           │
│  🚨 Hate Speech gia tăng                           │
│                                                     │
│  🎯 BÀI TOÁN                                       │
│  ┌──────────────────────────────────────────────┐ │
│  │  INPUT:  "Giỏi vcl, đỉnh vãi bạn ơi!"       │ │
│  │  OUTPUT: Label 0 (Clean) ✅                  │ │
│  │                                              │ │
│  │  3 NHÃN:                                    │ │
│  │  🟢 Clean (44.3%)  🟡 Toxic (27.0%)         │ │
│  │  🔴 Hate (28.6%)                            │ │
│  └──────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Bối cảnh Cards:**
- 2 cards side-by-side
- Background: White with subtle shadow
- Border-left: 4px solid #3498DB
- Icon: Large emoji center
- Numbers: 48pt, Bold, #2C3E50
- Labels: 20pt, #7F8C8D

**Warning Section:**
- Background: #FFF3CD (Light yellow)
- Border-left: 4px solid #F39C12
- Icons: ⚠️ and 🚨
- Text: 18pt, #856404

**Bài toán Box:**
- Background: #E8F4F8 (Light blue)
- Border: 2px solid #3498DB
- Input/Output: Monospace font (Consolas)
- Code-like appearance
- Green checkmark for positive example

**3 Nhãn Badges:**
```css
.badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
}
.clean { background: #D4EDDA; color: #155724; }
.toxic { background: #FFF3CD; color: #856404; }
.hate { background: #F8D7DA; color: #721C24; }
```

---

## SLIDE 2: TỨ ĐẠI THÁCH THỨC (1 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  🔥 TỨ ĐẠI THÁCH THỨC                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐       │
│  │  1️⃣ POSITIVE     │  │  2️⃣ PRONOUN      │       │
│  │     SLANG        │  │     TRIGGER      │       │
│  │                  │  │                  │       │
│  │  "Giỏi vcl" ✅   │  │  "Nên tù" ✅     │       │
│  │  "Ngu vcl"  ❌   │  │  "Thằng nên tù"❌│       │
│  │                  │  │                  │       │
│  │  Cùng "vcl"      │  │  Đại từ trigger  │       │
│  │  khác nghĩa!     │  │  đổi tính chất!  │       │
│  └──────────────────┘  └──────────────────┘       │
│                                                     │
│  ┌──────────────────┐  ┌──────────────────┐       │
│  │  3️⃣ INTENSITY    │  │  4️⃣ TOXIC VS     │       │
│  │     GRADIENT     │  │     HATE         │       │
│  │                  │  │                  │       │
│  │  "đm"     (-)    │  │  "Ngu quá"  →  T │       │
│  │  "địt mẹ" (--)   │  │  "Ba mẹ mày"→  H │       │
│  │  "dmmmm"  (---)  │  │  "Bị tử hình"→ C │       │
│  │                  │  │                  │       │
│  │  Normalize mất   │  │  Ranh giới mờ    │       │
│  │  thông tin! ⚠️    │  │  cần guideline!  │       │
│  └──────────────────┘  └──────────────────┘       │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Challenge Cards (2×2 grid):**
- 4 equal-sized cards
- Background: White
- Border: 3px solid matching color
  - Card 1: #3498DB (Blue)
  - Card 2: #9B59B6 (Purple)
  - Card 3: #E67E22 (Orange)
  - Card 4: #E74C3C (Red)
- Padding: 20px
- Shadow: 0 4px 8px rgba(0,0,0,0.1)

**Card Title:**
- Emoji + Number: 28pt
- Title: 20pt, Bold, matching border color
- Underline effect

**Examples:**
- Monospace font (Consolas, 16pt)
- ✅ = Green (#27AE60)
- ❌ = Red (#E74C3C)
- Background for code: #F8F9FA

**Key Insight (bottom of each card):**
- Italic, 14pt
- Color: #7F8C8D
- With emoji

---

## SLIDE 3: LÝ DO CHỌN ĐỀ TÀI (1 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  🌟 LÝ DO CHỌN ĐỀ TÀI                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌────────────────────────────────────────────┐    │
│  │  1️⃣ TÁC ĐỘNG XÃ HỘI LỚN                   │    │
│  │  🛡️ Bảo vệ 77.9M users VN                  │    │
│  │  🌱 Môi trường internet lành mạnh           │    │
│  └────────────────────────────────────────────┘    │
│                                                     │
│  ┌────────────────────────────────────────────┐    │
│  │  2️⃣ THÁCH THỨC KỸ THUẬT CAO               │    │
│  │  🧠 NLP tiếng Việt phức tạp                 │    │
│  │  🎯 Positive slang, context-dependent       │    │
│  └────────────────────────────────────────────┘    │
│                                                     │
│  ┌────────────────────────────────────────────┐    │
│  │  3️⃣ ỨNG DỤNG THỰC TẾ RÕ RÀNG              │    │
│  │  📱 Facebook, YouTube, TikTok               │    │
│  │  ⚡ Real-time detection (<100ms)            │    │
│  └────────────────────────────────────────────┘    │
│                                                     │
│  ┌────────────────────────────────────────────┐    │
│  │  4️⃣ THIẾU GIẢI PHÁP CHẤT LƯỢNG            │    │
│  │  📊 Chưa có dataset cao cấp                 │    │
│  │  📖 Chưa có guideline khoa học              │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Reason Cards (stacked vertically):**
- Full-width cards
- Background gradient: Light to white (left to right)
  - Card 1: #D4EDDA → White
  - Card 2: #D1ECF1 → White
  - Card 3: #FFF3CD → White
  - Card 4: #F8D7DA → White
- Border-left: 6px solid matching primary color
- Margin-bottom: 15px
- Animation: Slide in from left (staggered)

**Card Content:**
- Number + Title: 24pt, Bold
- Emoji: 32pt (prominent)
- Details: 18pt, with icons
- Bullet points with custom icons

---

## SLIDE 4: PHOBERT & DATASET (1 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  PHOBERT & DATASET                                  │
├─────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌────────────────────────┐ │
│  │   🤖 PHOBERT   │    │  📊 DATASET & QUALITY  │ │
│  │                 │    │                        │ │
│  │  vinai/         │    │  ┌──────────────────┐ │ │
│  │  phobert-base   │    │  │ Raw: 50,000+     │ │ │
│  │  -v2            │    │  │ Labeled: 7,626   │ │ │
│  │                 │    │  └──────────────────┘ │ │
│  │  📈 135M params │    │                        │ │
│  │  📝 256 tokens  │    │  Distribution:         │ │
│  │  ⚡ SOTA VN     │    │  [====Clean====] 44.3% │ │
│  │                 │    │  [==Toxic==] 27.0%     │ │
│  │                 │    │  [===Hate===] 28.6%    │ │
│  │                 │    │                        │ │
│  └─────────────────┘    │  ✅ Consensus 70-75%  │ │
│                         └────────────────────────┘ │
│                                                     │
│  🎯 GUIDELINE V7.2: "NGỮ CẢNH QUYẾT ĐỊNH NHÃN"    │
│  ┌───────────────────────────────────────────────┐ │
│  │ "Giỏi đm" → Label 0 (Từ tục khen ngợi)      │ │
│  │ "Ba mẹ mày ngu" → Label 2 (Family attack)   │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**PhoBERT Card:**
- Background: Linear gradient #667EEA → #764BA2
- White text
- Large robot emoji 🤖
- Stats with icons:
  - 📈 Parameters
  - 📝 Max length
  - ⚡ Performance
- Border-radius: 15px
- Shadow: Elevated

**Dataset Card:**
- Background: White
- Border: 2px solid #3498DB
- Funnel diagram for data flow
- Progress bars for distribution:
  ```
  Clean: ████████████████░░░░ 44.3%
  Toxic: ██████████░░░░░░░░░░ 27.0%
  Hate:  ██████████░░░░░░░░░░ 28.6%
  ```
- Colors match label badges

**Guideline Box:**
- Background: #FFF9E6 (Light yellow)
- Border-top: 3px solid #F39C12
- Icon: 🎯
- Examples in code blocks
- Arrow indicators (→)

---

## SLIDE 5: INTENSITY PRESERVATION INNOVATION ⭐ (1 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  ⭐ INTENSITY PRESERVATION INNOVATION               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ❌ TRADITIONAL APPROACH (WRONG)                    │
│  ┌──────────────────────────────────────────────┐  │
│  │  "đm"     → normalize → "địt mẹ"            │  │
│  │  "vcl"    → normalize → "vãi lồn"           │  │
│  │  "dmmmm"  → normalize → "địt mẹ"            │  │
│  │                                              │  │
│  │  ❌ Tất cả giống nhau → MẤT THÔNG TIN!      │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ✅ OUR APPROACH (CORRECT)                          │
│  ┌──────────────────────────────────────────────┐  │
│  │  INPUT: "Đ.m nguuuu vcl 😡"                 │  │
│  │                                              │  │
│  │  PROCESSING PIPELINE:                       │  │
│  │  1️⃣ Remove bypass    → "đm"                 │  │
│  │  2️⃣ Detect intensity → "ngu <very_intense>" │  │
│  │  3️⃣ Preserve slang   → "vcl" (GIỮ NGUYÊN!) │  │
│  │  4️⃣ Extract emoji    → "<emo_neg>"          │  │
│  │                                              │  │
│  │  OUTPUT: "đm ngu <very_intense> vcl <emo_neg>"│ │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  💡 WHY IT WORKS                                    │
│  "đm" (viết tắt) → Model: ít toxic                 │
│  "địt mẹ" (đầy đủ) → Model: toxic hơn              │
│  "dmmmm" → "đm <very_intense>" → Model: rất toxic  │
│                                                     │
│  → Phân biệt "Giỏi vcl" ✅ vs "Ngu vcl" ❌         │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Traditional Approach Box:**
- Background: #FFEBEE (Light red)
- Border: 3px solid #E74C3C
- Large ❌ icon top-left
- Code examples: Monospace, 16pt
- Arrow sequence: Left to right
- End with big red X and warning

**Our Approach Box:**
- Background: #E8F5E9 (Light green)
- Border: 3px solid #27AE60
- Large ✅ icon top-left
- Step-by-step pipeline:
  - Each step numbered with emoji
  - Different background color per step
  - Arrows between steps
- Final output highlighted in green

**Why It Works Section:**
- Background: #E3F2FD (Light blue)
- Border-left: 4px solid #2196F3
- Gradient intensity bars:
  ```
  đm:       [█░░░] Low
  địt mẹ:   [███░] Medium
  dmmmm:    [████] High
  ```
- Final example with color-coded results

**Animation Suggestions:**
1. Traditional box fades in with red X
2. Our approach box slides in from right
3. Pipeline steps appear one by one
4. Final comparison side-by-side

---

## SLIDE 6: TRAINING CONFIGURATION (0.5 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  ⚙️ TRAINING CONFIGURATION                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐  ┌──────────────────────┐   │
│  │ HYPERPARAMETERS │  │  OPTIMIZATION        │   │
│  │                  │  │                      │   │
│  │ Batch Size: 16   │  │ ✅ Class weights     │   │
│  │ LR: 2e-5         │  │ ✅ Label smoothing   │   │
│  │ Epochs: 5        │  │ ✅ Early stopping    │   │
│  │ Warmup: 0.1      │  │ ✅ Stratified split  │   │
│  └──────────────────┘  └──────────────────────┘   │
│                                                     │
│  📍 INFRASTRUCTURE                                  │
│  ┌────────────────────────────────────────────┐   │
│  │  Platform:  Kaggle Notebook                │   │
│  │  GPU:       T4 (16GB VRAM)                 │   │
│  │  Time:      ~8.3 minutes (495.7s)          │   │
│  │  Size:      ~500MB                         │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  🛠️ TECH STACK                                     │
│  [Python] [PyTorch] [Transformers] [Pandas]        │
│  [Scikit-learn] [VnCoreNLP] [FastAPI]              │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Hyperparameters Card:**
- Background: #F0F4F8
- Border-left: 4px solid #4A90E2
- Icon: ⚙️
- Key-value pairs in table format
- Monospace for values

**Optimization Card:**
- Background: #F0F4F8
- Border-left: 4px solid #27AE60
- Checkmarks in green
- Each technique on separate line

**Infrastructure Card:**
- Background: White with gradient border
- Icon: 📍
- Info grid (2 columns)
- Kaggle logo if possible

**Tech Stack:**
- Badge-style chips
- Different color per category:
  - Language: Blue
  - Framework: Orange
  - Libraries: Green
  - API: Purple
- With small logos/icons

---

## SLIDE 7: METHODOLOGY PIPELINE (0.5 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  METHODOLOGY PIPELINE                               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📈 METHODOLOGY PIPELINE                            │
│                                                     │
│         50,000+                                     │
│       Raw Comments                                  │
│            │                                        │
│            ▼                                        │
│     Guideline V7.2                                  │
│       Labeling                                      │
│            │                                        │
│            ▼                                        │
│        7,626                                        │
│    Quality Samples                                  │
│            │                                        │
│            ▼                                        │
│    ⭐ Intensity                                     │
│    Preservation                                     │
│    Text Cleaning                                    │
│            │                                        │
│            ▼                                        │
│     PhoBERT-v2                                      │
│       Training                                      │
│    (5 epochs, T4)                                   │
│            │                                        │
│            ▼                                        │
│    Production Model                                 │
│   F1: 0.7995 | Acc: 80.87%                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Pipeline Flowchart:**
- Vertical flow (top to bottom)
- Each box:
  - Rounded corners
  - Drop shadow
  - Icon on left
  - Numbers/stats on right
- Arrows:
  - Thick (4px)
  - Blue color
  - Animated (flow effect)
- Special highlight on "Intensity Preservation" (⭐)
  - Glow effect
  - Larger box
  - Gold border

**Color coding:**
- Data collection: #9B59B6 (Purple)
- Processing: #3498DB (Blue)
- Training: #E67E22 (Orange)
- Results: #27AE60 (Green)

---

## SLIDE 8: 5 ĐIỂM NỔI BẬT (2 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  🌟 5 ĐIỂM NỔI BẬT                                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1️⃣ INTENSITY PRESERVATION                         │
│  ┌──────────────────────────────────────────────┐  │
│  │  Novel approach cho Vietnamese NLP           │  │
│  │  Bảo toàn morphology → Model học gradient    │  │
│  │  ✅ "Giỏi vcl" vs "Ngu vcl" → 95% accurate   │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  2️⃣ CONTEXT-AWARE PROCESSING                       │
│  ┌──────────────────────────────────────────────┐  │
│  │  Title </s> Comment separator                │  │
│  │  "Confession FTU </s> boy phố..."            │  │
│  │  ✅ Model hiểu context → Predict chính xác   │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  3️⃣ GUIDELINE V7.2 KHOA HỌC                        │
│  ┌──────────────────────────────────────────────┐  │
│  │  Decision framework cho edge cases           │  │
│  │  Consensus 70-75% (vs industry 50-60%)       │  │
│  │  ✅ Higher quality annotations                │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  4️⃣ PRODUCTION-READY PERFORMANCE                   │
│  ┌──────────────────────────────────────────────┐  │
│  │  F1: 0.7995 (+11% vs target)                 │  │
│  │  Accuracy: 80.87%                            │  │
│  │  Response: <100ms | Throughput: 1K req/s     │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  5️⃣ SCALABLE & DEPLOYABLE                          │
│  ┌──────────────────────────────────────────────┐  │
│  │  FastAPI + Docker + Kubernetes               │  │
│  │  Horizontal scaling ready                    │  │
│  │  ✅ Production architecture complete          │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Feature Cards (5 stacked):**
- Each card:
  - Number emoji (1️⃣-5️⃣) large and prominent
  - Title: Bold, 22pt
  - Content box with light background
  - Checkmark with green highlight for key achievement
- Progressive color scheme:
  1. #E8F5E9 (Light green)
  2. #E3F2FD (Light blue)
  3. #FFF9C4 (Light yellow)
  4. #F3E5F5 (Light purple)
  5. #FFE0B2 (Light orange)

**Key Metrics Highlight:**
- Use gauge/progress bars for numbers
- Icons for each metric type
- Comparison arrows (↑ +11%)

---

## SLIDE 9: PERFORMANCE METRICS (1 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  📊 PERFORMANCE METRICS                             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌────────────────────────────────────────┐        │
│  │        F1 SCORE COMPARISON             │        │
│  │                                        │        │
│  │  Target ┃████████████░░░░░░│ 0.72     │        │
│  │         ┃                              │        │
│  │  Achieved ████████████████░░│ 0.7995   │        │
│  │         ┃              ↑ +11%          │        │
│  └────────────────────────────────────────┘        │
│                                                     │
│  PER-LABEL PERFORMANCE                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  CLEAN   │  │  TOXIC   │  │  HATE    │         │
│  │   0.85   │  │   0.73   │  │   0.82   │         │
│  │          │  │          │  │          │         │
│  │  ████▓   │  │  ███▒    │  │  ████░   │         │
│  │  85%     │  │  73%     │  │  82%     │         │
│  └──────────┘  └──────────┘  └──────────┘         │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  CONFUSION MATRIX                             │ │
│  │                                               │ │
│  │        Predicted                              │ │
│  │        Clean  Toxic  Hate                     │ │
│  │  Clean  [86%]  [9%]  [5%]  ← Low FP!         │ │
│  │  Toxic  [16%] [74%] [10%]                     │ │
│  │  Hate   [11%] [10%] [79%]                     │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**F1 Score Comparison:**
- Horizontal bar chart
- Target bar: Grey with dashed border
- Achieved bar: Green gradient
- Percentage difference with arrow
- Animation: Bars fill from left

**Per-Label Cards:**
- 3 cards side-by-side
- Each card:
  - Large number (48pt) at top
  - Label name below
  - Vertical progress bar
  - Color-coded by label type
- Clean: Green theme
- Toxic: Orange theme
- Hate: Red theme

**Confusion Matrix:**
- Heatmap style
- Color intensity based on percentage:
  - High (>70%): Dark green
  - Medium (40-70%): Yellow
  - Low (<40%): Light red
- Diagonal highlighted (correct predictions)
- Annotation for low FP (9%)

---

## SLIDE 10: DEMO CASE 1 - POSITIVE SLANG (0.5 phút)

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  DEMO CASE 1: POSITIVE SLANG ⭐                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🎬 CASE 1: POSITIVE SLANG ⭐                       │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Demo Case Box:**
- Full-width card
- White background with subtle gradient
- Border-left: 5px solid (color by case type)

**Input Section (📝):**
- Larger font (20pt)
- Light blue background (#E3F2FD)
- Monospace for comment text
- Speech bubble style

**Prediction Section (🤖):**
- Label badge:
  - Rounded pill shape
  - Color-coded by label
  - Large text
- Confidence bar:
  - Horizontal progress bar
  - Gradient fill
  - Percentage text on right
  - Animation: Fill on appear

**Reasoning Section (💡):**
- Light yellow background (#FFFDE7)
- Checkmarks (✓) in green
- Bullet points
- Italic text for key terms

**Result (✅/❌):**
- Large checkmark/cross
- Green for correct, red for error
- Bold text

**Layout for 4 cases:**
- 2 cases per slide (vertical split)
- OR 4 slides with 1 case each (recommended for clarity)

---

### Sub-slide 4.2: More Demo Cases

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  🎬 CASE 3: FAMILY ATTACK                           │
│  ┌──────────────────────────────────────────────┐  │
│  │  📝 "Ba mẹ mày ngu nên dạy ra thằng con..."  │  │
│  │                                              │  │
│  │  🤖 PREDICTION                               │  │
│  │  Label: 2 (Hate Speech) | Conf: 94.7%       │  │
│  │                                              │  │
│  │  💡 REASONING                                │  │
│  │  ✓ Family attack pattern: "ba mẹ mày"       │  │
│  │  ✓ Derogatory: "ngu", "thằng con"           │  │
│  │  ✓ Guideline V7.2: Auto Hate                │  │
│  │                                              │  │
│  │  ✅ CORRECT!                                 │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  🎬 CASE 4: NARRATIVE FACT                          │
│  ┌──────────────────────────────────────────────┐  │
│  │  📝 "Hình như vụ đó bị tử hình rồi"         │  │
│  │                                              │  │
│  │  🤖 PREDICTION                               │  │
│  │  Label: 0 (Clean) | Conf: 87.2%             │  │
│  │                                              │  │
│  │  💡 REASONING                                │  │
│  │  ✓ Uncertainty markers: "hình như"          │  │
│  │  ✓ Narrative tone (tường thuật)             │  │
│  │  ✓ No incitement                            │  │
│  │                                              │  │
│  │  ✅ CORRECT!                                 │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  📊 DEMO SUMMARY: 4/4 Correct (100%) | Avg: 92.3%  │
└─────────────────────────────────────────────────────┘
```

**Similar design to previous slide, with demo summary at bottom:**

**Demo Summary Box:**
- Background: #E8F5E9 (Light green)
- Border: 2px solid #27AE60
- Large checkmark icon
- Stats in bold
- Centered text

---

### Sub-slide 4.3: Ứng Dụng Thực Tế

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  📱 ỨNG DỤNG THỰC TẾ                                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐  ┌──────────────────────┐   │
│  │  SOCIAL MEDIA   │  │  FORUM MANAGEMENT    │   │
│  │                  │  │                      │   │
│  │  📘 Facebook     │  │  💬 Online Forums    │   │
│  │  ▶️ YouTube      │  │  🛒 E-commerce       │   │
│  │  📱 TikTok       │  │  📰 News Sites       │   │
│  │                  │  │                      │   │
│  │  Auto-filter     │  │  Auto-moderation     │   │
│  │  toxic comments  │  │  Review filtering    │   │
│  └──────────────────┘  └──────────────────────┘   │
│                                                     │
│  ┌──────────────────┐  ┌──────────────────────┐   │
│  │  CORPORATE      │  │  DEPLOYMENT          │   │
│  │                  │  │                      │   │
│  │  📞 Customer     │  │  ⚡ 1,000 req/s      │   │
│  │     Service      │  │  🚀 K8s scaling      │   │
│  │  👥 Employee     │  │  🐳 Docker ready     │   │
│  │     Comms        │  │  📊 Monitoring       │   │
│  │  🏢 Brand        │  │                      │   │
│  │     Protection   │  │  <100ms response     │   │
│  └──────────────────┘  └──────────────────────┘   │
│                                                     │
│  🏗️ ARCHITECTURE                                   │
│  ┌────────────────────────────────────────────┐   │
│  │  [Client] → [FastAPI] → [Model] → [DB]    │   │
│  │                                            │   │
│  │  Horizontal scaling với Kubernetes         │   │
│  └────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Use Case Cards (2×2 grid):**
- 4 equal cards
- Icon-heavy design
- Platform logos if available
- White background
- Border-left with different colors:
  - Social Media: #3B5998 (Facebook blue)
  - Forum: #FF6B6B (Coral)
  - Corporate: #4CAF50 (Green)
  - Deployment: #9C27B0 (Purple)

**Architecture Diagram:**
- Bottom section
- Flow from left to right
- Boxes with arrows
- Simple, clean design
- Icons for each component
- Subtle gradient background

---

## SLIDE 5: KẾT QUẢ & TÁC ĐỘNG (2.5 phút)

### Sub-slide 5.1: Training Results

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  5. KẾT QUẢ & TÁC ĐỘNG                             │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📈 TRAINING PROGRESSION (5 EPOCHS)                 │
│  ┌─────────────────────────────────────────────┐   │
│  │  0.80 ┃                            ●         │   │
│  │       ┃                         ●            │   │
│  │  0.75 ┃                    ●                 │   │
│  │       ┃               ●                      │   │
│  │  0.70 ┃          ●                           │   │
│  │       ┃                                      │   │
│  │  0.65 ┃                                      │   │
│  │       ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │   │
│  │         1    2    3    4    5               │   │
│  │                 EPOCHS                       │   │
│  │                                              │   │
│  │  ✅ Smooth convergence                       │   │
│  │  ✅ No overfitting                           │   │
│  │  ✅ Val F1: 0.69 → 0.80 (+16%)              │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  🎯 TEST SET RESULTS (763 samples độc lập)         │
│  ┌───────────────────────────────────────────────┐ │
│  │                                               │ │
│  │  ┌─────────────┐  ┌─────────────┐           │ │
│  │  │   F1 SCORE  │  │  ACCURACY   │           │ │
│  │  │             │  │             │           │ │
│  │  │   0.7995    │  │   80.87%    │           │ │
│  │  │             │  │             │           │ │
│  │  │   +11%      │  │   +7.8%     │           │ │
│  │  │  vs target  │  │  vs target  │           │ │
│  │  └─────────────┘  └─────────────┘           │ │
│  │                                               │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Training Curve:**
- Line chart with dots for epochs
- Blue line with gradient below
- Grid lines subtle
- Y-axis: F1 score
- X-axis: Epochs
- Checkmarks for key observations
- Light background (#F8F9FA)

**Test Results Cards:**
- 2 large metric cards side-by-side
- Circular progress indicators
- Large numbers (48pt)
- Green color for positive results
- Percentage increase in smaller text below
- Icon for each metric

---

### Sub-slide 5.2: Comparison & Impact

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  ⚖️ SO SÁNH VỚI YÊU CẦU & BENCHMARK                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  Metric          Target   Achieved   Margin │   │
│  │  ────────────────────────────────────────── │   │
│  │  F1-Score        >0.72    0.7995    +11.0% │   │
│  │  Accuracy        >0.75    0.8087    +7.8%  │   │
│  │  Clean F1        >0.80    0.85      +6.3%  │   │
│  │  Production      Yes      Yes ✅     ✅     │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  🌍 TÁC ĐỘNG XÃ HỘI                                │
│  ┌──────────────────┐  ┌──────────────────────┐   │
│  │  DIRECT IMPACT  │  │  COST SAVINGS        │   │
│  │                  │  │                      │   │
│  │  🛡️ Bảo vệ       │  │  Human: $5-10/hr    │   │
│  │     77.9M users  │  │  AI: $0.001/req     │   │
│  │                  │  │                      │   │
│  │  🌱 Internet     │  │  ROI: 1000x         │   │
│  │     lành mạnh    │  │                      │   │
│  │                  │  │  💰 Cost-effective   │   │
│  └──────────────────┘  └──────────────────────┘   │
│                                                     │
│  🔬 ĐÓNG GÓP KHOA HỌC                              │
│  ┌─────────────────────────────────────────────┐   │
│  │  ✓ Dataset 7,626 samples chất lượng cao    │   │
│  │  ✓ Guideline V7.2 reusable                 │   │
│  │  ✓ Intensity Preservation - Novel approach │   │
│  │  ✓ Open-source potential                   │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Comparison Table:**
- Clean table design
- Header row: Bold, dark background
- Data rows: Alternating light grey/white
- Achieved column: Bold, green
- Margin column: Green with ↑ arrow
- Checkmarks for Yes/No values

**Impact Cards:**
- 2 cards side-by-side
- Icon-driven
- Large numbers
- Color-coded:
  - Direct Impact: Blue theme
  - Cost Savings: Green theme

**Scientific Contribution Box:**
- Background: #F3E5F5 (Light purple)
- Border-left: 4px solid #9C27B0
- Checkmarks in purple
- Each contribution on separate line

---

### Sub-slide 5.3: Roadmap & Conclusion

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  🚀 ROADMAP & KẾT LUẬN                              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🗓️ FUTURE ROADMAP                                 │
│  ┌─────────────────────────────────────────────┐   │
│  │  Q1 2026  Migrate to ViDeBERTa              │   │
│  │           Expected F1: 0.82-0.84            │   │
│  │                                              │   │
│  │  Q2 2026  Scale dataset to 15,000+          │   │
│  │           Active learning pipeline          │   │
│  │                                              │   │
│  │  Q3 2026  Production deployment              │   │
│  │           Docker + Kubernetes                │   │
│  │                                              │   │
│  │  Q4 2026  Multi-modal & Explainable AI      │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  🏆 KẾT LUẬN                                       │
│  ┌─────────────────────────────────────────────┐   │
│  │                                              │   │
│  │  ✅ GIẢI QUYẾT BÀI TOÁN                      │   │
│  │     F1 0.7995 | Accuracy 80.87%             │   │
│  │                                              │   │
│  │  ⭐ INNOVATION                               │   │
│  │     Intensity Preservation                   │   │
│  │                                              │   │
│  │  🎯 VƯỢT TARGET +11%                         │   │
│  │     Production-ready                         │   │
│  │                                              │   │
│  │  🌍 TÁC ĐỘNG XÃ HỘI                          │   │
│  │     Bảo vệ users, Scalable, Real-time       │   │
│  │                                              │   │
│  │  🔬 ĐÓNG GÓP                                 │   │
│  │     Dataset, Guideline, Open-source         │   │
│  │                                              │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Design Details:**

**Roadmap Timeline:**
- Vertical timeline on left
- Quarter markers
- Each phase:
  - Title in bold
  - Description below
  - Icon for phase type
- Progressive color (lighter → darker)
- Connecting line between phases

**Conclusion Box:**
- Large, prominent box
- Center of slide
- 5 key points with icons
- Each point:
  - Emoji/icon
  - Bold title
  - Brief description
- Background gradient: Blue → Purple
- White text
- Drop shadow for elevation

---

## SLIDE 6: Q&A

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│                                                     │
│                                                     │
│                  ❓ Q&A                             │
│                                                     │
│           CẢM ƠN QUÝ BAN GIÁM KHẢO                 │
│                ĐÃ LẮNG NGHE!                       │
│                                                     │
│                                                     │
│  ┌─────────────────────────────────────────���───┐   │
│  │  📧 thientran805954@gmail.com              │   │
│  │  🏫 HUTECH - Lớp 22DTHG2                   │   │
│  │  👥 Trần Thanh Thiện - Nguyễn Đan Huy     │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Design Details:**
- Minimal, clean
- Large Q&A text (72pt)
- Thank you message (36pt)
- Contact info box at bottom
- Background: Same as title slide
- Subtle animation: Question mark bouncing

---

## 🎨 DESIGN SYSTEM SUMMARY

### Typography:
```
Headings:     Montserrat Bold (32-60pt)
Subheadings:  Montserrat SemiBold (24-28pt)
Body:         Open Sans Regular (16-18pt)
Code:         Consolas / Fira Code (14-16pt)
Numbers:      Roboto Bold (for metrics)
```

### Spacing:
```
Slide padding:    40px all sides
Section spacing:  30px between sections
Card padding:     20px
Line height:      1.5 for body text
```

### Icons & Emojis:
```
Use consistent emoji set (system or custom)
Icon size: 32-48px for section headers
Emoji size: 24-32pt inline with text
```

### Animations (subtle):
- Slide transitions: Fade (0.3s)
- Element entrance: Slide from left (0.5s)
- Progress bars: Fill animation (1s)
- Charts: Draw animation (1.5s)
- Avoid excessive motion

---

## 📦 DELIVERABLES CHECKLIST

### PowerPoint/Google Slides File:
- [ ] 7 slides total (Title + 5 main + Q&A)
- [ ] 16:9 aspect ratio
- [ ] Consistent fonts throughout
- [ ] Color palette applied
- [ ] All charts/graphs created
- [ ] Icons/emojis placed
- [ ] Speaker notes added
- [ ] Animations configured (if used)

### Supporting Materials:
- [ ] PDF export (backup)
- [ ] Demo screenshots/videos
- [ ] Handout version (if required)
- [ ] Script printed (for practice)

### Technical Checks:
- [ ] Test on projector/screen
- [ ] Font compatibility verified
- [ ] File size optimized (<50MB)
- [ ] Links working (if any)
- [ ] Animations smooth
- [ ] Readable from 5+ meters away

---

## 💡 PRESENTATION TIPS

### Visual Hierarchy:
1. **Most Important**: Big numbers, innovation highlights
2. **Important**: Key insights, comparisons
3. **Supporting**: Examples, details

### Slide Timing Guide:
- **Average**: 20-30 seconds per sub-slide
- **Demo**: 30-45 seconds per case
- **Charts**: 15-20 seconds to explain
- **Transitions**: 2-3 seconds

### Do's ✅:
- Use high contrast (text vs background)
- Keep text minimal (6-8 lines max per slide)
- Use visuals > text when possible
- Maintain consistent style
- Test readability from distance

### Don'ts ❌:
- Don't overcrowd slides
- Don't use too many fonts (max 2-3)
- Don't use low-quality images
- Don't rely on animations
- Don't use full sentences (bullet points!)

---

## 🎯 FINAL NOTES

### Creating in PowerPoint:
1. Set up master slide with color palette
2. Create text styles (Title, Heading, Body)
3. Build slide-by-slide following this guide
4. Add charts using Excel data
5. Insert icons from PowerPoint library or websites (flaticon.com)
6. Add subtle transitions
7. Review and refine

### Creating in Google Slides:
- Same process as PowerPoint
- Use built-in chart tools
- Google Fonts: Montserrat, Open Sans available
- Easy collaboration and cloud access

### Creating in Canva:
- Use "Presentation" template (16:9)
- Search for "Tech Presentation" templates
- Customize with provided color palette
- Export as PDF or PowerPoint

---

## 🏆 SUCCESS CRITERIA

Your slides are ready when:
✅ Clear hierarchy and flow
✅ Visually appealing and professional
✅ Not too text-heavy
✅ Charts and numbers prominent
✅ Innovation (Intensity Preservation) highlighted
✅ Easy to read from distance
✅ Consistent branding
✅ Within 15-minute timing
✅ Supports your script well
✅ Makes BGK interested and engaged!

---

**GOOD LUCK WITH YOUR PRESENTATION! 🚀**

Bạn đã có hệ thống slide hoàn chỉnh. Giờ chỉ cần triển khai theo guide này!
