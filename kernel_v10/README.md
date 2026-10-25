# Version 10 (V10) — Unified Frontier Master

V10 submitted as competition submission `57590094` and scored **0.464**, below the best local score of 0.465 from V7/V8.

V10 computes candidate-specific PubChem evidence but does not consistently use it to decide rank-1 promotion. The condition in the promotion loop still contains `rel > 150` and `rel > 125`, where `rel` is computed from the mass-window/channel-level leader fields (`fz_top` and `best_pool_fz`). Those branches can therefore promote a candidate using evidence that belongs to the retrieval window rather than the current PubChem leader. The helper also silently falls back to channel-level evidence when the candidate evidence is missing.

V11 fixes those two connected defects: every promotion branch uses the current candidate's own `S`, popularity, and `raw_fz - best_pool_fz`; missing or inconsistent candidate evidence now raises an error instead of silently falling back. V11 retains the V10 thresholds and other settings so the change directly tests this gate correction.

The V10 leaderboard score is a full competition submission result. The local notebook outputs in this folder are smoke-run diagnostics and should not be mistaken for held-out validation.
