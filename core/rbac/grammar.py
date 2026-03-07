
"""
GA Enterprise Core — RBAC Grammar
---------------------------------

LAYER: L3
Dependencies: core.errors (L0)
Deterministic: YES
No tenancy import: ENFORCED
"""


import re
from typing import Final

from core.errors import GrammarViolationError

ROLE_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")

SEG = r"[a-z][a-z0-9]*"
PERMISSION_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(rf"^{SEG}(?:\.{SEG})*$")
PERMISSION_PATTERN_PATTERN: Final[re.Pattern[str]] = re.compile(rf"^(?:{SEG}|\*|\*\*)(?:\.(?:{SEG}|\*|\*\*))*$")


def normalize_role_name(name: str) -> str:
    if name is None:
        raise GrammarViolationError("Role name must not be None")
    return name.strip().lower()


def normalize_permission_name(name: str) -> str:
    if name is None:
        raise GrammarViolationError("Permission name must not be None")
    return name.strip().lower()


def validate_role_name(name: str) -> str:
    n = normalize_role_name(name)
    if not ROLE_NAME_PATTERN.match(n):
        raise GrammarViolationError(f"Invalid role name: {name!r}")
    return n


def validate_permission_name(name: str) -> str:
    n = normalize_permission_name(name)
    if not PERMISSION_NAME_PATTERN.match(n):
        raise GrammarViolationError(f"Invalid permission name: {name!r}")
    return n


def validate_permission_pattern(pattern: str) -> str:
    p = normalize_permission_name(pattern)
    if not PERMISSION_PATTERN_PATTERN.match(p):
        raise GrammarViolationError(f"Invalid permission pattern: {pattern!r}")
    tokens = p.split('.')
    for i, tok in enumerate(tokens):
        if tok == "**" and i != len(tokens) - 1:
            raise GrammarViolationError("The '**' wildcard is only allowed as the last segment")
    return p
