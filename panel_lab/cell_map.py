"""Print a compact cell map of the V18 notebook: index, type, size, first lines."""

import json
import sys

NB = (
    r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\kernel_v18"
    r"\casmi26-v18-neural-rerank.ipynb"
)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with open(NB, encoding="utf-8") as handle:
        cells = json.load(handle)["cells"]
    print(f"total cells: {len(cells)}")
    for index, cell in enumerate(cells):
        text = "".join(cell["source"])
        lines = [line for line in text.splitlines() if line.strip()]
        head = " / ".join(line[:70] for line in lines[:2])
        print(f"{index:3d} {cell['cell_type'][:4]} {len(text):7d} | {head}")


if __name__ == "__main__":
    main()
