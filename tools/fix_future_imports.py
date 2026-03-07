import argparse
from pathlib import Path

SKIP = ("venv", ".venv", ".tox", "site-packages")
FUTURE_LINE = "from __future__ import annotations"

def should_skip(p: Path) -> bool:
    return any(part in SKIP for part in p.parts)

def fix_file(path: Path, mode: str) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Find future import lines
    idxs = [i for i, ln in enumerate(lines) if ln.strip() == FUTURE_LINE]
    if not idxs:
        return False

    if mode == "remove":
        for i in reversed(idxs):
            del lines[i]
        path.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
        return True

    if mode == "move":
        had_future = False
        for i in reversed(idxs):
            had_future = True
            del lines[i]
        if not had_future:
            return False

        # Find insertion point: after module docstring if present
        insert_at = 0
        # Skip shebang/encoding
        while insert_at < len(lines) and (
            lines[insert_at].startswith("#!") or lines[insert_at].startswith("# -*- coding:")
        ):
            insert_at += 1
        # Module docstring?
        if insert_at < len(lines) and lines[insert_at].lstrip().startswith(('"""', "'''")):
            quote = lines[insert_at].lstrip()[:3]
            j = insert_at
            if lines[j].count(quote) >= 2:
                insert_at = j + 1
            else:
                j += 1
                while j < len(lines):
                    if quote in lines[j]:
                        insert_at = j + 1
                        break
                    j += 1
        needs_blank = insert_at < len(lines) and lines[insert_at].strip() != ""
        lines.insert(insert_at, "from __future__ import annotations")
        if needs_blank:
            lines.insert(insert_at + 1, "")
        path.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
        return True

    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["remove", "move"], default="remove",
                    help="remove (Py3.11+) or move future import below module docstring")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default=".", help="project root")
    args = ap.parse_args()

    changed = 0
    for p in Path(args.root).rglob("*.py"):
        if should_skip(p):
            continue
        if args.dry_run:
            before = p.read_text(encoding="utf-8")
            if "from __future__ import annotations" in before and fix_file(p, args.mode):
                # revert (simulate)
                p.write_text(before, encoding="utf-8")
                print(f"[DRY] would fix: {p}")
                changed += 1
        else:
            if fix_file(p, args.mode):
                print(f"fixed: {p}")
                changed += 1
    print(f"\n{changed} file(s) {'would be ' if args.dry_run else ''}fixed.")

if __name__ == "__main__":
    main()
