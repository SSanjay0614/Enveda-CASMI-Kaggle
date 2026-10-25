# Version 12 — Neural Candidate-Only Rerank

V12 uses the confirmed V7 submission (0.465) as its baseline. It leaves V7's candidate generation, candidate-aware PubChem promotion, library shield, simulator handling, and fusion unchanged. After the final baseline submission list is written, the V12 cell scores only those existing candidates with the public CASMI spectrum-candidate model and applies reciprocal-rank fusion with fixed weight `0.15` and offset `3.0`.

The output is constrained to reorder each molecule's existing candidates. The cell checks the Kaggle sample row order, candidate count, candidate uniqueness, and exact candidate-set preservation. It logs the pinned model checkpoint SHA-256, number of processed molecules, number of reordered lists, and number of changed top-1 predictions. V12 requires the Kaggle GPU and keeps the competition's offline-inference setting.

## Evidence and limitations

The public reference [Sanpier neural rerank notebook](https://www.kaggle.com/code/sanpier/pubchem-neural025-lb-0-466) is titled `LB 0.466`. Its own notebook report for the fixed `0.15` experiment explicitly says the weight is unvalidated and no validation was performed. Its artifact also reports 12 changed rows and zero top-1 changes in the visible 12-molecule smoke run; that smoke set is not an accuracy evaluation. The public model's training audit says it used official competition training data only and did not read hidden test data, but its diagnostic MRR is measured on a random molecular holdout with the answer guaranteed in a limited candidate set. That number is not leaderboard MRR and does not establish that neural reranking will help our complete candidate generator.

The Kaggle dataset page reports an unknown asset license. The notebook attaches and calls its published inference bundle directly; no model code or checkpoint is vendored in this repository. The model author's README explicitly directs users to use `final_model.pt` for inference and warns not to use its raw scores at full weight without evaluation.

V12 is an isolated experiment based on V7, not V11. Its competition submission `57619742` completed with public score **0.465**, tying the V7/V8 best. It produced no leaderboard improvement. This result does not show whether its lower-rank reranking helped the reciprocal-rank metric at finer precision, but the fixed experiment did not move the reported public score.
