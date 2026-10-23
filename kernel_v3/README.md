# Version 3.0: Lineage A Data-Behind SOTA Architecture

* **Directory:** `kernel_v3/`
* **Kaggle Kernel Slug:** `sanjay0614/casmi26-sota-v3-databehind`
* **Target Benchmark:** **`0.464`** (Public Frontier)
* **Status:** Submitted & Actively Scoring on Hidden Test Set ⏳

---

## 🎯 Goal & Overview
Version 3.0 adopted the verified, top-tier public frontier architecture developed by Dmitrii Gluzdov (*"CASMI 26: The Data Behind Spectra to Structures"*). This represents the highest verified single-model benchmark published in the competition history (`0.464`).

---

## 🔬 Core Innovations in Lineage A

### 1. Fold-Safe FPNet Embeddings
* Utilizes cross-validation fold-safe FPNet checkpoints (`dmitriigluzdov/casmi26-fold-safe-fpnet`) that completely eliminate data leakage between training spectral representations and validation molecular structures.

### 2. Natural Product Knowledge Table
* Ingests the unified **LOTUS** (250,000+ natural products) and **NPAtlas** (30,000+ microbial metabolites) reference databases (`dmitriigluzdov/casmi26-natural-product-knowledge-table`).
* Incorporates depositor-source bonuses (+0.5) and natural-product bonuses (+1.0) to heavily prioritize authentic natural products.

### 3. N1A Adduct Fallback System
* Reconstructs synthetic `[M+H]+` proxy spectra for molecules detected only in negative mode (`[M-H]-`) or with sodium adducts (`[M+Na]+`), enabling forward simulation across all ion modes.

### 4. Critical Engineering Fix: Kaggle Python 3.13 Adaptation
* Kaggle upgraded its cloud runtime from Python 3.12 to Python 3.13. 
* The original notebook contained a rigid pre-flight assertion `assert platform.python_version_tuple()[:2] == ('3', '12')` that crashed under the new environment.
* We patched the assertion via [prepare_v3.py](file:///c:/Users/ssanj/OneDrive/Desktop/Sanjay/Antigravity/enveda_casmi/prepare_v3.py) to ensure universal Python 3.x compatibility while preserving all RDKit `2026.03.3` bindings.
