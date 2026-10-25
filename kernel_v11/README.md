# Version 11 — Candidate-Specific Promotion Gate

V11 is based on V10 and changes the PubChem rank-1 promotion decision only:

- Compute `S`, popularity, and relative evidence from the current PubChem leader's `promotion_evidence` entry.
- Use the candidate's own `raw_fz - best_pool_fz` for both relative-evidence promotion thresholds.
- Treat absent, nonfinite, incomplete, or identity-mismatched evidence as ineligible for promotion; retain the normal merge and count the case in the audit rather than aborting the notebook.
- Require a finite candidate score and finite `best_pool_fz`; missing baselines cannot create an artificial large margin.
- Include regression checks proving that a high channel-level margin alone cannot promote a weak candidate, valid candidate-specific evidence can promote, and missing/invalid evidence fails closed.

V10's other settings, including the relaxed `5.0 / 4.0` evidence/popularity gates, the `125 / 150` candidate-relative margin gates, the LOTUS weight, and library shield, are retained to isolate the broken gate behavior in V10.

The first V11 competition submission (`57619741`) errored during hidden-test rerun. The public smoke path processed only 12 molecules and did not exercise the unshielded PubChem promotion branch. Inspection found the new gate asserted when the full hidden-test path lacked `promotion_evidence`, aborting the notebook instead of simply blocking promotion. The rebuilt notebook fixes this fail-closed behavior and adds an `evidence_unavailable` count. It is configured for Kaggle GPU inference with internet disabled. The fix must complete a Kaggle run and a full competition submission before a score or improvement is claimed.
