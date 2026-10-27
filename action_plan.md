# Enveda CASMI 2026 — Action Plan for October 26, 2026

Planning and analysis only: no model or kernel code has been changed for this plan.

## Current facts

Kaggle CLI was checked on October 26, 2026. It reported **5 submissions remaining today** and **15 lifetime submissions**. Recheck Kaggle's live rules and quota immediately before submitting; older project notes mention a different daily limit.

Recent scored submissions:

| Candidate | Submission | Public MRR@25 |
|---|---:|---:|
| V7 — candidate-aware PubChem promotion | `57581596` | **0.465** |
| V8 — looser candidate-aware promotion | `57582145` | **0.465** |
| V12 — neural rerank of existing top-25 candidates | `57619742` | **0.465** |
| V13 — V7 evidence gate with candidate-aware early slots | `57631787` | **0.465** |
| V14 — stronger PubChem rescue gate with early slots | `57631794` | **0.465** |
| V11 corrected candidate-evidence gate | `57631114` | **0.455** |

Other nearby results include V6 at **0.464**, V9 at **0.464**, and V10 at **0.464**. V7/V8/V12/V13/V14 are tied at the displayed precision. The public score cannot tell whether their underlying per-row rankings are identical or whether small gains and losses cancel out.

The first V11 submission (`57619741`) completed without a displayed score; the corrected V11 submission (`57631114`) scored 0.455. Check the Kaggle submission record for any additional diagnostic before treating the first run as a valid score.

## What the experiments say

### The system is at a public-score plateau, not yet proven to have a single faulty component

V6–V14 mostly fall between 0.464 and 0.465. Changes to fusion, thresholds, evidence gates, early candidate slots, and a candidate-only neural reranker have not moved the displayed public score above 0.465. This is evidence that small policy tweaks are not reliably improving end-to-end performance; it does not prove the ceiling is 0.465.

### Candidate-only reranking did not improve the reported score

V12 can only reorder candidates already present in the baseline top 25. It scored 0.465, tying V7. If the true molecule is absent from the top 25, no reranker can recover it. Further reranking work should therefore be gated on measuring truth-in-candidate recall at 1/5/25 and full MRR@25 on identity-held-out data. Do not attach another opaque or unvalidated reranker based on an attractive notebook title alone.

### Panel wins did not transfer into a visible leaderboard gain

V13 and V14 changed early-slot/promotion policies using candidate-specific PubChem evidence and scored 0.465, the same displayed score as V7. Their curated 250-molecule replay showed large gains in the answer-removed-from-reference scenario, but flat or slightly negative results in other scenarios. That panel is a useful diagnostic, not a representative estimate of hidden-set performance. The mismatch suggests scenario mixture, panel selection, or broader hidden-test distribution may matter; the current score does not identify which.

### A gate can harm coverage if missing evidence is mishandled

The original V11 failed on missing candidate-level evidence; the corrected run scored 0.455. This is a concrete warning to audit missing/nonfinite evidence handling, fallback behavior, and how many rows receive promotions before changing gates again. The score alone does not establish that this fix caused the 0.010 drop; row-level paired diagnostics are needed.

### Small public-score ties require deeper diagnostics

The displayed 0.465 scores can mask different predictions. Compare per-molecule ranks and per-scenario results where labels are legitimately available. For the public leaderboard, treat a tie as no established improvement and avoid selecting a more complex candidate solely because of a favorable small-panel result.

## Plan for today's attempts

### Stage 1 — diagnose before submitting

1. Use V7 (0.465) as the control because it is the simplest confirmed top-scoring candidate-aware baseline. Preserve V13/V14 as policy variants, not as proven upgrades.
2. Re-run the V7, V12, V13, and V14 code against the same identity-held-out folds from the public benchmark. Keep validation molecule identities out of label-derived models, reference spectra, candidate pools, and any other target-derived lookup.
3. For every fold and candidate, report:
   - Full MRR@25 and paired per-molecule MRR deltas versus V7.
   - Truth-in-candidate recall at 1, 5, and 25, before and after promotion/reranking.
   - The fraction of rows changed, top-1 changes, and changes by reference-library / answer-removed / no-reference scenario.
   - Missing/nonfinite candidate evidence counts and promotion/fallback counts.
4. Determine whether errors are mostly **candidate-generation misses** (truth absent from top 25) or **ranking misses** (truth present but ranked too low). This decides whether the next experiment should target candidate recall or ranking.
5. For V11, inspect the corrected gate's paired per-row changes and evidence-availability strata against V7. Do not reintroduce a hard assertion or a success-shaped fallback for missing evidence.

### Stage 2 — conditional candidate priorities

Only spend an attempt on a candidate with reproducible, identity-held-out full-pipeline improvement and a completed Kaggle smoke/full rerun.

1. **First priority if truth-in-candidate recall is the bottleneck:** improve candidate generation/coverage using a permitted source or a better validated mass/spectral retrieval step. Keep the V7 ranker fixed so the effect is isolated.
2. **First priority if ranking is the bottleneck:** test one transparent, candidate-preserving ranker or promotion policy against V7, with a fixed protocol and no hidden-label tuning. Require paired full MRR@25 gains across folds, not only gains in one curated scenario.
3. **If V12/V13/V14 remain tied or mixed across folds:** do not submit them again as supposed improvements. Keep V7 as the incumbent and reserve the remaining attempts.
4. Do not repeat the V11 evidence-gate behavior without first verifying missing-evidence handling and paired validation. Do not stack another threshold, prior, shield, or neural rerank change onto a candidate whose individual contribution is unverified.
5. Treat the current five-attempt quota as a limit, not a target. Unless the diagnostics are decisive, make **zero or one** new submission today rather than spending all attempts on small variants.

If the identity-held-out full-pipeline diagnostics and Kaggle rerun cannot be completed in time, make no new submission. The known 0.465 result is preferable to an unvalidated experiment.

## Validation gate for each new candidate

- Change one clearly stated factor from the V7 control.
- Use the same identity-held-out folds for V7 and the candidate; report paired deltas and uncertainty.
- Audit truth-in-candidate recall separately from ranking quality.
- Ensure validation identities and their target-derived evidence are excluded from every training/reference/candidate source.
- Confirm all score claims are for full MRR@25; clearly label panel, proxy, smoke, and component-only metrics.
- Check missing evidence, fallbacks, output candidate count, uniqueness, valid SMILES, and exact competition template row alignment.
- Complete Kaggle offline inference and verify the full expected test set was processed before submitting.
- Record kernel version, submission reference, score, licenses/provenance, and negative results. A tie is not a demonstrated gain.

## Current recommendation

**Anchor on V7 at 0.465. First diagnose truth-in-top-25 recall versus ranking quality on identity-held-out folds.** Prioritize candidate coverage if the truth is usually absent; prioritize a simple ranker only if the truth is present but misplaced. V12–V14 and the corrected V11 do not justify another blind submission. Preserve most of today's reported five attempts unless a candidate clears the validation gate.

## Review update — October 26, 2026

Kaggle was checked again via CLI: our latest V14/V13/V12 submissions are complete at **0.465**, the corrected V11 is complete at **0.455**, and the account has **5 submissions remaining today** (15 lifetime). The public kernel list is led by the 0.468 Roman Rozen title, followed by 0.467 Kozykappa and Alex Chilton variants. No submission is pending.

### Decision: keep Stage 1, tighten the eligibility gate

The action plan remains valid. The V7–V14 leaderboard plateau makes a fold-safe breakdown of candidate coverage versus ranking a better next step than another threshold sweep. The identity-fold bundle provides five InChIKey14-disjoint folds; its documentation specifically warns that models trained on all competition training data have already seen those folds. Any comparison must therefore use fold-safe model artifacts and remove held-out identities from reference spectra, label-derived features, and candidate pools according to the scenario being measured.

### Public high-score scan

- The archived [Roman Rozen notebook](https://www.kaggle.com/code/romanrozen/0-468-casmi-from-peaks-to-structures) advertises **0.468**, and [Alex Chilton's notebook](https://www.kaggle.com/code/alexchilton/casmi26-lb-0-467-one-knob-rrf-offset-3-to-1) reports a tested RRF-offset change from 3 to 1 reaching **0.467**. These are small margins over our **0.465** control. Their notebook inputs include `sanpier/casmi-spectrum-model-v1` (Kaggle metadata says license `unknown`) and `casmi26-attributed-v4g-reproduction-assets` (CC-BY-NC-SA-4.0). The former's score claim is not independently established by the visible 12-molecule smoke; the latter license restricts commercial use.
- These notebooks are useful for identifying a testable idea, not as assets to attach to a prize-focused rerun. The RRF offset is a simple, reproducible hypothesis, but this project's V12 already tried neural candidate-only reranking and tied V7. Test a new rank-fusion policy only after the identity-fold diagnostics show ranking, rather than candidate recall, is the limiting factor.
- Kaggle's [competition overview](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/overview) allows public external data/models subject to competition conditions. The host's [licensing reminder](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/discussion/741359) says winning solutions must be compatible with commercial use and redistribution. Treat missing or incompatible asset terms as a stop for prize-eligible reuse until provenance is resolved. This applies to our existing V7 lineage too: its metadata includes the NC-SA reproduction-assets dataset, so review actual dependency usage and replace any incompatible dependency before claiming prize eligibility.

### Revised execution order

1. Keep V7 as the score control and run the planned identity-held-out diagnostic on Kaggle. Start with a fold and a smoke subset, then complete all folds only if runtime permits. Reuse fold-safe artifacts; do not evaluate full-training-data models on folds they have seen.
2. Report truth recall at 1/5/25 separately from MRR@25, and stratify by whether the held-out identity remains in the candidate pool or reference library. This will tell us whether to work on retrieval or ranking.
3. Audit each actual input dependency for license and provenance while building the validation run. Mark a source unresolved if Kaggle metadata says `other` or `unknown`; do not describe the resulting solution as prize-eligible until resolved.
4. If ranking is the bottleneck, test one protected-rank-1 RRF-offset policy inspired by the public 0.467/0.468 notebooks, using an allowed model/source and paired fold results. If recall is the bottleneck, hold ranking fixed and improve candidate generation with compatible assets.
5. Keep the submission budget for candidates that beat V7 on full identity-held-out paired MRR@25 and pass a complete Kaggle inference run. No new submission is justified by the public notebooks' small margin alone.

### Run update — October 26, 2026

- V15 Kaggle kernel version 1 completed. Its visible-run receipt has 400 output rows, 12 processed visible molecules, and 388 placeholders; the neural reranker changed 12 candidate lists and 0 top-1 entries. This is a smoke result, not a public score.
- V16 Kaggle kernel version 1 completed with 400 output rows, 12 processed visible molecules, 388 placeholders, 12 lists changed, and 1 top-1 change. This also is only a smoke result.
- Submitted both notebooks for hidden-test inference: V15 submission `57667149` and V16 submission `57667157`. Both are `PENDING`; no scores are recorded yet. Kaggle reports **3 submissions remaining today**.
- V17 and V18 kernel version 2 have started and are `RUNNING`. V19 remains saved without a run. Verify full hidden-test row processing and score each pending submission before treating any variant as an improvement.

### Follow-up — V17 submitted; V19 started

- V17 kernel version 2 completed successfully. Its visible run produced a 400-row output, processed the 12 visible molecules, preserved the candidate set, and recorded 12 changed lists / 1 changed top-1. The remaining 388 rows are visible-run placeholders, so the score must come from the hidden scoring rerun.
- Submitted V17 as competition ref `57668444`; status is `PENDING`. V15 (`57667149`) and V16 (`57667157`) remain `PENDING`. Two submissions remain today.
- V19 kernel version 2 is now `RUNNING`: protected-leader fusion, middle weight 0.50, offset 1. V18 had completed its visible run but was not submitted in this step.

### Follow-up — V18 submitted

- V18 kernel version 2 completed with 400 output rows, 12 visible molecules processed, 388 placeholders, 12 lists changed, and 1 top-1 change. This is a smoke run; the hidden scoring rerun supplies the score.
- Submitted V18 as ref `57668919`; status is `PENDING`. V15 (`57667149`), V16 (`57667157`), and V17 (`57668444`) are also still pending. Kaggle reports **1 submission remaining today**.
- V19 (protected leader, middle weight 0.50, offset 1) is already running as kernel version 2: https://www.kaggle.com/code/sanjay0614/casmi26-v19-leader-safe-offset-1

## References

- [Competition workflow and rules](./competition_info.md)
- [Submission history and experiment lineage](./README.md)
- [V7 candidate-aware baseline](./kernel_v7/README.md)
- [V11 evidence-gate fix](./kernel_v11/README.md)
- [V12 neural rerank](./kernel_v12/README.md)
- [V13 early-slot policy](./kernel_v13/README.md)
- [V14 stronger promotion gate](./kernel_v14/README.md)

### Final submission update — October 26, 2026

- V19 kernel version 2 completed. Its saved visible run processed 12 of 400 rows and used placeholders for the remaining rows; this is the notebook smoke path, not its leaderboard result. Submitted the kernel-backed code entry as ref `57669437`, which is **PENDING** while Kaggle performs hidden-test inference/scoring.
- Today's Enveda quota is exhausted: 5 submissions used, 0 remaining. V15–V19 are all pending; wait for scores before planning more submissions.

## October 27 score update

Kaggle CLI shows all five October 26 Enveda submissions completed:

| Version | Submission ref | Public MRR@25 | Result |
|---|---:|---:|---|
| V15 — neural RRF offset 1 | `57667149` | 0.467 | Above the prior 0.465 control |
| V16 — leader-safe, middle weight 0.50 | `57667157` | 0.468 | Matches the earlier public lead |
| V17 — leader-safe, middle weight 0.35 | `57668444` | 0.467 | Above the prior control |
| V18 — leader-safe, middle weight 1.00 | `57668919` | **0.470** | New best confirmed public score |
| V19 — leader-safe RRF offset 1 | `57669437` | 0.466 | Above the prior control, below V18 |

V18 is the current public-score incumbent, improving by 0.005 over the previous 0.465 best and by 0.002 over the previous public 0.468 lead. This is public leaderboard evidence; private-score performance remains unconfirmed. The five attempts used on October 26 are complete. On October 27, the quota has reset: **5 available, 0 used today** (20 lifetime submissions).

### Next action

Use V18 as the control for the next Enveda experiment. Preserve the leader-safe rank-1 protection and change one factor at a time. Require identity-held-out paired MRR@25 and candidate-recall diagnostics before spending today's attempts; do not repeat V19's lower-scoring offset change without new evidence. Continue the license/provenance audit for dependencies used by the V18 lineage before describing the solution as prize-eligible.

## Addendum - October 27, 2026 (afternoon): GPU quota, CPU feasibility, offline rule lab

This section only adds information; nothing above is retracted.

### 1. The 5 daily submissions are not usable today, because submissions cost GPU hours

- Kaggle's GPU quota for this account reads **0.00 h remaining of 30 h** (40.52 h used). It refreshes **2026-10-31 00:00 UTC**.
- A submission in this competition is a *kernel rerun*: `kaggle competitions submit ... -k <kernel> -v <version>` queues a fresh run of the notebook on the full hidden test set, and only that rerun sees all 400 molecules. The uploaded file name is just the artifact to collect.
- Every CASMI kernel (V15-V19 and the V18 lineage) declares `"enable_gpu": true`, and the pipeline hard-asserts a T4 (`c29:20`, `assert 'T4' in gpu`) while ICEBERG, GLACIER, N1 and the V12 rerank are launched with `device='cuda'`.
- Consequence: the daily submission limit (5) is not the binding constraint; **GPU hours are**. Today's 5 attempts cannot be spent on GPU reruns, which is why no Enveda submission was made today.

### 2. The visible 12 molecules measure nothing (verified, not assumed)

- The 12 visible test molecules are present in `train.parquet`, so the reference library already contains their answers.
- Replaying every submitted list variant (V7, V15, V16, V18, V19) against recovered ground truth gives **MRR@25 = 1.000 for all five**.
- Therefore the repeatedly reported "12 lists changed / 1 top-1 changed" lines in earlier sections are packaging checks only. They cannot rank two variants, and they must never again be cited as evidence of progress.

### 3. New CPU asset: `kernel_v20` probe (pushed, no GPU requested)

- Builder: `kernel_v20/build_probe.py`; notebook `kernel_v20/casmi26-v20-cpu-probe.ipynb`; metadata `enable_gpu: false`.
- Diff versus V18 is limited to five cells and one appended report cell (verified by `kernel_v20/verify_diff.py`):
  - `c27`: ICE budget 5400 s -> 1800 s;
  - `c29`: the T4 assertion is replaced by a recorded `CPU-ONLY` value; every other preflight check is kept;
  - `c31`: `IS_RERUN = True`, so the run exercises the scoring branch instead of the CUDA-only smoke assertions;
  - `c42`: ICE / GLACIER / N1 device `cuda` -> `cpu`, GL budget 4000 s -> 1800 s, N1 budget -> 600 s;
  - `c61`: the V12 rerank picks `cuda if cuda available else cpu` instead of asserting CUDA.
- All scoring maths, fusion weights, promotion gate and candidate sets are untouched. Every engine in the source already had a CPU fallback (`cuda if torch.cuda.is_available() else cpu`), so this is a device change, not a rewrite.
- Purpose: measure (a) whether the V18 pipeline executes at all without a GPU, and (b) CPU seconds per molecule, which is the only thing that can say whether a CPU-only submission fits inside the 9 h notebook limit for 400 molecules.
- Kernel: https://www.kaggle.com/code/sanjay0614/casmi26-v20-cpu-probe

### 4. Offline rule lab on the 250-molecule natural-product panel (CPU, seconds per rule)

Downloaded `dmitriigluzdov/casmi26-natural-product-panel-benchmark` (167 MB) to `data/panel_benchmark/` and replayed the production PubChem-channel formula exactly (`panel_lab/rule_lab.py`), including the pass-1 truncation (top-1000 by the cheap partial score, union top-200 by the prior).

The panel ships two fingerprint columns: `fold0_full` (fold-safe checkpoint that never saw these molecules = honest) and `ab_full` (model has seen them = optimistic). MRR@25 of the channel ordering:

| rule | fold0, full window | fold0, pass1+pass2 | ab, pass1+pass2 |
|---|---:|---:|---:|
| fp only | 0.1566 | 0.1856 | 0.4069 |
| pop 0.15 (v16) | 0.5861 | 0.7417 | 0.8343 |
| **V18 production set** (0.15 + src 0.5 + np 1.0 + lotus 0.5) | **0.6531** | **0.8367** | **0.8679** |
| pop 0.30 | 0.6497 | 0.8204 | 0.8587 |
| pop 0.30 + np 2.0 | 0.6620 | 0.8438 | 0.8700 |
| pop 0.30 + np 2.0 + lotus 0.5 + src 0.5 | 0.6591 | 0.8446 | 0.8675 |

Paired bootstrap (2000 resamples) of every challenger against the V18 production set:

- `pop 0.30`: -0.0034 [-0.0255, +0.0189] (fold0, full window);
- `pop 0.30 + np 2.0`: +0.0089 [-0.0112, +0.0294];
- best challenger on pass1+pass2: +0.0078 [-0.0053, +0.0225].

**Conclusion: the prior weights are already at the panel's plateau; no CI excludes zero.** Tuning `POP_LAM`, `NP_BONUS`, `SRC_BONUS` or `LOTUS_W` on this panel is noise-chasing and must not be spent as a leaderboard attempt. The documentation prior itself is doing the work (fp-only 0.19 -> 0.84 with priors on pass1+pass2), which confirms the ratio in the dataset README rather than contradicting it.

Panel limits found while building this lab (important for future planning):

- `main_candidates.parquet` covers only **3** molecules (in 3 simulated classes); `pubchem_candidates.parquet` covers **246**. So the *main* list cannot be replayed on the panel.
- Ground truth is inside the main pool for **all 246** molecules, so the channel's own output excludes it by construction: the panel can compare channel *orderings*, not end-to-end MRR.
- `merge_eval.py` needs replay pickles that are not shipped (only result JSONs), so the published 0.361 -> 0.718 promotion story cannot be re-derived locally.

### 5. Sequencing decision for the remaining competition weeks

- ARC-AGI-3 closes **2026-11-02 23:59 UTC**; Enveda closes **2026-12-14 23:59 UTC**. GPU hours refresh on **2026-10-31 00:00 UTC**.
- Therefore: ARC owns the Oct 31 - Nov 2 GPU window (three scored attempts prepared in `arc_agi_3/v3/`), and Enveda resumes Nov 3 with roughly six weeks and about 30 h/week of quota.
- TPU (20 h) remains unusable for ARC: every top stack is CUDA-only (Pennyroyal SGLang fork, vLLM NVFP4, W4A16/NVFP4 kernels). It is also unusable for CASMI, whose models are torch/CUDA.
- The only route to an Enveda submission before Oct 31 is a CPU-only kernel rerun that fits 400 molecules inside 9 h. The `kernel_v20` probe exists to decide that with a measurement instead of an estimate.

### 6. What is still missing before the next submission

- An identity-held-out evaluator: run the pipeline on molecules from `fold_identity == 0` in `data/identity_folds/spectra_folds.parquet` (2,539,608 rows; `row` aligns with competition `train.parquet` row order) with all spectra of those identities removed from the reference library, then compute official MRR@25. This is the gate the earlier plan demanded and it still does not exist.
- CPU seconds per molecule for the full V18 path (pending `kernel_v20`).
- A CPU-only submission variant with a hard in-notebook deadline: molecules not reached before the budget expires must be filled from a defined fallback list so `submission.csv` is always complete and valid.

### 7. Measured cost anatomy of the V18 GPU run (from the V18 submission log)

The V18 visible-run log timestamps every stage (24 min total for 12 molecules, 400-row output, Tesla T4):

| stage | wall clock | marginal cost |
|---|---:|---|
| setup, dataset mount, prior tables, RDKit wheel | ~66 s | fixed |
| engine 2 (two-ranker, `generate=True`) | ~118 s -> 675 s | ~46 s/molecule |
| PubChem-only channel (pass 1 + pass 2) | ~805 s -> 880 s | ~11 s/molecule |
| engine 1 (v1 / v4n main list) | ~1029 s -> 1091 s | ~5 s/molecule |
| ICEBERG (model load 41.7 s + 1599 predictions in 39.6 s) | 87 s | ~3 s/molecule |
| GLACIER (model load 31.1 s + 1599 predictions in 19.0 s) | 55 s | ~2 s/molecule |
| N1 driver | 40 s | ~3 s/molecule |
| merge, fusion, metric audit, V12 rerank | ~110 s | fixed + small |

Quota cross-check: 5 submissions on Oct 26 consumed ~40.5 h. Each submission runs twice (commit run 0.4 h + scoring rerun). That implies a **hidden scoring rerun of roughly 7.5-8 h**, i.e. 80-90 % of the 9 h limit is already spent, and the per-molecule costs above (46 + 11 + 5 + 3 + 2 + 3 = ~70 s/molecule x 400 = 7.8 h) reproduce that number independently.

Implications, stated plainly:

- There is no GPU headroom for additional work inside a submission; any extra stage must displace an existing one.
- A CPU rerun of this full path is not viable: the fingerprint stages alone are ~86 % of the run and would be several times slower without a GPU, i.e. 20 h+ against a 9 h cap.
- A CPU submission is only possible for a **reduced** pipeline (drop engine 2, or drop the PubChem channel, or prior-only), and each of those gives up score versus the 0.470 incumbent. None of them can beat V18 today; their value is as a free, repeatable evaluation platform for the six weeks after ARC closes.



---

## STOP NOTICE - all three competitions paused until 2026-10-31 00:00 UTC (added October 27, 2026)

All three active competitions are at a stop, and the reason is the same for each: the Kaggle GPU
quota is exhausted.

- GPU hours used: 40.52 h out of 30 h. Remaining: **0.00 h**. The allowance refreshes on **2026-10-31 00:00 UTC**.
- Every submission path in this project needs a GPU. Kaggle re-runs a notebook-backed submission on the
  hidden data, so nothing can be submitted from local CPU work or from an already cached output.
- Therefore no submission can be made to any of the three competitions until the reset.

What each competition is waiting for:

- **ARC-AGI-3** (closes 2026-11-02 23:59 UTC): gets first call on the refreshed quota. Three scored
  attempts on Oct 31, Nov 1 and Nov 2, using the Franzen setup that already passed CPU validation. This
  competition has the earliest deadline, so it takes priority over the other two.
- **Enveda CASMI26** (closes 2026-12-14): resumes Nov 3, leaving about six weeks at roughly 30 h per week.
  Incumbent score stays at 0.470.
- **Name That LLM** (closes 2027-01-14): resumes after ARC. Incumbent score stays at 0.640. A full-recipe
  CPU run does not fit the 9 h limit and would score near 0.48 anyway, so it is not an option.

Nothing above retracts earlier content in this file. It only records the current pause.
