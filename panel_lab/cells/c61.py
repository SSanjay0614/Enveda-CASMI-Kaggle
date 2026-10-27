# V12 reranks the finalized candidate lists only; it never changes candidate membership.
import gc as _gc
import hashlib as _hashlib
import importlib as _importlib
import json as _json
import sys as _sys
from pathlib import Path as _Path

import numpy as _np
import pandas as _pd

_V12_WEIGHT = 1.0  # retained for report compatibility
_V12_TOP_WEIGHT = 0.25
_V12_MIDDLE_WEIGHT = 1.0
_V12_OFFSET = 3.0
_V12_CHECKPOINT_SHA256 = "44436b2daec64373e66f9120dd2389c24fc83dd9430ebeeac18e3cb49dcb9642"
_V12_BUNDLE_CANDIDATES = [
    path.parent for path in _Path("/kaggle/input").rglob("final_model.pt")
    if (path.parent / "config.json").is_file()
    and (path.parent / "features.py").is_file()
    and (path.parent / "model.py").is_file()
    and (path.parent / "sha256.json").is_file()
]
_V12_MATCHING_BUNDLES = []
for _candidate_bundle in _V12_BUNDLE_CANDIDATES:
    _pins = _json.loads((_candidate_bundle / "sha256.json").read_text())
    if _pins.get("final_model.pt") == _V12_CHECKPOINT_SHA256:
        _V12_MATCHING_BUNDLES.append(_candidate_bundle)
assert len(_V12_MATCHING_BUNDLES) == 1, (
    f"Expected one pinned V12 model bundle; found {len(_V12_MATCHING_BUNDLES)}"
)
_V12_BUNDLE = _V12_MATCHING_BUNDLES[0]
_V12_MODEL_SHA = _hashlib.sha256(
    (_V12_BUNDLE / "final_model.pt").read_bytes()
).hexdigest()
assert _V12_MODEL_SHA == _V12_CHECKPOINT_SHA256

import torch as _torch
assert _torch.cuda.is_available(), "V12 requires the configured Kaggle GPU"
_gc.collect()
_torch.cuda.empty_cache()

# Load the dataset's documented Scorer API in an isolated import namespace.
_module_names = ("features", "model", "inference")
_old_modules = {name: _sys.modules.pop(name, None) for name in _module_names}
_bundle_string = str(_V12_BUNDLE)
_sys.path.insert(0, _bundle_string)
try:
    _inference = _importlib.import_module("inference")
    _V12Scorer = _inference.Scorer
finally:
    _sys.path.remove(_bundle_string)
    for _name, _module in _old_modules.items():
        _sys.modules.pop(_name, None)
        if _module is not None:
            _sys.modules[_name] = _module

_scorer = _V12Scorer(
    _V12_BUNDLE,
    checkpoint="final_model.pt",
    device="cuda",
)
_queries_by_molecule = {
    str(_mid): _group
    for _mid, _group in te.groupby("molecule_id", sort=False)
}
_v12_control = _pd.read_csv("submission.csv", dtype=str, keep_default_na=False)
_v12_control.to_csv("submission_v12_control.csv", index=False)
_v12_sample = _pd.read_csv(
    os.path.join(COMP, "sample_submission.csv"),
    dtype=str,
    keep_default_na=False,
)
assert _v12_control.columns.tolist() == ["molecule_id", "smiles"]
assert _v12_control["molecule_id"].tolist() == _v12_sample["molecule_id"].tolist()


def _v12_rrf_order(_neural_scores):
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


_v12_probe = _v12_rrf_order(_np.arange(25, dtype=_np.float64))
assert _v12_probe[0] == 0 and sorted(_v12_probe.tolist()) == list(range(25))
assert not _np.array_equal(_v12_probe, _np.arange(25))

_v12_rows = []
_v12_audit = []
for _mid, _candidate_text in _v12_control.itertuples(index=False, name=None):
    _candidates = _candidate_text.split(";") if _candidate_text else []
    assert 1 <= len(_candidates) <= 25 and len(set(_candidates)) == len(_candidates), _mid
    _query_rows = _queries_by_molecule.get(str(_mid))
    if _query_rows is None:
        _v12_rows.append((_mid, _candidate_text))
        _v12_audit.append({
            "molecule_id": _mid,
            "processed": False,
            "changed": False,
            "changed_top1": False,
            "candidate_count": len(_candidates),
            "finite_neural_scores": 0,
        })
        continue

    _spectra = [
        {
            "mzs": _row.ms2_mzs,
            "intensities": _row.ms2_normalized_intensities,
            "precursor_mz": _row.precursor_mz,
            "adduct": _row.adduct,
            "ionization_mode": _row.ionization_mode,
            "collision_energy": _row.collision_energy_ev,
        }
        for _row in _query_rows.itertuples(index=False)
    ]
    _neural_scores = _np.asarray(
        _scorer.score_candidates(_spectra, _candidates),
        dtype=_np.float64,
    )
    assert _neural_scores.shape == (len(_candidates),), _mid
    assert not _np.isnan(_neural_scores).any() and not _np.isposinf(_neural_scores).any(), _mid
    assert _np.isfinite(_neural_scores).any(), f"No valid neural candidate scores for {_mid}"

    _order = _v12_rrf_order(_neural_scores)
    _reranked = [_candidates[int(_index)] for _index in _order]
    assert len(_reranked) == len(_candidates) and set(_reranked) == set(_candidates), _mid
    _v12_rows.append((_mid, ";".join(_reranked)))
    _v12_audit.append({
        "molecule_id": _mid,
        "processed": True,
        "changed": _reranked != _candidates,
        "changed_top1": _reranked[0] != _candidates[0],
        "candidate_count": len(_candidates),
        "finite_neural_scores": int(_np.isfinite(_neural_scores).sum()),
    })

_v12_result = _pd.DataFrame(_v12_rows, columns=["molecule_id", "smiles"])
assert _v12_result["molecule_id"].tolist() == _v12_sample["molecule_id"].tolist()
_v12_result.to_csv("submission.csv", index=False)
_pd.DataFrame(_v12_audit).to_csv("neural_rerank_audit.csv", index=False)
_changed = sum(row["changed"] for row in _v12_audit)
_changed_top1 = sum(row["changed_top1"] for row in _v12_audit)
_report = {
    "version": "V18",
    "method": "candidate-preserving leader-safe reciprocal-rank fusion after the complete V7 ranking",
    "baseline": "V7 candidate-aware promotion",
    "neural_weight": 1.0,
    "top_weight": 0.25,
    "rrf_offset": 3.0,
    "leader_protected": True,
    "checkpoint": "final_model.pt",
    "checkpoint_sha256": _V12_MODEL_SHA,
    "candidate_set_preserved": True,
    "rows": len(_v12_result),
    "processed_molecules": sum(row["processed"] for row in _v12_audit),
    "changed_molecules": _changed,
    "changed_top1": _changed_top1,
    "weight_validation": "none; fixed experiment; The public 0.468 notebook's high-variance V4 setting tests neural weight 1.00 below the preserved leader.",
    "accuracy_validation": False,
}
_Path("neural_rerank_report.json").write_text(_json.dumps(_report, indent=2))
print("V12_NEURAL_RERANK", _json.dumps(_report, sort_keys=True), flush=True)
del _scorer
_gc.collect()
_torch.cuda.empty_cache()
