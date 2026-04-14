"""
AfriHome Platform — Governance · Identity (Phase 1.2)

Pure, deterministic identity aggregates & invariants.
No services/orchestration. No I/O/ORM/Django.

Contains:
- UserId (strong wrapper; deterministic factory via core.identity.UUIDProvider)
- Permission (pure VO; normalized/validated via core.rbac.grammar)
- Role (pure VO; normalized/validated via core.rbac.grammar)
- User (immutable aggregate; tenant-scoped identity with roles & direct grants)
- Identity invariants (email/display name validation)
"""
from .user_id import UserId
from .permission import Permission
from .role import Role
from .user import User
from .identity_invariants import validate_email, normalize_display_name

__all__ = [
    "UserId",
    "Permission",
    "Role",
    "User",
    "validate_email",
    "normalize_display_name",
]