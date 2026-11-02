import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "kernel_v21"
SOURCE_NOTEBOOK = SOURCE_DIR / "casmi26-v21-dual-472-consensus.ipynb"
CONFIGS = [
    (27, "wmid065", 0.25, 0.65, 0),
    (28, "wmid060", 0.25, 0.60, 0),
    (29, "wmid080", 0.25, 0.80, 0),
    (30, "wtop000-wmid075", 0.00, 0.75, 0),
]


def source_text(cell):
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def main():
    base = json.loads(SOURCE_NOTEBOOK.read_text(encoding="utf-8"))
    for version, slug, w_top, w_mid, rescue in CONFIGS:
        notebook = json.loads(json.dumps(base))
        title = f"CASMI26 V{version} {slug}"
        kernel_id = f"sanjay0614/casmi26-v{version}-{slug}"
        settings = notebook["cells"][1]
        text = source_text(settings)
        old = "CUSTOM = dict(w_top=0.25, w_mid=0.75, rescue=0)"
        new = f"CUSTOM = dict(w_top={w_top:.2f}, w_mid={w_mid:.2f}, rescue={rescue})"
        if text.count(old) != 1:
            raise ValueError(f"V{version}: expected one V21 consensus setting")
        settings["source"] = text.replace(old, new).splitlines(keepends=True)

        for cell in notebook["cells"]:
            if cell.get("cell_type") != "markdown":
                continue
            content = source_text(cell).replace(
                "LB 0.477 · Two 0.472 Fixes, Merged the Right Way",
                title,
            )
            cell["source"] = content.splitlines(keepends=True)
        kaggle = notebook.setdefault("metadata", {}).setdefault("kaggle", {})
        code_file = f"casmi26-v{version}-{slug}.ipynb"
        kaggle.update({"id": kernel_id, "title": title, "code_file": code_file})

        output_dir = ROOT / f"kernel_v{version}"
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / code_file).write_text(
            json.dumps(notebook, ensure_ascii=True, indent=1) + "\n", encoding="utf-8"
        )
        metadata = json.loads((SOURCE_DIR / "kernel-metadata.json").read_text(encoding="utf-8"))
        metadata.update({"id": kernel_id, "title": title, "code_file": code_file})
        (output_dir / "kernel-metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )
        (output_dir / "README.md").write_text(
            f"# CASMI26 V{version}: {slug}\n\n"
            "Parent: V21, score 0.477 (`57829820`); fragment-gated rank-1 rule retained.\n"
            f"Consensus settings: `w_top={w_top:.2f}`, `w_mid={w_mid:.2f}`, `rescue={rescue}`.\n"
            "This is a controlled inference-policy probe, not a validated improvement. "
            "Fast commit copies the sample output; scoring mode must execute the full pipeline.\n"
            "Score: pending.\n",
            encoding="utf-8",
        )
        print(f"Built V{version}: {kernel_id}")


if __name__ == "__main__":
    main()
