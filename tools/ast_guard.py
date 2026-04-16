# tools/ast_guard.py
import ast
from pathlib import Path
from typing import Set

from afritech.guards.result import GuardResult

# ------------------------------------------------------------
# Utilities
# ------------------------------------------------------------

def _extract_call_name(node: ast.Call) -> str | None:
    """
    Return the full dotted name of a function call if possible.

    Examples:
        open(...)                 -> "open"
        Path.read_text(...)       -> "Path.read_text"
        self.foo(...)             -> None  (ignored)
    """
    if isinstance(node.func, ast.Name):
        return node.func.id

    if isinstance(node.func, ast.Attribute):
        parts = []
        current = node.func
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
            return ".".join(reversed(parts))

    return None


def _is_forbidden_module_node(node: ast.AST) -> bool:
    """
    Return True if a module-level AST node represents
    forbidden *mutable or executable* behavior at import time.

    CORE-007 semantics:
        - Declarative definitions are allowed.
        - Executable or mutating logic is forbidden.
    """

    # --------------------------------------------------------
    # ✅ Allowed declarative constructs
    # --------------------------------------------------------
    if isinstance(
        node,
        (
            ast.ClassDef,
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.Import,
            ast.ImportFrom,
            ast.Assign,      # constants / enums / grammar objects
            ast.AnnAssign,   # typed constants
            ast.Expr,        # docstrings
            ast.Pass,
        ),
    ):
        return False

    # --------------------------------------------------------
    # ❌ Forbidden executable / mutable constructs
    # --------------------------------------------------------
    return isinstance(
        node,
        (
            ast.AugAssign,   # +=, -=, etc.
            ast.Delete,
            ast.For,
            ast.While,
            ast.Try,
            ast.With,
            ast.Raise,
        ),
    )


# ------------------------------------------------------------
# Guard Entrypoint
# ------------------------------------------------------------

def run(rule: dict, context: dict) -> GuardResult:
    rule_id = rule["id"]
    rule_type = rule["type"]
    scope = rule.get("scope")

    violations: list[str] = []
    errors: list[str] = []
    checked = 0

    forbidden_calls: Set[str] = set(rule.get("forbidden_calls", []))

    for path_str in context["files"]:
        if scope and not path_str.startswith(scope):
            continue

        checked += 1
        path = Path(path_str)

        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(
                f"{path_str}: failed to parse ({exc})"
            )
            continue

        # --------------------------------------------------------
        # Rule: CORE-004 — forbidden_call
        # --------------------------------------------------------
        if rule_type == "forbidden_call":
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    name = _extract_call_name(node)
                    if name and name in forbidden_calls:
                        violations.append(
                            f"{path_str}:{node.lineno} forbidden call '{name}'"
                        )

        # --------------------------------------------------------
        # Rule: CORE-007 — no_global_state
        # --------------------------------------------------------
        elif rule_type == "no_global_state":
            for node in tree.body:
                if _is_forbidden_module_node(node):
                    violations.append(
                        f"{path_str}:{node.lineno} module-level mutable execution"
                    )

    return GuardResult(
        rule_id=rule_id,
        rule_type=rule_type,
        violations=violations,
        errors=errors,
        checked=checked,
    )