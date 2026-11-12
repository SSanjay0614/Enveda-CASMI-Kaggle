import json
from pathlib import Path


def cells(path):
    nb = json.loads(Path(path).read_text(encoding="utf-8"))
    return ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]


for path in ["kernel_v37/casmi_v37_lb487_repro.ipynb", "public_new4/casmi26-peaks-to-structures-v2.ipynb"]:
    c = cells(path)
    print("#" * 40, path, "cell 7")
    print(c[7])
    print("#" * 40, path, "cell 8")
    print(c[8])
