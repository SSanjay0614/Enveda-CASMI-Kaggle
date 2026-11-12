# CASMI26 v55 apex tau075

- Kaggle kernel: `sanjay0614/casmi26-v55-apex-tau075` (private, GPU, no internet)
- Source: `public_new4/casmi26-peaks-to-structures-v2.ipynb` (public, Apache-2.0)
- Built by: `tools_build_apex.py` v55 branch (2026-11-12)

One asserted edit: the overlay's local threshold literal `TAU = 0.80 -> 0.75`, plus the cosmetic cell-0 constant kept in sync. Everything else is v50/v53's shared code.

Purpose: bracket the external-library cosine threshold against v50. Precision is protected by adduct compatibility, a 12 ppm neutral-mass window, a 15 ppm exact-mass gate and the 0.90 pipeline-library shield, so this tests whether the promotion is recall-limited.
