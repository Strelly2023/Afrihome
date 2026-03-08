"""
GA Governance — Permissions (pure)
----------------------------------

Provides canonical permission grammar validation and pattern matching.

LAYER: Governance (pure)
IO/ORM: NO
"""

from .pattern import permission_matches, validate_permission_pattern
from .permission import Permission, validate_permission_name

__all__ = [
    "Permission",
    "validate_permission_name",
    "validate_permission_pattern",
    "permission_matches",
]
