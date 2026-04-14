from __future__ import annotations

"""
GA Enterprise Core â€” Quota Snapshot
----------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable snapshot of quota usage
- Provide deterministic input to quota evaluation

Rules:
- Pure value object only
- No kernel dependencies
- No clocks or persistence
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Quota Snapshot (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class QuotaSnapshot:
    """
    Immutable snapshot of quota usage.

    Attributes:
        quota_id:
            Logical identifier of the quota this snapshot applies to.
        used:
            Amount of usage already consumed.
        remaining:
            Remaining allowance (may be derived by higher layers
            but stored explicitly here for convenience).
        window_start_ms:
            Start timestamp (milliseconds since epoch) of the
            usage window, if applicable.
        window_end_ms:
            End timestamp (milliseconds since epoch) of the
            usage window, if applicable.
    """

    quota_id: str
    used: int
    remaining: Optional[int]
    window_start_ms: Optional[int] = None
    window_end_ms: Optional[int] = None

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation
        # ----------------------------------------------------

        if not isinstance(self.quota_id, str) or not self.quota_id.strip():
            raise ValidationError(
                "quota_id must be a non-empty string",
                metadata={"quota_id": self.quota_id},
            )

        if not isinstance(self.used, int) or self.used < 0:
            raise ValidationError(
                "used must be a non-negative integer",
                metadata={"used": self.used},
            )

        if self.remaining is not None:
            if not isinstance(self.remaining, int) or self.remaining < 0:
                raise ValidationError(
                    "remaining must be None or a non-negative integer",
                    metadata={"remaining": self.remaining},
                )

        # ----------------------------------------------------
        # Temporal invariants (if windowed)
        # ----------------------------------------------------

        if self.window_start_ms is not None:
            if not isinstance(self.window_start_ms, int):
                raise ValidationError(
                    "window_start_ms must be an integer if provided",
                    metadata={"window_start_ms": self.window_start_ms},
                )

        if self.window_end_ms is not None:
            if not isinstance(self.window_end_ms, int):
                raise ValidationError(
                    "window_end_ms must be an integer if provided",
                    metadata={"window_end_ms": self.window_end_ms},
                )

        if (
            self.window_start_ms is not None
            and self.window_end_ms is not None
            and self.window_end_ms < self.window_start_ms
        ):
            raise ValidationError(
                "window_end_ms must be >= window_start_ms",
                metadata={
                    "window_start_ms": self.window_start_ms,
                    "window_end_ms": self.window_end_ms,
                },
            )


# ============================================================
# Quota Snapshot ABI (explicit, frozen)
# ============================================================

__all__ = [
    "QuotaSnapshot",
]
