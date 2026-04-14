from __future__ import annotations

"""
GA Enterprise Core â€” RBAC Grammar
--------------------------------

LAYER: L2 (Pure Engine)
Dependencies: stdlib + core.errors.base
Deterministic: YES
Side effects: NONE

Purpose:
- Define the canonical grammar for RBAC role names and permission names
- Support deterministic validation and normalization
- Serve as the single grammar authority for RBAC engines

Rules:
- Grammar ONLY (no resolution, no policy, no persistence)
- No kernel imports
- No tenancy or identity imports
- Violations MUST raise GrammarViolationError
"""

import re
from typing import Final

from afritech.platform.core.errors.base import GrammarViolationError


# ============================================================
# Grammar primitives
# ============================================================

# Role names:
# - lowercase
# - letters, digits, underscore, hyphen
# - length 3â€“64
ROLE_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[a-z][a-z0-9_-]{2,63}$"
)

# Permission segment:
# - lowercase
# - letters and digits
_SEGMENT = r"[a-z][a-z0-9]*"

# Permission name:
#   invoice.read
#   audit.export.logs
PERMISSION_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(
    rf"^{_SEGMENT}(?:\.{_SEGMENT})*$"
)

# Permission pattern with wildcards:
#   invoice.*
#   invoice.**
#   audit.export.*
PERMISSION_PATTERN_PATTERN: Final[re.Pattern[str]] = re.compile(
    rf"^(?:{_SEGMENT}|\*|\*\*)(?:\.(?:{_SEGMENT}|\*|\*\*))*$"
)


# ============================================================
# Normalization helpers (pure)
# ============================================================

def normalize_role_name(value: str) -> str:
    if not isinstance(value, str):
        raise GrammarViolationError(
            "Role name must be a string",
            metadata={"value": value},
        )
    return value.strip().lower()


def normalize_permission_name(value: str) -> str:
    if not isinstance(value, str):
        raise GrammarViolationError(
            "Permission name must be a string",
            metadata={"value": value},
        )
    return value.strip().lower()


# ============================================================
# Validators
# ============================================================

def validate_role_name(value: str) -> str:
    name = normalize_role_name(value)
    if not ROLE_NAME_PATTERN.fullmatch(name):
        raise GrammarViolationError(
            "Invalid RBAC role name",
            metadata={"value": value, "normalized": name},
        )
    return name


def validate_permission_name(value: str) -> str:
    name = normalize_permission_name(value)
    if not PERMISSION_NAME_PATTERN.fullmatch(name):
        raise GrammarViolationError(
            "Invalid RBAC permission name",
            metadata={"value": value, "normalized": name},
        )
    return name


def validate_permission_pattern(pattern: str) -> str:
    value = normalize_permission_name(pattern)

    if not PERMISSION_PATTERN_PATTERN.fullmatch(value):
        raise GrammarViolationError(
            "Invalid RBAC permission pattern",
            metadata={"pattern": pattern, "normalized": value},
        )

    # '**' wildcard may only appear once, and only as the final segment
    tokens = value.split(".")
    for i, tok in enumerate(tokens):
        if tok == "**" and i != len(tokens) - 1:
            raise GrammarViolationError(
                "The '**' wildcard is only allowed as the final segment",
                metadata={"pattern": value, "segment_index": i},
            )

    return value


# ============================================================
# RBAC Grammar ABI (explicit, frozen)
# ============================================================

__all__ = [
    "ROLE_NAME_PATTERN",
    "PERMISSION_NAME_PATTERN",
    "PERMISSION_PATTERN_PATTERN",
    "normalize_role_name",
    "normalize_permission_name",
    "validate_role_name",
    "validate_permission_name",
    "validate_permission_pattern",
]
