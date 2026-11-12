"""Build today's CASMI26 kernels on the 0.500-class public apex overrides.

Context: the account's best board number is 0.487 (v37: the 0.487 public pipeline
plus the popwenman v80 scorer in a 0.5/0.5 neural z-score ensemble). Yesterday's
five scorer swaps (v38-v42) all lost, 0.465-0.476, so the remaining headroom is not
in the scorer. Three independent public forks published on 2026-11-11 claim 0.500+
by changing what happens *after* the ranking: an external-library rank-1 promotion
overlay (Takumu Hata CC0 extlib + MassBank harmonized), plus an evidence-based
natural-product promotion and a calibrated timsTOF mass rule.

These candidates port those overlays onto our 0.487 core. The overlay code is
copied verbatim from the public notebooks (Apache-2.0, attribution preserved in
each notebook's own markdown); the only edits are configuration constants, applied
by exact match and asserted, so every delta is attributable to a named knob.

Run from the enveda_casmi folder:  python tools_build_apex.py
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V37 = HERE / "kernel_v37"
PUB = HERE / "public_new4"

PIPELINE = PUB / "casmi26-peaks-to-structures-v2.ipynb"
DUALTIER = PUB / "0-500-casmi26-dual-neural-physical-isomer.ipynb"
IONWRAITH = PUB / "ionwraith-v11-evidence-guided-molecule-id.ipynb"

with (V37 / "kernel-metadata.json").open(encoding="utf-8") as fh:
    BASE_META = json.load(fh)

DATASETS = list(BASE_META["dataset_sources"])
DOCKER = BASE_META["docker_image"]
V80_SOURCE = "popwenman/casmi26-scorer-train-v80"

ATTRIBUTION = (
    "\n\n---\n\n"
    "Lineage: the pipeline and every overlay below are public Kaggle notebook code "
    "(Apache-2.0), authored by dmitriigluzdov, sanpier, romanrozen, romantamrazov, "
    "busyaprime, alexchilton, takumuhata, zz3t3rn41, Ertugrul Ozer, Adaptive Agent "
    "Systems, popwenman and others. The code cells are copied unchanged apart from "
    "the named configuration constants documented in this kernel's README.\n"
)


def source_lines(text: str) -> list[str]:
    lines = text.splitlines()
    return [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines else [])


def patch(text: str, old: str, new: str, tag: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"{tag}: expected exactly one match, got {text.count(old)}")
    return text.replace(old, new)


V37_CONFIG = [
    ("LIB_HIT_GATE = 0.75", "LIB_HIT_GATE = 0.78"),
    ("NP_PROMO_MARGIN = 0.048", "NP_PROMO_MARGIN = 0.040"),
    (
        "V8 = 'BOTH'                   # 'MASS': timsTOF mass prior ON, destructive RR8 isomer reranker OFF                   # 'MASS' | 'RR' | 'BOTH' | 'BASE' (the Version 22 rule exactly)",
        "V8 = 'MASS'",
    ),
    ("MASS_CENTER, MASS_FREE, MASS_FULL, MASS_W = -1.5, 2.8, 8.0, 0.15",
     "MASS_CENTER, MASS_FREE, MASS_FULL, MASS_W = -1.5, 3.0, 8.0, 0.15"),
    ("MASS_LEAD_OFF, MASS_LIB_TAU = 4.5, 0.9",
     "MASS_LEAD_OFF, MASS_LIB_TAU = 5.0, 0.9"),
    ("RR8_ALPHA = 0.25", "RR8_ALPHA = 1.0"),
]

CANDIDATES = [
    {
        "folder": "kernel_v50_apex_adduct",
        "slug": "casmi26-v50-apex-adduct",
        "title": "CASMI26 v50 apex adduct",
        "source": PIPELINE,
        "patches": [],
        "kernel_sources": [V80_SOURCE],
        "header": (
            "# v50 - 0.500-class adduct-aware library overlay on our 0.487 core\n\n"
            "Copies the 2026-11-11 public `casmi26-peaks-to-structures-v2` recipe verbatim, "
            "including its adduct-aware calibrated external-library rank-1 promotion, the "
            "multi-rank MSI Level-1 natural-product promotion, the evidence-based NP rule, "
            "and the `V8='BOTH'` mass prior plus isomer reranker at alpha 0.25. Our v80 "
            "scorer is attached, so the neural channel runs the same 0.5*public + 0.5*v80 "
            "z-score ensemble that produced the account's 0.487 board score.\n\n"
            "Run mode is the pipeline's own `COMMIT_MODE='fast'`: the visible run checks the "
            "stage wiring and writes a placeholder, and the hidden scoring rerun executes the "
            "full pipeline."
        ),
        "notes": "Highest-EV candidate: the most documented 0.500-class public recipe, with our 0.487 neural ensemble.",
    },
    {
        "folder": "kernel_v51_apex_dualtier",
        "slug": "casmi26-v51-apex-dualtier",
        "title": "CASMI26 v51 apex dualtier",
        "source": DUALTIER,
        "patches": [],
        "kernel_sources": [V80_SOURCE],
        "header": (
            "# v51 - dual-tier external-library promotion on our 0.487 core\n\n"
            "Implements the overlay as rank-1 *and* rank-2 promotion tiers, with the same "
            "adduct-aware neutral-mass alignment and exact-mass sanity gate as v50, but a "
            "different promotion cascade and `RR8_ALPHA = 0.20`. Independent implementation "
            "of the same idea from a different author, so it is a genuine second opinion "
            "rather than a threshold probe.\n\n"
            "Our v80 scorer is attached and used by the pipeline's own `_swap_to_ours` "
            "ensemble path."
        ),
        "notes": "Independent dual-tier overlay; diversifies the implementation risk of v50.",
    },
    {
        "folder": "kernel_v52_apex_ionwraith",
        "slug": "casmi26-v52-apex-ionwraith",
        "title": "CASMI26 v52 apex ionwraith",
        "source": IONWRAITH,
        "patches": [],
        "kernel_sources": [V80_SOURCE],
        "header": (
            "# v52 - evidence-guided overlay with the dual-band promotion rule\n\n"
            "Third independent implementation of the 0.500-class overlay: dual-band external "
            "spectral matching with `V8='MASS'` (mass prior on, destructive isomer reranker "
            "off) and the evidence-guided promotion layer. Kept because it deliberately does "
            "*not* run the aggressive RR8 reranker, which is the one component our own screen "
            "could not validate on the board.\n\n"
            "Our v80 scorer is attached and used by the pipeline's own `_swap_to_ours` "
            "ensemble path."
        ),
        "notes": "Third overlay implementation, with the conservative mass-only v8 setting.",
    },
    {
        "folder": "kernel_v53_apex_pocket",
        "slug": "casmi26-v53-apex-pocket",
        "title": "CASMI26 v53 apex pocket",
        "source": PIPELINE,
        "patches": V37_CONFIG,
        "kernel_sources": [V80_SOURCE],
        "header": (
            "# v53 - new overlay, our old v8 and prior settings\n\n"
            "A hedge on attribution. v50 changes two things at once against our scored 0.487 "
            "core: the adduct-aware overlay and the v8/prior constants (`V8` BOTH, alpha 0.25, "
            "mass offset 4.5 ppm, `LIB_HIT_GATE` 0.75, `NP_PROMO_MARGIN` 0.048). This candidate "
            "keeps the new overlay but reverts every one of those constants to the values our "
            "0.487 run actually used, so it is the overlay's own contribution with nothing else "
            "moving.\n\n"
            "If v53 beats v50, the new v8 settings are the problem and the overlay is the gain. "
            "If v50 beats v53, the constants carry part of the improvement."
        ),
        "notes": "Attribution hedge: new overlay with the exact v37 v8/prior constants that scored 0.487.",
    },
    {
        "folder": "kernel_v54_apex_recall",
        "slug": "casmi26-v54-apex-recall",
        "title": "CASMI26 v54 apex recall",
        "source": PIPELINE,
        "patches": [
            (
                "EXTLIB_TAU = 0.80             # Calibrated cross-instrument cosine threshold (high recall with strict K=4)",
                "EXTLIB_TAU = 0.75             # loosened from 0.80: more rank-1 promotions, same strict K=4",
            ),
        ],
        "kernel_sources": [V80_SOURCE],
        "header": (
            "# v54 - the same overlay with a wider library-recall threshold\n\n"
            "One constant against v50: `EXTLIB_TAU` 0.80 -> 0.75. The overlay's precision is "
            "already protected three ways - strict adduct compatibility, a 12 ppm neutral-mass "
            "window, and a 15 ppm exact-mass sanity gate on the matched structure - so lowering "
            "the cosine threshold mostly adds correct matches the reference library just missed. "
            "If the promotion rule is recall-limited this moves up; if it is precision-limited "
            "this moves down, and the pair brackets the threshold."
        ),
        "notes": "One-constant probe against v50: library cosine threshold 0.80 -> 0.75.",
    },
]


def build(candidate: dict) -> None:
    notebook = json.loads(Path(candidate["source"]).read_text(encoding="utf-8"))
    code_cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]

    if candidate["patches"]:
        text = "".join(code_cells[0]["source"])
        for old, new in candidate["patches"]:
            text = patch(text, old, new, candidate["slug"])
        code_cells[0]["source"] = source_lines(text)

    notebook["cells"][0] = {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_lines(candidate["header"] + ATTRIBUTION),
    }

    for cell in code_cells:
        ast.parse("".join(cell["source"]))
        cell["execution_count"] = None
        cell["outputs"] = []

    out_dir = HERE / candidate["folder"]
    out_dir.mkdir(parents=True, exist_ok=True)
    code_file = f"{candidate['slug'].replace('-', '_')}.ipynb"
    (out_dir / code_file).write_text(json.dumps(notebook, ensure_ascii=False), encoding="utf-8")

    metadata = {
        "id": f"sanjay0614/{candidate['slug']}",
        "title": candidate["title"],
        "code_file": code_file,
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": True,
        "enable_tpu": False,
        "enable_internet": False,
        "keywords": ["gpu", "chemistry"],
        "dataset_sources": DATASETS,
        "kernel_sources": candidate["kernel_sources"],
        "competition_sources": ["enveda-CASMI26-molecule-id-mass-spectra"],
        "model_sources": [],
        "docker_image": DOCKER,
        "machine_shape": "NvidiaTeslaT4",
    }
    (out_dir / "kernel-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    (out_dir / "README.md").write_text(
        f"# {candidate['title']}\n\n"
        f"- Kaggle kernel: `sanjay0614/{candidate['slug']}` (private, GPU, no internet)\n"
        f"- Source notebook: `{Path(candidate['source']).name}` (public, Apache-2.0)\n"
        f"- Built by: `tools_build_apex.py` (2026-11-12)\n\n"
        f"{candidate['notes']}\n\n"
        "## What changed against the source\n\n"
        + (
            "No code edits. The notebook is copied verbatim; only the first markdown cell is "
            "replaced with this account's provenance note.\n"
            if not candidate["patches"]
            else "Configuration-only edits, each applied by exact match and asserted:\n\n"
            + "\n".join(f"- `{old.split('#')[0].strip()}` -> `{new.split('#')[0].strip()}`" for old, new in candidate["patches"])
            + "\n"
        )
        + "\n## Contract\n\n"
        "- Inputs: the competition data plus the attached public datasets listed in "
        "`kernel-metadata.json` (candidate structures, PubChem popularity, natural-product "
        "knowledge table, external spectral libraries, the public spectrum-model kit).\n"
        "- No hidden labels are read; the validation-prediction file from the public kit is "
        "used only as the pipeline does.\n"
        "- Output: `submission.csv` with one semicolon-separated ranked SMILES list per "
        "`molecule_id`, at most 25 entries, deduplicated on the scorer's InChIKey-14 key.\n",
        encoding="utf-8",
    )
    print(f"built {candidate['folder']} -> {candidate['slug']}")


if __name__ == "__main__":
    for item in CANDIDATES:
        build(item)
