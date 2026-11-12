# CASMI26 v54 apex recall

- Kaggle kernel: `sanjay0614/casmi26-v54-apex-recall` (private, GPU, no internet)
- Source notebook: `casmi26-peaks-to-structures-v2.ipynb` (public, Apache-2.0)
- Built by: `tools_build_apex.py` (2026-11-12)

One-constant probe against v50: library cosine threshold 0.80 -> 0.75.

## What changed against the source

Configuration-only edits, each applied by exact match and asserted:

- `EXTLIB_TAU = 0.80` -> `EXTLIB_TAU = 0.75`

## Contract

- Inputs: the competition data plus the attached public datasets listed in `kernel-metadata.json` (candidate structures, PubChem popularity, natural-product knowledge table, external spectral libraries, the public spectrum-model kit).
- No hidden labels are read; the validation-prediction file from the public kit is used only as the pipeline does.
- Output: `submission.csv` with one semicolon-separated ranked SMILES list per `molecule_id`, at most 25 entries, deduplicated on the scorer's InChIKey-14 key.
