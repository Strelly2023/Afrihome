from __future__ import annotations

"""
GA Enterprise Core â€” Immutable Request Context
----------------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib + core.typing + core.errors.base
Deterministic: YES
Side effects: NONE
IO / Time access: NONE

Purpose:
- Carry immutable, request-scoped metadata
- Provide deterministic tracing, correlation, and identity references
- Establish a single execution boundary snapshot

Rules:
- Fully immutable
- No global state
- No implicit defaults
- All values injected explicitly
- No authorization or RBAC logic
- Structural invariants MUST raise InvariantViolationError
"""

from dataclasses import dataclass
from typing import Optional

from afritech.platform.core.typing import (
    TenantId,
    UserId,
    RequestId,
    CorrelationId,
    CausationId,
    UnixMillis,
    FrozenModel,
)
from afritech.platform.core.errors.base import (
    ValidationError,
    InvariantViolationError,
)


# ============================================================
# Request Context
# ============================================================

@dataclass(frozen=True, slots=True)
class RequestContext(FrozenModel):
    """
    Immutable request metadata snapshot.

    This object represents a single execution boundary
    and is safe to pass across application, domain, and
    infrastructure layers.

    Canonical time field:
        - timestamp_ms: UnixMillis

    Compatibility:
        - Accepts legacy alias `timestamp` for GAâ€‘v1 / test callers.
          If both `timestamp_ms` and `timestamp` are provided,
          `timestamp_ms` takes precedence.
    """

    request_id: RequestId
    correlation_id: CorrelationId
    causation_id: Optional[CausationId]
    timestamp_ms: UnixMillis

    tenant_id: Optional[TenantId] = None
    user_id: Optional[UserId] = None

    # --------------------------------------------------------
    # Custom initializer (timestamp alias support)
    # --------------------------------------------------------

    def __init__(
        self,
        request_id: RequestId,
        correlation_id: CorrelationId,
        *,
        timestamp_ms: Optional[UnixMillis] = None,
        timestamp: Optional[UnixMillis] = None,  # legacy alias
        causation_id: Optional[CausationId] = None,
        tenant_id: Optional[TenantId] = None,
        user_id: Optional[UserId] = None,
    ) -> None:
        ts = timestamp_ms if timestamp_ms is not None else timestamp

        if ts is None:
            raise ValidationError(
                "timestamp_ms (or legacy alias 'timestamp') must be provided",
                metadata={
                    "timestamp_ms": timestamp_ms,
                    "timestamp": timestamp,
                },
            )

        if int(ts) < 0:
            raise ValidationError(
                "timestamp_ms must be non-negative",
                metadata={"timestamp_ms": ts},
            )

        object.__setattr__(self, "request_id", request_id)
        object.__setattr__(self, "correlation_id", correlation_id)
        object.__setattr__(self, "causation_id", causation_id)
        object.__setattr__(self, "timestamp_ms", UnixMillis(int(ts)))
        object.__setattr__(self, "tenant_id", tenant_id)
        object.__setattr__(self, "user_id", user_id)

        self.__post_init__()

    # --------------------------------------------------------
    # Structural invariants
    # --------------------------------------------------------

    def __post_init__(self) -> None:
        if self.request_id is None:
            raise InvariantViolationError(
                "request_id must not be None",
                metadata={"field": "request_id"},
            )

        if self.correlation_id is None:
            raise InvariantViolationError(
                "correlation_id must not be None",
                metadata={"field": "correlation_id"},
            )

        if self.timestamp_ms is None:
            raise InvariantViolationError(
                "timestamp_ms must not be None",
                metadata={"field": "timestamp_ms"},
            )

    # --------------------------------------------------------
    # Derived helpers (pure, non-authoritative)
    # --------------------------------------------------------

    def is_authenticated(self) -> bool:
        """
        Returns True if a user_id is present.

        NOTE:
        - This does NOT authorize anything.
        """
        return self.user_id is not None

    def is_tenant_scoped(self) -> bool:
        """
        Returns True if a tenant_id is present.
        """
        return self.tenant_id is not None

    # --------------------------------------------------------
    # Serialization
    # --------------------------------------------------------

    def to_dict(self) -> dict[str, str | int | None]:
        """
        Deterministic dictionary representation.
        """
        return {
            "request_id": str(self.request_id),
            "correlation_id": str(self.correlation_id),
            "causation_id": (
                str(self.causation_id)
                if self.causation_id is not None
                else None
            ),
            "timestamp_ms": int(self.timestamp_ms),
            "tenant_id": (
                str(self.tenant_id)
                if self.tenant_id is not None
                else None
            ),
            "user_id": (
                str(self.user_id)
                if self.user_id is not None
                else None
            ),
        }
