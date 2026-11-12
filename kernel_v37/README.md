# kernel_v37 — 0.487 reproduction (upstream v589 + popwenman scorer v80)

**What it is.** `guhongbin/casmi26-v589-alex0484-extlib` (public LB 0.487, 207 votes)
pulled and re-pushed **verbatim** under our account, with its own dataset list and
`popwenman/casmi26-scorer-train-v80` attached as a kernel source.

**Why.**
1. It re-establishes our best public score at 0.487 (we sat at 0.480 with `kernel_v31`).
2. It validates the deployment path we need for `kernel_v38`: a private copy of the
   notebook can reach a scorer kernel's output under `/kaggle/input` and swap it in.

**No code changes.** The notebook is byte-identical to upstream (`casmi26-v589-...ipynb`,
810 963 bytes). Its own cell 15 already implements the two-scorer ensemble:
`neural_score = 0.5*z(public kit scorer) + 0.5*z(attached scorer)` on ranks 2–25,
rank 1 unchanged. Cell 5 config is `CUSTOM: w_top=0.25, w_mid=0.75, rescue=0`.

**How the swap works (important for v38).** `_swap_to_ours()` scans `/kaggle/input` for
`final_model.pt` next to a `config_used.json`, skipping the kit bundle, then builds
`/kaggle/working/ours_bundle` from the public bundle's `model.py`/`features.py` and the
found checkpoint. It copies the **public** `config.json`, which is why it only works for
v80's width-192 model; v38 patches exactly that line.

**Submission.** `kaggle competitions submit -c enveda-CASMI26-molecule-id-mass-spectra
-k sanjay0614/casmi26-v37-lb487-repro -v <version> -f submission.csv -m "..."`.
A submission is a hidden-test kernel rerun, not the visible smoke run; only the rerun
sees all 400 molecules.
