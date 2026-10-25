import json

# Start from Kernel V9 (which has LOTUS_W = 1.0 and Library Shield)
with open('kernel_v9/casmi26-v9-apex-supreme-consensus.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Also load Kernel V7's Cell 43 to get candidate_promotion_evidence logic
with open('kernel_v7/casmi26-v7-candidate-aware-0465.ipynb', 'r', encoding='utf-8') as f:
    v7_nb = json.load(f)

c43_v7 = ''.join(v7_nb['cells'][43]['source'])

# In V9 Cell 42 (the merge/promotion gate), we replace the promotion loop with candidate-aware loose promotion
# First let's inspect V9 Cell 42
c42_v9 = ''.join(nb['cells'][42]['source'])

# Inject candidate_promotion_evidence function definition if not present
candidate_fn = '''
def candidate_promotion_evidence(p):
    key = p['pc_keys'][0]
    evidence = p.get('promotion_evidence', {}).get(key)
    if evidence is None:
        return float(p.get('S') or 0.0), float(p.get('top_pop') or 0.0), float(p.get('fz_top') or 0.0)
    S, pop, raw = (float(evidence.get(x, 0.0)) for x in ('S', 'pop', 'raw_fz'))
    return S, pop, raw
'''

# Update Cell 42 in V9
c42_new = c42_v9.replace(
    "print('merge/promote self-test OK')",
    "print('merge/promote self-test OK')\n" + candidate_fn
)

# Update the promotion condition to use candidate-specific evidence with the relaxed criteria
old_cond = "if (S is not None and float(S) > 5.0 and pop_top >= 4.0) or (rel > 150.0) or (rel > 125.0 and pop_top >= 3.0):"
new_cond = """        cand_S, cand_pop, cand_raw = candidate_promotion_evidence(p)
        if (cand_S > 5.0 and cand_pop >= 4.0) or (rel > 150.0) or (rel > 125.0 and cand_pop >= 3.0):"""

c42_new = c42_new.replace(old_cond, new_cond)
nb['cells'][42]['source'] = [line + '\n' for line in c42_new.split('\n')]

out_nb_path = 'kernel_v10/casmi26-v10-unified-frontier-master.ipynb'
with open(out_nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=True)

print("Saved kernel_v10 notebook to", out_nb_path)

meta = {
  "id": "sanjay0614/casmi26-v10-unified-frontier-master",
  "title": "CASMI26 V10 Unified Frontier Master",
  "code_file": "casmi26-v10-unified-frontier-master.ipynb",
  "language": "python",
  "kernel_type": "notebook",
  "is_private": True,
  "enable_gpu": True,
  "enable_tpu": False,
  "enable_internet": False,
  "dataset_sources": [
    "dmitriigluzdov/casmi26-fold-safe-fpnet",
    "dmitriigluzdov/casmi26-natural-product-knowledge-table",
    "dmitriigluzdov/casmi26-natural-product-panel-benchmark",
    "dmitriigluzdov/casmi26-pubchem-popularity-prior",
    "dmitriigluzdov/casmi26-attributed-v4g-reproduction-assets"
  ],
  "competition_sources": [
    "enveda-CASMI26-molecule-id-mass-spectra"
  ]
}

with open('kernel_v10/kernel-metadata.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2, ensure_ascii=True)

print("Saved kernel_v10 metadata to kernel_v10/kernel-metadata.json")
