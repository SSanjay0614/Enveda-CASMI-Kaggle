# Version 1.0: Multimodal Top Baseline

* **Directory:** `kernel/`
* **Kaggle Kernel Slug:** `sanjay0614/casmi26-multimodal-top-baseline`
* **Leaderboard Score:** **`0.423`**
* **Status:** Scored & Verified ✅

---

## 🎯 Goal & Overview
Version 1.0 established our baseline environment and validated the complete cloud submission workflow:
1. Automated setup of Kaggle API credentials on the local workstation.
2. Direct CLI deployment of private GPU notebooks to Kaggle Cloud (`kaggle kernels push`).
3. Verification of candidate retrieval, deep neural fingerprint prediction (FPNet), and 4-seed LightGBM rankers.
4. Autonomous generation and submission of `submission.csv` to the official competition leaderboard.

---

## 🔬 Architecture Details
* **Candidate Retrieval:** 10 ppm neutral mass precursor cluster snapping from COCONUT natural products, ChEBI, and LIPID MAPS.
* **Engine 1:** Neural spectral fingerprint projection (FPNet) + 4-booster LightGBM ranking.
* **Engine 2:** Analog graph propagation over chemical similarity neighborhoods.
* **Fusion:** Reciprocal Rank Fusion ($\alpha = 0.60, k = 3.0$).

---

## 🔍 Post-Mortem Analysis: Why It Scored 0.423
* **Clickbait Title:** The original notebook was titled `"LB TOP 1 ⭐🏅??"` by its author, but internally corresponded to the early v42 baseline that mathematically evaluates to `0.423`.
* **Forward Simulators Disabled:** Inside Cell 15 and 19, `BASE_ICE = False` and `CELL19_ICE = False`, disabling the `ICEBERG` fragmentation simulator.
* **Solvent Outliers:** The raw PubChem popularity prior (`POOL_POP`) had no cap, allowing common industrial solvents with huge PubMed counts to unfairly override true natural product candidates.
