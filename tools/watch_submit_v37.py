"""Watch the CASMI kernels and submit v37 as soon as its visible run completes.

Runs in the background so the agent does not poll. Prints a line on every state change
and, once `casmi26-v37-lb487-repro` reports COMPLETE, submits kernel version 1 to the
competition (one submission slot), then keeps reporting the big scorer's progress and exits.
"""
import subprocess
import sys
import time

COMP = "enveda-CASMI26-molecule-id-mass-spectra"
V37 = "sanjay0614/casmi26-v37-lb487-repro"
BIG = "sanjay0614/casmi26-scorer-big-a"
T0 = time.time()
DEADLINE = T0 + 4 * 3600


def run(args, timeout=300):
    r = subprocess.run([sys.executable, "-X", "utf8", "-m", "kaggle"] + args,
                       capture_output=True, text=True, timeout=timeout)
    return (r.stdout or "") + (r.stderr or "")


def status(kernel):
    out = run(["kernels", "status", kernel])
    for line in out.splitlines():
        if "has status" in line:
            return line.split('"')[1].replace("KernelWorkerStatus.", "")
    return out.strip().splitlines()[-1][:120] if out.strip() else "UNKNOWN"


def log(msg):
    print(f"[{round(time.time() - T0):6d}s] {msg}", flush=True)


prev = {}
submitted = False
big_done = False

while time.time() < DEADLINE:
    for kernel, tag in ((V37, "v37"), (BIG, "big")):
        try:
            st = status(kernel)
        except Exception as exc:  # noqa: BLE001
            log(f"{tag}: status error {type(exc).__name__}")
            continue
        if prev.get(tag) != st:
            log(f"{tag}: {st}")
            prev[tag] = st
        if tag == "v37" and st == "COMPLETE" and not submitted:
            log("v37 complete -> submitting kernel version 1")
            out = run(["competitions", "submit", "-c", COMP, "-k", V37, "-v", "1",
                       "-f", "submission.csv",
                       "-m", "v37: upstream v589 + popwenman v80 scorer (0.487 reproduction)"],
                      timeout=900)
            log("submit output: " + " | ".join(l for l in out.splitlines() if l.strip())[-600:])
            submitted = True
        if tag == "v37" and st == "ERROR" and not submitted:
            log("v37 ERROR -> log tail:\n" + "\n".join(run(["kernels", "output", V37,
                                                           "-p", "kernel_v37/output"]).splitlines()[-20:]))
            submitted = True  # give up on v37, do not resubmit blindly
        if tag == "big" and st in ("COMPLETE", "ERROR"):
            big_done = True
    if submitted and big_done:
        log("watcher finished")
        break
    time.sleep(120)
else:
    log("watch window expired; manual follow-up needed")

log("final states: " + repr(prev))
