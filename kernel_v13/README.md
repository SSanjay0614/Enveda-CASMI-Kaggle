# Version 13 — CASMI26 V13 Evidence Early Slots

V7 promotion gate (S > 6 and popularity >= 5), with earlier interleaving slots when candidate-specific S > 5.

This is a one-policy-change branch from the scored V7 pipeline. Candidate generation, ranker weights, simulator behavior, library shield, final fusion, and output format remain unchanged. It uses the candidate-specific PubChem evidence already computed by V7 for both the promotion rule and the early-slot decision.

The public identity-disjoint natural-product panel replay measured this policy on a 250-molecule panel. On the 250-molecule answer-removed-from-reference panel, the matching published early-slot replay gained +0.1994 MRR@25 (paired 95% bootstrap CI +0.1649 to +0.2341); reference-library delta was 0.0000 and no-reference-spectrum delta was -0.0020 (CI -0.0060 to 0.0000). This curated natural-product panel is not a representative hidden-test sample or a full V7 rerun. Treat these results as motivation, not a leaderboard-score prediction. The notebook must complete a GPU smoke run, then a full competition submission is appropriate only if resource budget allows.
