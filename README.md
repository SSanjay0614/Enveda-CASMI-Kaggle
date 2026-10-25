# Enveda CASMI 2026: Molecule Identification from Mass Spectra

An elite, multi-engine competitive machine learning repository developed for the **[Enveda CASMI 2026 Kaggle Competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra)** ($50,000 Prize Pool).

---

## 🔬 Competition Overview

* **Objective:** Predict 2D chemical molecular structures (`SMILES`) of small molecules from biological and botanical extracts using high-resolution tandem mass spectrometry (LC-MS/MS) experimental spectra.
* **Evaluation Metric:** **Mean Reciprocal Rank (MRR@25)** evaluated strictly on the first 14 characters of the molecular InChIKey (`InChIKey-14`), encoding the 2D planar molecular skeleton while remaining invariant to stereochemistry.
* **Compute Sandbox:** Kaggle Cloud GPU runner (NVIDIA T4 / P100), max 9-hour execution budget, strictly zero internet access (`enable_internet: false`) during submission inference.

---

## 📈 Leaderboard Progression & Engineering Milestones

| Version | Tag | Model Architecture / Breakthrough | Public Score | Key Analysis & Forensic Post-Mortem |
| :--- | :--- | :--- | :---: | :--- |
| **V1.0** | `v1.0` | Initial Multi-Engine Pipeline | `0.423` | Baseline verification, dataset mounting, and automated submission harness. |
| **V2.0** | `v2.0` | BioPrior Calibration & Outlier Protection | **`0.429`** *(+0.006)* | Clipped solvent popularity z-score at 8.0, tuned RRF $\alpha=0.65, k=2.5$. |
| **V3.0** | `v3.0` | Lineage A: Data-Behind Architecture | `0.460` | Post-mortem revealed an experimental overlay cell at the notebook end (`metric_identity_fusion`) altered top-1 predictions, reducing the score from `0.464` to `0.460`. |
| **V4.0** | `v4.0` | Lineage B: N1 Challenger Architecture | `0.457` | Proxy GLACIER simulation with N1 adduct handling; slightly lower top-1 hit rate compared to Lineage A. |
| **V5.0** | `v5.0` | Master Cross-Lineage Ensemble | `0.460` | RRF blending of Lineage A and Lineage B diluted high-confidence top-1 answers where one model had direct evidence. |
| **V6.0** | `v6.0` | Dual-Gated Loose PubChem Merge (`dg-gate-loose`) | **`0.464`** | Kaggle submission `57581695`; the claimed `0.497` in the upstream notebook tag is not our score. |
| **V7.0** | `v7.0` | Candidate-Aware PubChem Promotion | **`0.465`** | Submission `57581596`; best confirmed local score. Promotion uses the current PubChem leader's own evidence. |
| **V8.0** | `v8.0` | Candidate-Aware Loose Promotion | **`0.465`** | Submission `57582145`; relaxed candidate-specific thresholds tied V7, no demonstrated gain. |
| **V9.0** | `v9.0` | Apex Supreme Consensus | **`0.464`** | Submission `57582485`; combined prior/gate/shield changes did not improve on V7/V8. |
| **V10.0** | `v10.0` | Unified Frontier Master | **`0.464`** | Submission `57590094`; code still used window-level relative evidence in two promotion branches, despite computing candidate evidence. |
| **V11.0** | `v11.0` | Candidate Evidence Gate Fix | **Corrected competition rerun pending** | Original submission `57619741` failed because the first build asserted when candidate-level evidence was missing. Corrected version 2 was submitted as `57631114`; score pending. |
| **V12.0** | `v12.0` | V7 + Neural Candidate-Only Rerank | **`0.465`** (`57619742`) | Tied V7/V8; candidate-preserving neural rerank did not improve the public score. |
| **V13.0** | `v13.0` | V7 Evidence Gate + Candidate-Aware Early Slots | **Competition rerun pending** (`57631787`) | Controlled V7 branch; visible smoke run processed 12 molecules and retained baseline placeholders for 388. |
| **V14.0** | `v14.0` | Stronger Candidate Evidence Gate + Early Slots | **Competition rerun pending** (`57631794`) | Controlled V7 branch; visible smoke run processed 12 molecules and retained baseline placeholders for 388. |

---

## 🧠 System Architecture

```
                                [Query MS/MS Spectra]
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
         [Precursor Mass Snapping]                       [Ion Mode Separation]
         10 ppm cluster consensus                       Positive & Negative Adducts
                  │                                               │
                  ├───────────────────────────────────────────────┤
                  ▼                                               ▼
     ┌─────────────────────────┐                     ┌─────────────────────────┐
     │   Lineage A: Chemistry  │                     │    Lineage B: Physics   │
     │     Priors & Fold-Safe  │                     │   In-Silico Simulation  │
     ├─────────────────────────┤                     ├─────────────────────────┤
     │ * Fold-Safe FPNet (x5)  │                     │ * N1 Challenger         │
     │ * LOTUS Knowledge Table │                     │ * Joint ICEBERG/GLACIER │
     │ * NPAtlas Bio-Prior     │                     │ * PubChemLite CC0 FPs   │
     │ * Organic Solvent Clip  │                     │ * E2R2 Rank-2 Injection │
     └────────────┬────────────┘                     └────────────┬────────────┘
                  │                                               │
                  └───────────────────────┬───────────────────────┘
                                          ▼
                      ┌───────────────────────────────────────┐
                      │   Candidate-Aware PubChem Promotion   │
                      │ ───────────────────────────────────── │
                      │ * Candidate-Specific Evidence (S, pop)│
                      │ * Elimination of Rank-1 Dilution      │
                      │ * Strict InChIKey-14 Skeleton Dedupe  │
                      └───────────────────┬───────────────────┘
                                          ▼
                         [Top 25 Ranked SMILES per Molecule]
```

---

## 📁 Repository Directory Structure

```
enveda_casmi/
├── kernel/              # Version 1.0: Baseline pipeline (Score: 0.423)
├── kernel_v2/           # Version 2.0: BioPrior outlier protection (Score: 0.429)
├── kernel_v3/           # Version 3.0: Lineage A Data-Behind baseline (Score: 0.460)
├── kernel_v4/           # Version 4.0: Lineage B N1 Challenger baseline (Score: 0.457)
├── kernel_v5/           # Version 5.0: Master Cross-Lineage Ensemble (Score: 0.460)
├── kernel_v6/           # Version 6.0: Dual-Gated Loose PubChem Merge (Score: 0.464)
├── kernel_v7/           # Version 7.0: Candidate-Aware PubChem Promotion (Score: 0.465)
├── kernel_v8/           # Version 8.0: Candidate-Aware Loose Promotion (Score: 0.465)
├── kernel_v9/           # Version 9.0: Apex Supreme Consensus (Score: 0.464)
├── kernel_v10/          # Version 10.0: Unified Frontier Master (Score: 0.464)
├── kernel_v11/          # Version 11.0: Candidate Evidence Gate Fix (corrected Kaggle inference completed)
├── kernel_v12/          # Version 12.0: V7 + neural candidate-only rerank
├── kernel_v13/          # Version 13.0: V7 evidence gate with candidate-aware early slots
├── kernel_v14/          # Version 14.0: stronger evidence gate with candidate-aware early slots
├── public_notebooks/    # Community research archives, genealogies, and source notebooks
├── patch_v6.py          # Python 3.13 & RDKit compatibility patcher for V6
├── prepare_v7.py        # Automated patcher and builder for V7
├── prepare_v11.py       # Automated builder for the V10 candidate-evidence fix
├── prepare_v12.py       # Automated builder for the V7 neural-rerank experiment
├── prepare_v13_v14.py   # Automated builders for two controlled V7 ranking-policy branches
└── README.md            # Comprehensive documentation and experiment tracking
```

### Current V6–V14 findings

Kaggle submission history confirms V6 = **0.464**, V7 = **0.465**, V8 = **0.465**, V9 = **0.464**, V10 = **0.464**, and V12 = **0.465**. The V12 neural candidate-only rerank tied the existing best; the extra threshold/prior/shield combinations in V8–V10 also did not improve on V7. V11's first hidden-test submission failed because missing candidate evidence raised an assertion; the local smoke test did not exercise that branch. The V11 builder has now been corrected so unavailable/nonfinite evidence blocks only promotion and is audited, rather than aborting inference.

V12 returns to the best confirmed **V7** baseline rather than stacking V11. It reranks only the existing top-25 candidates using the public CASMI spectrum-candidate model and fixed reciprocal-rank fusion (`weight=0.15`, `offset=3`). Competition submission `57619742` scored **0.465**, tying V7/V8. The newer Sanpier notebook is titled 0.466, but its own report says the 0.15 weight is unvalidated and documents only a submission experiment; its model diagnostic is on a random molecular holdout with the answer guaranteed in a limited candidate set, not leaderboard MRR. The experiment therefore did not establish a gain. Kaggle's dataset listing reports the model asset license as unknown; V12 references the public dataset directly rather than copying its implementation or checkpoint into this repository.

V13 and V14 are controlled inference-policy branches from V7, not newly trained models. They keep candidate generation, weights, simulator, and fusion fixed; only the PubChem promotion threshold and candidate-aware early-slot decision differ. Public replay on a curated 250-molecule natural-product panel motivates testing them: for the answer-removed-from-reference scenario, paired MRR@25 deltas were +0.1994 (95% bootstrap CI +0.1649 to +0.2341) for V13 and +0.2432 (+0.2023 to +0.2839) for V14. Those are panel-replay results, not competition-hidden-set estimates; the library and no-reference scenarios were approximately flat or slightly negative. Both Kaggle visible smoke runs completed and both versions were submitted for hidden-test reruns: V13 `57631787`, V14 `57631794`. Their visible smoke path processed 12 molecules, preserving the baseline rows for the other 388; this is intentional notebook behavior, with the competition rerun expected to process the full hidden set. V13's smoke CSV matched the official 400-row template with nonempty predictions. Neither candidate has a leaderboard score yet, so no gain is established.

### Next-version and submission plan

The public [identity-disjoint validation-fold dataset](https://www.kaggle.com/datasets/dmitriigluzdov/casmi26-natural-product-panel-benchmark) includes five ready-made identity folds and harder scaffold/library/instrument splits. Its documentation confirms that random spectrum splits leak heavily: 185,962 molecules occur on both sides of a random 20% split. The inference runs establish execution and visible-output shape only; the submitted hidden reruns are needed for competition scores. For predictive validation beyond the leaderboard, use identity-held-out data with validation identities removed from label-derived models, reference spectra, and candidate pools, and report official MRR@25 plus truth-in-candidate recall at 1/5/25.

V11 version 2, V13, and V14 are pending hidden competition reruns. The two available daily attempts were used for V13 and V14; Kaggle reports **0 submissions remaining today**. Do not interpret the curated-panel deltas or visible smoke runs as leaderboard results.

---

## 🛠️ Execution & Deployment

Every kernel version is configured with a complete `kernel-metadata.json` and notebook ready for direct deployment via Kaggle CLI:

```powershell
# Deploying Version 7
kaggle kernels push -p enveda_casmi/kernel_v7
```
