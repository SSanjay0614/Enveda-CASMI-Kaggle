"""Grep the V18 notebook cell-by-cell and print matches with cell index + line number."""

import json
import re
import sys

NB = (
    r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\kernel_v18"
    r"\casmi26-v18-neural-rerank.ipynb"
)

PATTERNS = sys.argv[1].split("|")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    with open(NB, encoding="utf-8") as handle:
        cells = json.load(handle)["cells"]
    for index, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        for lineno, line in enumerate("".join(cell["source"]).splitlines(), 1):
            if any(re.search(pattern, line) for pattern in PATTERNS):
                print(f"c{index}:{lineno}: {line[:190]}")


if __name__ == "__main__":
    main()
