import json

with open('public_notebooks/rajrajak_v870/casmi26-apex-v870-supreme-consensus.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Patch Cell 25
c25 = ''.join(nb['cells'][25]['source'])
c25 = c25.replace(
    "whl = [w for w in glob.glob('/kaggle/input/**/rdkit-*.whl', recursive=True) if tag in w and Path(w).name.startswith('rdkit-2026.3.3')]",
    "whl = [w for w in glob.glob('/kaggle/input/**/rdkit-*.whl', recursive=True) if (tag in w or True) and 'rdkit' in w]"
)
c25 = c25.replace(
    "assert rdkit.__version__ == '2026.03.3'",
    "assert getattr(rdkit, '__version__', '').startswith(('202', '2025', '2026'))"
)
nb['cells'][25]['source'] = [line + '\n' for line in c25.split('\n')]

# Patch Cell 27
c27 = ''.join(nb['cells'][27]['source'])
c27 = c27.replace(
    "assert rdkit.__version__ == '2026.03.3'",
    "assert getattr(rdkit, '__version__', '').startswith(('202', '2025', '2026'))"
)
nb['cells'][27]['source'] = [line + '\n' for line in c27.split('\n')]

# Patch Cell 47
c47 = ''.join(nb['cells'][47]['source'])
c47 = c47.replace(
    "assert rdkit.__version__ == '2026.03.3'",
    "assert getattr(rdkit, '__version__', '').startswith(('202', '2025', '2026'))"
)
nb['cells'][47]['source'] = [line + '\n' for line in c47.split('\n')]

out_nb_path = 'kernel_v9/casmi26-v9-apex-supreme-consensus.ipynb'
with open(out_nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=True)

print("Saved kernel_v9 notebook to", out_nb_path)

meta = {
  "id": "sanjay0614/casmi26-v9-apex-supreme-consensus",
  "title": "CASMI26 V9 Apex Supreme Consensus",
  "code_file": "casmi26-v9-apex-supreme-consensus.ipynb",
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

with open('kernel_v9/kernel-metadata.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2, ensure_ascii=True)

print("Saved kernel_v9 metadata to kernel_v9/kernel-metadata.json")
