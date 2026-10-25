# Version 9 (V9) — Apex Supreme Consensus SOTA

## 1. Overview & Innovations
Version 9 introduces three breakthrough refinements identified from the community's latest frontier:
1. **Doubled LOTUS Literature Prior (`LOTUS_W = 1.0`):**
   - Natural product candidates with verified botanical citations in the LOTUS database receive double the weight in score aggregation.
2. **Adaptive Evidence Promotion Thresholds:**
   - In addition to standard outlier gates, introduces:
     ```python
     if (S > 5.0 and pop_top >= 4.0) or (rel > 150.0) or (rel > 125.0 and pop_top >= 3.0):
     ```
     This captures high-confidence, well-documented structures that previously fell just below the rigid 150 margin threshold.
3. **Explicit Library Match Shield (`BASE` Shield $\tau = 0.90$):**
   - Prevents experimental re-rankings or simulated fallbacks from displacing confident experimental library matches ($\ge 0.90$).

## 2. Kaggle Configuration
- **Kernel ID:** `sanjay0614/casmi26-v9-apex-supreme-consensus`
- **Accelerator:** GPU (NVIDIA T4)
- **Internet:** Off
- **Competition:** `enveda-CASMI26-molecule-id-mass-spectra`
