import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "kernel_v21"
OUTPUT_DIR = ROOT / "kernel_v26"
SOURCE_NOTEBOOK = SOURCE_DIR / "casmi26-v21-dual-472-consensus.ipynb"
NOTEBOOK_NAME = "casmi26-v26-consensus-wmid070.ipynb"
KERNEL_ID = "sanjay0614/casmi26-v26-consensus-wmid070"
TITLE = "CASMI26 V26 Consensus Wmid070"


def replace_once(source, old, new, description):
    if source.count(old) != 1:
        raise ValueError(f"Expected one {description}, found {source.count(old)}")
    return source.replace(old, new)


def main():
    notebook = json.loads(SOURCE_NOTEBOOK.read_text(encoding="utf-8"))
    settings = notebook["cells"][1]
    source = "".join(settings["source"]) if isinstance(settings["source"], list) else settings["source"]
    source = replace_once(
        source,
        "CUSTOM = dict(w_top=0.25, w_mid=0.75, rescue=0)",
        "CUSTOM = dict(w_top=0.25, w_mid=0.70, rescue=0)",
        "V21 consensus setting",
    )
    settings["source"] = source.splitlines(keepends=True)
    for cell in notebook["cells"]:
        if cell.get("cell_type") == "markdown":
            content = "".join(cell.get("source", [])) if isinstance(cell.get("source"), list) else cell.get("source", "")
            content = content.replace("CASMI26 V21 Dual-472 Consensus Merge", TITLE)
            content = content.replace("w_mid=0.75", "w_mid=0.70")
            cell["source"] = content.splitlines(keepends=True)

    notebook.setdefault("metadata", {}).setdefault("kaggle", {})
    notebook["metadata"]["kaggle"].update(
        {"id": KERNEL_ID, "title": TITLE, "code_file": NOTEBOOK_NAME}
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / NOTEBOOK_NAME).write_text(
        json.dumps(notebook, ensure_ascii=True, indent=1) + "\n", encoding="utf-8"
    )
    metadata = json.loads((SOURCE_DIR / "kernel-metadata.json").read_text(encoding="utf-8"))
    metadata.update({"id": KERNEL_ID, "title": TITLE, "code_file": NOTEBOOK_NAME})
    (OUTPUT_DIR / "kernel-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Built {NOTEBOOK_NAME}: w_top=0.25, w_mid=0.70, rescue=0")


if __name__ == "__main__":
    main()
