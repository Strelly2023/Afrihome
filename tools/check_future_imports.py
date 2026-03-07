# tools/check_future_imports.py
from pathlib import Path

SKIP = ("venv", ".venv", ".tox", "site-packages")

def should_skip(p: Path) -> bool:
    return any(part in SKIP for part in p.parts)

def first_future_line(p: Path) -> int | None:
    try:
        with p.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                if "from __future__ import" in line:
                    return i
    except Exception:
        return None
    return None

def main():
    roots = Path(".").rglob("*.py")
    violations = []
    for py in roots:
        if should_skip(py):
            continue
        n = first_future_line(py)
        if n and n > 15:
            violations.append((py.as_posix(), n))
    for f, n in sorted(violations):
        print(f"{f}:{n}")
    if violations:
        print(f"\n{len(violations)} file(s) have 'from __future__ import' after line 15.")

if __name__ == "__main__":
    main()
