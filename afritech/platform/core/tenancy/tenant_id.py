from __future__ import annotations

"""
GA Enterprise Core â€” Tenant Identifier
-------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.typing + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE

Purpose:
- Define the canonical TenantId representation
- Provide a stable tenant boundary identifier

Rules:
- Value object only
- No resolution or lookup
- No persistence semantics
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass

from afritech.platform.core.typing import (
    TenantId,
    FrozenModel,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Canonical Tenant Identifier
# ============================================================

@dataclass(frozen=True, slots=True)
class CanonicalTenantId(FrozenModel):
    """
    Canonical tenant identifier value object.

    IMPORTANT:
    - This is NOT a resolver or registry handle
    - This is a pure value used for boundary enforcement
    """

    value: TenantId

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation (fail-fast, deterministic)
        # ----------------------------------------------------

        if self.value is None:
            raise ValidationError(
                "tenant_id must not be None",
                metadata={"field": "tenant_id"},
            )

    def __str__(self) -> str:
        return str(self.value)


# ============================================================
# Tenant Identifier ABI (explicit, frozen)
# ============================================================

__all__ = [
    "CanonicalTenantId",
]
