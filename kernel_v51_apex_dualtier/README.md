# CASMI26 v51 apex dualtier

- Kaggle kernel: `sanjay0614/casmi26-v51-apex-dualtier` (private, GPU, no internet)
- Source notebook: `0-500-casmi26-dual-neural-physical-isomer.ipynb` (public, Apache-2.0)
- Built by: `tools_build_apex.py` (2026-11-12)

Independent dual-tier overlay; diversifies the implementation risk of v50.

## What changed against the source

No code edits. The notebook is copied verbatim; only the first markdown cell is replaced with this account's provenance note.

## Contract

- Inputs: the competition data plus the attached public datasets listed in `kernel-metadata.json` (candidate structures, PubChem popularity, natural-product knowledge table, external spectral libraries, the public spectrum-model kit).
- No hidden labels are read; the validation-prediction file from the public kit is used only as the pipeline does.
- Output: `submission.csv` with one semicolon-separated ranked SMILES list per `molecule_id`, at most 25 entries, deduplicated on the scorer's InChIKey-14 key.
