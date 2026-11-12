# kernel_c1_scorer_big — our own CASMI spectrum→structure scorer (run A)

**What it is.** A private training run of the public kit (`sanpier/casmi-spectrum-model-v1`,
Apache-2.0) with a wider transformer and a much longer schedule than either the public
16-epoch checkpoint or `popwenman/casmi26-scorer-train-v80` (56 epochs).

**Why.** The only public-verified lever in this competition so far is scorer quality, not
pipeline knobs: the 0.480 → 0.487 jump is popwenman's v80 scorer (diagnostic MRR@25
0.4844 → 0.6603 on a 256-candidate random-molecule holdout) attached to the same notebook.
v80 early-stopped at epoch 52 with the diagnostic still high, so the next thing to buy is
capacity, not more epochs at width 192.

**Change vs v80** (everything else identical — same kit, same data, same seed):

| knob | v80 | here |
|---|---|---|
| width / layers / heads / embedding | 192 / 3 / 6 / 192 | **256 / 4 / 8 / 256** |
| steps per epoch | 500 | **600** |
| max epochs | 80 (stopped at 56) | **170** |
| patience | 4 | 6 |
| holdout / refit budgets | 5.0 h / 6.0 h | 3.0 h / 3.5 h |
| seed | 20261023 | 20261023 (same holdout identities as v80, for a paired diagnostic) |

Keep `seed=20261023` on purpose: the holdout split is a function of the seed, so the
256-candidate diagnostic is computed on exactly the same 1000 molecules as v80's 0.6603.
Comparing across seeds would add ±0.015 noise to every decision.

**Budget.** prepare is a fixed 6175 s (2.43 M spectra / 273 833 molecules); ~47 s per
training epoch at width 256 plus ~12 s validation. Holdout is deadline-capped at 3.0 h
(~170 epochs), refit replays `best_epoch` epochs at 3.5 h cap. Expected wall time ≈ 6–7 h
of the 9 h GPU limit.

**Outputs** (kernel output, consumed by `kernel_v38` as a kernel source):
`final_model.pt`, `config_used.json`, `model.py`, `features.py`, `training_history.json`,
`training_result.json`, `data_audit.json`.

**Notes.**
- `config_used.json` is written on purpose: the 0.487 notebook looks for
  `final_model.pt + config_used.json` to find "our" bundle, but its `Scorer` reads
  `config.json`. `kernel_v38` therefore merges `config_used.json` over the kit config and
  writes it as `config.json` — without that the width-256 `state_dict` cannot load.
- Training data is competition `train.parquet` only (`external_paths=[]`), same as v80, so
  no extra provenance/licensing question is introduced for a prize-eligible model.
- Deployed model = `final_model.pt` (full-data refit on `best_epoch` epochs). Never
  evaluate it on the holdout identities.
