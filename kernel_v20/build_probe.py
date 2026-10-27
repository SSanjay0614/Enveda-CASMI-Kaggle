"""Build kernel_v20: V18 pipeline forced onto CPU, full 12-molecule path, timings.

Purpose: answer, with one cheap CPU Kaggle run, whether the V18 pipeline executes
without a GPU and how many CPU seconds per molecule it costs.  Every engine in the
source already falls back to CPU (`cuda if torch.cuda.is_available() else cpu`); the
hard gates are the T4 preflight assert, the ICE/GLACIER/N1 device arguments and the
V12 rerank assert.  Nothing about the scoring maths is changed.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "kernel_v18" / "casmi26-v18-neural-rerank.ipynb"
OUT_NB = HERE / "casmi26-v20-cpu-probe.ipynb"
OUT_META = HERE / "kernel-metadata.json"

CAP = {}

# ---------------------------------------------------------------- cell edits


def patch_preflight(text):
    """c29: drop the T4 requirement, keep every other check."""
    marker = "    # Do not initialize a parent CUDA context before the source's Engine2 subprocess.\n"
    start = text.index(marker)
    end = text.index("    ids = sorted(", start)
    replacement = (
        "    # CPU build: no GPU is requested for this kernel, so record the absence instead of asserting T4.\n"
        "    try:\n"
        "        gpu = subprocess.check_output(\n"
        "            ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'], text=True).strip()\n"
        "    except Exception:\n"
        "        gpu = 'CPU-ONLY'\n"
    )
    return text[:start] + replacement + text[end:]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    notebook = json.loads(SRC.read_text(encoding="utf-8"))
    cells = notebook["cells"]
    assert len(cells) == 62, len(cells)

    def src(index):
        return "".join(cells[index]["source"])

    def set_src(index, text):
        cells[index]["source"] = text.splitlines(keepends=True)

    # --- c27: total ICE budget fits a CPU trial run (default 5400 s).
    c27 = src(27)
    before = c27
    c27 = c27.replace(
        "TOPN, ICE_LAM, ICE_BUDGET, ICE_PC = 60, 1.0, 5400, True",
        "TOPN, ICE_LAM, ICE_BUDGET, ICE_PC = 60, 1.0, 1800, True",
    )
    assert c27 != before, "c27 ICE budget line not found"
    set_src(27, c27)

    # --- c29: CPU-safe preflight.
    c29 = src(29)
    set_src(29, patch_preflight(c29))

    # --- c31: always take the full-data branch so the run behaves like a scoring
    #         rerun (the smoke branch asserts a CUDA device downstream).
    c31 = src(31)
    before = c31
    c31 = c31.replace(
        "IS_RERUN = bool(os.getenv('KAGGLE_IS_COMPETITION_RERUN')) or _sig != '654e030e4173780e945252b4a5adf70b'",
        "IS_RERUN = True   # CPU probe: exercise the scoring path, not the GPU-only smoke asserts",
    )
    assert c31 != before, "c31 IS_RERUN line not found"
    set_src(31, c31)

    # --- c42: ICE / GLACIER / N1 device arguments -> cpu, budgets cut for a probe.
    c42 = src(42)
    edits = [
        (
            "run_ice(ICE_PKG, items, workdir='/kaggle/working/ice_work', device='cuda', budget_s=ICE_BUDGET,",
            "run_ice(ICE_PKG, items, workdir='/kaggle/working/ice_work', device='cpu', budget_s=ICE_BUDGET,",
        ),
        (
            "run_gl(GL_PKG, gl_items, workdir='/kaggle/working/gl_work', device='cuda', budget_s=GL_BUDGET,",
            "run_gl(GL_PKG, gl_items, workdir='/kaggle/working/gl_work', device='cpu', budget_s=GL_BUDGET,",
        ),
        (
            "dict(molecules=0, changed_vs_ice_top25=0, changed_vs_ice_top1=0), 1.0, 4000",
            "dict(molecules=0, changed_vs_ice_top25=0, changed_vs_ice_top1=0), 1.0, 1800",
        ),
        (
            "N1_BUDGET = 1200.0 if IS_RERUN else 600.0",
            "N1_BUDGET = 600.0 if IS_RERUN else 300.0",
        ),
        (
            "N1_WORK, N1_SITE, N1_DEVICE, N1_DRIVER_EXTRA = '/kaggle/working/n1_work', '/kaggle/working/ice_site', 'cuda', []",
            "N1_WORK, N1_SITE, N1_DEVICE, N1_DRIVER_EXTRA = '/kaggle/working/n1_work', '/kaggle/working/ice_site', 'cpu', []",
        ),
    ]
    for old, new in edits:
        assert old in c42, f"c42 patch not found: {old[:60]}"
        c42 = c42.replace(old, new)
    set_src(42, c42)

    # --- c61: allow the rerank to run on CPU.
    c61 = src(61)
    edits = [
        (
            'import torch as _torch\nassert _torch.cuda.is_available(), "V12 requires the configured Kaggle GPU"\n_gc.collect()\n_torch.cuda.empty_cache()',
            'import torch as _torch\n_V12_DEVICE = "cuda" if _torch.cuda.is_available() else "cpu"\nprint("V12 device:", _V12_DEVICE, flush=True)\n_gc.collect()\nif _V12_DEVICE == "cuda":\n    _torch.cuda.empty_cache()',
        ),
        (
            '    checkpoint="final_model.pt",\n    device="cuda",\n)',
            '    checkpoint="final_model.pt",\n    device=_V12_DEVICE,\n)',
        ),
        (
            "del _scorer\n_gc.collect()\n_torch.cuda.empty_cache()",
            "del _scorer\n_gc.collect()\nif _V12_DEVICE == 'cuda':\n    _torch.cuda.empty_cache()",
        ),
    ]
    for old, new in edits:
        assert old in c61, f"c61 patch not found: {old[:60]}"
        c61 = c61.replace(old, new)
    set_src(61, c61)

    # --- new final cell: per-stage wall clock + output sanity.
    probe = '''# CPU probe report: wall clock per stage and the shape of what we produced.
import json as _pj, platform as _pf, sys as _ps, time as _pt
try:
    _probe = {}
    for _name, _path in (('ice', 'ice_work/ice_out.json.meta.json'), ('gl', 'gl_work/gl_out.json.meta.json'),
                         ('n1', 'n1_work/n1_out.json.meta.json')):
        try:
            _probe[_name] = _pj.load(open(_path))
        except Exception as _e:
            _probe[_name] = {'status': f'missing: {_e!r}'}
    _sub = _pd.read_csv('submission.csv', dtype=str, keep_default_na=False)
    _probe['summary'] = dict(
        elapsed_s=round(_pt.time() - T0, 1),
        molecules=int(_sub.molecule_id.nunique()),
        rows=int(len(_sub)),
        avg_candidates=round(float(_sub.smiles.map(lambda s: len(s.split(';'))).mean()), 2),
        ice_health=CLAW_ICE_HEALTH,
        gl_health=CLAW_GL_HEALTH,
        n1_health=N1_HEALTH,
        gpu=None,
        python=_pf.python_version(),
        executable=_ps.executable,
        is_rerun=bool(IS_RERUN),
        ice_budget=ICE_BUDGET,
    )
    open('/kaggle/working/cpu_probe.json', 'w').write(_pj.dumps(_probe, indent=1, default=str))
    print('CPU_PROBE', _pj.dumps(_probe['summary'], sort_keys=True), flush=True)
    for _name in ('ice', 'gl', 'n1'):
        _m = _probe.get(_name) or {}
        print(f'CPU_PROBE_STAGE {_name}', _pj.dumps({k: _m.get(k) for k in
              ('status', 'device', 'seconds', 'n_mols_scored', 'n_scored', 'n_pred_fail')}, default=str), flush=True)
except Exception as _e:
    print('CPU_PROBE_FAILED', repr(_e), flush=True)
'''

    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": probe.splitlines(keepends=True),
    }
    # insert before the trailing markdown-free end
    cells.append(new_cell)

    OUT_NB.write_text(json.dumps(notebook, indent=1, ensure_ascii=False), encoding="utf-8")

    meta = json.loads((HERE.parent / "kernel_v18" / "kernel-metadata.json").read_text(encoding="utf-8"))
    meta.update(
        {
            "id": "sanjay0614/casmi26-v20-cpu-probe",
            "title": "CASMI26 V20 CPU Probe",
            "code_file": OUT_NB.name,
            "enable_gpu": False,
            "enable_tpu": False,
            "enable_internet": False,
        }
    )
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"built {OUT_NB.name} ({len(cells)} cells)")
    print(f"wrote {OUT_META.name}")


if __name__ == "__main__":
    main()
