"""Dump the cells we must patch to run the V18 pipeline on CPU with our own eval inputs."""

import os
import sys

import pandas as pd

NB = (
    r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\kernel_v18"
    r"\casmi26-v18-neural-rerank.ipynb"
)
SMOKE = (
    r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\kernel_v15"
    r"\output\smoke_comp\test.parquet"
)
CELLS = [5, 29, 31]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    import json

    with open(NB, encoding="utf-8") as handle:
        cells = json.load(handle)["cells"]
    for index in CELLS:
        print("=" * 25, "cell", index)
        print("".join(cells[index]["source"])[:3000])
    print("=" * 25, "smoke test.parquet exists:", os.path.exists(SMOKE))
    if os.path.exists(SMOKE):
        df = pd.read_parquet(SMOKE)
        print(df.shape)
        print(df.dtypes.to_string())
        print(df.head(2).to_string(max_colwidth=45)[:1200])


if __name__ == "__main__":
    main()
