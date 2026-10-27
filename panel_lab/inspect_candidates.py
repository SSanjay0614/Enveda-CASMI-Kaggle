"""Inspect the shipped panel candidate tables: can ranking rules be scored offline?"""

import sys
from pathlib import Path

import pandas as pd

D = Path(r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\data\panel_benchmark")


def show(name, n=4):
    path = D / name
    if not path.is_file():
        print(f"-- {name}: MISSING")
        return None
    df = pd.read_parquet(path)
    print(f"-- {name}: {df.shape}  {path.stat().st_size/1e6:.1f} MB")
    print("   cols:", list(df.columns))
    print(df.head(n).to_string(max_colwidth=34))
    print()
    return df


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    main_c = show("main_candidates.parquet")
    pc = show("pubchem_candidates.parquet")
    fs = show("panel_fpnet_scores.parquet")
    panel = show("panel.parquet")
    if main_c is not None:
        print("main_candidates dtypes:\n", main_c.dtypes.to_string(), sep="")
        print("molecules in main:", main_c[main_c.columns[0]].nunique())
        for col in main_c.columns:
            if main_c[col].dtype.kind in "fi" and col != "molecule":
                print(f"  {col}: min={main_c[col].min():.4g} max={main_c[col].max():.4g}")
    if pc is not None:
        print("\npubchem_candidates dtypes:\n", pc.dtypes.to_string(), sep="")
    if fs is not None:
        print("\npanel_fpnet_scores dtypes:\n", fs.dtypes.to_string(), sep="")


if __name__ == "__main__":
    main()
