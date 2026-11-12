import json
from pathlib import Path

for name in ['andrewoscar_borrow518', 'guhongbin_v551']:
    p = Path(f'enveda_casmi/public_notebooks/{name}')
    nb_files = list(p.glob('*.ipynb'))
    if not nb_files:
        continue
    nb = json.loads(nb_files[0].read_text(encoding='utf-8'))
    print(f"=== {name}: {nb_files[0].name} (cells: {len(nb['cells'])}) ===")
    meta_path = p / 'kernel-metadata.json'
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        print(f"Title: {meta.get('title')}")
        print(f"Datasets: {meta.get('dataset_sources', [])}")
        print(f"Kernels: {meta.get('kernel_sources', [])}")
    for i, cell in enumerate(nb['cells'][:8]):
        src = "".join(cell.get('source', []))
        first = src.splitlines()[0] if src.splitlines() else ""
        print(f"  Cell {i} ({cell.get('cell_type')}): {first[:80]}")
    print()
