#!/usr/bin/env python3#!/ Configuration
# ---------------------------------------------------------------------

ANALYZED_ROOTS = [
    "afritech/platform/core/identity",
    "afritech/platform/core/decision",
    "afritech/platform/core/policy",
    "afritech/platform/core/risk",
    "afritech/platform/core/governance",
]

FORBIDDEN_RANDOM_MODULES = {
    "random",
    "uuid",
    "secrets",
}

FORBIDDEN_CALLS = {
    # random
    "random.random",
    "random.randint",
    "random.choice",
    "random.shuffle",
    "random.uniform",

    # uuid
    "uuid.uuid4",
    "uuid.uuid1",

    # secrets
    "secrets.token_bytes",
    "secrets.token_hex",
    "secrets.choice",
}

REPORT_PATH = Path("docs/reports/core-purity-report.json")

# ---------------------------------------------------------------------
# Violation model
# ---------------------------------------------------------------------

def make_violation(
    *,
    file: str,
    function: str | None,
    description: str,
) -> dict:
    return {
        "file": file,
        "function": function,
        "violation_type": "randomness",
        "rule": "ADR-KE-FT-002",
        "description": description,
        "severity": "critical",
        "allowed_fix": "Generate entropy outside Core and inject it explicitly",
        "detected_at": datetime.now(timezone.utc).isoformat(),
    }

# ---------------------------------------------------------------------
# AST Visitor
# ---------------------------------------------------------------------

class RandomnessVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.violations: list[dict] = []
        self.current_function: str | None = None

    # ----- Function handling (sync + async) ----------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._visit_function(node)

    def _visit_function(self, node):
        prev = self.current_function
        self.current_function = node.name

        # Default argument evaluation (e.g. seed=random.random())
        for default in node.args.defaults:
            if isinstance(default, ast.Call):
                call_name = self._call_name(default.func)
                if call_name in FORBIDDEN_CALLS:
                    self.violations.append(
                        make_violation(
                            file=self.file_path,
                            function=node.name,
                            description=f"Default argument calls forbidden randomness function '{call_name}'",
                        )
                    )

        self.generic_visit(node)
        self.current_function = prev

    # ----- Imports -----------------------------------------------------

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name in FORBIDDEN_RANDOM_MODULES:
                self.violations.append(
                    make_violation(
                        file=self.file_path,
                        function=self.current_function,
                        description=f"Imports forbidden randomness module '{alias.name}'",
                    )
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module in FORBIDDEN_RANDOM_MODULES:
            self.violations.append(
                make_violation(
                    file=self.file_path,
                    function=self.current_function,
                    description=f"Imports from forbidden randomness module '{node.module}'",
                )
            )
        self.generic_visit(node)

    # ----- Calls -------------------------------------------------------

    def visit_Call(self, node: ast.Call):
        call_name = self._call_name(node.func)
        if call_name in FORBIDDEN_CALLS:
            self.violations.append(
                make_violation(
                    file=self.file_path,
                    function=self.current_function,
                    description=f"Calls forbidden randomness function '{call_name}'",
                )
            )
        self.generic_visit(node)

    # ----- Utilities ---------------------------------------------------

    def _call_name(self, func: ast.AST) -> str:
        try:
            if isinstance(func, ast.Attribute):
                if isinstance(func.value, ast.Name):
                    return f"{func.value.id}.{func.attr}"
            elif isinstance(func, ast.Name):
                return func.id
        except Exception:
            pass
        return ""

# ---------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------

def analyze_file(path: Path) -> list[dict]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return []

    visitor = RandomnessVisitor(path.as_posix())
    visitor.visit(tree)
    return visitor.violations


def main() -> None:
    all_violations: list[dict] = []

    for root in ANALYZED_ROOTS:
        base = Path(root)
        if not base.exists():
            continue

        for py in base.rglob("*.py"):
            all_violations.extend(analyze_file(py))

    if not REPORT_PATH.exists():
        raise SystemExit("❌ Purity report JSON missing.")

    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    report.setdefault("violations", [])
    report["violations"].extend(all_violations)
    report["results"]["summary"]["violation_count"] = len(report["violations"])
    report["results"]["status"] = "FAIL" if report["violations"] else "PASS"

    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if report["violations"]:
        print("❌ Randomness / entropy purity violations detected:")
        for v in report["violations"]:
            print(f"  - {v['file']}: {v['description']}")
        raise SystemExit(1)

    print("✅ Randomness / entropy purity check passed.")

if __name__ == "__main__":
    main()
from __future__ import annotations

"""
AfriTech Static Randomness / Entropy Access Checker
==================================================

Enforces:
- ADR-KE-FT-002 — Randomness / Entropy Injection Enforcement
- ADR-DS-BI-001 — Pure-Function Boundary Enforcement

Detects forbidden implicit randomness in:
- sync functions
- async functions

Analysis-only. Fail-closed.
"""

import ast
import json
from pathlib import Path
from datetime import datetime, timezone

# ---------------------------------------------------------------------
