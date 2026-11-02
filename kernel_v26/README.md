# CASMI26 V26 Consensus Wmid070

- **Competition:** Enveda CASMI 2026 (`enveda-CASMI26-molecule-id-mass-spectra`)
- **Parent:** V21 (`0.477`, submission `57829820`)
- **Change:** reduce the neural middle-rank contribution from `w_mid=0.75` to `0.70`, retaining the fragment-gated rank-1 rule and disabling tail rescue.
- **Rationale:** V21 is the strongest confirmed candidate; V22-V25 scored 0.465. This tests one conservative ranking change without altering candidate generation or rank-1 protection.
- **Validation:** no identity-disjoint paired MRR@25 is available for this setting. The Kaggle fast-commit path is packaging-only; the scoring rerun provides the leaderboard evaluation.
- **Kaggle submission:** `57874984`, pending.

Build from the project root with `python .\enveda_casmi\build_v26.py`, then push this folder to Kaggle.
