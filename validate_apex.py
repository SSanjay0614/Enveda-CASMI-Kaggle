import json
from pathlib import Path

for d in sorted(Path(".").glob("kernel_v5*")):
    nb = json.loads(next(d.glob("*.ipynb")).read_text(encoding="utf-8"))
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    text = "".join("".join(c["source"]) for c in code)
    cfg = "".join(code[0]["source"])
    keys = {}
    for k in ["EXTLIB_TAU", "EXTLIB_K", "V8 =", "RR8_ALPHA", "LIB_HIT_GATE", "NP_PROMO_MARGIN", "MASS_FREE"]:
        line = [l for l in cfg.splitlines() if l.startswith(k)]
        keys[k] = line[0][:70] if line else "MISSING"
    print("=" * 20, d.name, "| cells", len(code), "| chars", len(text))
    print("  overlay call:", text.count("_apex_extlib_overlay("), "| swap:", text.count("_swap_to_ours("), "| submission.csv:", text.count("submission.csv"))
    for k, v in keys.items():
        print("   ", k, "->", v)
