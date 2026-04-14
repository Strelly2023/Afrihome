"""
GA Core â€” RBAC Public API Stability Test
---------------------------------------

Purpose:
- Freeze the RBAC (L2) public API
- Prevent accidental symbol exposure
- Enforce explicit RBAC ABI via __all__

RULES:
- RBAC public API is defined ONLY by core/rbac/__init__.py __all__
- Any change here is a BREAKING CHANGE and requires an ADR
"""

import afritech.platform.core.rbac as rbac


def public_api(module):
    """
    RBAC ABI is defined strictly by __all__.
    """
    assert hasattr(module, "__all__"), (
        f"{module.__name__} must define __all__"
    )
    return sorted(module.__all__)


def test_core_rbac_public_api_stable():
    """
    RBAC public API MUST remain stable across GA releases.
    """
    expected = sorted([
        # ----------------------------
        # Typing primitives (L1, allowed)
        # ----------------------------
        "Permission",
        "RoleName",

        # ----------------------------
        # Permission helpers
        # ----------------------------
        "permission_matches",

        # ----------------------------
        # Roles
        # ----------------------------
        "Role",
        "RoleDefinition",

        # ----------------------------
        # Policy engine
        # ----------------------------
        "Subject",
        "Policy",
        "Decision",
        "evaluate",

        # ----------------------------
        # State
        # ----------------------------
        "RBACState",

        # ----------------------------
        # Errors (domain-level only)
        # ----------------------------
        "RBACError",
        "RoleAlreadyExistsError",
        "RoleNotFoundError",
        "InvalidRoleAssignmentError",
        "PermissionDeniedError",
    ])

    assert public_api(rbac) == expected
