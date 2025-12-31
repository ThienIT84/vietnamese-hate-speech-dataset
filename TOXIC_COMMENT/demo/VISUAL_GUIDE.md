# 🔥 Preprocessing Demo - Visual Guide

## 🎨 Interface Preview

```
╔════════════════════════════════════════════════════════════════════╗
║                🔥 Advanced Text Cleaning Demo                      ║
║           Interactive Preprocessing Pipeline for Vietnamese        ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Sidebar          │  Main Content Area                            ║
║  ┌──────────────┐ │  ┌─────────────────────────────────────────┐ ║
║  │ ⚙️ Settings   │ │  │ 🔍 Single Text │ 📊 Batch │ 📖 Examples│ ║
║  │              │ │  └─────────────────────────────────────────┘ ║
║  │ ☑️ Steps     │ │                                              ║
║  │ ☑️ Stats     │ │  ┌─────────────┐   ┌─────────────┐         ║
║  │              │ │  │ 📝 Input    │   │ ✨ Output   │         ║
║  │ Pipeline:    │ │  │             │   │             │         ║
║  │ 1. Unicode   │ │  │ ko biết ns  │→  │ không biết  │         ║
║  │ 2. URLs      │ │  │ gì luôn ạ   │   │ nói gì luôn │         ║
║  │ 3. Tags      │ │  │             │   │ ạ           │         ║
║  │ 4. Mentions  │ │  │             │   │             │         ║
║  │ 5. Teencode✨│ │  └─────────────┘   └─────────────┘         ║
║  │ 6. Names✨   │ │                                              ║
║  │ 7. Lower     │ │  [🚀 Process]  [🗑️ Clear]                  ║
║  │ 8. Emoji✨   │ │                                              ║
║  │ ...          │ │  ─────────────────────────────────────────  ║
║  └──────────────┘ │  🔬 Step-by-Step Pipeline                   ║
║                   │                                              ║
║                   │  ✅ Step 6: Teencode - CHANGED               ║
║                   │     Before: ko biết ns gì                    ║
║                   │     After:  không biết nói gì                ║
║                   │                                              ║
║                   │  ✅ Step 9: Emoji - CHANGED                  ║
║                   │     Before: nguuu 😡                         ║
║                   │     After:  ngu <intense> <emo_neg>         ║
║                   │                                              ║
║                   │  ─────────────────────────────────────────  ║
║                   │  📊 Statistics                               ║
║                   │  Original: 35 │ Cleaned: 52 │ Tags: 2       ║
║                   │                                              ║
║                   │  Detected Features:                          ║
║                   │  - 😡 Negative Emotion                       ║
║                   │  - ⚡ Intensity Markers                       ║
╚════════════════════════════════════════════════════════════════════╝
```

## 🔄 Processing Flow

### Single Text Flow:
```
┌──────────────┐
│ User Input   │
│ "ko biết ns" │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────┐
│   Advanced Pipeline (14 Steps)   │
├───────────────────────────────────┤
│ 1. Unicode NFC                    │
│ 2. Remove URLs/HTML               │
│ 3. Remove Hashtags                │
│ 4. Remove Mentions                │
│ 5. 🔥 Teencode Normalize          │
│ 6. 🔥 Person Names → <person>     │
│ 7. Lowercase                      │
│ 8. 🔥 Emoji → Tags                │
│ 9. 🔥 English Insults             │
│ 10. Bypass Patterns               │
│ 11. Leetspeak                     │
│ 12. 🔥 Repeated Chars + Intensity │
│ 13. 🔥 Context-aware "m"          │
│ 14. Punctuation + Whitespace      │
└───────────┬───────────────────────┘
            │
            ▼
     ┌──────────────┐
     │ Clean Output │
     │ "không biết  │
     │  nói"        │
     └──────────────┘
```

### Batch Processing Flow:
```
┌─────────────────┐
│ Upload File     │
│ (.txt or .csv)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Select Column   │
│ (if CSV)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Process All     │
│ ╔══════════╗    │
│ ║ █████░░░ ║    │ Progress bar
│ ║   80%    ║    │
│ ╚══════════╝    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Results Table   │
│ ┌──────────────┐│
│ │ID│Original  ││
│ │1 │ko biết   ││
│ │2 │m yêu t   ││
│ └──────────────┘│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Download CSV    │
│ 📥 cleaned.csv  │
└─────────────────┘
```

## 🎯 Tab Navigation

```
╔════════════════════════════════════════════════════╗
║  [🔍 Single Text] │ [📊 Batch] │ [📖 Examples]    ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  TAB 1: Single Text Processing                    ║
║  ┌──────────────────────────────────────────────┐ ║
║  │ • Input box                                  │ ║
║  │ • Process button                             │ ║
║  │ • Output display                             │ ║
║  │ • Step-by-step view (optional)               │ ║
║  │ • Statistics (optional)                      │ ║
║  └──────────────────────────────────────────────┘ ║
║                                                    ║
║  TAB 2: Batch Processing                          ║
║  ┌──────────────────────────────────────────────┐ ║
║  │ • File upload (TXT/CSV)                      │ ║
║  │ • Column selection                           │ ║
║  │ • Process all button                         │ ║
║  │ • Results table                              │ ║
║  │ • Download CSV button                        │ ║
║  └──────────────────────────────────────────────┘ ║
║                                                    ║
║  TAB 3: Example Use Cases                         ║
║  ┌──────────────────────────────────────────────┐ ║
║  │ • 9 pre-made examples                        │ ║
║  │ • Test buttons                               │ ║
║  │ • Expected vs Actual comparison              │ ║
║  │ • Copy examples                              │ ║
║  └──────────────────────────────────────────────┘ ║
╚════════════════════════════════════════════════════╝
```

## 📊 Statistics Display

```
╔═══════════════════════════════════════════════╗
║           📊 Statistics                       ║
╠═══════════════════════════════════════════════╣
║  ┌────────────┬────────────┬──────────────┐  ║
║  │ Original   │ Cleaned    │ Reduction    │  ║
║  │    35      │    52      │    -17       │  ║
║  └────────────┴────────────┴──────────────┘  ║
║                                               ║
║  ┌──────────────────────────────────────┐    ║
║  │ Tags Added                           │    ║
║  │        2                             │    ║
║  └──────────────────────────────────────┘    ║
║                                               ║
║  Detected Features:                           ║
║  ┌────────────────────────────────────────┐  ║
║  │ ✓ 😡 Negative Emotion                  │  ║
║  │ ✓ ⚡ Intensity Markers                  │  ║
║  │ ✓ 👤 Person Names                      │  ║
║  │ ✓ @ Mentions                           │  ║
║  │ ✓ 🌐 English Insults                   │  ║
║  └────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════╝
```

## 🔬 Step-by-Step Example

```
Input: "Đ.m nguuuu vcl 😡 ko biết ns gì ạ"

╔════════════════════════════════════════════════╗
║  Step 1: Unicode Normalize                    ║
║  Before: Đ.m nguuuu vcl 😡 ko biết ns gì ạ   ║
║  After:  Đ.m nguuuu vcl 😡 ko biết ns gì ạ   ║
║  Status: ⏭️ No change                          ║
╚════════════════════════════════════════════════╝

╔════════════════════════════════════════════════╗
║  Step 6: 🔥 Teencode Normalize                ║
║  Before: Đ.m nguuuu vcl 😡 ko biết ns gì ạ   ║
║  After:  Đ.m nguuuu vcl 😡 không biết nói gì ạ║
║  Status: ✅ CHANGED                            ║
║          ┗━━━━━━━━━━━┛ ┗━━━━━━━┛              ║
║             ko→không      ns→nói              ║
╚════════════════════════════════════════════════╝

╔════════════════════════════════════════════════╗
║  Step 7: Lowercase                            ║
║  Before: Đ.m nguuuu vcl 😡 không biết nói gì ạ║
║  After:  đ.m nguuuu vcl 😡 không biết nói gì ạ║
║  Status: ✅ CHANGED                            ║
║          ┗━┛                                   ║
║          Đ→đ                                   ║
╚════════════════════════════════════════════════╝

╔════════════════════════════════════════════════╗
║  Step 9: 🔥 Emoji → Tags                      ║
║  Before: đ.m nguuuu vcl 😡 không biết nói gì ạ║
║  After:  đ.m nguuuu vcl <emo_neg> không biết..║
║  Status: ✅ CHANGED                            ║
║                      ┗━━━━━━━━━┛              ║
║                       😡→<emo_neg>            ║
╚════════════════════════════════════════════════╝

╔════════════════════════════════════════════════╗
║  Step 12: 🔥 Bypass Patterns                  ║
║  Before: đ.m nguuuu vcl <emo_neg> không biết..║
║  After:  đm nguuuu vcl <emo_neg> không biết.. ║
║  Status: ✅ CHANGED                            ║
║          ┗━┛                                   ║
║          đ.m→đm                                ║
╚════════════════════════════════════════════════╝

╔════════════════════════════════════════════════╗
║  Step 14: 🔥 Repeated Chars + Intensity       ║
║  Before: đm nguuuu vcl <emo_neg> không biết.. ║
║  After:  đm ngu <intense> vcl <emo_neg> ...   ║
║  Status: ✅ CHANGED                            ║
║             ┗━━━━━━━━━━┛                       ║
║             nguuuu→ngu <intense>              ║
╚════════════════════════════════════════════════╝

Final Output:
┌────────────────────────────────────────────────┐
│ đm ngu <intense> vcl <emo_neg> không biết     │
│ nói gì ạ                                       │
└────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

```
┌─────────────────────────────────────┐
│  Input Box   │ #fff3cd │ 🟡 Yellow │
│  Output Box  │ #d4edda │ 🟢 Green  │
│  Step Box    │ #f0f2f6 │ 🔵 Blue   │
│  Changed     │ #fff3cd │ 🟡 Yellow │
└─────────────────────────────────────┘
```

## 📱 Responsive Design

### Desktop View (Wide):
```
┌──────────┬─────────────────────────────┐
│ Sidebar  │  Main Content (Full width)  │
│ (Fixed)  │  ┌───────────────────────┐  │
│          │  │ Tabs                  │  │
│          │  └───────────────────────┘  │
│          │  ┌────────┬──────────────┐  │
│          │  │ Input  │  Output      │  │
│          │  └────────┴──────────────┘  │
└──────────┴─────────────────────────────┘
```

### Tablet/Mobile (Narrow):
```
┌───────────────────────┐
│ Sidebar (Collapsible) │
├───────────────────────┤
│ Main Content          │
│ ┌───────────────────┐ │
│ │ Tabs              │ │
│ └───────────────────┘ │
│ ┌───────────────────┐ │
│ │ Input (Full)      │ │
│ └───────────────────┘ │
│ ┌───────────────────┐ │
│ │ Output (Full)     │ │
│ └───────────────────┘ │
└───────────────────────┘
```

## 🎯 Quick Actions

```
Main Actions:
┌────────────────────────────────┐
│ [🚀 Process Text]              │ Primary
│ [🗑️  Clear Input]               │ Secondary
│ [📥 Download Results]          │ Success
│ [🔄 Reset Settings]            │ Info
└────────────────────────────────┘
```

---

**Visual Guide v1.0 - December 31, 2025**
