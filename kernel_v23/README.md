# CASMI26 V23 Consensus Wmid 0.775

- **Competition:** Enveda CASMI 2026 (`enveda-CASMI26-molecule-id-mass-spectra`)
- **Hypothesis:** Finely tunes neural middle weight `w_mid=0.775` (the exact optimal interpolation between 0.75 and 0.80 tested by top competitor Gu Hongbin) on ranks 2-25 while retaining Roman Tamrazov's fragment-gated rank 1 moves from V2 order.
- **Weights:** `CUSTOM = dict(w_top=0.25, w_mid=0.775, rescue=0)`
- **GPU Protection:** Fast commit completed in <20s (0.00h GPU consumed).
- **Kaggle result:** submission `57831786` scored **0.465**.
