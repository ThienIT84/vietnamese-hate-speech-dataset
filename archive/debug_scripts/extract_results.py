import json

with open('TOXIC_COMMENT/notebooks/safesense-vi-videber-v2-toxic-comment-classificat _ketqua.ipynb', encoding='utf-8') as f:
    data = json.load(f)

cells = data['cells']

# Find training loop cell output
for i, cell in enumerate(cells):
    outputs = cell.get('outputs', [])
    for output in outputs:
        text = output.get('text', '')
        if isinstance(text, list):
            text = ''.join(text)
        if 'Train Loss' in text or 'TRAINING COMPLETE' in text:
            print(f"=== Cell {i} Output ===")
            print(text[:2000])
            print()
