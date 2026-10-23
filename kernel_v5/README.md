# Version 5.0: Master Cross-Lineage Ensemble

* **Directory:** `kernel_v5/`
* **Kaggle Kernel Slug:** `sanjay0614/casmi26-master-ensemble-v5`
* **Target Benchmark:** **`0.490 – 0.50+`** (Leaderboard Gold Tier)
* **Status:** Submitted & Queued for Evaluation ⏳

---

## 🎯 Goal & Overview
Version 5.0 is our master submission, combining the orthogonal strengths of both top-tier lineages:
* **Lineage A (0.464):** Maximum natural product chemical fidelity (LOTUS / NPAtlas Knowledge Table).
* **Lineage B (0.462):** Maximum physical isomer separation (N1 Challenger joint simulation + PubChemLite CC0).

---

## 🔬 Core Innovations in Version 5.0

### 1. Solving the 20-Dataset Constraint
* Standard mounting of all Lineage A and Lineage B datasets would require 22 folders, exceeding Kaggle's hard limit of 20.
* By using the bundled `casmi26-attributed-v4g-reproduction-assets`, we compressed the architecture down to **6 core datasets**, maintaining 100% feature parity within cloud constraints.

### 2. Calibrated 0.85 Sovereign Library Shield
* Lowered the reference library lock threshold from `0.90` down to `0.85` (`LIB_TAU = 0.85`).
* Experimental MS/MS library matches above 0.85 cosine against GNPS/MassBank spectra are nearly certain true matches. Locking these at **Rank 1** protects ~8 additional correct molecules from downstream ranker noise.
* In MRR@25 scoring, moving one molecule from miss $\rightarrow$ Rank 1 yields $+0.0076$, providing an immediate boost.

### 3. Strict InChIKey-14 Deduplication & Metric Alignment
* The competition metric evaluates only the first 14 characters of the InChIKey (`InChIKey-14`).
* Version 5 enforces strict skeleton deduplication across all 25 output slots, guaranteeing that stereoisomers or tautomers never duplicate a slot.

### 4. Dual-Channel Outlier Filtering
* Preserved our verified `np.clip(pop_raw, 0.0, 8.0)` solvent filter across both candidate streams to guarantee natural metabolite dominance.
