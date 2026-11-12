import difflib, json, sys
from pathlib import Path


def cells(path):
    nb = json.loads(Path(path).read_text(encoding="utf-8"))
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


a = cells("kernel_v37/casmi_v37_lb487_repro.ipynb")
b = cells("public_new4/casmi26-peaks-to-structures-v2.ipynb")
for i in [0, 12, 13, 14]:
    print("#" * 30, "cell", i, "v37 vs peaks-v2")
    d = list(difflib.unified_diff(a[i].splitlines(), b[i].splitlines(), "v37", "peaks-v2", n=2, lineterm=""))
    if len(d) > 400:
        d = d[:400] + ["... truncated ..."]
    print("\n".join(d))
