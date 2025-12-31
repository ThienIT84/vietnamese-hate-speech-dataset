import json

try:
    with open(r'c:\Học sâu\Dataset\TOXIC_COMMENT\notebooks\01_Data_Journey_Presentation.ipynb', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f'✅ JSON hợp lệ! Notebook có {len(data["cells"])} cells')
    
    for i, cell in enumerate(data['cells'][:5]):
        print(f'Cell {i+1}: {cell["cell_type"]} - {len(cell["source"])} lines')
        
    # Kiểm tra metadata
    print(f'Nbformat: {data["nbformat"]}.{data["nbformat_minor"]}')
    
except json.JSONDecodeError as e:
    print(f'❌ Lỗi JSON: {e}')
    print(f'Vị trí lỗi: dòng {e.lineno}, cột {e.colno}')
except Exception as e:
    print(f'❌ Lỗi khác: {e}')