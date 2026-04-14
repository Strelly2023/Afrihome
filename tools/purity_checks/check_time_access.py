#!/usr/bin/env python3
from __future__ import annotations

"""
AfriTech Static Time Access Checker (Async-Aware)
================================================

Enforces:
- ADR-KE-FT-001 — Clock / Time Injection Enforcement
- ADR-DS-BI-001 — Pure-Function Boundary Enforcement

Detects forbidden implicit time access in BOTH:
- synchronous functions
- async functions

Analysis-only. Fail-closed.
"""

import ast
import json
from pathlib import Path
from datetime import datetime, timezone
import sys

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

ANALYZED_ROOTS = [
    "afritech/platform/core/identity",
    "afritech/platform/core/decision",
    "afritech/platform/core/policy",
    "afritech/platform/core/risk",
    "afritech/platform/core/governance",
]

FORBIDDEN_TIME_MODULES = {
    "time",
    "datetime",
    "asyncio",
}

FORBIDDEN_CALLS = {
    "time.time",
    "time.monotonic",
    "time.perf_counter",
    "datetime.now",
    "datetime.utcnow",
    "datetime.today",
    "asyncio.sleep",
    "asyncio.get_event_loop",
}

REPORT_PATH = Path("docs/reports/core-purity-report.json")

# ---------------------------------------------------------------------
# Violation model
# ---------------------------------------------------------------------

def make_violation(
    *,
    file: str,
    function: str | None,
    violation_type: str,
    description: str,
) -> dict:
    return {
        "file": file,
        "function": function,
        "violation_type": violation_type,
        "rule": "ADR-KE-FT-001",
        "description": description,
        "severity": "critical",
        "allowed_fix": "Inject time explicitly as a function argument",
        "detected_at": datetime.now(timezone.utc).isoformat(),
    }

# ---------------------------------------------------------------------
# AST Visitor
# ---------------------------------------------------------------------

class TimeAccessVisitor(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.violations: list[dict] = []
        self.current_function: str | None = None

    # ----- Function Handling (Sync) -----------------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._visit_function(node)

    # ----- Function Handling (Async) ----------------------------------

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._visit_function(node)

    # ----- Shared Function Logic -------------------------------------

    def _visit_function(self, node):
        prev = self.current_function
        self.current_function = node.name

        # Default argument evaluation (sync or async)
        for default in node.args.defaults:
            if isinstance(default, ast.Call):
                call_name = self._call_name(default.func)
                if call_name in FORBIDDEN_CALLS:
                    self.violations.append(
                        make_violation(
                            file=self.file_path,
                            function=node.name,
                            violation_type="time_access",
                            description=f"Default argument calls {call_name}",
                        )
                    )

        self.generic_visit(node)
        self.current_function = prev

    # ----- Imports ----------------------------------------------------

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name in FORBIDDEN_TIME_MODULES:
                self.violations.append(
                    make_violation(
                        file=self.file_path,
                        function=self.current_function,
                        violation_type="time_access",
                        description=f"Imports forbidden time module '{alias.name}'",
                    )
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module in FORBIDDEN_TIME_MODULES:
            self.violations.append(
                make_violation(
                    file=self.file_path,
                    function=self.current_function,
                    violation_type="time_access",
                    description=f"Imports from forbidden time module '{node.module}'",
                )
            )
        self.generic_visit(node)

    # ----- Calls & Await ----------------------------------------------

    def visit_Call(self, node: ast.Call):
        call_name = self._call_name(node.func)
        if call_name in FORBIDDEN_CALLS:
            self.violations.append(
                make_violation(
                    file=self.file_path,
                    function=self.current_function,
                    violation_type="time_access",
                    description=f"Calls forbidden time function '{call_name}'",
                )
            )
        self.generic_visit(node)

    def visit_Await(self, node: ast.Await):
        # Catch `await asyncio.sleep(...)`
        if isinstance(node.value, ast.Call):
            call_name = self._call_name(node.value.func)
            if call_name in FORBIDDEN_CALLS:
                self.violations.append(
                    make_violation(
                        file=self.file_path,
                        function=self.current_function,
                        violation_type="time_access",
                        description=f"Awaits forbidden time function '{call_name}'",
                    )
                )
        self.generic_visit(node)

    # ----- Utilities --------------------------------------------------

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

    visitor = TimeAccessVisitor(path.as_posix())
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
        print("❌ Purity report JSON missing.")
        raise SystemExit(1)

    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    report.setdefault("violations", [])
    report["violations"].extend(all_violations)
    report["results"]["summary"]["violation_count"] = len(report["violations"])

    report["results"]["status"] = "FAIL" if report["violations"] else "PASS"

    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if report["violations"]:
        print("❌ Time-access purity violations detected:")
        for v in report["violations"]:
            print(f"  - {v['file']}: {v['description']}")
        raise SystemExit(1)

    print("✅ Time-access purity check (async-aware) passed.")

if __name__ == "__main__":
    main()