# CASMI26 V25 Consensus Rescue 1

- **Competition:** Enveda CASMI 2026 (`enveda-CASMI26-molecule-id-mass-spectra`)
- **Hypothesis:** Conservative single-slot tail rescue `rescue=1` with `w_mid=0.75`. Keeps ranks 1-24 strictly identical to the 0.477 baseline, while granting rank 25 to the highest-scoring neural outsider to boost recall on borderline molecules.
- **Weights:** `CUSTOM = dict(w_top=0.25, w_mid=0.75, rescue=1)`
- **GPU Protection:** Fast commit completed in <20s (0.00h GPU consumed).
- **Kaggle result:** submission `57832621` scored **0.465**.
