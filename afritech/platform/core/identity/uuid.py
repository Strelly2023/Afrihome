from __future__ import annotations

"""
GA Enterprise Core â€” Deterministic UUID Authority
------------------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib + core.typing + core.errors.base
Randomness: FORBIDDEN
Time access: FORBIDDEN
Global state: NONE

Purpose:
- Define deterministic UUID generation contracts
- Enforce explicit, injected uniqueness
- Prevent implicit UUID creation inside models

Rules:
- Models must NEVER generate UUIDs
- UUIDs must be derived from explicit discriminators
- No clocks, no counters, no randomness
- Structural invariants MUST raise ValidationError
"""

import hashlib
import uuid
from typing import Protocol, runtime_checkable, Final

from afritech.platform.core.typing import (
    EventId,
    AggregateId,
    CorrelationId,
    CausationId,
)
from afritech.platform.core.errors.base import ValidationError


# ============================================================
# UUID Provider Protocol (GAâ€‘Canonical)
# ============================================================

@runtime_checkable
class UUIDProvider(Protocol):
    """
    Deterministic UUID provider contract.

    All uniqueness MUST be supplied explicitly by the caller
    via a discriminator string.
    """

    def event_id(self, *, discriminator: str) -> EventId: ...
    def aggregate_id(self, *, discriminator: str) -> AggregateId: ...
    def correlation_id(self, *, discriminator: str) -> CorrelationId: ...
    def causation_id(self, *, discriminator: str) -> CausationId: ...


# Backwardâ€‘compatibility alias (intentional)
UuidProvider = UUIDProvider


# ============================================================
# Deterministic UUIDv5 Provider (GAâ€‘Approved)
# ============================================================

class DeterministicUUIDProvider:
    """
    Deterministic UUIDv5-based provider.

    Properties:
    - Stateless
    - Replayâ€‘safe
    - Deterministic by construction

    Uniqueness derives ONLY from:
    - seed
    - kind
    - discriminator
    """

    _NAMESPACE: Final[uuid.UUID] = uuid.UUID(
        "12345678-1234-5678-1234-567812345678"
    )

    def __init__(self, seed: str) -> None:
        if not isinstance(seed, str) or not seed.strip():
            raise ValidationError(
                "UUID seed must be a non-empty string",
                metadata={"seed": seed},
            )

        self._seed = seed.strip()

    # --------------------------------------------------------
    # Internal deterministic derivation
    # --------------------------------------------------------

    def _derive(self, *, kind: str, discriminator: str) -> str:
        if not isinstance(discriminator, str) or not discriminator.strip():
            raise ValidationError(
                "UUID discriminator must be a non-empty string",
                metadata={
                    "kind": kind,
                    "discriminator": discriminator,
                },
            )

        material = f"{self._seed}:{kind}:{discriminator.strip()}"
        digest = hashlib.sha256(material.encode("utf-8")).hexdigest()

        # UUIDv5 is deterministic over (namespace, name)
        return str(uuid.uuid5(self._NAMESPACE, digest))

    # --------------------------------------------------------
    # Canonical GA API (explicit discriminators)
    # --------------------------------------------------------

    def event_id(self, *, discriminator: str) -> EventId:
        return EventId(
            self._derive(kind="event", discriminator=discriminator)
        )

    def aggregate_id(self, *, discriminator: str) -> AggregateId:
        return AggregateId(
            self._derive(kind="aggregate", discriminator=discriminator)
        )

    def correlation_id(self, *, discriminator: str) -> CorrelationId:
        return CorrelationId(
            self._derive(kind="correlation", discriminator=discriminator)
        )

    def causation_id(self, *, discriminator: str) -> CausationId:
        return CausationId(
            self._derive(kind="causation", discriminator=discriminator)
        )

    # --------------------------------------------------------
    # Legacy compatibility API (TEMPORARY)
    # --------------------------------------------------------
    # DO NOT use in new code.
    # Exists only until all call sites are migrated.

    def new_event_id(self) -> EventId:
        return self.event_id(discriminator="legacy")

    def new_aggregate_id(self) -> AggregateId:
        return self.aggregate_id(discriminator="legacy")

    def new_correlation_id(self) -> CorrelationId:
        return self.correlation_id(discriminator="legacy")

    def new_causation_id(self) -> CausationId:
        return self.causation_id(discriminator="legacy")


# ============================================================
# Public API
# ============================================================

__all__ = [
    "UUIDProvider",
    "UuidProvider",
    "DeterministicUUIDProvider",
]
