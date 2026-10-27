"""Inspect the identity-disjoint fold tables so the eval kit can build a leakage-free split."""

import sys
from pathlib import Path

import pandas as pd

D = Path(r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\data\identity_folds")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    folds = pd.read_parquet(D / "spectra_folds.parquet")
    print("spectra_folds:", folds.shape)
    print("columns:", list(folds.columns))
    print(folds.dtypes.to_string())
    print()
    print(folds.head(2).to_string(max_colwidth=60))
    print()
    for col in folds.columns:
        if folds[col].dtype.name in ("object", "category", "bool") and col not in ("ms2_mzs", "ms2_normalized_intensities"):
            n = folds[col].nunique(dropna=False)
            if n <= 40:
                print(f"{col}: {n} uniques ->", folds[col].value_counts(dropna=False).to_dict())
    print()
    structs = pd.read_parquet(D / "structures.parquet")
    print("structures:", structs.shape, list(structs.columns))
    splits = pd.read_parquet(D / "structure_splits.parquet")
    print("structure_splits:", splits.shape, list(splits.columns))
    print(splits.head(3).to_string(max_colwidth=40))


if __name__ == "__main__":
    main()
