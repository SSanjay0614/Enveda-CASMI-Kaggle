"""Search the long embedded code strings in c33/c35/c42 for CPU/GPU handling."""

import re
import sys
from pathlib import Path

CELLS = Path(
    r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\panel_lab\cells"
)

PATTERNS = ("cuda", "device", "is_available", "cpu")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for name in ("c33", "c35", "c42"):
        text = (CELLS / f"{name}.py").read_text(encoding="utf-8", errors="replace")
        # unescape the embedded "\n" inside string literals so lines are readable
        flat = text.replace("\\n", "\n")
        lines = flat.splitlines()
        print("=" * 20, name, len(text), "chars", len(lines), "lines after unescape")
        hits = 0
        for index, line in enumerate(lines, 1):
            stripped = line.strip()
            if "cuda" in stripped or "is_available" in stripped:
                print(f"  {index:5d}: {stripped[:150]}")
                hits += 1
                if hits > 40:
                    print("  ... truncated")
                    break
        print()


if __name__ == "__main__":
    main()
