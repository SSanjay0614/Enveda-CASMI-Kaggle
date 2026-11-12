import json, re
from pathlib import Path

files = [
    "public_new4/casmi26-peaks-to-structures-v2.ipynb",
    "public_new4/0-500-casmi26-dual-neural-physical-isomer.ipynb",
    "public_new4/ionwraith-v11-evidence-guided-molecule-id.ipynb",
    "kernel_v37/*.ipynb",
]
for pat in files:
    for p in sorted(Path(".").glob(pat)):
        nb = json.loads(p.read_text(encoding="utf-8"))
        code = "".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
        print("=" * 30, p)
        pats = sorted(set(re.findall(r"glob\.glob\((.{0,140}?)\)", code)))
        for x in pats:
            print("  glob:", x)
        for key in ["BUNDLE", "materialise_sources", "torch.load", "model.pt", "spectrum_model", "extlib"]:
            hits = code.count(key)
            print(f"  count {key}: {hits}")
