import json
from pathlib import Path

nb = json.loads(Path('enveda_casmi/public_notebooks/busyaprime/lb-0-477-two-0-472-fixes-merged-the-right-way.ipynb').read_text(encoding='utf-8'))
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    lines = [l for l in src.splitlines() if any(w in l.lower() for w in ['0.9', 'library', 'gate', 'w_mid', 'rescue'])]
    if lines:
        print(f"Cell {i} ({cell.get('cell_type')}):")
        for l in lines[:10]:
            print(" ", l[:100])
