import json

with open('kernel_v7/casmi26-v7-candidate-aware-0465.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Patch Cell 43 to use loose thresholds with candidate-aware verification
c43 = ''.join(nb['cells'][43]['source'])
c43 = c43.replace(
    'S_TAU, POP_TAU = 6.0, 5.0',
    'S_TAU, POP_TAU = 5.0, 4.0'
)
nb['cells'][43]['source'] = [line + '\n' for line in c43.split('\n')]

out_nb_path = 'kernel_v8/casmi26-v8-candidate-aware-loose.ipynb'
with open(out_nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=True)

print("Saved kernel_v8 notebook to", out_nb_path)

meta = {
  "id": "sanjay0614/casmi26-v8-candidate-aware-loose-sota",
  "title": "CASMI26 V8 Candidate Aware Loose SOTA",
  "code_file": "casmi26-v8-candidate-aware-loose.ipynb",
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

with open('kernel_v8/kernel-metadata.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2, ensure_ascii=True)

print("Saved kernel_v8 metadata to kernel_v8/kernel-metadata.json")
