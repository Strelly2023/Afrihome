# control_plane/governance/organisations/organisation.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from control_plane.governance.identity.identity_invariants import (
    normalize_display_name,
    normalize_user_id,
)
from core.errors import ValidationError
from core.typing import TenantId


def _norm_slug(s: str) -> str:
    """
    Deterministic slug normalizer:
    - lower, trim, internal spaces -> '-', letters/digits/hyphen only
    """
    if not isinstance(s, str):
        raise ValidationError("slug must be a string")
    base = "-".join(s.strip().lower().split())
    if not base or any(c for c in base if not (c.isalnum() or c == "-")):
        raise ValidationError("slug contains invalid characters")
    return base


@dataclass(frozen=True, slots=True)
class OrganisationId:
    # Human-facing org ID (distinct from TenantId; often a stable UUID or slug)
    value: str

    def __post_init__(self) -> None:
        v = self.value.strip()
        if not v:
            raise ValidationError("OrganisationId must be non-empty")
        object.__setattr__(self, "value", v)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Organisation:
    """
    Human-facing Organisation that surfaces tenant-backed isolation.

    Invariants:
    - `tenant_id` is authoritative for isolation/billing scope.
    - `slug` is human-unique (enforced by repo adapter).
    - `owner_user_id` references a platform UserId (not duplicated here).
    - No secrets, no IO, no ORM; immutable snapshot.
    """

    id: OrganisationId
    tenant_id: TenantId
    name: str
    slug: str
    owner_user_id: str  # normalized user id
    active: bool = True
    attributes: Mapping[str, str] | None = None  # branded hints (e.g., 'logo_url')

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", normalize_display_name(self.name))
        object.__setattr__(self, "slug", _norm_slug(self.slug))
        object.__setattr__(self, "owner_user_id", normalize_user_id(self.owner_user_id))
