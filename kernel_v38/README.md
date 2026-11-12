# kernel_v38 — 0.487 pipeline + our own big scorer (z-score blend)

Built from `kernel_v37` (upstream v589, byte-identical) by `tools/make_v38.py`. Only
cell 15 changes.

**Patches**

1. `_swap_to_ours()` can now pick our bundle when **both** `popwenman/casmi26-scorer-train-v80`
   and `sanjay0614/casmi26-scorer-big-a` are attached. Upstream takes `_hits[0]`, i.e. an
   arbitrary filesystem-order bundle. Now bundles are ranked: config width ≠ 192 first
   (v80 is 192 by construction, ours is 256), then paths containing "big", then path name.
   The candidates and the chosen width are printed so the log proves which model ran.
2. That bundle's `config_used.json` is **merged over** the kit `config.json` and written as
   `config.json`. Upstream copies the kit config, which pins width 192 / 3 layers, so a
   width-256 `state_dict` would fail to load. This is the mandatory edit for any scorer
   that is not v80's exact architecture.
3. The ensemble weight is a top-of-cell constant `OURS_W` (upstream hard-codes 0.5/0.5),
   used as `(1-OURS_W)*z(public) + OURS_W*z(ours)` on ranks 2–25. Rank 1 is untouched.

**Build variants**

```
python tools/make_v38.py 0.5    # neutral, matches upstream's proven weight
python tools/make_v38.py 0.65   # tilt towards our scorer
python tools/make_v38.py 0.35   # tilt towards v80
```

**What to verify in the log before submitting**

- `OURS candidates: [...]` lists both bundles and `OURS BUNDLE READY ... from ...` points at
  `casmi_scorer_big_a`.
- `OURS config: width 256 layers 4 heads 8 embedding 256`.
- `ENSEMBLE neural = 0.5*z(public) + 0.5*z(ours)` (or whatever `OURS_W` is).
- The hidden scoring rerun (not the fast commit) is the run that counts.

**Fallbacks.** If our config does not load, the run raises rather than silently scoring
with v80 — then change `OURS_W` or detach our bundle and resubmit v37.
