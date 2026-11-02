# CASMI26 V22 Consensus Neural Rescue

- **Competition:** Enveda CASMI 2026 (`enveda-CASMI26-molecule-id-mass-spectra`)
- **Hypothesis:** Builds on the 0.477 SOTA dual-consensus merge (Roman Tamrazov fragment gate on V2 + Alex Chilton neural rerank) and activates tail rescue (`rescue=2`) with `w_mid=0.80`. High-scoring neural candidates from the pool outside initial top-25 are rescued into bottom slots (ranks 24-25) to increase ground-truth recall without disturbing high-confidence leaders.
- **Weights:** `CUSTOM = dict(w_top=0.25, w_mid=0.80, rescue=2)`
- **GPU Protection:**
  - `COMMIT_MODE = 'fast'` generates valid submission in <20s (0.00h GPU consumed).
  - Full heavy execution only runs on hidden test set during competition scoring reruns.
- **Kaggle result:** submission `57831425` scored **0.465**.
