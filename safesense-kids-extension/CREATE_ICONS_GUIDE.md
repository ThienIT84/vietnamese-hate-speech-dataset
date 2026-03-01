# Quick Icon Generator for SafeSense Kids Guardian

## Option 1: Download Free Icons

Tải icons từ các nguồn miễn phí:

1. **Flaticon** (https://www.flaticon.com/search?word=shield)
   - Search "shield kids"
   - Download 16x16, 48x48, 128x128
   - Rename: icon-16.png, icon-48.png, icon-128.png

2. **Icons8** (https://icons8.com/icons/set/shield)
   - Free PNG icons
   - Multiple sizes available

3. **Noun Project** (https://thenounproject.com/)
   - Search "child protection"

---

## Option 2: Generate with Python (Pillow)

```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    # Create gradient background
    img = Image.new('RGBA', (size, size), (102, 126, 234, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw shield
    shield_color = (255, 255, 255, 230)
    margin = size // 6
    
    # Shield path (simplified)
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=shield_color)
    
    # Draw checkmark or emoji
    try:
        font = ImageFont.truetype("seguiemj.ttf", size // 2)
        draw.text((size // 4, size // 6), "🛡️", 
                 font=font, embedded_color=True)
    except:
        # Fallback: simple checkmark
        draw.line([size//3, size//2, size//2, size*2//3], 
                 fill=(102, 126, 234, 255), width=size//10)
        draw.line([size//2, size*2//3, size*3//4, size//3], 
                 fill=(102, 126, 234, 255), width=size//10)
    
    img.save(output_path)
    print(f"Created {output_path}")

# Generate all sizes
os.makedirs('assets', exist_ok=True)
create_icon(16, 'assets/icon-16.png')
create_icon(48, 'assets/icon-48.png')
create_icon(128, 'assets/icon-128.png')
```

Run: `python generate_icons.py`

---

## Option 3: Convert SVG to PNG

Use online converter:
1. Go to https://svgtopng.com/
2. Upload `assets/icon.svg`
3. Download as 16x16, 48x48, 128x128
4. Save as icon-16.png, icon-48.png, icon-128.png

---

## Option 4: Use Emoji as Icon (Simplest!)

```python
# Simple emoji to PNG
from PIL import Image, ImageDraw, ImageFont

def emoji_to_icon(emoji, size, output):
    img = Image.new('RGBA', (size, size), (102, 126, 234, 255))
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("seguiemj.ttf", int(size * 0.7))
        bbox = draw.textbbox((0, 0), emoji, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((size - w) / 2, (size - h) / 2 - size * 0.1), 
                 emoji, font=font, embedded_color=True)
    except Exception as e:
        print(f"Error: {e}")
        # Fallback
        draw.ellipse([size//4, size//4, 3*size//4, 3*size//4], 
                    fill=(255, 255, 255))
    
    img.save(output)
    print(f"Created {output}")

emoji_to_icon("🛡️", 16, "assets/icon-16.png")
emoji_to_icon("🛡️", 48, "assets/icon-48.png")
emoji_to_icon("🛡️", 128, "assets/icon-128.png")
```

Save as `generate_emoji_icons.py` and run!

---

## Quick Test

After creating icons, enable them in manifest.json:

```json
"icons": {
  "16": "assets/icon-16.png",
  "48": "assets/icon-48.png",
  "128": "assets/icon-128.png"
},
```

Then reload extension!
