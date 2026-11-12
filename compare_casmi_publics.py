import json
from pathlib import Path

nb1 = json.loads(Path('enveda_casmi/public_notebooks/busyaprime/lb-0-477-two-0-472-fixes-merged-the-right-way.ipynb').read_text(encoding='utf-8'))
nb2 = json.loads(Path('enveda_casmi/public_notebooks/andrewoscar_borrow518/casmi26-borrow518.ipynb').read_text(encoding='utf-8'))
nb3 = json.loads(Path('enveda_casmi/public_notebooks/guhongbin_v551/casmi26-v551-frag-wmid0775.ipynb').read_text(encoding='utf-8'))

print("=== Comparing busyaprime vs andrewoscar_borrow518 ===")
for i, (c1, c2) in enumerate(zip(nb1['cells'], nb2['cells'])):
    s1 = "".join(c1.get('source', []))
    s2 = "".join(c2.get('source', []))
    if s1 != s2:
        print(f"Diff in cell {i} ({c1.get('cell_type')})")
        print("--- busyaprime ---")
        print(s1[:200])
        print("--- andrewoscar ---")
        print(s2[:200])
        print()

print("=== Comparing busyaprime vs guhongbin_v551 ===")
for i, (c1, c3) in enumerate(zip(nb1['cells'], nb3['cells'])):
    s1 = "".join(c1.get('source', []))
    s3 = "".join(c3.get('source', []))
    if s1 != s3:
        print(f"Diff in cell {i} ({c1.get('cell_type')})")
        print("--- busyaprime ---")
        print(s1[:200])
        print("--- guhongbin ---")
        print(s3[:200])
        print()
