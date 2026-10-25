# Version 7 (V7) — Candidate-Aware PubChem Promotion SOTA (LB 0.465 Frontier)

## 1. Overview & Competitive Context
Version 7 integrates the breakthrough innovation from Saner Turhaner ([sanpier/candidate-aware-pubchem-promotion-0-465](https://www.kaggle.com/code/sanpier/candidate-aware-pubchem-promotion-0-465)), which established the verified highest public score (**0.465**) in the CASMI 2026 competition.

## 2. The Core Innovation: Candidate-Aware vs Channel-Level Promotion
In all previous public pipelines (Dmitrii Gluzdov V16-V24, Bob V18, canqiang E006):
- PubChem candidate structures were promoted to **Rank 1** whenever channel-level statistics satisfied:
  $S_{\text{channel}} > S_{\tau} \text{ (6.0)}$ and $\text{pop}_{\text{channel}} \ge \text{pop}_{\tau} \text{ (5.0)}$ or $\Delta_{\text{retrieval}} > 150.0$.
- **The Critical Flaw:** $S$ and $\text{pop}$ were computed as the *maximum* across the entire mass-window retrieval pool. If a single irrelevant molecule in the window had high popularity or score, the top retrieved candidate was promoted to Rank 1 *even if that specific candidate was low-confidence or weakly documented*!
- **Sanpier's Fix:** The promotion decision evaluates the candidate's **own specific evidence**:
  ```python
  def candidate_promotion_evidence(p):
      key = p['pc_keys'][0]
      evidence = p.get('promotion_evidence', {}).get(key)
      S, pop, raw = (float(evidence[x]) for x in ('S', 'pop', 'raw_fz'))
      return S, pop, raw
  ```
  Rank 1 promotion is granted *only* when the specific leader satisfies $(S_{\text{candidate}} > 6.0 \land \text{pop}_{\text{candidate}} \ge 5.0) \lor \Delta_{\text{candidate}} > 150.0$.

## 3. Elimination of Top-1 Rank Dilution
- In V3 (Dmitrii Gluzdov), an experimental post-processing cell (`metric_identity_fusion`) was appended at the very end of the notebook. That cell reordered top-1 predictions and dropped the public leaderboard score from `0.464` down to `0.460`.
- In V7, this experimental overlay is completely removed. Pure candidate-aware scoring flows directly into `submission.csv`.

## 4. Environment & Platform Patches
- Patched Python 3.13 and RDKit version assertions across Cells 26, 28, and 48 for seamless execution on Kaggle Cloud GPU environments.

## 5. Kaggle Configuration
- **Kernel ID:** `sanjay0614/casmi26-v7-candidate-aware-0465`
- **Accelerator:** GPU (NVIDIA T4)
- **Internet:** Off
- **Competition:** `enveda-CASMI26-molecule-id-mass-spectra`
- **Attached Datasets (5 Verified):**
  1. `dmitriigluzdov/casmi26-fold-safe-fpnet`
  2. `dmitriigluzdov/casmi26-natural-product-knowledge-table`
  3. `dmitriigluzdov/casmi26-natural-product-panel-benchmark`
  4. `dmitriigluzdov/casmi26-pubchem-popularity-prior`
  5. `dmitriigluzdov/casmi26-attributed-v4g-reproduction-assets`
