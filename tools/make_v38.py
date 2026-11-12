"""Build kernel_v38: the 0.487 notebook (v37, verbatim v589) plus our own trained scorer.

Two patches, both inside cell 15:
1. `_swap_to_ours` must be able to pick *our* bundle when both popwenman's v80
   and our big scorer are attached, and it must write that bundle's own
   `config_used.json` as `config.json` (width 256 / layers 4 instead of the kit's
   192/3). Without this the state_dict does not load.
2. The ensemble weight between the public v80 scorer and ours is exposed as
   OURS_W (upstream hard-codes 0.5/0.5).

A third optional argument patches the CUSTOM consensus weights, e.g. a higher `w_mid`
(more trust in the neural ordering of ranks 2-25 now that the scorer is stronger than the
one `w_mid=0.75` was tuned for); it writes to kernel_v40/.

Usage: python tools/make_v38.py [OURS_W] [W_MID]
"""
import json
import sys
from pathlib import Path

OURS_W = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
W_MID = float(sys.argv[2]) if len(sys.argv) > 2 else None
HERE = Path(__file__).resolve().parent.parent
SRC = HERE / "kernel_v37" / "casmi_v37_lb487_repro.ipynb"
if W_MID is not None:
    DST = HERE / "kernel_v40" / f"casmi_v40_wmid{int(round(W_MID * 100)):03d}.ipynb"
elif abs(OURS_W - 0.5) > 1e-9:
    DST = HERE / "kernel_v41" / f"casmi_v41_ours{int(round(OURS_W * 100)):03d}.ipynb"
else:
    DST = HERE / "kernel_v38" / "casmi_v38_ours_scorer.ipynb"

OLD_WMID = "CUSTOM = dict(w_top=0.25, w_mid=0.75, rescue=0)\n"

OLD_PICK = "    _src = _hits[0].parent\n"
NEW_PICK = '''    import json as _json
    def _rank(_p):
        _c = _p.parent / 'config_used.json'
        try:
            _w = _json.loads(_c.read_text()).get('width') if _c.is_file() else None
        except Exception:
            _w = None
        # prefer a bundle whose config is NOT the public kit's width-192 default,
        # then one whose path says "big", then a stable alphabetical order
        return (0 if (_w and int(_w) != 192) else 1, 0 if 'big' in str(_p).lower() else 1, str(_p))
    _hits.sort(key=_rank)
    print('OURS candidates:', [str(_p) for _p in _hits], flush=True)
    _src = _hits[0].parent
'''

OLD_CFG = "    _s.copy2(_P(base_bundle) / 'config.json', _dst / 'config.json')\n"
NEW_CFG = '''    if _cfg.is_file():
        _merged = _json.loads((_P(base_bundle) / 'config.json').read_text())
        _merged.update(_json.loads(_cfg.read_text()))
        (_dst / 'config.json').write_text(_json.dumps(_merged, indent=2))
        print('OURS config: width', _merged['width'], 'layers', _merged['layers'],
              'heads', _merged['heads'], 'embedding', _merged['embedding'], flush=True)
    else:
        _s.copy2(_P(base_bundle) / 'config.json', _dst / 'config.json')
'''

OLD_W = "        _a['neural_score'] = 0.5 * _z(_a['neural_score'].fillna(0.0)) + 0.5 * _z(_b['neural_score'].fillna(0.0))\n"
NEW_W = ("        _a['neural_score'] = (1.0 - OURS_W) * _z(_a['neural_score'].fillna(0.0)) "
         f"+ OURS_W * _z(_b['neural_score'].fillna(0.0))\n")
OLD_PRINT = "        print('ENSEMBLE neural = 0.5*z(public) + 0.5*z(ours)', flush=True)\n"
NEW_PRINT = ("        print('ENSEMBLE neural = %s*z(public) + %s*z(ours)' % (1.0 - OURS_W, OURS_W), flush=True)\n")

HEAD = (
    "OURS_W = " + repr(OURS_W) + "  # weight of our own scorer in the z-score blend\n\n"
)
OLD_HEAD = "BUNDLE = materialise_sources()\n"


def patch_cell(src: str) -> str:
    for old, new in ((OLD_PICK, NEW_PICK), (OLD_CFG, NEW_CFG), (OLD_W, NEW_W),
                     (OLD_PRINT, NEW_PRINT), (OLD_HEAD, HEAD + OLD_HEAD)):
        assert src.count(old) == 1, (old[:60], src.count(old))
        src = src.replace(old, new)
    return src


def main() -> None:
    nb = json.loads(SRC.read_text(encoding="utf-8"))
    cell = nb["cells"][15]
    assert cell["cell_type"] == "code"
    text = "".join(cell["source"])
    assert "def _swap_to_ours" in text and "neural_ours.parquet" in text, "unexpected cell 15"
    patched = patch_cell(text)
    cell["source"] = patched.splitlines(keepends=True)
    nb["cells"][15]["outputs"] = []
    nb["cells"][15]["execution_count"] = None
    if W_MID is not None:
        hit = [c for c in nb["cells"] if c["cell_type"] == "code"
               and OLD_WMID in "".join(c["source"])]
        assert len(hit) == 1, f"w_mid patch found {len(hit)} cells"
        src = "".join(hit[0]["source"])
        hit[0]["source"] = src.replace(
            OLD_WMID, f"CUSTOM = dict(w_top=0.25, w_mid={W_MID!r}, rescue=0)\n"
        ).splitlines(keepends=True)
        print("patched CUSTOM w_mid ->", W_MID)
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(json.dumps(nb, ensure_ascii=False), encoding="utf-8")
    print("wrote", DST.relative_to(HERE), "| OURS_W =", OURS_W, "| chars", len(patched))


if __name__ == "__main__":
    main()
