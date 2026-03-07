#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AfriHome Hygiene & Architecture Linter

Features
--------
• Detects known hygiene violations
• Detects duplicate functions
• Detects literal bracket regex mistakes
• Detects HTML-escaped or backslash-escaped arrows
• Detects split-union artifacts (`\ None`)
• Detects circular imports
• Detects forbidden layer dependencies
• Provides weighted scoring out of 100 (capped)
• Optional auto-fix for safe patterns (arrow fixes)
• Deterministic and dependency-free

Usage
-----
python tools/afrihome_lint.py --root . --format text --fail-under 92
python tools/afrihome_lint.py --root . --format json --fix
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys
import ast
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple, Set

# -------------------------------------------------------------
# Types & Models
# -------------------------------------------------------------

Severity = str  # "ERROR" | "WARN"
RuleCheck = Callable[[str, str], List["Violation"]]
Fixer = Callable[[str], Tuple[str, int]]

@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    severity: Severity
    weight: int
    pattern: Optional[re.Pattern] = None
    check: Optional[RuleCheck] = None
    fixer: Optional[Fixer] = None

@dataclass(frozen=True)
class Violation:
    rule_id: str
    file: str
    line: int
    col: int
    excerpt: str

    def to_dict(self) -> Dict:
        return {
            "rule_id": self.rule_id,
            "file": self.file,
            "line": self.line,
            "col": self.col,
            "excerpt": self.excerpt,
        }

@dataclass
class FileReport:
    file: str
    violations: List[Violation] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {"file": self.file, "violations": [v.to_dict() for v in self.violations]}

@dataclass
class LintReport:
    files: List[FileReport]
    score: float
    total: int
    by_rule: Dict[str, int]

    def to_dict(self) -> Dict:
        return {
            "files": [f.to_dict() for f in self.files],
            "score": self.score,
            "total": self.total,
            "by_rule": dict(self.by_rule),
        }

# -------------------------------------------------------------
# Config: layers & exclusions
# -------------------------------------------------------------

LAYER_RULES: Dict[str, List[str]] = {
    "core": [],
    "control_plane": ["core"],
    "adapters": ["core", "control_plane"],
    "apps": ["core", "control_plane", "adapters"],
}

EXCLUDE_DIRS = {".git", ".pytest_cache", "__pycache__", "venv", ".venv"}

# -------------------------------------------------------------
# Helpers
# -------------------------------------------------------------

def iter_python_files(root: str, include_ext: Sequence[str] = (".py",)) -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if any(fn.endswith(ext) for ext in include_ext):
                yield os.path.join(dirpath, fn)

def safe_read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def safe_write(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def pos_to_linecol(text: str, pos: int) -> Tuple[int, int]:
    line = text.count("\n", 0, pos) + 1
    last_nl = text.rfind("\n", 0, pos)
    col = (pos - last_nl)
    return line, col

def snippet(text: str, start: int, maxlen: int = 80) -> str:
    return text[start:start + maxlen].replace("\n", " ")

def module_name_from_path(root: str, path: str) -> str:
    rel = os.path.relpath(path, root)
    rel_no_ext = os.path.splitext(rel)[0]
    # Convert path to dotted module, strip leading ./ or .\
    parts = []
    for p in rel_no_ext.split(os.sep):
        if p in ("",):
            continue
        parts.append(p)
    return ".".join(parts)

def find_layer_from_path(path: str) -> Optional[str]:
    parts = path.split(os.sep)
    for p in parts:
        if p in LAYER_RULES:
            return p
    return None

# -------------------------------------------------------------
# Fixers (safe)
# -------------------------------------------------------------

def fix_backslash_arrow(text: str) -> Tuple[str, int]:
    # Replace "-\>" with "->"
    return re.subn(r"-\\>", "->", text)

def fix_html_entity_arrow(text: str) -> Tuple[str, int]:
    # Replace "->" with "->"
    return re.subn(r"->", "->", text)

# -------------------------------------------------------------
# Checkers
# -------------------------------------------------------------

def regex_rule_checker(rule: Rule, text: str, path: str) -> List[Violation]:
    assert rule.pattern is not None
    out: List[Violation] = []
    for m in rule.pattern.finditer(text):
        ln, col = pos_to_linecol(text, m.start())
        out.append(Violation(rule.id, path, ln, col, snippet(text, m.start())))
    return out

def duplicate_function_checker(text: str, path: str) -> List[Violation]:
    out: List[Violation] = []
    try:
        tree = ast.parse(text, filename=path)
    except Exception:
        return out
    funcs: Dict[str, List[ast.FunctionDef]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs.setdefault(node.name, []).append(node)
    for name, defs in funcs.items():
        if len(defs) > 1:
            for d in defs[1:]:
                out.append(Violation("DUPLICATE_FUNC", path, d.lineno, d.col_offset + 1, f"duplicate def {name}"))
    return out

def check_literal_bracket_regex(text: str, path: str) -> List[Violation]:
    patterns = [
        re.compile(r"\\\[a-z\]"),
        re.compile(r"\\\[A-Za-z"),
        re.compile(r"\\\[-a-zA-Z0-9"),
    ]
    out: List[Violation] = []
    for pat in patterns:
        for m in pat.finditer(text):
            ln, col = pos_to_linecol(text, m.start())
            out.append(Violation("BAD_REGEX_BRACKETS", path, ln, col, snippet(text, m.start())))
    return out

def split_union_checker(text: str, path: str) -> List[Violation]:
    out: List[Violation] = []
    for m in re.finditer(r"\\\s*None\b", text):
        ln, col = pos_to_linecol(text, m.start())
        out.append(Violation("SPLIT_UNION", path, ln, col, snippet(text, m.start())))
    return out

def _collect_import_roots_from_ast(text: str) -> Set[str]:
    roots: Set[str] = set()
    try:
        tree = ast.parse(text)
    except Exception:
        return roots
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = (alias.name or "").split(".")[0]
                if root:
                    roots.add(root)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root = node.module.split(".")[0]
                if root:
                    roots.add(root)
    return roots

def layer_violation_checker(text: str, path: str) -> List[Violation]:
    out: List[Violation] = []
    layer = find_layer_from_path(path)
    if not layer:
        return out
    allowed = set(LAYER_RULES[layer]) | {layer}
    # Get import roots via AST
    roots = _collect_import_roots_from_ast(text)
    for root in roots:
        if root in LAYER_RULES and root not in allowed:
            # Find first occurrence for line/col
            m = re.search(rf"(?:from|import)\s+{re.escape(root)}\b", text)
            if m:
                ln, col = pos_to_linecol(text, m.start())
            else:
                ln, col = (1, 1)
            out.append(Violation("LAYER_VIOLATION", path, ln, col, f"{layer} importing {root}"))
    return out

# Circular imports: build per-module edges using AST and detect cycles
def build_import_graph(root: str, files: List[str]) -> Dict[str, Set[str]]:
    graph: Dict[str, Set[str]] = {}
    for path in files:
        text = safe_read(path)
        this_mod = module_name_from_path(root, path)
        deps: Set[str] = set()
        try:
            tree = ast.parse(text, filename=path)
        except Exception:
            graph[this_mod] = deps
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    mod = alias.name.split(".")[0]
                    deps.add(mod)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    mod = node.module.split(".")[0]
                    deps.add(mod)
        graph[this_mod] = deps
    return graph

def circular_imports(root: str, files: List[str]) -> List[Tuple[List[str], List[str]]]:
    """
    Returns a list of cycles: (modules_in_cycle, files_in_cycle)
    """
    graph = build_import_graph(root, files)
    # Map module -> file candidates (first match wins)
    mod_to_file: Dict[str, str] = {}
    for path in files:
        mod = module_name_from_path(root, path)
        mod_to_file[mod] = path

    visited: Set[str] = set()
    stack: Set[str] = set()
    cycles: List[List[str]] = []

    def dfs(u: str, trail: List[str]) -> None:
        if u in stack:
            # cycle found; cut trail from first occurrence
            if u in trail:
                i = trail.index(u)
                cycles.append(trail[i:] + [u])
            return
        if u in visited:
            return
        visited.add(u)
        stack.add(u)
        for v in graph.get(u, ()):
            if v in graph:  # only consider modules we control
                dfs(v, trail + [u])
        stack.remove(u)

    for mod in graph.keys():
        if mod not in visited:
            dfs(mod, [])

    out: List[Tuple[List[str], List[str]]] = []
    for cyc in cycles:
        unique_mods = []
        for m in cyc:
            if not unique_mods or unique_mods[-1] != m:
                unique_mods.append(m)
        # map to files
        cyc_files = [mod_to_file.get(m) for m in unique_mods if m in mod_to_file]
        out.append((unique_mods, [f for f in cyc_files if f]))
    return out

# -------------------------------------------------------------
# Ruleset
# -------------------------------------------------------------

RULES: List[Rule] = [
    # Arrows
    Rule(
        id="BACKSLASH_ARROW",
        description="Backslash-escaped return arrow '-\\>' should be '->'",
        severity="ERROR",
        weight=2,
        pattern=re.compile(r"-\\>"),
        fixer=fix_backslash_arrow,
    ),
    Rule(
        id="HTML_ENTITY_ARROW",
        description="HTML-escaped arrow '->' should be '->'",
        severity="ERROR",
        weight=2,
        pattern=re.compile(r"->"),
        fixer=fix_html_entity_arrow,
    ),
    # Regex literal bracket mistakes
    Rule(
        id="BAD_REGEX_BRACKETS",
        description="Regex contains literal bracket classes (e.g., '\\[a-z\\]')",
        severity="ERROR",
        weight=3,
        check=check_literal_bracket_regex,
    ),
    # Split union artifacts
    Rule(
        id="SPLIT_UNION",
        description="Split union artifact detected (e.g., '\\ None')",
        severity="ERROR",
        weight=2,
        check=split_union_checker,
    ),
    # Duplicate functions
    Rule(
        id="DUPLICATE_FUNC",
        description="Duplicate function name in the same file",
        severity="ERROR",
        weight=5,
        check=duplicate_function_checker,
    ),
    # Architecture layer violations
    Rule(
        id="LAYER_VIOLATION",
        description="Forbidden dependency across layers",
        severity="ERROR",
        weight=8,
        check=layer_violation_checker,
    ),
]

# -------------------------------------------------------------
# Scoring
# -------------------------------------------------------------

def compute_score(violations: List[Violation], ruleset: List[Rule]) -> Tuple[float, Dict[str, int]]:
    weights = {r.id: r.weight for r in ruleset}
    counts: Dict[str, int] = {}
    for v in violations:
        counts[v.rule_id] = counts.get(v.rule_id, 0) + 1
    deduction = sum(weights.get(rid, 1) * c for rid, c in counts.items())
    # Cap total deduction to 100 to keep score in [0, 100]
    score = max(0.0, 100.0 - min(100.0, float(deduction)))
    return score, counts

# -------------------------------------------------------------
# Runner
# -------------------------------------------------------------

def lint_path(root: str, do_fix: bool = False) -> LintReport:
    files = list(iter_python_files(root))
    file_reports: List[FileReport] = []
    all_vios: List[Violation] = []

    for path in files:
        text = safe_read(path)
        vios: List[Violation] = []

        # Pattern-based rules (with optional fixers)
        for rule in RULES:
            if rule.pattern is None:
                continue
            matches = regex_rule_checker(rule, text, path)
            if do_fix and rule.fixer and matches:
                new_text, n = rule.fixer(text)
                if n:
                    text = new_text
                    safe_write(path, text)
                    # rescan to update remaining matches
                    matches = regex_rule_checker(rule, text, path)
            vios.extend(matches)

        # Custom checkers
        for rule in RULES:
            if rule.check is None:
                continue
            try:
                vios.extend(rule.check(text, path))
            except Exception as e:
                # Non-fatal: surface as a synthetic violation
                vios.append(Violation(rule.id, path, 1, 1, f"[checker error: {type(e).__name__}] {e}"))

        if vios:
            fr = FileReport(path, vios)
            file_reports.append(fr)
            all_vios.extend(vios)

    # Cross-file architecture: circular imports
    cycles = circular_imports(root, files)
    for mods, cyc_files in cycles:
        for f in set(cyc_files):
            # Try to pin the violation to the first import line referencing another module in the cycle
            text = safe_read(f)
            m = re.search(r"(?:from|import)\s+([A-Za-z0-9_\.]+)", text)
            ln, col = (pos_to_linecol(text, m.start()) if m else (1, 1))
            v = Violation("CIRCULAR_IMPORT", f, ln, col, " -> ".join(mods))
            # Add to file report
            fr = next((x for x in file_reports if x.file == f), None)
            if fr:
                fr.violations.append(v)
            else:
                file_reports.append(FileReport(f, [v]))
            all_vios.append(v)

    score, counts = compute_score(all_vios, RULES + [Rule("CIRCULAR_IMPORT", "", "ERROR", 8)])
    return LintReport(file_reports, score, len(all_vios), counts)

# -------------------------------------------------------------
# CLI
# -------------------------------------------------------------

def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="AfriHome Hygiene & Architecture Linter")
    ap.add_argument("--root", default=".", help="Root directory to scan")
    ap.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    ap.add_argument("--fix", action="store_true", help="Attempt safe auto-fixes (arrows only)")
    ap.add_argument("--fail-under", type=float, default=0.0, help="Exit non-zero if score < threshold")
    args = ap.parse_args(argv)

    report = lint_path(args.root, args.fix)

    if args.format == "json":
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(f"\nScore: {report.score:.1f}/100")
        print(f"Violations: {report.total}\n")
        for rid, c in sorted(report.by_rule.items(), key=lambda x: (-x[1], x[0])):
            print(f"{rid:<20} {c:>4}")
        for fr in report.files:
            print(f"\n{fr.file}")
            for v in fr.violations:
                print(f"  L{v.line:>4}:C{v.col:<3} {v.rule_id:<18} {v.excerpt}")

    if report.score < args.fail_under:
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())