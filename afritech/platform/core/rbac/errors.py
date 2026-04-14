from __future__ import annotations

"""
GA Enterprise Core â€” RBAC Errors
-------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + core.errors.codes + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Define RBAC-specific domain errors
- Group structural and semantic RBAC failures

Rules:
- MUST derive from CoreError
- MUST use canonical error codes
- MUST be deterministic and replay-safe
- Raised ONLY for invalid RBAC state or misuse
"""

from typing import Optional, Mapping, Any

from afritech.platform.core.errors.base import CoreError
from afritech.platform.core.errors import codes


# ============================================================
# Base RBAC Error
# ============================================================

class RBACError(CoreError):
    """
    Base error for RBAC domain violations.

    NOTES:
    - This is an L2 engine error (NOT kernel, NOT L1)
    - Carries a stable error code for audit and handling
    """

    def __init__(
        self,
        message: str,
        *,
        code: str,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            metadata=metadata,
        )


# ============================================================
# RBAC Structural Errors
# ============================================================

class RoleAlreadyExistsError(RBACError):
    """Raised when attempting to register a role that already exists."""

    def __init__(
        self,
        role_name: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Role already exists: {role_name!r}",
            code=codes.RBAC_INVALID_ROLE,
            metadata={
                "role_name": role_name,
                **(dict(metadata) if metadata else {}),
            },
        )


class RoleNotFoundError(RBACError):
    """Raised when a referenced role is not present."""

    def __init__(
        self,
        role_name: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Role not found: {role_name!r}",
            code=codes.RBAC_INVALID_ROLE,
            metadata={
                "role_name": role_name,
                **(dict(metadata) if metadata else {}),
            },
        )


class InvalidRoleDefinitionError(RBACError):
    """Raised when a role definition violates grammar or structure."""

    def __init__(
        self,
        role_name: str,
        reason: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=f"Invalid role definition for {role_name!r}: {reason}",
            code=codes.RBAC_INVALID_ROLE,
            metadata={
                "role_name": role_name,
                "reason": reason,
                **(dict(metadata) if metadata else {}),
            },
        )


class InvalidRoleAssignmentError(RBACError):
    """Raised when role assignment violates RBAC invariants."""

    def __init__(
        self,
        subject_id: str,
        role_name: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=(
                f"Invalid role assignment: subject={subject_id!r}, "
                f"role={role_name!r}"
            ),
            code=codes.RBAC_INVALID_ASSIGNMENT,
            metadata={
                "subject_id": subject_id,
                "role_name": role_name,
                **(dict(metadata) if metadata else {}),
            },
        )


class PermissionDeniedError(RBACError):
    """Raised when RBAC explicitly denies a permission."""

    def __init__(
        self,
        subject_id: str,
        permission: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=(
                f"RBAC permission denied: subject={subject_id!r}, "
                f"permission={permission!r}"
            ),
            code=codes.RBAC_PERMISSION_DENIED,
            metadata={
                "subject_id": subject_id,
                "permission": permission,
                **(dict(metadata) if metadata else {}),
            },
        )


# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    "RBACError",
    "RoleAlreadyExistsError",
    "RoleNotFoundError",
    "InvalidRoleDefinitionError",
    "InvalidRoleAssignmentError",
    "PermissionDeniedError",
]
