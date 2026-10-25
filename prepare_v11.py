import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_NOTEBOOK = ROOT / "kernel_v10" / "casmi26-v10-unified-frontier-master.ipynb"
OUTPUT_DIR = ROOT / "kernel_v11"
OUTPUT_NOTEBOOK = OUTPUT_DIR / "casmi26-v11-candidate-evidence-gate.ipynb"
METADATA_SOURCE = ROOT / "kernel_v10" / "kernel-metadata.json"

OLD_EVIDENCE_HELPER = """def candidate_promotion_evidence(p):
    key = p['pc_keys'][0]
    evidence = p.get('promotion_evidence', {}).get(key)
    if evidence is None:
        return float(p.get('S') or 0.0), float(p.get('top_pop') or 0.0), float(p.get('fz_top') or 0.0)
    S, pop, raw = (float(evidence.get(x, 0.0)) for x in ('S', 'pop', 'raw_fz'))
    return S, pop, raw"""

NEW_EVIDENCE_HELPER = """def candidate_promotion_evidence(p):
    key = p['pc_keys'][0]
    records = p.get('promotion_evidence')
    if not isinstance(records, dict):
        return None
    evidence = records.get(key)
    if not isinstance(evidence, dict) or evidence.get('smiles') != p['pc'][0]:
        return None
    try:
        S, pop, raw = (
            float(evidence[name])
            for name in ('S', 'pop', 'raw_fz')
        )
        best_pool_fz = float(p['best_pool_fz'])
    except (KeyError, TypeError, ValueError):
        return None
    if not all(np.isfinite(value) for value in (S, pop, raw, best_pool_fz)):
        return None
    candidate_rel = raw - best_pool_fz
    return S, pop, candidate_rel


def candidate_promotion_decision(p):
    evidence = candidate_promotion_evidence(p)
    if evidence is None:
        return False, False
    S, pop, candidate_rel = evidence
    promote = (S > 5.0 and pop >= 4.0) or candidate_rel > 150.0 or (
        candidate_rel > 125.0 and pop >= 3.0
    )
    return bool(promote), True


_channel_only_probe = {
    'pc': ['CCO'],
    'pc_keys': ['leader'],
    'promotion_evidence': {
        'leader': {'smiles': 'CCO', 'S': 1.0, 'pop': 1.0, 'raw_fz': 20.0}
    },
    'best_pool_fz': 0.0,
    'fz_top': 1000.0,
}
assert candidate_promotion_decision(_channel_only_probe) == (False, True)
_candidate_margin_probe = {
    **_channel_only_probe,
    'promotion_evidence': {
        'leader': {'smiles': 'CCO', 'S': 1.0, 'pop': 1.0, 'raw_fz': 151.0}
    },
}
assert candidate_promotion_decision(_candidate_margin_probe) == (True, True)
_missing_evidence_probe = {**_channel_only_probe, 'promotion_evidence': {}}
assert candidate_promotion_decision(_missing_evidence_probe) == (False, False)
_invalid_baseline_probe = {**_channel_only_probe, 'best_pool_fz': float('nan')}
assert candidate_promotion_decision(_invalid_baseline_probe) == (False, False)
print('candidate-specific promotion regression checks passed')"""

OLD_PROMOTION = """        cand_S, cand_pop, cand_raw = candidate_promotion_evidence(p)
        if (cand_S > 5.0 and cand_pop >= 4.0) or (rel > 150.0) or (rel > 125.0 and cand_pop >= 3.0):"""

NEW_PROMOTION = """        new_promote, evidence_valid = candidate_promotion_decision(p)
        if not evidence_valid:
            stats['evidence_unavailable'] += 1
        if new_promote:"""
OLD_STATS = "rows, stats = [], dict(untouched=0, gentle=0, aggressive=0, no_pc=0, promoted=0)"
NEW_STATS = "rows, stats = [], dict(untouched=0, gentle=0, aggressive=0, no_pc=0, promoted=0, evidence_unavailable=0)"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    notebook = json.loads(SOURCE_NOTEBOOK.read_text(encoding="utf-8"))
    cell = notebook["cells"][42]
    source = "".join(cell["source"])

    assert source.count(OLD_EVIDENCE_HELPER) == 1
    assert source.count(OLD_PROMOTION) == 1
    assert source.count(OLD_STATS) == 1
    source = source.replace(OLD_EVIDENCE_HELPER, NEW_EVIDENCE_HELPER, 1)
    source = source.replace(OLD_PROMOTION, NEW_PROMOTION, 1)
    source = source.replace(OLD_STATS, NEW_STATS, 1)
    ast.parse(source)
    cell["source"] = source.splitlines(keepends=True)
    cell["outputs"] = []
    cell["execution_count"] = None

    notebook["metadata"]["kernelspec"]["name"] = "python3"
    OUTPUT_NOTEBOOK.write_text(
        json.dumps(notebook, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    metadata = json.loads(METADATA_SOURCE.read_text(encoding="utf-8"))
    metadata["id"] = "sanjay0614/casmi26-v11-candidate-evidence-gate"
    metadata["title"] = "CASMI26 V11 Candidate Evidence Gate"
    metadata["code_file"] = OUTPUT_NOTEBOOK.name
    (OUTPUT_DIR / "kernel-metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_NOTEBOOK}")


if __name__ == "__main__":
    main()
