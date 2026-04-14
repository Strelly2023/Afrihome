from __future__ import annotations

"""
GA Enterprise Core â€” Consent Snapshot
------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.consent.grammar + core.errors.base + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent an immutable snapshot of observed consent state
- Provide deterministic input to consent evaluation

Rules:
- Pure value object only
- No kernel dependencies
- No clocks or persistence (time is injected as data)
- Structural invariants MUST raise ValidationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.consent.grammar import (
    validate_consent_state,
    validate_consent_scope,
    validate_legal_basis,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# Consent Snapshot (pure value object)
# ============================================================

@dataclass(frozen=True, slots=True)
class ConsentSnapshot:
    """
    Immutable snapshot of observed consent state.

    Attributes:
        consent_id:
            Logical identifier of the consent requirement
            (must match ConsentDefinition.consent_id).
        scope:
            Consent scope to which this snapshot applies
            (e.g. "marketing", "analytics").
        state:
            Observed consent state
            ("granted", "revoked", or "expired").
        legal_basis:
            Legal basis under which processing is attempted
            (e.g. "consent", "legitimate_interest").
        granted_at_ms:
            Optional timestamp (ms since epoch) when consent was granted.
        expires_at_ms:
            Optional timestamp (ms since epoch) when consent expires.
        revoked_at_ms:
            Optional timestamp (ms since epoch) when consent was revoked.
    """

    consent_id: str
    scope: str
    state: str
    legal_basis: str

    granted_at_ms: Optional[int] = None
    expires_at_ms: Optional[int] = None
    revoked_at_ms: Optional[int] = None

    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # Structural validation
        # ----------------------------------------------------

        if not isinstance(self.consent_id, str) or not self.consent_id.strip():
            raise ValidationError(
                "consent_id must be a non-empty string",
                metadata={"consent_id": self.consent_id},
            )

        # Grammarâ€‘authoritative normalization
        object.__setattr__(
            self,
            "scope",
            validate_consent_scope(self.scope),
        )

        object.__setattr__(
            self,
            "state",
            validate_consent_state(self.state),
        )

        object.__setattr__(
            self,
            "legal_basis",
            validate_legal_basis(self.legal_basis),
        )

        # ----------------------------------------------------
        # Temporal validation (data only, no clocks)
        # ----------------------------------------------------

        for name, value in (
            ("granted_at_ms", self.granted_at_ms),
            ("expires_at_ms", self.expires_at_ms),
            ("revoked_at_ms", self.revoked_at_ms),
        ):
            if value is not None:
                if not isinstance(value, int) or value < 0:
                    raise ValidationError(
                        f"{name} must be None or a non-negative integer",
                        metadata={name: value},
                    )

        # ----------------------------------------------------
        # Basic consistency invariants (no inference)
        # ----------------------------------------------------

        if self.state == "granted" and self.revoked_at_ms is not None:
            raise ValidationError(
                "revoked_at_ms must be None when state is 'granted'",
                metadata={
                    "state": self.state,
                    "revoked_at_ms": self.revoked_at_ms,
                },
            )

        if self.state == "revoked" and self.revoked_at_ms is None:
            raise ValidationError(
                "revoked_at_ms is required when state is 'revoked'",
                metadata={
                    "state": self.state,
                    "revoked_at_ms": self.revoked_at_ms,
                },
            )


# ============================================================
# Consent Snapshot ABI (explicit, frozen)
# ============================================================

__all__ = [
    "ConsentSnapshot",
]
