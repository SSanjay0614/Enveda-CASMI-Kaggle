# CASMI26 v53 apex pocket

- Kaggle kernel: `sanjay0614/casmi26-v53-apex-pocket` (private, GPU, no internet)
- Source notebook: `casmi26-peaks-to-structures-v2.ipynb` (public, Apache-2.0)
- Built by: `tools_build_apex.py` (2026-11-12)

Attribution hedge: new overlay with the exact v37 v8/prior constants that scored 0.487.

## What changed against the source

Configuration-only edits, each applied by exact match and asserted:

- `LIB_HIT_GATE = 0.75` -> `LIB_HIT_GATE = 0.78`
- `NP_PROMO_MARGIN = 0.048` -> `NP_PROMO_MARGIN = 0.040`
- `V8 = 'BOTH'` -> `V8 = 'MASS'`
- `MASS_CENTER, MASS_FREE, MASS_FULL, MASS_W = -1.5, 2.8, 8.0, 0.15` -> `MASS_CENTER, MASS_FREE, MASS_FULL, MASS_W = -1.5, 3.0, 8.0, 0.15`
- `MASS_LEAD_OFF, MASS_LIB_TAU = 4.5, 0.9` -> `MASS_LEAD_OFF, MASS_LIB_TAU = 5.0, 0.9`
- `RR8_ALPHA = 0.25` -> `RR8_ALPHA = 1.0`

## Contract

- Inputs: the competition data plus the attached public datasets listed in `kernel-metadata.json` (candidate structures, PubChem popularity, natural-product knowledge table, external spectral libraries, the public spectrum-model kit).
- No hidden labels are read; the validation-prediction file from the public kit is used only as the pipeline does.
- Output: `submission.csv` with one semicolon-separated ranked SMILES list per `molecule_id`, at most 25 entries, deduplicated on the scorer's InChIKey-14 key.
