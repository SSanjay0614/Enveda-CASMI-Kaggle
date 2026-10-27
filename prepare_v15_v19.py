"""Build five isolated neural rank-fusion variants from the scored V7 pipeline.

All model inference and competition execution happens in Kaggle. This script only
assembles notebook files and metadata locally.
"""

import ast
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
V7_NOTEBOOK = ROOT / "kernel_v7" / "casmi26-v7-candidate-aware-0465.ipynb"
V7_METADATA = ROOT / "kernel_v7" / "kernel-metadata.json"
V12_BUILDER = ROOT / "prepare_v12.py"

VARIANTS = (
    {
        "version": 15,
        "slug": "casmi26-v15-neural-rrf-offset-1",
        "title": "CASMI26 V15 Neural RRF Offset 1",
        "top": 0.25,
        "middle": 0.25,
        "offset": 1.0,
        "protected": False,
        "lead": "Alex Chilton's public 0.467 experiment changed the neural RRF offset from 3 to 1 at weight 0.25.",
    },
    {
        "version": 16,
        "slug": "casmi26-v16-leader-safe-mid-050",
        "title": "CASMI26 V16 Leader Safe Mid 050",
        "top": 0.25,
        "middle": 0.50,
        "offset": 3.0,
        "protected": True,
        "lead": "Roman Rozen's public 0.468 recipe keeps the weight-0.25 leader and uses neural weight 0.50 for ranks 2–25.",
    },
    {
        "version": 17,
        "slug": "casmi26-v17-leader-safe-mid-035",
        "title": "CASMI26 V17 Leader Safe Mid 035",
        "top": 0.25,
        "middle": 0.35,
        "offset": 3.0,
        "protected": True,
        "lead": "A lower-variance middle-list interpolation tests whether the public 0.50 weight is too strong for our V7 baseline.",
    },
    {
        "version": 18,
        "slug": "casmi26-v18-leader-safe-mid-100",
        "title": "CASMI26 V18 Leader Safe Mid 100",
        "top": 0.25,
        "middle": 1.00,
        "offset": 3.0,
        "protected": True,
        "lead": "The public 0.468 notebook's high-variance V4 setting tests neural weight 1.00 below the preserved leader.",
    },
    {
        "version": 19,
        "slug": "casmi26-v19-leader-safe-offset-1",
        "title": "CASMI26 V19 Leader Safe Offset 1",
        "top": 0.25,
        "middle": 0.50,
        "offset": 1.0,
        "protected": True,
        "lead": "This interaction test combines Alex Chilton's offset 1 with the protected leader and middle weight 0.50.",
    },
)

SIMPLE_ORDER = '''def _v12_rrf_order(_neural_scores):
    _neural_order = _np.argsort(-_neural_scores, kind="stable")
    _neural_ranks = _np.empty(len(_neural_scores), dtype=_np.int64)
    _neural_ranks[_neural_order] = _np.arange(1, len(_neural_scores) + 1)
    _baseline_ranks = _np.arange(1, len(_neural_scores) + 1, dtype=_np.float64)
    _rrf = (
        1.0 / (_V12_OFFSET + _baseline_ranks)
        + _V12_WEIGHT / (_V12_OFFSET + _neural_ranks)
    )
    return _np.argsort(-_rrf, kind="stable")
'''

PROTECTED_ORDER = '''def _v12_rrf_order(_neural_scores):
    _neural_order = _np.argsort(-_neural_scores, kind="stable")
    _neural_ranks = _np.empty(len(_neural_scores), dtype=_np.int64)
    _neural_ranks[_neural_order] = _np.arange(1, len(_neural_scores) + 1)
    _baseline_ranks = _np.arange(1, len(_neural_scores) + 1, dtype=_np.float64)
    _top_rrf = (
        1.0 / (_V12_OFFSET + _baseline_ranks)
        + _np.float64(_V12_TOP_WEIGHT) / (_V12_OFFSET + _neural_ranks)
    )
    _leader = int(_np.argmax(_top_rrf))
    _middle_rrf = (
        1.0 / (_V12_OFFSET + _baseline_ranks)
        + _np.float64(_V12_MIDDLE_WEIGHT) / (_V12_OFFSET + _neural_ranks)
    )
    _rest = [int(_i) for _i in _np.argsort(-_middle_rrf, kind="stable") if int(_i) != _leader]
    return _np.asarray([_leader, *_rest], dtype=_np.int64)
'''


def load_v12_template():
    spec = importlib.util.spec_from_file_location("v12_builder", V12_BUILDER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.RERANK_CELL


def build_one(variant, template, metadata_template):
    version = variant["version"]
    folder = ROOT / f"kernel_v{version}"
    folder.mkdir(parents=True, exist_ok=True)

    code = template.replace("_V12_WEIGHT = 0.15", f"_V12_WEIGHT = {variant['top']}")
    code = code.replace("_V12_OFFSET = 3.0", f"_V12_OFFSET = {variant['offset']}")
    if code == template or f"_V12_WEIGHT = {variant['top']}" not in code or f"_V12_OFFSET = {variant['offset']}" not in code:
        raise RuntimeError(f"Failed to set fusion parameters for V{version}")

    if variant["protected"]:
        code = code.replace(
            "_V12_WEIGHT = " + str(variant["top"]),
            f"_V12_WEIGHT = {variant['middle']}  # retained for report compatibility\n_V12_TOP_WEIGHT = {variant['top']}\n_V12_MIDDLE_WEIGHT = {variant['middle']}",
            1,
        )
        if SIMPLE_ORDER not in code:
            raise RuntimeError("Could not locate the V12 RRF ordering function")
        code = code.replace(SIMPLE_ORDER, PROTECTED_ORDER, 1)
    else:
        code = code.replace(SIMPLE_ORDER, SIMPLE_ORDER, 1)

    code = code.replace('"version": "V12"', f'"version": "V{version}"')
    code = code.replace(
        '"method": "candidate-preserving reciprocal-rank fusion after the complete V7 ranking"',
        f'"method": "candidate-preserving {"leader-safe " if variant["protected"] else ""}reciprocal-rank fusion after the complete V7 ranking"',
    )
    code = code.replace('"neural_weight": _V12_WEIGHT,', f'"neural_weight": {variant["middle"]},\n    "top_weight": {variant["top"]},')
    code = code.replace('"rrf_offset": _V12_OFFSET,', f'"rrf_offset": {variant["offset"]},\n    "leader_protected": {variant["protected"]},')
    code = code.replace('"weight_validation": "none; fixed experiment",', f'"weight_validation": "none; fixed experiment; {variant["lead"]}",')
    ast.parse(code)

    note = (
        f"# Version {version} — {variant['title']}\n\n"
        f"{variant['lead']}\n\n"
        "This notebook starts from the scored V7 candidate-aware pipeline and reranks only its existing top-25 candidates with the pinned spectrum-candidate model. "
        f"Fusion settings: top weight {variant['top']}, middle weight {variant['middle']}, RRF offset {variant['offset']}; "
        f"leader preservation: {variant['protected']}. Candidate generation and candidate membership remain unchanged.\n\n"
        "The public score is a hypothesis from another notebook, not a result for this adapted pipeline. The model dataset metadata reports an unknown license; the attached attributed reproduction-assets dataset is CC-BY-NC-SA-4.0. Record this run as score exploration, and resolve asset compatibility before treating it as prize-eligible. The Kaggle run logs the processed row count and rerank changes.\n"
    )

    notebook = json.loads(V7_NOTEBOOK.read_text(encoding="utf-8"))
    notebook["cells"].insert(0, {
        "cell_type": "markdown", "metadata": {}, "source": note.splitlines(keepends=True)
    })
    notebook["cells"].append({
        "cell_type": "markdown", "metadata": {},
        "source": ["\n## Neural candidate rerank\n\n", "This cell runs after the V7 output and preserves the candidate set.\n"],
    })
    notebook["cells"].append({
        "cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
        "source": code.splitlines(keepends=True),
    })

    notebook_path = folder / f"casmi26-v{version}-neural-rerank.ipynb"
    notebook_path.write_text(json.dumps(notebook, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    metadata = json.loads(json.dumps(metadata_template))
    metadata["id"] = f"sanjay0614/{variant['slug']}"
    metadata["title"] = variant["title"]
    metadata["code_file"] = notebook_path.name
    metadata["dataset_sources"] = list(dict.fromkeys(
        metadata["dataset_sources"] + ["sanpier/casmi-spectrum-model-v1"]
    ))
    (folder / "kernel-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (folder / "README.md").write_text(note, encoding="utf-8")
    return notebook_path


def main():
    template = load_v12_template()
    metadata_template = json.loads(V7_METADATA.read_text(encoding="utf-8"))
    for variant in VARIANTS:
        path = build_one(variant, template, metadata_template)
        print(path)


if __name__ == "__main__":
    main()
