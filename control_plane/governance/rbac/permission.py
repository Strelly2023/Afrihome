# control_plane/governance/rbac/permission.py
"""
DEPRECATED shim — use control_plane.governance.permissions.*

This module re-exports the canonical permission APIs so older imports continue to work:
    from control_plane.governance.rbac.permission import Permission, validate_permission_name, ...
should be moved to:
    from control_plane.governance.permissions import Permission, validate_permission_name, ...
"""

from __future__ import annotations

from ..permissions.pattern import permission_matches, validate_permission_pattern

# Canonical implementations live in governance/permissions/*
from ..permissions.permission import Permission, validate_permission_name

__all__ = [
    "Permission",
    "validate_permission_name",
    "validate_permission_pattern",
    "permission_matches",
]
