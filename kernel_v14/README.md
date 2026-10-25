# Version 14 — CASMI26 V14 Stronger PubChem Rescue

Promotion gate (S > 5.5 and popularity >= 8), with earlier interleaving slots when candidate-specific S > 5.

This is a one-policy-change branch from the scored V7 pipeline. Candidate generation, ranker weights, simulator behavior, library shield, final fusion, and output format remain unchanged. It uses the candidate-specific PubChem evidence already computed by V7 for both the promotion rule and the early-slot decision.

The public identity-disjoint natural-product panel replay measured this policy on a 250-molecule panel. On the 250-molecule answer-removed-from-reference panel, the matching published replay gained +0.2432 MRR@25 (paired 95% bootstrap CI +0.2023 to +0.2839); reference-library and no-reference-spectrum deltas were each -0.0040 (paired 95% bootstrap CI -0.0100 to 0.0000). This curated natural-product panel is not a representative hidden-test sample or a full V7 rerun. Treat these results as motivation, not a leaderboard-score prediction. The notebook must complete a GPU smoke run, then a full competition submission is appropriate only if resource budget allows.
