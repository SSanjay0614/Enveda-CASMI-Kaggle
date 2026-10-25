# Version 6 (V6) — Dual-Gated Loose PubChem Promotion

## 1. Overview & Competitive Context
Our V6 submission `57581695` scored **0.464**. The upstream kernel slug contains `v497`, but that is not evidence that our submitted version achieved 0.497; the V6-V10 results below are the scores returned by this account's Kaggle submissions.

## 2. Core Architecture & Enhancements over V3/V5

1. **Dual-Gated Loose PubChem Promotion (`dg-gate-loose`):**
   - In previous versions (V3/V5), PubChem-only candidates were rigidly filtered or aggressively blocked unless library match confidence was exceedingly low (`lib_max < 0.9`), starving molecules of valid novel structures.
   - V6 implements an adaptive loose threshold with synonym-count weighting, enabling high-scoring novel candidates to reach the top-25 ranking.

2. **ICEBERG/GLACIER path:**
   - Uses the selected upstream inference pipeline and its simulator configuration. Do not describe disabling ICEBERG as a verified correction: the score table provides no isolated ablation demonstrating that change helps.

3. **Natural Product Knowledge Tables (LOTUS & NPAtlas Fusion):**
   - Integrates the curated 2026 LOTUS database and NPAtlas citation tables from `dmitriigluzdov/casmi26-natural-product-knowledge-table`.
   - Structural likelihoods are up-weighted when natural-product occurrence is supported by multi-source botanical literature.

4. **Five Fold-Safe FPNet Fingerprint Models:**
   - Instead of a single FPNet model, evaluates an ensemble of five fold-safe fingerprint models (`dmitriigluzdov/casmi26-fold-safe-fpnet`) to predict molecular fingerprint probabilities robustly.

5. **Sodiated and Non-[M+H]+ Proxy Alignment:**
   - Enhanced handling for alternative adducts (`[M+Na]+`, `[M+K]+`) using proxy reference spectra from MassBank, MoNA, and GNPS.

## 3. Kaggle Configuration

- **Kernel ID:** `sanjay0614/casmi26-v6-dg-gate-loose-sota`
- **Accelerator:** GPU (NVIDIA T4)
- **Internet:** Off
- **Competition:** `enveda-CASMI26-molecule-id-mass-spectra`
- **Attached Datasets (5 Verified):**
  1. `dmitriigluzdov/casmi26-fold-safe-fpnet`
  2. `dmitriigluzdov/casmi26-natural-product-knowledge-table`
  3. `dmitriigluzdov/casmi26-natural-product-panel-benchmark`
  4. `dmitriigluzdov/casmi26-pubchem-popularity-prior`
  5. `dmitriigluzdov/casmi26-attributed-v4g-reproduction-assets`

## 4. Result interpretation

The public score is the only confirmed V6 leaderboard result. Local output/audit artifacts in this folder are smoke-run artifacts and are not independent held-out accuracy measurements.
