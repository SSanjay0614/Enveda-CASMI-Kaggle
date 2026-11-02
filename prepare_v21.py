import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_NB = ROOT / "public_notebooks" / "busyaprime" / "lb-0-477-two-0-472-fixes-merged-the-right-way.ipynb"
DEST_DIR = ROOT / "kernel_v21"
DEST_DIR.mkdir(parents=True, exist_ok=True)
DEST_NB = DEST_DIR / "casmi26-v21-dual-472-consensus.ipynb"

nb = json.loads(SRC_NB.read_text(encoding="utf-8"))
cells = nb["cells"]

# Ensure Cell 1 has COMMIT_MODE = 'fast'
c1_src = cells[1]["source"] if isinstance(cells[1]["source"], str) else "".join(cells[1]["source"])
assert "COMMIT_MODE = 'smoke'" in c1_src or "COMMIT_MODE = 'fast'" in c1_src
c1_src = c1_src.replace("COMMIT_MODE = 'smoke'", "COMMIT_MODE = 'fast'")
cells[1]["source"] = [l + "\n" for l in c1_src.split("\n")]

# Patch Cell 11 to not raise SystemExit
c11_src = cells[11]["source"] if isinstance(cells[11]["source"], str) else "".join(cells[11]["source"])
old_c11 = """BUNDLE = materialise_sources()
PIPELINE_DONE = run_public_pipeline()
if not PIPELINE_DONE and not IS_RERUN and COMMIT_MODE == 'fast':
    shutil.copyfile(COMP / 'sample_submission.csv', ROOT / 'submission.csv')
    raise SystemExit('fast commit: sample file written, the scoring rerun runs every stage')"""

new_c11 = """BUNDLE = materialise_sources()
PIPELINE_DONE = run_public_pipeline()
if not PIPELINE_DONE and not IS_RERUN and COMMIT_MODE == 'fast':
    shutil.copyfile(COMP / 'sample_submission.csv', ROOT / 'submission.csv')
    print('fast commit: sample file written, the scoring rerun runs every stage')
else:"""

assert old_c11 in c11_src, "Could not find expected block in Cell 11"
c11_patched = c11_src.replace(old_c11, new_c11)
# Indent the remainder of cell 11 under the else block
c11_lines = c11_patched.split("\n")
idx = c11_lines.index("else:")
c11_lines = c11_lines[:idx+1] + ["    " + line if line.strip() else "" for line in c11_lines[idx+1:]]
cells[11]["source"] = [l + "\n" for l in c11_lines]

# Wrap cells 12, 14, 15, 17 under if RUN_PIPELINE:
for c_idx in [12, 14, 15, 17]:
    orig = cells[c_idx]["source"] if isinstance(cells[c_idx]["source"], str) else "".join(cells[c_idx]["source"])
    indented = ["    " + line if line.strip() else "" for line in orig.split("\n")]
    wrapped = ["if RUN_PIPELINE:\n"] + [l + "\n" for l in indented]
    cells[c_idx]["source"] = wrapped

# Clean outputs
for i, cell in enumerate(cells):
    cell.setdefault("id", f"cell-{i}")
    if cell["cell_type"] == "code":
        cell["outputs"] = []
        cell["execution_count"] = None

# Metadata
KERNEL_ID = "sanjay0614/casmi26-v21-dual-472-consensus"
TITLE = "CASMI26 V21 Dual-472 Consensus Merge"

nb.setdefault("metadata", {})["kaggle"] = {
    "id": KERNEL_ID,
    "title": TITLE,
    "code_file": DEST_NB.name,
    "language": "python",
    "sourceType": "notebook",
    "isGpuEnabled": True,
    "isInternetEnabled": False,
    "accelerator": "NvidiaTeslaT4"
}

DEST_NB.write_text(json.dumps(nb, ensure_ascii=True, indent=1) + "\n", encoding="utf-8")

meta = {
    "id": KERNEL_ID,
    "title": TITLE,
    "code_file": DEST_NB.name,
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True,
    "enable_gpu": True,
    "enable_tpu": False,
    "enable_internet": False,
    "keywords": ["gpu"],
    "dataset_sources": [
        "sanpier/casmi-spectrum-model-v1",
        "dmitriigluzdov/casmi26-fold-safe-fpnet",
        "dmitriigluzdov/casmi26-natural-product-knowledge-table",
        "dmitriigluzdov/casmi26-natural-product-panel-benchmark",
        "dmitriigluzdov/casmi26-pubchem-popularity-prior",
        "dmitriigluzdov/casmi26-attributed-v4g-reproduction-assets",
        "sanpier/catalogue-experiment-saner"
    ],
    "kernel_sources": [],
    "competition_sources": [
        "enveda-CASMI26-molecule-id-mass-spectra"
    ],
    "model_sources": [],
    "machine_shape": "NvidiaTeslaT4"
}
(DEST_DIR / "kernel-metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
print(f"Built {DEST_NB} successfully with COMMIT_MODE='fast'!")
