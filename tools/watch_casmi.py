"""Long-running background watcher for the two CASMI kernels.

Duties
------
1. Poll `kaggle kernels status` every 3 min and log every state change.
2. While a kernel is RUNNING, pull its log every ~15 min and log the last progress line
   (HOLDOUT/REFIT epoch records, HEARTBEAT, PREP milestones, tracebacks).
3. As soon as `casmi26-v37-lb487-repro` is COMPLETE, submit kernel version 1 to the
   competition exactly once (guarded by a lock file *and* a scan of existing submissions
   for a description starting with "v37:").
4. When `casmi26-scorer-big-a` finishes, download its output to `out_big_a/` and print
   `training_result.json` plus the last few holdout records, which is the decision input for
   the v38 blend weight.

Run in the background; it exits when both kernels are finished or after 14 h.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
COMP = "enveda-CASMI26-molecule-id-mass-spectra"
V37 = "sanjay0614/casmi26-v37-lb487-repro"
BIG = "sanjay0614/casmi26-scorer-big-a"
LOCK = HERE / "tools" / ".v37_submitted"
OUT_BIG = HERE / "out_big_a"
T0 = time.time()
DEADLINE = T0 + 14 * 3600
PROGRESS_EVERY = 15 * 60


def run(args, timeout=1800):
    try:
        r = subprocess.run([sys.executable, "-X", "utf8", "-m", "kaggle"] + args,
                           capture_output=True, text=True, timeout=timeout)
        return (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def status(kernel):
    out = run(["kernels", "status", kernel], timeout=300)
    for line in out.splitlines():
        if "has status" in line:
            return line.split('"')[1].replace("KernelWorkerStatus.", "")
    return out.strip().splitlines()[-1][:120] if out.strip() else "UNKNOWN"


def log(msg):
    print(f"[{round(time.time() - T0):6d}s] {msg}", flush=True)


def progress_line(kernel):
    out = run(["kernels", "logs", kernel], timeout=900)
    keys = ("HOLDOUT", "REFIT", "HEARTBEAT", "PREP_DONE", "PREPARED", "TRAIN_RESULT",
            "Error", "Traceback", "OURS", "ENSEMBLE", "BUNDLE", "SUBMITTED", "stage")
    hits = [ln.strip() for ln in out.splitlines() if any(k in ln for k in keys)]
    return hits[-1][:400] if hits else ""


def already_submitted():
    if LOCK.is_file():
        return True
    out = run(["competitions", "submissions", "-c", COMP], timeout=900)
    return any("v37:" in ln for ln in out.splitlines())


def submit_v37():
    if already_submitted():
        log("v37: already submitted (lock or existing submission), not spending a slot")
        return
    log("v37 COMPLETE -> submitting kernel version 1")
    out = run(["competitions", "submit", "-c", COMP, "-k", V37, "-v", "1",
               "-f", "submission.csv",
               "-m", "v37: upstream v589 + popwenman v80 scorer (0.487 reproduction)"],
              timeout=1800)
    log("submit: " + " | ".join(ln for ln in out.splitlines() if ln.strip())[-500:])
    LOCK.write_text(f"submitted at {time.strftime('%Y-%m-%d %H:%M:%S')}\n{out}", encoding="utf-8")


def report_big():
    log("big-a finished -> downloading output")
    out = run(["kernels", "output", BIG, "-p", str(OUT_BIG)], timeout=3600)
    log("download tail: " + out.strip().splitlines()[-1][:200] if out.strip() else "download: empty")
    for res in OUT_BIG.rglob("training_result.json"):
        log(f"training_result {res}: {res.read_text(encoding='utf-8')[:600]}")
    for hist in OUT_BIG.rglob("training_history.json"):
        try:
            h = json.loads(hist.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            log(f"history unreadable: {type(exc).__name__}")
            continue
        best = max((e.get("diagnostic_mrr25", 0) or 0, e) for e in h)
        log(f"history epochs={len(h)} best_epoch={best[1].get('epoch')} "
            f"best_diag={round(best[0], 4)} last={h[-1].get('epoch')} "
            f"last_diag={round(h[-1].get('diagnostic_mrr25') or 0, 4)}")
        for e in h[-3:]:
            log(f"  epoch {e.get('epoch')} diag {round(e.get('diagnostic_mrr25') or 0, 4)} "
                f"top1 {round(e.get('top1') or 0, 3)}")


prev = {}
last_progress = {}
fin = {}
while time.time() < DEADLINE:
    for kernel, tag in ((V37, "v37"), (BIG, "big")):
        st = status(kernel)
        if prev.get(tag) != st:
            log(f"{tag}: {prev.get(tag, '-')} -> {st}")
            prev[tag] = st
        if st == "RUNNING" and time.time() - last_progress.get(tag, 0) > PROGRESS_EVERY:
            last_progress[tag] = time.time()
            line = progress_line(kernel)
            log(f"{tag} progress: {line or 'no lines yet'}")
        if st in ("COMPLETE", "ERROR", "CANCEL_ACKNOWLEDGED") and tag not in fin:
            fin[tag] = st
            if st != "COMPLETE":
                log(f"{tag} ended {st}; log tail: {progress_line(kernel)[:600]}")
            if tag == "v37" and st == "COMPLETE":
                submit_v37()
            if tag == "big":
                report_big()
    if len(fin) == 2:
        log("both kernels finished")
        break
    time.sleep(180)
else:
    log("14 h watch window expired")

log("final: " + json.dumps(prev))
