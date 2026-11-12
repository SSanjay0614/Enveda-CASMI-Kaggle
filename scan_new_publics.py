import json, re
from pathlib import Path

for name in [
    "casmi26-peaks-to-structures-v2.ipynb",
    "0-500-casmi26-dual-neural-physical-isomer.ipynb",
    "ionwraith-v11-evidence-guided-molecule-id.ipynb",
]:
    nb = json.loads((Path("public_new4") / name).read_text(encoding="utf-8"))
    code = "".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    print("=" * 20, name)
    for pat in [
        r"[A-Za-z0-9_\-/]*kaggle/input/[A-Za-z0-9_\-/\.]+",
        r"ext_meta\.parquet",
        r"massbank[^\n\"']{0,90}",
        r"dataset[A-Za-z_]*\s*=\s*[^\n]{0,90}",
    ]:
        hits = sorted(set(re.findall(pat, code, flags=re.I)))[:10]
        print(pat, "->", hits)
