# Version 15 — CASMI26 V15 Neural RRF Offset 1

Alex Chilton's public 0.467 experiment changed the neural RRF offset from 3 to 1 at weight 0.25.

This notebook starts from the scored V7 candidate-aware pipeline and reranks only its existing top-25 candidates with the pinned spectrum-candidate model. Fusion settings: top weight 0.25, middle weight 0.25, RRF offset 1.0; leader preservation: False. Candidate generation and candidate membership remain unchanged.

The public score is a hypothesis from another notebook, not a result for this adapted pipeline. The model dataset metadata reports an unknown license; the attached attributed reproduction-assets dataset is CC-BY-NC-SA-4.0. Record this run as score exploration, and resolve asset compatibility before treating it as prize-eligible. The Kaggle run logs the processed row count and rerank changes.
