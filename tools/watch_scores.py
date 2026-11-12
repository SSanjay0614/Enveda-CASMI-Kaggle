"""Watch today's five CASMI submissions until they score.

Prints every status transition with the public score, and exits when all refs are done or
after 12 h, so the agent resumes exactly when the numbers are actionable.
"""
import subprocess
import sys
import time

COMP = "enveda-CASMI26-molecule-id-mass-spectra"
REFS = {
    "58228612": "v38  big-a @0.50 blend",
    "58228650": "v39  4-scorer, public 0.25",
    "58229302": "v40  v38 + w_mid 0.85",
    "58229308": "v41  big-a @0.65 blend",
    "58229377": "v42  2 ours + public 0.25",
}
T0 = time.time()
DEADLINE = T0 + 12 * 3600


def submissions():
    r = subprocess.run([sys.executable, "-X", "utf8", "-m", "kaggle", "competitions",
                        "submissions", "-c", COMP],
                       capture_output=True, text=True, timeout=900)
    return (r.stdout or "") + (r.stderr or "")


def log(msg):
    print(f"[{round(time.time() - T0):6d}s] {msg}", flush=True)


seen = {}
done = set()
while time.time() < DEADLINE:
    out = submissions()
    for line in out.splitlines():
        tokens = line.split()
        if not tokens or tokens[0] not in REFS:
            continue
        ref = tokens[0]
        idx = next((i for i, t in enumerate(tokens) if t.startswith("SubmissionStatus.")), None)
        if idx is None:
            continue
        status = tokens[idx].replace("SubmissionStatus.", "")
        score = tokens[idx + 1] if idx + 1 < len(tokens) else ""
        key = (status, score)
        if seen.get(ref) != key:
            log(f"{ref} {REFS[ref]}: {status} score={score or '-'}")
            seen[ref] = key
        if status in ("COMPLETE", "ERROR", "INVALID"):
            done.add(ref)
    if done >= set(REFS):
        log("all five submissions finished")
        break
    time.sleep(300)
else:
    log("watch window expired")

log("final: " + repr(seen))
