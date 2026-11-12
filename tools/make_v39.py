"""Build kernel_v39: 0.487 pipeline + BOTH of our big scorers in the z-blend.

v38 blends the pipeline's built-in scorer with one attached private scorer at 50/50.
v39 attaches two private scorers (big-a and big-b) and gives the public scorer a smaller
weight, because the holdout says the public 16-epoch model is the weakest member
(0.484 vs 0.716 / 0.695):

    neural_score = PUB_W * z(public) + (1-PUB_W)/2 * z(big_a) + (1-PUB_W)/2 * z(big_b)

Only cell 15 changes. The public scorer's pass is unchanged; each attached bundle gets its
own neural pass (score_final_lists() reads the global BUNDLE), is saved to its own parquet,
and the four neural columns are combined with the same weights.

Usage: python tools/make_v39.py [PUB_W]
"""
import json
import sys
from pathlib import Path

PUB_W = float(sys.argv[1]) if len(sys.argv) > 1 else 0.25
EXCLUDE = sys.argv[2] if len(sys.argv) > 2 else None  # skip attached bundles whose folder name contains this
HERE = Path(__file__).resolve().parent.parent
SRC = HERE / "kernel_v37" / "casmi_v37_lb487_repro.ipynb"
if EXCLUDE:
    DST = HERE / "kernel_v42" / "casmi_v42_three_scorer_nov80.ipynb"
else:
    DST = HERE / "kernel_v39" / "casmi_v39_three_scorer.ipynb"

HELPER = '''
def _attached_bundles(base_bundle):
    """One bundle per attached private scorer; the public kit bundle is skipped."""
    import json as _json
    import shutil as _s
    from pathlib import Path as _P
    EXCLUDE_TAG = %s
    out = []
    for _p in sorted(_P('/kaggle/input').rglob('final_model.pt')):
        if 'casmi-spectrum-model-v1' in str(_p) or 'kit_staged' in str(_p):
            continue
        _cfg = _p.parent / 'config_used.json'
        if not _cfg.is_file():
            continue
        _tag = _p.parent.name
        if EXCLUDE_TAG and EXCLUDE_TAG in _tag:
            print('BUNDLE skipped', _tag, flush=True)
            continue
        _dst = _P('/kaggle/working/bundle_%s' % _tag)
        _dst.mkdir(parents=True, exist_ok=True)
        _s.copy2(_P(base_bundle) / 'model.py', _dst / 'model.py')
        _s.copy2(_P(base_bundle) / 'features.py', _dst / 'features.py')
        _merged = _json.loads((_P(base_bundle) / 'config.json').read_text())
        _merged.update(_json.loads(_cfg.read_text()))
        (_dst / 'config.json').write_text(_json.dumps(_merged, indent=2))
        _s.copy2(_cfg, _dst / 'config_used.json')
        _s.copy2(_p, _dst / 'final_model.pt')
        print('BUNDLE', _tag, 'width', _merged['width'], 'layers', _merged['layers'], flush=True)
        out.append((_tag, str(_dst)))
    print('ATTACHED scorers:', [t for t, _ in out], flush=True)
    return out


'''

HELPER = HELPER.replace('EXCLUDE_TAG = %s', 'EXCLUDE_TAG = ' + repr(EXCLUDE))

OLD_HEAD = "PUB_BUNDLE = BUNDLE\nOURS_BUNDLE = _swap_to_ours(PUB_BUNDLE)\n"
NEW_HEAD = (HELPER + "PUB_BUNDLE = BUNDLE\nOURS_BUNDLE = _swap_to_ours(PUB_BUNDLE)\n"
            "ATTACHED = _attached_bundles(PUB_BUNDLE)\n")

NEW_BLOCK = '''    BUNDLE = PUB_BUNDLE
    NEURAL_OK = score_final_lists()
    shutil.copyfile(ROOT / 'neural_candidate_features.parquet', ROOT / 'neural_public.parquet')
    PARTS = [('public', ROOT / 'neural_public.parquet')]
    for _i, (_tag, _b) in enumerate(ATTACHED):
        BUNDLE = _b
        _ok = score_final_lists()
        if _ok and (ROOT / 'neural_candidate_features.parquet').is_file():
            _dest = ROOT / ('neural_part%d.parquet' % _i)
            shutil.copyfile(ROOT / 'neural_candidate_features.parquet', _dest)
            PARTS.append((_tag, _dest))
            print('PART ok', _i, _tag, flush=True)
        else:
            print('PART failed', _i, _tag, flush=True)
    if len(PARTS) > 1:
        import pandas as _pd
        def _z(_s):
            _g = _s.groupby(level=0)
            return (_s - _g.transform('mean')) / _g.transform(lambda x: x.std(ddof=0)).clip(lower=1e-6)
        _frames = {_k: _pd.read_parquet(_s).set_index(['molecule_id', 'smiles']) for _k, _s in PARTS}
        _idx = _frames['public'].index
        _att = [k for k in _frames if k != 'public']
        _wmap = {k: PUB_W for k in ['public']}
        _wmap.update({k: (1.0 - PUB_W) / max(len(_att), 1) for k in _att})
        _out = _pd.DataFrame(index=_idx)
        _score = None
        _okall = None
        for _c in ('neural_cos', 'neural_fp', 'neural_std'):
            _out[_c] = 0.0
        for _k, _s in PARTS:
            _f = _frames[_k].reindex(_idx)
            _w = _wmap[_k]
            _zs = _w * _z(_f['neural_score'].fillna(0.0))
            _score = _zs if _score is None else _score + _zs
            for _c in ('neural_cos', 'neural_fp', 'neural_std'):
                _out[_c] = _out[_c] + _w * _f[_c].fillna(0.0)
            _o = _f['neural_ok'].fillna(False).astype(bool)
            _okall = _o if _okall is None else (_okall & _o)
        _out['neural_score'] = _score
        _out['neural_ok'] = _okall
        _out.reset_index().to_parquet(ROOT / 'neural_candidate_features.parquet', index=False)
        print('ENSEMBLE neural weights', {k: round(v, 3) for k, v in _wmap.items()}, flush=True)
    BUNDLE = ATTACHED[0][1] if ATTACHED else PUB_BUNDLE
    if not NEURAL_OK:
'''


def main() -> None:
    nb = json.loads(SRC.read_text(encoding="utf-8"))
    cell = nb["cells"][15]
    src = "".join(cell["source"])
    assert "def _swap_to_ours" in src, "cell 15 changed"
    assert src.count(OLD_HEAD) == 1, src.count(OLD_HEAD)

    start = src.index("    BUNDLE = PUB_BUNDLE\n")
    end = src.index("    if not NEURAL_OK:\n", start) + len("    if not NEURAL_OK:\n")
    assert start < end and "neural_ours.parquet" in src[start:end], "unexpected neural block"

    patched = (src[:start] + NEW_BLOCK + src[end:]).replace(OLD_HEAD, NEW_HEAD)
    assert "neural_ours.parquet" not in patched
    cell["source"] = patched.splitlines(keepends=True)
    cell["outputs"] = []
    cell["execution_count"] = None

    nb["cells"].insert(5, {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": (f"PUB_W = {PUB_W!r}   # weight of the pipeline's built-in scorer;\n"
                   "# the rest is split evenly between the attached private scorers\n").splitlines(keepends=True),
    })
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")
    print("wrote", DST.relative_to(HERE), "| PUB_W =", PUB_W)


if __name__ == "__main__":
    main()
