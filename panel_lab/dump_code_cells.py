"""Dump selected V18 cells to text files for close reading."""

import json
import sys
from pathlib import Path

NB = Path(
    r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\kernel_v18"
    r"\casmi26-v18-neural-rerank.ipynb"
)
OUT = Path(
    r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\panel_lab\cells"
)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    with open(NB, encoding="utf-8") as handle:
        cells = json.load(handle)["cells"]
    wanted = [int(x) for x in sys.argv[1:]] or list(range(len(cells)))
    for index in wanted:
        cell = cells[index]
        if cell["cell_type"] != "code":
            continue
        path = OUT / f"c{index:02d}.py"
        path.write_text("".join(cell["source"]), encoding="utf-8")
        print(f"wrote {path.name} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
