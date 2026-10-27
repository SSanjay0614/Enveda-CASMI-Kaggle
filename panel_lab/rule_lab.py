"""Offline CPU rule lab for the PubChem-channel ordering on the 250-molecule NP panel.

Mirrors the production scoring formula in the V18 PubChem runner:

    score = z(fp) + lam * ( log1p(sid) + log1p(pmid)
                            + SRC_BONUS*src_mask   [if src_bonus]
                            + NP_BONUS*np          [if np_bonus]
                            + LOTUS_W*log1p(refs)  [if lotus_w] )

z(fp) is taken within the candidate subset; `pass1` additionally reproduces the
production truncation (top-1000 by the cheap partial score, union top-200 by the
prior).  Pool keys are NOT removed here: the panel's ground truth is inside the
main pool for every molecule, so removing pool rows would make every rule score
zero.  What is being compared, therefore, is the channel's ORDERING quality --
the thing that decides which PubChem proposals take the interleaved slots and
which one the promotion gate can put first.

Two fingerprints:
  fold0_full -- fold-safe checkpoint that never saw these molecules (honest column)
  ab_full    -- the A+B model that has seen them (optimistic; README 0.51/0.95 regime)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\data\panel_benchmark")

PC_N1 = 1000
POP_UNION = 200
TOPN = 25


@dataclass(frozen=True)
class Rule:
    name: str
    lam: float = 0.15
    src_bonus: float = 0.0
    np_bonus: float = 0.0
    lotus_w: float = 0.0


def load() -> pd.DataFrame:
    cand = pd.read_parquet(
        D / "pubchem_candidates.parquet",
        columns=["molecule", "tier_row", "is_truth", "connectivity"],
    )
    fp = pd.read_parquet(
        D / "panel_fpnet_scores.parquet",
        columns=["molecule", "tier_row", "ab_full", "fold0_full", "ab_partial", "fold0_partial"],
    )
    sig = pd.read_parquet(
        D / "pubchem_signals.parquet",
        columns=["molecule", "tier_row", "lsid", "lpmid", "np", "src_mask", "lotus_refs"],
    )
    frame = cand.merge(fp, on=["molecule", "tier_row"], how="left", validate="one_to_one")
    return frame.merge(sig, on=["molecule", "tier_row"], how="left", validate="one_to_one")


def prior_of(block: pd.DataFrame, rule: Rule) -> np.ndarray:
    prior = rule.lam * (block.lsid.to_numpy(np.float64) + block.lpmid.to_numpy(np.float64))
    if rule.src_bonus:
        prior = prior + rule.src_bonus * ((block.src_mask.to_numpy() & 1) != 0)
    if rule.np_bonus:
        prior = prior + rule.np_bonus * (block.np.to_numpy() != 0)
    if rule.lotus_w:
        prior = prior + rule.lotus_w * np.log1p(block.lotus_refs.to_numpy(np.float64))
    return prior


def rr_of(block: pd.DataFrame, rule: Rule, col: str, pass1: bool) -> float:
    full = block[col].to_numpy(np.float64)
    prior = prior_of(block, rule)
    keep = np.arange(len(block))
    if pass1:
        partial = block[col.replace("_full", "_partial")].to_numpy(np.float64)
        n = len(block)
        n1 = min(PC_N1, n)
        top = set(np.argpartition(-partial, n1 - 1)[:n1].tolist()) if n1 > 1 else {0}
        if POP_UNION and n > 1:
            ku = min(POP_UNION, n)
            top |= set(np.argpartition(-prior, ku - 1)[:ku].tolist())
        keep = np.array(sorted(top))
    fz = full[keep]
    z = (fz - fz.mean()) / (fz.std() + 1e-9)
    sc = z + prior[keep]
    order = keep[np.argsort(-sc, kind="stable")]
    keys = block.connectivity.to_numpy()
    seen, out = set(), []
    for j in order:
        k = keys[j]
        if k in seen:
            continue
        seen.add(k)
        out.append(j)
        if len(out) >= TOPN:
            break
    truth = block.is_truth.to_numpy()
    hit = next((i for i, j in enumerate(out) if truth[j]), None)
    return 1.0 / (hit + 1) if hit is not None else 0.0


def score_rule(frame, rule, col, pass1):
    return np.array([rr_of(b, rule, col, pass1) for _, b in frame.groupby("molecule", sort=False, observed=True)])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    frame = load()
    print(f"rows {len(frame):,} | molecules {frame.molecule.nunique()} | truth rows {int(frame.is_truth.sum())}")

    rules = [
        Rule("fp only", lam=0.0),
        Rule("pop .15 (v16)", lam=0.15),
        Rule("production .15 + src .5 + np 1 + lotus .5", lam=0.15, src_bonus=0.5, np_bonus=1.0, lotus_w=0.5),
        Rule("pop .30", lam=0.30),
        Rule("pop .45", lam=0.45),
        Rule("pop .30 + np 2.0", lam=0.30, np_bonus=2.0),
        Rule("pop .45 + np 2.0", lam=0.45, np_bonus=2.0),
        Rule("pop .30 + np 2.0 + lotus .5", lam=0.30, np_bonus=2.0, lotus_w=0.5),
        Rule("pop .30 + np 2.0 + lotus .5 + src .5", lam=0.30, np_bonus=2.0, lotus_w=0.5, src_bonus=0.5),
    ]

    for col in ("fold0_full", "ab_full"):
        for pass1 in (False, True):
            tag = "pass1+pass2" if pass1 else "full window"
            print(f"\n== {col} / {tag} ==   (MRR@{TOPN} of the channel order)")
            table = {}
            for rule in rules:
                table[rule.name] = score_rule(frame, rule, col, pass1)
                print(f"  {rule.name:44s} {table[rule.name].mean():.4f}")
            base = table["production .15 + src .5 + np 1 + lotus .5"]
            rng = np.random.default_rng(0)
            for challenger in ("pop .30", "pop .30 + np 2.0", "pop .30 + np 2.0 + lotus .5 + src .5"):
                diff = table[challenger] - base
                boots = np.array([diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)])
                lo, hi = np.percentile(boots, [2.5, 97.5])
                print(f"    delta {challenger:42s} {diff.mean():+.4f} [{lo:+.4f}, {hi:+.4f}]")


if __name__ == "__main__":
    main()
