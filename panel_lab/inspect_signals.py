"""Columns of the auxiliary prior tables, so the rule lab can mirror production exactly."""

import sys
from pathlib import Path

import pandas as pd

D = Path(r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\data\panel_benchmark")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for name in ("pubchem_signals.parquet", "pubchemlite_annotations.parquet",
                 "panel_same_formula.parquet", "panel_tier_formulas.parquet"):
        path = D / name
        if not path.is_file():
            print(f"-- {name}: MISSING")
            continue
        df = pd.read_parquet(path)
        print(f"-- {name}: {df.shape}")
        print("   cols:", list(df.columns))
        print(df.head(3).to_string(max_colwidth=30))
        print()


if __name__ == "__main__":
    main()
