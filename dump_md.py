import json, re
from pathlib import Path

p = Path("public_new4/casmi26-peaks-to-structures-v2.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
md = [(i, "".join(c["source"])) for i, c in enumerate(nb["cells"]) if c["cell_type"] == "markdown"]
for i, s in md:
    print("=" * 25, "markdown cell", i, len(s))
    print(s[:2500])
