# Version 4.0: Lineage B N1 Challenger Architecture

* **Directory:** `kernel_v4/`
* **Kaggle Kernel Slug:** `sanjay0614/casmi26-n1-challenger-v4`
* **Target Benchmark:** **`0.462`**
* **Status:** Submitted & Queued for Evaluation ⏳

---

## 🎯 Goal & Overview
Version 4.0 captures the competing high-performance branch of the CASMI public chain: **Lineage B (Flexonafft's *"Closing the Evidence Gap"*)**. 

While Lineage A relies on deep botanical reference databases, Lineage B specializes in **in-silico physics simulation** and expanded chemical fingerprint analog propagation.

---

## 🔬 Core Innovations in Lineage B

### 1. The N1 Challenger Joint MS/MS Simulator
* Unlike the early baseline where forward simulation was restricted to isolated $[M+H]^+$ ions, the N1 Challenger runs **joint ICEBERG and proxy GLACIER simulation** simultaneously.
* It eliminates the strict complement filter, allowing synthetic MS/MS fragments from both neural simulators to jointly re-order constitutional isomers sharing identical molecular formulas.

### 2. PubChemLite CC0 Fingerprint Search
* Integrates `franciscoangulo/casmi26-pubchemlite-cc0-candidate-fingerprints`, searching a specialized 360,000+ bio-relevant candidate collection in Engine 2.
* Expands the structural analog neighborhood beyond the training set, capturing rare or novel scaffolds.

### 3. E2R2 Metric-Exact Rank-2 Insertion
* Evaluates the leading proposal from the analog propagation engine (Engine 2).
* When Engine 2 shows high structural margin, its leading candidate is moved directly to **Rank 2** (unless it already holds Rank 1), maximizing the metric discount factor for high-confidence analogs.
