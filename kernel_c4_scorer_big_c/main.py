# CASMI26 scorer "big": our own spectrum->structure scorer, trained from the public kit
# (sanpier/casmi-spectrum-model-v1, Apache-2.0) with a wider transformer and a much longer
# schedule than the public 16-epoch model or popwenman's 56-epoch v80.
#
# Why: the public 0.480 -> 0.487 jump came from training the same kit for 56 instead of 16
# epochs (diagnostic MRR 0.4844 -> 0.6603 on a 256-candidate holdout, still rising). One
# epoch is ~17 s at width 192, so the whole budget goes into epochs and width rather than
# into more clever features.
#
# Output: final_model.pt + config_used.json + training_result.json, the files the ensemble
# notebook looks for under /kaggle/input.
import json
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

T0 = time.time()


def log(*a):
    print(*a, flush=True)


def heartbeat():
    while True:
        time.sleep(60)
        log(f"HEARTBEAT {round(time.time() - T0)}s")


threading.Thread(target=heartbeat, daemon=True).start()

import torch

log("ENV python", sys.version.split()[0], "| torch", torch.__version__,
    "| cuda", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NONE")
try:
    from rdkit import rdBase
except ImportError:
    wh = sorted(Path("/kaggle/input").rglob("rdkit-*.whl"))
    assert wh, "rdkit wheel dataset not attached"
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-index",
                    "--find-links", str(wh[0].parent), "rdkit==2026.03.3"], check=True)
    from rdkit import rdBase
log("rdkit", rdBase.rdkitVersion)

hits = sorted(Path("/kaggle/input").rglob("casmi_spectrum_model_v1/train.py"))
assert len(hits) == 1, hits
kit = hits[0].parent
stage = Path("/kaggle/working/kit_staged")
shutil.copytree(kit, stage, dirs_exist_ok=True)
prep = stage / "prepare.py"
src = prep.read_text()
OLD, NEW = "'smiles':['smiles','canonical_smiles']", "'smiles':['smiles','canonical_smiles','normalized_smiles']"
if OLD in src:
    prep.write_text(src.replace(OLD, NEW))
    log("KIT_DELTA applied: normalized_smiles alias")
sys.path.insert(0, str(stage))
import prepare  # noqa: E402
import train  # noqa: E402

cfg = json.loads((kit / "config.json").read_text())
comp = sorted(Path("/kaggle/input").rglob("train.parquet"))
assert len(comp) == 1, comp
cfg.update(
    seed=20261112,
    width=256,
    heads=8,
    layers=4,
    embedding=256,
    epochs=170,
    steps_per_epoch=600,
    patience=6,
    holdout_hours=3.0,
    refit_hours=3.5,
    train_path=str(comp[0]),
    work="/kaggle/working/cache_big_c",
    output="/kaggle/working/casmi_scorer_big_c",
    external_paths=[],
)
log("CFG", json.dumps({k: cfg[k] for k in ("seed", "epochs", "batch_size", "steps_per_epoch",
                                          "patience", "holdout_hours", "refit_hours",
                                          "width", "layers", "heads", "embedding")}))

audit = prepare.prepare(cfg)
work, out = Path(cfg["work"]), Path(cfg["output"])
out.mkdir(parents=True, exist_ok=True)
shutil.copy2(work / "data_audit.json", out / "data_audit.json")
log("PREP_DONE", round(time.time() - T0), "s")

result = train.run(cfg)
log("TRAIN_RESULT", json.dumps(result))
(out / "training_result.json").write_text(json.dumps(result, indent=2))
(out / "config_used.json").write_text(json.dumps(cfg, indent=2))
for name in ("model.py", "features.py"):
    shutil.copy2(kit / name, out / name)
for p in sorted(out.iterdir()):
    log("ARTIFACT", p.name, p.stat().st_size)
shutil.rmtree(work, ignore_errors=True)
log(f"SCORER_BIG_C_DONE {round(time.time() - T0)}s")

