# Enveda CASMI 2026 — Molecule Identification from Mass Spectra

Competition page: <https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra>  
Rules: <https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/rules>

## Competition at a glance

- **Goal:** Rank candidate molecular structures (SMILES) for each molecule from high-resolution tandem mass spectrometry data.
- **Metric:** Mean Reciprocal Rank at 25 (MRR@25), evaluated using the first 14 characters of the molecular InChIKey (the 2D molecular skeleton, without stereochemistry). The required output is a ranked list of up to 25 SMILES per test row.
- **Submission type:** Kaggle code/notebook inference that produces the competition's required `submission.csv`.
- **Known constraints:** Existing project notes describe an offline Kaggle GPU notebook with up to nine hours of runtime. Confirm the current accelerator, internet setting, submission quota, deadlines, output schema, and eligibility rules on the live competition page before each run.
- **Inference policy:** Prepare dependencies and assets as Kaggle inputs. Do not depend on downloading packages, models, or data during an offline competition rerun.

## Our approach

1. **Find strong public baselines.** Search Kaggle notebooks, GitHub, papers, and other public technical write-ups for high-scoring CASMI solutions and relevant mass-spectrometry candidate-ranking methods. Capture the exact competition, leaderboard score, version, data split, and whether a result is an official submission, cross-validation estimate, or a small diagnostic.
2. **Audit licenses and provenance.** Before using public code, datasets, checkpoints, or derived assets, check their licenses and the competition terms. Preserve source attribution and per-source license details. If reuse permission is missing or unclear, do not copy the implementation or asset; use only general design concepts and build an original alternative.
3. **Reproduce a competitive baseline in Kaggle.** Verify the attached data/model files, dependencies, full inference path, and exact submission schema. A local proxy score, curated-panel replay, or visible smoke run is not a hidden-test leaderboard score.
4. **Fine-tune/adapt carefully.** Start from the strongest allowed public approach and make controlled improvements—such as candidate generation, spectral matching, chemical priors, or rank fusion—one at a time. Use identity/scaffold-aware validation where possible to avoid molecule leakage, and keep hidden competition labels out of tuning.
5. **Gate and log every submission.** Confirm the full test set was processed, every row has valid candidates, ranking/deduplication is correct, the CSV matches the official template, and the Kaggle run completes within resource limits. Record the code lineage, asset licenses, validation evidence, kernel version, submission reference, and score.

The objective is to improve on a known strong approach, not to assume that a public notebook's title, CV result, or author's score will transfer to our pipeline.

## Build, validate, and submit

1. Review the live competition rules and check the current submission limit:

   ```powershell
   kaggle competitions submission-limits enveda-CASMI26-molecule-id-mass-spectra
   ```

2. Push the candidate notebook to Kaggle:

   ```powershell
   kaggle kernels push -p .\enveda_casmi\kernel_v14
   ```

   Substitute the folder for the candidate version. Check the resulting kernel ID, then inspect its status and logs:

   ```powershell
   kaggle kernels status <owner>/<kernel-name>
   kaggle kernels logs <owner>/<kernel-name>
   ```

3. Confirm the Kaggle competition rerun—not only the small visible smoke path—processes the complete hidden test set and creates a valid `submission.csv`.
4. Submit the completed kernel output to the competition:

   ```powershell
   kaggle competitions submit enveda-CASMI26-molecule-id-mass-spectra `
     -f submission.csv `
     -k <owner>/<kernel-name> `
     -v <kernel-version> `
     -m "Short description of the tested candidate"
   ```

   Use the exact output filename, kernel ID, and version from the successful run. Do not submit a preview or partial fallback artifact as a complete prediction.
5. Verify the accepted submission and score:

   ```powershell
   kaggle competitions submissions enveda-CASMI26-molecule-id-mass-spectra
   ```

   Save the submission reference and public score in the project history. Check the current daily quota before planning another attempt.

## Git and project workflow

- Keep large model files, generated outputs, caches, and scratch artifacts out of Git; follow the repository `.gitignore`.
- After a Kaggle submission, provide Git commands for the user to inspect and run. Do not run Git/GitHub commands unless explicitly requested.
- Do not add a Copilot co-author trailer to suggested commit commands.
- Treat the official competition page as authoritative if these notes or old version READMEs differ from current rules.

## Current project status

See [the project README](./README.md) for version lineage and score history. The best score recorded there is 0.465; submissions and reruns that are pending must not be presented as scored results. Update this section after checking current Kaggle status.
