from __future__ import annotations

"""
GA Enterprise Core â€” RBAC Permission
-----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.rbac.grammar + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Define canonical RBAC permission value objects
- Provide pure permission pattern matching logic

Rules:
- Grammar enforced deterministically
- Pure value semantics only
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass

from afritech.platform.core.rbac.grammar import (
    validate_permission_name,
    validate_permission_pattern,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Permission matching (pure function)
# ============================================================

def permission_matches(pattern: str, permission: str) -> bool:
    """
    Determine whether a permission string matches a permission pattern.

    Supported wildcards:
    - *  : matches exactly one segment
    - ** : matches remaining segments (only allowed as final segment)
    """
    p = validate_permission_pattern(pattern)
    s = validate_permission_name(permission)

    ptoks = p.split(".")
    stoks = s.split(".")

    i = j = 0
    while i < len(ptoks) and j < len(stoks):
        tok = ptoks[i]

        if tok == "*":
            i += 1
            j += 1
            continue

        if tok == "**":
            return True

        if tok == stoks[j]:
            i += 1
            j += 1
            continue

        return False

    # Remaining pattern handling
    if i == len(ptoks) - 1 and ptoks[-1] == "**":
        return True

    return i == len(ptoks) and j == len(stoks)


# ============================================================
# Permission value object
# ============================================================

@dataclass(frozen=True, slots=True)
class Permission:
    """
    GA v1 RBAC Permission (Value Object).

    Represents a single canonical permission name
    (no wildcards, no patterns).

    Examples:
        - "inventory.item.read"
        - "orders.create"

    IMPORTANT:
    - Pure value object
    - No evaluation logic
    - Patterns belong to permission_matches
    """

    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise ValidationError(
                "Permission.name must be a string",
                metadata={"name": self.name},
            )

        canonical = validate_permission_name(self.name)
        object.__setattr__(self, "name", canonical)

    def __str__(self) -> str:
        return self.name


# ============================================================
# RBAC Permission ABI (explicit, frozen)
# ============================================================

__all__ = [
    "Permission",
    "permission_matches",
]
