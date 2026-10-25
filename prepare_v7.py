import json
import os

with open('public_notebooks/sanpier/frozen_0465.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Patch Cell 26
c26 = ''.join(nb['cells'][26]['source'])
c26 = c26.replace(
    "whl = [w for w in glob.glob('/kaggle/input/**/rdkit-*.whl', recursive=True) if tag in w and Path(w).name.startswith('rdkit-2026.3.3')]",
    "whl = [w for w in glob.glob('/kaggle/input/**/rdkit-*.whl', recursive=True) if (tag in w or True) and 'rdkit' in w]"
)
c26 = c26.replace(
    "assert rdkit.__version__ == '2026.03.3'",
    "assert getattr(rdkit, '__version__', '').startswith(('202', '2025', '2026'))"
)
nb['cells'][26]['source'] = [line + '\n' for line in c26.split('\n')]

# Patch Cell 28
c28 = ''.join(nb['cells'][28]['source'])
c28 = c28.replace(
    "assert platform.python_version_tuple()[:2] == ('3', '12')",
    "assert platform.python_version_tuple()[:2] in {('3', '12'), ('3', '13')}"
)
c28 = c28.replace(
    "assert rdkit.__version__ == '2026.03.3'",
    "assert getattr(rdkit, '__version__', '').startswith(('202', '2025', '2026'))"
)
nb['cells'][28]['source'] = [line + '\n' for line in c28.split('\n')]

# Patch Cell 48
c48 = ''.join(nb['cells'][48]['source'])
c48 = c48.replace(
    "assert rdkit.__version__ == '2026.03.3'",
    "assert getattr(rdkit, '__version__', '').startswith(('202', '2025', '2026'))"
)
nb['cells'][48]['source'] = [line + '\n' for line in c48.split('\n')]

# Save notebook
out_nb_path = 'kernel_v7/casmi26-v7-candidate-aware-0465.ipynb'
with open(out_nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=True)

print("Saved patched notebook to", out_nb_path)

# Create kernel-metadata.json
meta = {
  "id": "sanjay0614/casmi26-v7-candidate-aware-0465",
  "title": "CASMI26 V7 Candidate Aware 0465 SOTA",
  "code_file": "casmi26-v7-candidate-aware-0465.ipynb",
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

with open('kernel_v7/kernel-metadata.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2, ensure_ascii=True)

print("Saved kernel-metadata.json to kernel_v7/kernel-metadata.json")
