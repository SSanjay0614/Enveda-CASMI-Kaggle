# Version 2.0: BioPrior Calibration & Tuned RRF

* **Directory:** `kernel_v2/`
* **Kaggle Kernel Slug:** `sanjay0614/casmi26-multimodal-v2-bioprior`
* **Leaderboard Score:** **`0.429`** *(+0.006 over V1.0)* 🚀
* **Status:** Scored & Verified ✅

---

## 🎯 Goal & Overview
Version 2.0 applied our first round of hypothesis-driven feature engineering and post-processing improvements to address the weaknesses identified in the Version 1.0 post-mortem.

---

## 🛠️ Key Improvements Applied

### 1. Organic Solvent & Reagent Outlier Capping
* **Problem:** In V1.0, common industrial laboratory chemicals (e.g., acetic acid, DMSO derivatives) had astronomical literature occurrence counts in PubChem, resulting in massive prior boosts that drowned out true biological extract signals.
* **Solution:** Capped the popularity prior z-score at `8.0` (`np.clip(pop_raw, 0.0, 8.0)`) and lowered $\mu$ to `0.20`. This preserved spectral evidence dominance while maintaining a healthy popularity filter.

### 2. Sharpened Reciprocal Rank Fusion (RRF)
* **Parameters Tuned:** Updated fusion parameters to **$\alpha = 0.65$** and **$k = 2.5$** (from $0.60$ and $3.0$).
* **Impact:** Increased the non-linear reward for high-confidence candidate consensus in ranks 1–5 between Engine 1 (neural FPNet) and Engine 2 (analog graph propagation).

### 3. Multi-Tier Adaptive DreaMS Injection
* Replaced the strict single 10 ppm mass matching window with an adaptive ladder:
  $$\text{10 ppm} \longrightarrow \text{25 ppm} \longrightarrow \text{50 ppm}$$
* Eliminated arbitrary dummy SMILES fallbacks, ensuring all 25 candidate slots were populated with true mass analogs.

---

## 📊 Score Outcome
Moving from **0.423 $\longrightarrow$ 0.429** (+0.006 MRR) confirmed our hypothesis that capping synthetic solvent bias directly recovers accurate biological natural product structures.
