from __future__ import annotations
#afritech/platform/core/errors/base.py
"""
GA Enterprise Core â€” Deterministic Error Hierarchy
--------------------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib only
Deterministic: YES
Infrastructure: NONE
Time access: NONE
UUID access: NONE

Rules:
- All core errors derive from CoreError
- Errors are mutable due to Python exception machinery
- Immutability is enforced by convention, not by frozen dataclasses
- Errors must be reproducible and deterministic
- No side effects beyond Python exception mechanics
"""

from typing import Optional, Mapping, Any
from types import MappingProxyType


# ============================================================
# Base Error (DO NOT make frozen or dataclass)
# ============================================================

class CoreError(Exception):
    """
    Root deterministic error for the entire GA core.

    IMPORTANT:
    - MUST remain mutable for Python exception machinery
    - Python WILL mutate __traceback__ during propagation

    Guarantees:
    - message: human-readable explanation (deterministic)
    - code: stable machine-readable identifier (REQUIRED)
    - cause: optional chained exception (deterministic if provided)
    - metadata: optional immutable diagnostic context (pure data)
    """

    __slots__ = ("message", "code", "cause", "metadata")

    def __init__(
        self,
        message: str,
        *,
        code: str,
        cause: Optional[BaseException] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        # --------------------------------------------------------
        # Deterministic validation
        # --------------------------------------------------------
        if not isinstance(message, str) or not message.strip():
            raise InvariantViolationError(
                "CoreError.message must be a non-empty string",
                metadata={"field": "message"},
            )

        if not isinstance(code, str) or not code.strip():
            raise InvariantViolationError(
                "CoreError.code must be a non-empty string",
                metadata={"field": "code"},
            )

        # --------------------------------------------------------
        # Base initialization
        # --------------------------------------------------------
        super().__init__(message)

        self.message = message.strip()
        self.code = code.strip()
        self.cause = cause

        # --------------------------------------------------------
        # Immutable metadata (defensive copy)
        # --------------------------------------------------------
        if metadata is None:
            self.metadata = MappingProxyType({})
        else:
            self.metadata = MappingProxyType(dict(metadata))

        # --------------------------------------------------------
        # Exception chaining (Python-native)
        # --------------------------------------------------------
        if cause is not None:
            self.__cause__ = cause

    # --------------------------------------------------------
    # Representations
    # --------------------------------------------------------

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"code={self.code!r}, "
            f"message={self.message!r}, "
            f"metadata={dict(self.metadata)!r}"
            f")"
        )

    # --------------------------------------------------------
    # Helpers (pure, no mutation)
    # --------------------------------------------------------

    def with_metadata(self, **extra: Any) -> "CoreError":
        """
        Return a new CoreError with merged metadata.

        NOTE:
        - Does NOT mutate the current instance
        - Maintains determinism
        """
        merged = dict(self.metadata)
        merged.update(extra)

        return CoreError(
            message=self.message,
            code=self.code,
            cause=self.cause,
            metadata=merged,
        )


# ============================================================
# Invariant / Validation Errors (NON-KERNEL)
# ============================================================

class InvariantViolationError(CoreError):
    """
    Raised when a domain or core invariant is violated.

    NOTE:
    - Kernel raises RuntimeError only
    - Core/domain layers wrap invariants using this error
    """

    def __init__(
        self,
        message: str = "Invariant violated",
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="INVARIANT_VIOLATION",
            metadata=metadata,
        )


class ValidationError(CoreError):
    """
    Input or structural validation failure.
    """

    def __init__(
        self,
        message: str = "Validation failed",
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            metadata=metadata,
        )


class GrammarViolationError(CoreError):
    """
    Raised when a grammar rule (regex authority) is violated.
    """

    def __init__(
        self,
        message: str = "Grammar violation",
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="GRAMMAR_VIOLATION",
            metadata=metadata,
        )


# ============================================================
# Authorization / Governance
# ============================================================

class AuthorizationError(CoreError):
    """
    Raised when access control denies execution.
    """

    def __init__(
        self,
        message: str = "Access denied",
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="AUTHORIZATION_DENIED",
            metadata=metadata,
        )


class TenantIsolationError(CoreError):
    """
    Raised when cross-tenant access is attempted.
    """

    def __init__(
        self,
        message: str = "Tenant isolation violation",
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="TENANT_ISOLATION_VIOLATION",
            metadata=metadata,
        )


# ============================================================
# Execution Discipline
# ============================================================

class StrictWriteViolationError(CoreError):
    """
    Raised when a write operation occurs outside strict write-mode.
    """

    def __init__(
        self,
        message: str = "Write operation outside strict write mode",
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="STRICT_WRITE_VIOLATION",
            metadata=metadata,
        )


class IdempotencyViolationError(CoreError):
    """
    Raised when idempotency constraints are violated.
    """

    def __init__(
        self,
        message: str = "Idempotency violation",
        *,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="IDEMPOTENCY_VIOLATION",
            metadata=metadata,
        )


# ============================================================
# Public ABI (explicit, frozen)
# ============================================================

__all__ = [
    "CoreError",
    "InvariantViolationError",
    "ValidationError",
    "GrammarViolationError",
    "AuthorizationError",
    "TenantIsolationError",
    "StrictWriteViolationError",
    "IdempotencyViolationError",
]
