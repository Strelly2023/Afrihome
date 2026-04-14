"""
GA Core — No String Domain Enforcement Tests
===========================================

Purpose:
- Prevent re-introduction of stringly-typed DECISION LOGIC
- Enforce enums as the ONLY semantic authority
- Allow strings only where they are CONSTITUTIONALLY required

This test enforces MEANING, not mere vocabulary.
"""

from pathlib import Path
import ast

CORE_ROOT = Path("afritech/platform/core")

# ------------------------------------------------------------
# Semantic string domains that must NOT drive logic
# ------------------------------------------------------------

FORBIDDEN_SEMANTIC_LITERALS = {
    "allow",
    "deny",
    "conditional",
    "rbac",
    "policy",
    "quota",
    "risk",
    "consent",
    "audit",
    "combined",
    "granted",
    "revoked",
    "expired",
}

# ------------------------------------------------------------
# Files/modules where semantic strings ARE ALLOWED BY DESIGN
# ------------------------------------------------------------

ALLOWED_MODULE_PREFIXES = (
    # Enum authority (definitions)
    "typing/enums.py",
    "typing/system.py",
    "decision/decision.py",   # DecisionVerdict enum alias

    # Grammar authority
    "consent/grammar.py",
    "policy/grammar.py",
    "rbac/grammar.py",
    "quota/grammar.py",
    "risk/grammar.py",

    # Declarative registries / projections
    "registry/",
    "audit/",
    "contracts/",
)

# ------------------------------------------------------------
# Decision-authoritative locations (STRICT)
# ------------------------------------------------------------

STRICT_MODULE_PREFIXES = (
    "decision/",
)

# ------------------------------------------------------------
# Helper: extract executable string literals (modern AST)
# ------------------------------------------------------------

def extract_executable_strings(py_file: Path) -> set[str]:
    with py_file.open("r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(py_file))

    literals: set[str] = set()

    for node in ast.walk(tree):
        # Skip docstrings
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)):
            continue

        # ✅ Modern, future-proof string literal detection
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            literals.add(node.value)

    return literals


# ------------------------------------------------------------
# Main enforcement test
# ------------------------------------------------------------

def test_no_string_based_decisions():
    """
    Enforce that raw strings are NEVER used as decision truth.

    Enums MUST be the only semantic authority for decisions.
    """
    violations: dict[str, set[str]] = {}

    for py_file in CORE_ROOT.rglob("*.py"):
        relative_path = py_file.relative_to(CORE_ROOT).as_posix()

        # Enforce ONLY inside decision-authoritative area
        if not relative_path.startswith(STRICT_MODULE_PREFIXES):
            continue

        # Skip constitutionally allowed modules
        if any(relative_path.startswith(p) for p in ALLOWED_MODULE_PREFIXES):
            continue

        literals = extract_executable_strings(py_file)
        banned = literals & FORBIDDEN_SEMANTIC_LITERALS

        if banned:
            violations[relative_path] = banned

    assert not violations, (
        "STRING-BASED DECISION SEMANTICS DETECTED\n\n"
        + "\n".join(
            f"- {path}: {sorted(values)}"
            for path, values in sorted(violations.items())
        )
        + "\n\nGA VIOLATION:\n"
        "Decision truth MUST be represented by canonical enums ONLY.\n"
        "If this change is intentional, an ADR is required.\n"
    )