import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_NOTEBOOK = ROOT / "kernel_v7" / "casmi26-v7-candidate-aware-0465.ipynb"

EXPERIMENTS = (
    {
        "version": 13,
        "folder": "kernel_v13",
        "slug": "casmi26-v13-evidence-early-slots",
        "title": "CASMI26 V13 Evidence Early Slots",
        "s_tau": 6.0,
        "pop_tau": 5.0,
        "panel_results": (
            "On the 250-molecule answer-removed-from-reference panel, the matching "
            "published early-slot replay gained +0.1994 MRR@25 (paired 95% bootstrap "
            "CI +0.1649 to +0.2341); reference-library delta was 0.0000 and "
            "no-reference-spectrum delta was -0.0020 (CI -0.0060 to 0.0000)."
        ),
        "description": (
            "V7 promotion gate (S > 6 and popularity >= 5), with earlier "
            "interleaving slots when candidate-specific S > 5."
        ),
    },
    {
        "version": 14,
        "folder": "kernel_v14",
        "slug": "casmi26-v14-stronger-pubchem-rescue",
        "title": "CASMI26 V14 Stronger PubChem Rescue",
        "s_tau": 5.5,
        "pop_tau": 8.0,
        "panel_results": (
            "On the 250-molecule answer-removed-from-reference panel, the matching "
            "published replay gained +0.2432 MRR@25 (paired 95% bootstrap CI +0.2023 "
            "to +0.2839); reference-library and no-reference-spectrum deltas were "
            "each -0.0040 (paired 95% bootstrap CI -0.0100 to 0.0000)."
        ),
        "description": (
            "Promotion gate (S > 5.5 and popularity >= 8), with earlier "
            "interleaving slots when candidate-specific S > 5."
        ),
    },
)

OLD_THRESHOLDS = "S_TAU, POP_TAU = 6.0, 5.0"
OLD_SLOT_AND_PROMOTION = """        slots = SLOTS_AGG if rel > REL_TH else SLOTS_GENTLE
        stats['aggressive' if rel > REL_TH else 'gentle'] += 1
        old_S = p.get('S'); old_pop = float(p.get('top_pop') or 0.0)
        old_promote = bool((old_S is not None and float(old_S) > S_TAU and old_pop >= POP_TAU) or rel > 150.0)
        S, pop_top, candidate_rel = candidate_promotion_evidence(p)
        new_promote = bool((S > S_TAU and pop_top >= POP_TAU) or candidate_rel > 150.0)"""
NEW_SLOT_AND_PROMOTION = """        S, pop_top, candidate_rel = candidate_promotion_evidence(p)
        slots = SLOTS_AGG if (S > EARLY_SLOT_S or rel > REL_TH) else SLOTS_GENTLE
        stats['aggressive' if slots == SLOTS_AGG else 'gentle'] += 1
        old_S = p.get('S'); old_pop = float(p.get('top_pop') or 0.0)
        old_promote = bool((old_S is not None and float(old_S) > S_TAU and old_pop >= POP_TAU) or rel > 150.0)
        new_promote = candidate_promotes(S, pop_top, candidate_rel)"""
FINAL_SLOT_AND_PROMOTION = NEW_SLOT_AND_PROMOTION.replace(
    "slots = SLOTS_AGG if (S > EARLY_SLOT_S or rel > REL_TH) else SLOTS_GENTLE",
    "slots = candidate_slots(S, rel)",
)


def cell_text(cell):
    source = cell.get("source", [])
    return source if isinstance(source, str) else "".join(source)


def set_cell_text(cell, text):
    source = cell.get("source", [])
    cell["source"] = text if isinstance(source, str) else text.splitlines(keepends=True)
    if cell.get("cell_type") == "code":
        cell["outputs"] = []
        cell["execution_count"] = None


def build_one(experiment):
    output_dir = ROOT / experiment["folder"]
    output_dir.mkdir(parents=True, exist_ok=True)
    notebook = json.loads(SOURCE_NOTEBOOK.read_text(encoding="utf-8"))
    cell = notebook["cells"][43]
    source = cell_text(cell)

    if source.count(OLD_THRESHOLDS) != 1:
        raise RuntimeError("Could not uniquely locate V7 promotion thresholds")
    if source.count(OLD_SLOT_AND_PROMOTION) != 1:
        raise RuntimeError("Could not uniquely locate V7 slot/promotion logic")

    source = source.replace(
        OLD_THRESHOLDS,
        f"S_TAU, POP_TAU = {experiment['s_tau']}, {experiment['pop_tau']}\n"
        "EARLY_SLOT_S = 5.0",
        1,
    )
    source = source.replace(
        "def promote(base, base_keys, pc, pc_keys, slots, n=25):",
        """def candidate_promotes(S, pop, candidate_rel):
    return bool((S > S_TAU and pop >= POP_TAU) or candidate_rel > 150.0)


def candidate_slots(S, rel):
    return SLOTS_AGG if (S > EARLY_SLOT_S or rel > REL_TH) else SLOTS_GENTLE


assert candidate_promotes(S_TAU + 0.01, POP_TAU, 0.0)
assert not candidate_promotes(S_TAU, POP_TAU, 0.0)
assert candidate_promotes(0.0, 0.0, 150.01)
assert candidate_slots(EARLY_SLOT_S + 0.01, 0.0) == SLOTS_AGG
assert candidate_slots(EARLY_SLOT_S, 0.0) == SLOTS_GENTLE


def promote(base, base_keys, pc, pc_keys, slots, n=25):""",
        1,
    )
    source = source.replace(
        OLD_SLOT_AND_PROMOTION,
        FINAL_SLOT_AND_PROMOTION,
        1,
    )
    if source.count(FINAL_SLOT_AND_PROMOTION) != 1:
        raise RuntimeError("Failed to apply the controlled V13/V14 ranking policy")
    set_cell_text(cell, source)

    note = (
        f"# Version {experiment['version']} — {experiment['title']}\n\n"
        f"{experiment['description']}\n\n"
        "This is a one-policy-change branch from the scored V7 pipeline. Candidate generation, "
        "ranker weights, simulator behavior, library shield, final fusion, and output format "
        "remain unchanged. It uses the candidate-specific PubChem evidence already computed "
        "by V7 for both the promotion rule and the early-slot decision.\n\n"
        f"The public identity-disjoint natural-product panel replay measured this policy on a "
        f"250-molecule panel. {experiment['panel_results']} This curated natural-product panel is not a representative "
        "hidden-test sample or a full V7 rerun. Treat these results as motivation, not a "
        "leaderboard-score prediction. The notebook must complete a GPU smoke run, then a "
        "full competition submission is appropriate only if resource budget allows.\n"
    )
    notebook["cells"].insert(
        0,
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": note.splitlines(keepends=True),
        },
    )
    notebook_path = output_dir / f"casmi26-v{experiment['version']}-{experiment['slug'].split('-', 2)[-1]}.ipynb"
    notebook_path.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )

    metadata = json.loads((ROOT / "kernel_v7" / "kernel-metadata.json").read_text(encoding="utf-8"))
    metadata["id"] = f"sanjay0614/{experiment['slug']}"
    metadata["title"] = experiment["title"]
    metadata["code_file"] = notebook_path.name
    (output_dir / "kernel-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "README.md").write_text(note, encoding="utf-8")
    return notebook_path


def main():
    for experiment in EXPERIMENTS:
        print(f"Wrote {build_one(experiment)}")


if __name__ == "__main__":
    main()
