from __future__ import annotations

"""
GA Enterprise Core â€” Quota Definition
------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.quota.grammar + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable quota definition
- Describe quota limits without measuring or enforcing usage

Rules:
- Pure value object only
- No kernel dependencies
- No evaluation logic
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.quota.grammar import (
    validate_unit,
    validate_scope,
    validate_dimension,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Quota Definition (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class QuotaDefinition:
    """
    Immutable quota definition.

    Attributes:
        quota_id:
            Logical identifier for the quota (e.g. "api-requests").
        unit:
            What is being counted (e.g. "requests", "bytes").
        scope:
            Who the quota applies to (e.g. "tenant", "user").
        dimension:
            How usage is grouped (e.g. "per_day", "rolling_window").
        limit:
            Maximum allowed usage within the defined dimension.
        window_ms:
            Optional rolling window size in milliseconds.
            Required only when dimension == "rolling_window".
    """

    quota_id: str
    unit: str
    scope: str
    dimension: str
    limit: int
    window_ms: Optional[int] = None

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Basic structural validation
        # ----------------------------------------------------

        if not isinstance(self.quota_id, str) or not self.quota_id.strip():
            raise ValidationError(
                "quota_id must be a non-empty string",
                metadata={"quota_id": self.quota_id},
            )

        if not isinstance(self.limit, int) or self.limit < 0:
            raise ValidationError(
                "limit must be a non-negative integer",
                metadata={"limit": self.limit},
            )

        # ----------------------------------------------------
        # Grammar validation (centralized authority)
        # ----------------------------------------------------

        validate_unit(self.unit)
        validate_scope(self.scope)
        validate_dimension(self.dimension)

        # ----------------------------------------------------
        # Dimension-specific constraints
        # ----------------------------------------------------

        if self.dimension == "rolling_window":
            if self.window_ms is None:
                raise ValidationError(
                    "window_ms is required for rolling_window dimension",
                    metadata={
                        "dimension": self.dimension,
                        "window_ms": self.window_ms,
                    },
                )

            if not isinstance(self.window_ms, int) or self.window_ms <= 0:
                raise ValidationError(
                    "window_ms must be a positive integer (milliseconds)",
                    metadata={"window_ms": self.window_ms},
                )
        else:
            if self.window_ms is not None:
                raise ValidationError(
                    "window_ms must be None unless dimension is 'rolling_window'",
                    metadata={
                        "dimension": self.dimension,
                        "window_ms": self.window_ms,
                    },
                )


# ============================================================
# Quota Definition ABI (explicit, frozen)
# ============================================================

__all__ = [
    "QuotaDefinition",
]
