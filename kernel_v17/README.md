# Version 17 — CASMI26 V17 Leader Safe Mid 035

A lower-variance middle-list interpolation tests whether the public 0.50 weight is too strong for our V7 baseline.

This notebook starts from the scored V7 candidate-aware pipeline and reranks only its existing top-25 candidates with the pinned spectrum-candidate model. Fusion settings: top weight 0.25, middle weight 0.35, RRF offset 3.0; leader preservation: True. Candidate generation and candidate membership remain unchanged.

The public score is a hypothesis from another notebook, not a result for this adapted pipeline. The model dataset metadata reports an unknown license; the attached attributed reproduction-assets dataset is CC-BY-NC-SA-4.0. Record this run as score exploration, and resolve asset compatibility before treating it as prize-eligible. The Kaggle run logs the processed row count and rerank changes.
