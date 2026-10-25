# Version 8 (V8) — Candidate-Aware Loose Promotion SOTA (Synthesis of Sanpier + Guhongbin)

## 1. Hypothesis & Architectural Motivation
- **Sanpier (0.465 LB):** Introduced candidate-specific evidence checks ($S_{\text{candidate}} > 6.0, \text{pop}_{\text{candidate}} \ge 5.0$) rather than window-wide maximums, eliminating false promotions of weak candidates. However, it kept conservative thresholds ($6.0 / 5.0$).
- **Guhongbin (`dg-gate-loose`):** Showed that relaxing thresholds to $S_{\tau}=5.0, \text{pop}_{\tau}=4.0$ expands recall for moderately documented natural products that were previously blocked by conservative gates.
- **The V8 Synthesis:** V8 applies **candidate-specific evidence validation** using the **relaxed thresholds (`5.0 / 4.0`)**. This grants Rank 1 promotion only to candidates whose individual evidence confirms their quality, while capturing genuine botanical structures that conservative thresholds missed.

## 2. Mathematical Definition
```python
def candidate_promotion_evidence(p):
    key = p['pc_keys'][0]
    evidence = p.get('promotion_evidence', {}).get(key)
    return float(evidence['S']), float(evidence['pop']), float(evidence['raw_fz'])

S, pop_top, candidate_rel = candidate_promotion_evidence(p)
new_promote = bool((S > 5.0 and pop_top >= 4.0) or candidate_rel > 150.0)
```

## 3. Kaggle Configuration
- **Kernel ID:** `sanjay0614/casmi26-v8-candidate-aware-loose-sota`
- **Accelerator:** GPU (NVIDIA T4)
- **Internet:** Off
- **Competition:** `enveda-CASMI26-molecule-id-mass-spectra`
