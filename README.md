# Enveda CASMI 2026: Molecule Identification from Mass Spectra

An elite, multi-engine competitive machine learning repository developed for the **[Enveda CASMI 2026 Kaggle Competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra)** ($50,000 Prize Pool).

---

## 🔬 Competition Overview

* **Objective:** Predict 2D chemical molecular structures (`SMILES`) of small molecules from biological and botanical extracts using high-resolution tandem mass spectrometry (LC-MS/MS) experimental spectra.
* **Evaluation Metric:** **Mean Average Precision (MRR@25)** evaluated strictly on the first 14 characters of the molecular InChIKey (`InChIKey-14`), which encodes the 2D planar molecular skeleton while remaining invariant to stereochemistry.
* **Compute Sandbox:** Kaggle Cloud GPU runner (NVIDIA T4 / P100), max 9-hour execution budget, strictly zero internet access (`enable_internet: false`) during submission inference.

---

## 📈 Leaderboard Progression & Engineering Milestones

| Version | Tag | Model Architecture / Breakthrough | Public Score | Key Focus |
| :--- | :--- | :--- | :---: | :--- |
| **V1.0** | `v1.0` | Initial Multi-Engine Pipeline (Clickbait baseline) | `0.423` | Baseline verification, dataset mounting, and automated submission harness |
| **V2.0** | `v2.0` | BioPrior Calibration & Outlier Protection | **`0.429`** *(+0.006)* | Clipped raw solvent popularity z-score at 8.0, tuned RRF $\alpha=0.65, k=2.5$, adaptive DreaMS injection |
| **V3.0** | `v3.0` | Lineage A: Data-Behind SOTA Architecture | *Target: 0.464* | Fold-Safe FPNet, LOTUS/NPAtlas Knowledge Table, Python 3.13 compatibility fix |
| **V4.0** | `v4.0` | Lineage B: N1 Challenger Architecture | *Target: 0.462* | Joint ICEBERG + proxy GLACIER simulation, PubChemLite CC0 candidate fingerprints |
| **V5.0** | `v5.0` | **Master Cross-Lineage Ensemble** | **Target: 0.490–0.50+** | Multi-source candidate fusion, calibrated 0.85 Sovereign Library Shield, InChIKey-14 deduplication |

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
     │ * Fold-Safe FPNet       │                     │ * N1 Challenger         │
     │ * LOTUS Knowledge Table │                     │ * Joint ICEBERG/GLACIER │
     │ * NPAtlas Bio-Prior     │                     │ * PubChemLite CC0 FPs   │
     │ * Organic Solvent Clip  │                     │ * E2R2 Rank-2 Injection │
     └────────────┬────────────┘                     └────────────┬────────────┘
                  │                                               │
                  └───────────────────────┬───────────────────────┘
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    Master Cross-Lineage RRF Blend     │
                      │ ───────────────────────────────────── │
                      │ * Sovereign Library Shield (tau=0.85) │
                      │ * Strict InChIKey-14 Skeleton Dedupe  │
                      │ * Adaptive Multi-Tier Mass Backfill   │
                      └───────────────────┬───────────────────┘
                                          ▼
                         [Top 25 Ranked SMILES per Molecule]
```

---

## 📁 Repository Directory Structure

```
enveda_casmi/
├── kernel/              # Version 1.0: Initial reproduction baseline (Score: 0.423)
├── kernel_v2/           # Version 2.0: BioPrior outlier protection & tuned RRF (Score: 0.429)
├── kernel_v3/           # Version 3.0: Lineage A Data-Behind SOTA (Target: 0.464)
├── kernel_v4/           # Version 4.0: Lineage B N1 Challenger SOTA (Target: 0.462)
├── kernel_v5/           # Version 5.0: Master Cross-Lineage Ensemble (Target: 0.490 - 0.50+)
├── public_notebooks/    # Community research archives and reverse-engineered lineage tree
│   ├── chain/           # Full genealogical audit of all 170+ public versions
│   ├── data_behind/     # Reference source for Lineage A (0.464)
│   ├── evidence_gap/    # Reference source for Lineage B (0.462)
│   └── lb_top1/         # Reference source for early V1 baseline
├── prepare_v3.py        # Automated patcher for Python 3.13 assertions & popularity clipping
├── prepare_v4.py        # Automated verification script for Lineage B
├── prepare_v5.py        # Automated blender configuration for Master Ensemble
├── update_v2.py         # Version 2 feature patcher
└── inspect_enveda.py    # Kaggle API live status & dataset querying utility
```

---

## 🛠️ Reproduction & Kaggle Execution

Every version folder contains a self-contained notebook (`.ipynb`) and its corresponding `kernel-metadata.json`. You can push any version directly to Kaggle using the Kaggle CLI:

```bash
# Example: Deploying Version 5
kaggle kernels push -p enveda_casmi/kernel_v5
```
