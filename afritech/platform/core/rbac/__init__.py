from __future__ import annotations
"""
GA Enterprise Core â€” RBAC Engine
-------------------------------

LAYER: L2 (Pure Engine)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose the frozen public RBAC API
- Provide deterministic, replay-safe permission evaluation primitives

Notes:
- This module is the ONLY supported entrypoint for RBAC consumers
- All exports are GA-stable and ADR-protected
"""


# ============================================================
# Typing Primitives
# ============================================================

from afritech.platform.core.typing import (
    Permission,
    RoleName,
)

# ============================================================
# Grammar & Matching
# ============================================================

from afritech.platform.core.rbac.permission import (
    permission_matches,
)

# ============================================================
# Roles
# ============================================================

from afritech.platform.core.rbac.role import (
    Role,
    RoleDefinition,
)

# ============================================================
# Policy Engine
# ============================================================

from afritech.platform.core.rbac.policy_engine import (
    Subject,
    Policy,
    Decision,
    evaluate,
)

# ============================================================
# RBAC State
# ============================================================

from afritech.platform.core.rbac.rbac_state import (
    RBACState,
)

# ============================================================
# Errors
# ============================================================

from afritech.platform.core.rbac.errors import (
    RBACError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
    InvalidRoleAssignmentError,
    PermissionDeniedError,
)

# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    # Typing
    "Permission",
    "RoleName",

    # Grammar / matching
    "permission_matches",

    # Roles
    "Role",
    "RoleDefinition",

    # Policy engine
    "Subject",
    "Policy",
    "Decision",
    "evaluate",

    # State
    "RBACState",

    # Errors
    "RBACError",
    "RoleAlreadyExistsError",
    "RoleNotFoundError",
    "InvalidRoleAssignmentError",
    "PermissionDeniedError",
]
