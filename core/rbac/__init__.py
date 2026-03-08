"""
GA Enterprise Core — RBAC (Deterministic, Deny-Wins)

LAYER: L3

Purpose:
- Canonical grammar for roles & permissions
- Immutable role model
- Deterministic permission matching (with patterns)
- Deny-wins policy evaluation
- No tenancy import (strict boundary)
"""

from .grammar import (
    PERMISSION_NAME_PATTERN,
    PERMISSION_PATTERN_PATTERN,
    ROLE_NAME_PATTERN,
    normalize_permission_name,
    normalize_role_name,
    validate_permission_name,
    validate_permission_pattern,
    validate_role_name,
)
from .permissions import permission_matches
from .policy_engine import (
    Decision,
    Policy,
    PolicyEngine,
    Subject,
    evaluate,
)
from .roles import Role

__all__ = [
    "ROLE_NAME_PATTERN",
    "PERMISSION_NAME_PATTERN",
    "PERMISSION_PATTERN_PATTERN",
    "normalize_role_name",
    "normalize_permission_name",
    "validate_role_name",
    "validate_permission_name",
    "validate_permission_pattern",
    "permission_matches",
    "Role",
    "Subject",
    "Policy",
    "Decision",
    "PolicyEngine",
    "evaluate",
]
