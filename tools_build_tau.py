"""Build the last CASMI26 slot: the real library-recall threshold test.

v54 was intended to loosen the overlay's cosine threshold from 0.80 to 0.75, but
`EXTLIB_TAU` in cell 0 is unused by `_apex_extlib_overlay`; the threshold is a
local literal inside the function. This version patches the function body itself
and leaves the (cosmetic) config constant in sync.

Run from the enveda_casmi folder:  python tools_build_apex.py  (candidate v55)
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUB = HERE / "public_new4" / "casmi26-peaks-to-structures-v2.ipynb"
V37 = HERE / "kernel_v37"

with (V37 / "kernel-metadata.json").open(encoding="utf-8") as fh:
    BASE_META = json.load(fh)

HEADER = (
    "# v55 - the overlay's real library-recall threshold\n\n"
    "v50 runs the public `casmi26-peaks-to-structures-v2` recipe exactly, with the external-library "
    "match threshold at 0.80. That notebook exposes an `EXTLIB_TAU` constant in cell 0, but the "
    "overlay function never reads it: the threshold is a local literal. This candidate edits the "
    "function body, `TAU = 0.80 -> 0.75`, and the exposed constant to match, so the change is real.\n\n"
    "Why loosening is the right direction: the promotion is already protected three ways - strict "
    "adduct compatibility, a 12 ppm neutral-mass window, and a 15 ppm exact-mass sanity gate on the "
    "matched structure - and it refuses to touch a query whose pipeline library confidence is "
    "already at or above 0.90. Under those gates, most wrong matches are already excluded, so the "
    "binding limit is recall: queries whose reference spectrum was measured on a different "
    "instrument and lands at 0.75-0.80 cosine. This candidate measures that margin; if it loses, "
    "0.80 is the calibrated optimum.\n\n"
    "Against v50 the only change is the threshold literal, so the two bracket it cleanly."
)

ATTRIBUTION = (
    "\n\n---\n\n"
    "Lineage: pipeline and overlay are public Kaggle notebook code (Apache-2.0), authored by "
    "dmitriigluzdov, sanpier, romanrozen, romantamrazov, busyaprime, alexchilton, takumuhata, "
    "zz3t3rn41 and popwenman. Code copied unchanged apart from the single threshold literal "
    "documented above.\n"
)


def source_lines(text: str) -> list[str]:
    lines = text.splitlines()
    return [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines else [])


def main() -> None:
    notebook = json.loads(PUB.read_text(encoding="utf-8"))
    code = [c for c in notebook["cells"] if c["cell_type"] == "code"]

    body = "".join(code[14]["source"])
    old = "    TAU = 0.80          # Minimum cosine similarity for direct Rank-1 hit"
    new = "    TAU = 0.75          # Minimum cosine similarity for direct Rank-1 hit (loosened from 0.80)"
    assert body.count(old) == 1, body.count(old)
    code[14]["source"] = source_lines(body.replace(old, new))

    cfg = "".join(code[0]["source"])
    old_cfg = "EXTLIB_TAU = 0.80             # Calibrated cross-instrument cosine threshold (high recall with strict K=4)"
    new_cfg = "EXTLIB_TAU = 0.75             # kept in sync with the overlay's local TAU below; the function literal is what runs"
    assert cfg.count(old_cfg) == 1
    code[0]["source"] = source_lines(cfg.replace(old_cfg, new_cfg))

    notebook["cells"][0] = {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_lines(HEADER + ATTRIBUTION),
    }
    for cell in code:
        ast.parse("".join(cell["source"]))
        cell["execution_count"] = None
        cell["outputs"] = []

    out_dir = HERE / "kernel_v55_apex_tau075"
    out_dir.mkdir(parents=True, exist_ok=True)
    code_file = "casmi26_v55_apex_tau075.ipynb"
    (out_dir / code_file).write_text(json.dumps(notebook, ensure_ascii=False), encoding="utf-8")

    meta = dict(
        id="sanjay0614/casmi26-v55-apex-tau075",
        title="CASMI26 v55 apex tau075",
        code_file=code_file,
        language="python",
        kernel_type="notebook",
        is_private=True,
        enable_gpu=True,
        enable_tpu=False,
        enable_internet=False,
        keywords=["gpu", "chemistry"],
        dataset_sources=list(BASE_META["dataset_sources"]),
        kernel_sources=["popwenman/casmi26-scorer-train-v80"],
        competition_sources=["enveda-CASMI26-molecule-id-mass-spectra"],
        model_sources=[],
        docker_image=BASE_META["docker_image"],
        machine_shape="NvidiaTeslaT4",
    )
    (out_dir / "kernel-metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    (out_dir / "README.md").write_text(
        "# CASMI26 v55 apex tau075\n\n"
        "- Kaggle kernel: `sanjay0614/casmi26-v55-apex-tau075` (private, GPU, no internet)\n"
        "- Source: `public_new4/casmi26-peaks-to-structures-v2.ipynb` (public, Apache-2.0)\n"
        "- Built by: `tools_build_apex.py` v55 branch (2026-11-12)\n\n"
        "One asserted edit: the overlay's local threshold literal `TAU = 0.80 -> 0.75`, plus the "
        "cosmetic cell-0 constant kept in sync. Everything else is v50/v53's shared code.\n\n"
        "Purpose: bracket the external-library cosine threshold against v50. Precision is protected "
        "by adduct compatibility, a 12 ppm neutral-mass window, a 15 ppm exact-mass gate and the "
        "0.90 pipeline-library shield, so this tests whether the promotion is recall-limited.\n",
        encoding="utf-8",
    )
    print("built kernel_v55_apex_tau075 -> sanjay0614/casmi26-v55-apex-tau075")


if __name__ == "__main__":
    main()
