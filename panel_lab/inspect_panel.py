"""Inspect the CASMI panel-benchmark tables so we can build an offline rule lab."""

import sys
from pathlib import Path

import pandas as pd

D = Path(r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\data\panel_benchmark")


def head(name, rows=3):
    path = D / name
    if not path.exists():
        print(f"-- {name}: MISSING")
        return
    df = pd.read_parquet(path)
    print(f"-- {name}: {df.shape}  {path.stat().st_size / 1e6:.1f} MB")
    print("   columns:", list(df.columns))
    print(df.head(rows).to_string(max_colwidth=40))
    print()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for name in (
        "panel.parquet",
        "main_candidates.parquet",
        "pubchem_candidates.parquet",
        "panel_fpnet_scores.parquet",
        "panel_fpnet_per_molecule.csv",
        "prior_rule_summary.csv",
    ):
        head(name)


if __name__ == "__main__":
    main()
