# CASMI26 V24 Consensus Wmid 0.85

- **Competition:** Enveda CASMI 2026 (`enveda-CASMI26-molecule-id-mass-spectra`)
- **Hypothesis:** Stronger neural middle weight `w_mid=0.85` on ranks 2-25. Since rank 1 is strictly protected by Roman Tamrazov's fragment-gated moves on V2 order, pushing neural reranking weight on ranks 2-25 improves deep-slot discrimination without leader dilution.
- **Weights:** `CUSTOM = dict(w_top=0.25, w_mid=0.85, rescue=0)`
- **GPU Protection:** Fast commit completed in <20s (0.00h GPU consumed).
- **Kaggle result:** submission `57831900` scored **0.465**.
