from __future__ import annotations
import re
from pathlib import Path

SKIP_DIRS = {"venv", ".venv", ".tox", "site-packages", ".git"}
EXTS = {".py"}  # limit to Python; extend if needed

# Patterns for high-confidence code contexts
PATTERNS = [
    # return annotation in function signatures
    (re.compile(r"\)\s*-\&gt;\s*"), ") -> "),
    # type hints around arrow (identifiers, [], |, , etc.)
    (re.compile(r"([^\S\r\n]|:)\s*-\&gt;\s*"), r"\1 -> "),
    # comparisons
    (re.compile(r"\s+\&lt;\s+"), " < "),
    (re.compile(r"\s+\&gt;\s+"), " > "),
]

# Optional: conservative quote entity fixes in code-ish contexts
# We will not touch lines that look like HTML (contain '<div', '<span', '</', '<!--', etc.)
HTMLY = re.compile(r"<(/|div|span|p|h[1-6]|!--)")

QUOTE_FIXES = [
    (re.compile(r'&quot;'), '"'),
    (re.compile(r'&#39;'), "'"),
]

def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)

def fix_line(line: str) -> str:
    original = line
    # skip obvious HTML/template lines
    if HTMLY.search(line):
        for pat, repl in PATTERNS:  # still allow arrow/comparison fixes
            line = pat.sub(repl, line)
        return line

    # apply code patterns
    for pat, repl in PATTERNS:
        line = pat.sub(repl, line)

    # optional: quote fixes (conservative)
    # limit to lines that already look like Python (def/class/annotation/dict keys)
    if re.search(r"\b(def|class)\b|:\s*dict\[|:\s*list\[|:\s*set\[|->|=\s*{|^\s*\w+\s*:", line):
        for pat, repl in QUOTE_FIXES:
            line = pat.sub(repl, line)

    return line

def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed = False
    new_lines = []
    for ln in lines:
        fixed = fix_line(ln)
        if fixed != ln:
            changed = True
        new_lines.append(fixed)
    if changed:
        path.write_text("\n".join(new_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return changed

def main():
    changed = 0
    for p in Path(".").rglob("*"):
        if p.is_dir() or should_skip(p) or p.suffix not in EXTS:
            continue
        try:
            if process_file(p):
                print(f"fixed: {p}")
                changed += 1
        except Exception as e:
            print(f"skip (error): {p} -> {e}")
    print(f"\n{changed} file(s) fixed.")

if __name__ == "__main__":
    main()
