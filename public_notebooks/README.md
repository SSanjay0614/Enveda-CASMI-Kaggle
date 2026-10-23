# Public Research Archives & Community Lineage

* **Directory:** `public_notebooks/`

This directory contains the decompiled reference solutions, genealogical analyses, and reverse-engineered architectures that informed our competitive strategy for the Enveda CASMI 2026 challenge.

---

## 📚 Archive Structure

### 1. `chain/` (*CASMI 26: The Public Chain, Version by Version* by Dariush Afshar)
* A comprehensive genealogical study auditing all 170+ public versions submitted in the competition.
* Quantifies what every individual code change was mathematically worth on the public test set (e.g., one molecule at Rank 1 = $+0.0076$).
* Identified the two distinct high-scoring branches:
  * **Lineage A:** Dmitrii Gluzdov (v55 / Data Behind) $\longrightarrow$ **0.464**
  * **Lineage B:** Flexonafft (Closing the Evidence Gap) $\longrightarrow$ **0.462**

### 2. `data_behind/` (*CASMI 26: The Data Behind Spectra to Structures* by Dmitrii Gluzdov)
* The reference implementation for Lineage A (0.464).
* Introduces fold-safe FPNet checkpoints and the LOTUS / NPAtlas Natural Product Knowledge Table.

### 3. `evidence_gap/` (*CASMI 26: Closing the Evidence Gap* by Flexonafft)
* The reference implementation for Lineage B (0.462).
* Introduces the N1 Challenger joint MS/MS forward simulation and PubChemLite CC0 candidate fingerprints.

### 4. `lb_top1/` (*CASMI 26: LB TOP 1* by Lavin Wins)
* The early baseline used as our initial exploration point (evaluates to 0.423 due to disabled forward simulation flags).

### 5. `tutorial/` (*CASMI De Novo Tutorial Notebook* by Kaggle GM Inversion)
* The official starter notebook defining the competition data schema, Morgan radius 2 fingerprint generator, and submission contracts.
