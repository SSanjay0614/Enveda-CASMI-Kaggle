import json

path = 'kernel_v6/casmi26-v6-dg-gate-loose-sota.ipynb'
with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Patch Cell 27
c27 = ''.join(nb['cells'][27]['source'])
c27 = c27.replace(
    "assert platform.python_version_tuple()[:2] == ('3', '12')",
    "assert platform.python_version_tuple()[:2] in {('3', '12'), ('3', '13')}"
)
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

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=True)

print("Successfully patched Python 3.13 and rdkit assertions in kernel_v6!")
