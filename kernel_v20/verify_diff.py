"""Verify the V20 probe differs from V18 only in the intended places."""

import json
import sys
from pathlib import Path

BASE = Path(r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\kernel_v18\casmi26-v18-neural-rerank.ipynb")
NEW = Path(r"C:\Users\ssanj\OneDrive\Desktop\Sanjay\Antigravity\enveda_casmi\kernel_v20\casmi26-v20-cpu-probe.ipynb")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    base = [''.join(c['source']) for c in json.loads(BASE.read_text(encoding='utf-8'))['cells']]
    new = [''.join(c['source']) for c in json.loads(NEW.read_text(encoding='utf-8'))['cells']]
    print(f"cells: base {len(base)} new {len(new)}")
    for i in range(max(len(base), len(new))):
        a = base[i] if i < len(base) else '<missing>'
        b = new[i] if i < len(new) else '<missing>'
        if a != b:
            print(f"--- cell {i} differs (base {len(a)} new {len(b)} chars)")
            if i >= len(base):
                print(b[:600])
    print("\n== residual GPU gates in new notebook ==")
    for i, text in enumerate(new):
        for lineno, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if ('assert' in s and ('cuda' in s.lower() or 'T4' in s)) or 'device="cuda"' in s or "device='cuda'" in s:
                print(f"c{i}:{lineno}: {s[:140]}")


if __name__ == "__main__":
    main()
