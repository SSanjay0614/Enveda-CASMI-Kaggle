"""Faithful offline replay of the V18 PubChem-only channel on the 250-molecule NP panel.

This mirrors the production runner (`kernel_v18` cell 35):
  pass 1 : the cheap fingerprint score truncates the mass window to the top PC_N1
           rows, union the top POP_UNION rows by the documentation prior
  pass 2 : the full fingerprint score is z-scored WITHIN that subset
  score  : z(fp) + lam * prior, where prior = log1p(sid) + log1p(pmid)
           + SRC_BONUS*mask + NP_BONUS*np + LOTUS_W*log1p(refs)
  output : descending score, one row per connectivity key, pool keys removed

Two fingerprint columns are scored separately:
  ab_full    -- model saw these molecules (optimistic, matches the README 0.51/0.95)
  fold0_full -- fold-safe checkpoint that never saw them (honest)

MRR@25 is reported on the hard subset (the truth is NOT in the main candidate
pool), because that is the only subset where the PubChem channel can decide the
answer; the README's 0.361 -> 0.718 story lives there.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\data\panel_benchmark")

PC_N1 = 1000        # v4n pass-1 depth
POP_UNION = 200     # v17 prior union
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
        columns=["molecule", "tier_row", "is_truth", "in_pool", "connectivity"],
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
    frame = frame.merge(sig, on=["molecule", "tier_row"], how="left", validate="one_to_one")
    return frame


def prior_of(block: pd.DataFrame, rule: Rule) -> np.ndarray:
    prior = rule.lam * (block.lsid.to_numpy(np.float64) + block.lpmid.to_numpy(np.float64))
    if rule.src_bonus:
        prior = prior + rule.src_bonus * ((block.src_mask.to_numpy() & 1) != 0)
    if rule.np_bonus:
        prior = prior + rule.np_bonus * (block.np.to_numpy() != 0)
    if rule.lotus_w:
        prior = prior + rule.lotus_w * np.log1p(block.lotus_refs.to_numpy(np.float64))
    return prior


def channel_list(block: pd.DataFrame, rule: Rule, col: str) -> np.ndarray:
    """Return the channel's ordered keys (pool keys removed), exactly like production."""
    partial = block[col.replace("_full", "_partial")].to_numpy(np.float64)
    full = block[col].to_numpy(np.float64)
    prior = prior_of(block, rule)
    n = len(block)
    n1 = min(PC_N1, n)
    top = set(np.argpartition(-partial, n1 - 1)[:n1].tolist()) if n1 > 1 else {0}
    if POP_UNION:
        ku = min(POP_UNION, n)
        if ku > 1:
            top |= set(np.argpartition(-prior, ku - 1)[:ku].tolist())
    idx = np.array(sorted(top))
    fz = full[idx]
    z = (fz - fz.mean()) / (fz.std() + 1e-9)
    sc = z + prior[idx]
    order = idx[np.argsort(-sc, kind="stable")]
    keys, seen = [], set()
    keys_arr = block.connectivity.to_numpy()
    pool = block.in_pool.to_numpy()
    for j in order:
        k = keys_arr[j]
        if k in seen:
            continue
        seen.add(k)
        if pool[j]:
            continue
        keys.append(k)
        if len(keys) >= TOPN:
            break
    return np.array(keys)


def evaluate(frame: pd.DataFrame, rule: Rule, col: str, subsets: dict[str, list[str]]):
    rr: dict[str, list[float]] = {name: [] for name in subsets}
    leader: dict[str, list[float]] = {name: [] for name in subsets}
    for mid, block in frame.groupby("molecule", sort=False, observed=True):
        truth = block.is_truth.to_numpy()
        truth_keys = set(block.connectivity.to_numpy()[truth].tolist())
        hard = not (truth & block.in_pool.to_numpy()).any()
        name = "hard" if hard else "easy"
        keys = channel_list(block, rule, col)
        hit = next((i for i, k in enumerate(keys) if k in truth_keys), None)
        if mid in subsets[name]:
            rr[name].append(1.0 / (hit + 1) if hit is not None and hit < TOPN else 0.0)
            leader[name].append(1.0 if hit == 0 else 0.0)
    return rr, leader


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    frame = load()
    mols = frame.groupby("molecule", observed=True).agg(
        truth=("is_truth", "any"), pool_truth=("is_truth", lambda s: bool((s & frame.loc[s.index, "in_pool"]).any()))
    )
    hard = mols.index[~mols.pool_truth].tolist()
    easy = mols.index[mols.pool_truth].tolist()
    print(f"panel molecules {len(mols)} | truth in pool {len(easy)} | truth NOT in pool {len(hard)}")
    subsets = {"hard": hard, "easy": easy}

    rules = [
        Rule("fp only (lam 0)", lam=0.0),
        Rule("production lam .15 + src .5 np 1 lotus .5", lam=0.15, src_bonus=0.5, np_bonus=1.0, lotus_w=0.5),
        Rule("pop only lam .15", lam=0.15),
        Rule("pop lam .30", lam=0.30),
        Rule("pop lam .30 + np 2.0", lam=0.30, np_bonus=2.0),
        Rule("pop lam .45 + np 2.0", lam=0.45, np_bonus=2.0),
        Rule("pop lam .30 + np 2.0 + lotus .5", lam=0.30, np_bonus=2.0, lotus_w=0.5),
    ]

    for col in ("fold0_full", "ab_full"):
        print(f"\n== {col} ==")
        print(f"{'rule':46s} {'hard MRR':>9s} {'hard top1':>10s} {'easy MRR':>9s} {'easy top1':>10s}")
        cache = {}
        for rule in rules:
            rr, lead = evaluate(frame, rule, col, subsets)
            cache[rule.name] = rr
            print(
                f"{rule.name:46s} {np.mean(rr['hard']):9.4f} {np.mean(lead['hard']):10.4f}"
                f" {np.mean(rr['easy']):9.4f} {np.mean(lead['easy']):10.4f}"
            )

        base = np.array(cache["production lam .15 + src .5 np 1 lotus .5"]["hard"])
        best_name = "pop lam .30 + np 2.0"
        cand = np.array(cache[best_name]["hard"])
        diff = cand - base
        rng = np.random.default_rng(0)
        boots = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(2000)]
        lo, hi = np.percentile(boots, [2.5, 97.5])
        print(f"paired delta ({best_name} - production), hard subset: {diff.mean():+.4f} [{lo:+.4f}, {hi:+.4f}]")


if __name__ == "__main__":
    main()
