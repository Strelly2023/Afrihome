
"""
GA Enterprise Core — Deterministic Error Hierarchy
--------------------------------------------------

LAYER: L0 (Bedrock)
Dependencies: stdlib only
Deterministic: YES
Infrastructure: NONE
Time access: NONE
UUID access: NONE

Rules:
- All core errors must derive from CoreError.
- Errors must be immutable.
- Errors must be reproducible (no dynamic message mutation).
- No side effects.
"""


from dataclasses import dataclass
from typing import Optional


# ============================================================
# Base Error
# ============================================================

@dataclass(frozen=True, slots=True)
class CoreError(Exception):
    """
    Root deterministic error for the entire GA core.

    Invariants:
    - Immutable (frozen dataclass + slots)
    - Deterministic message and code
    - No contextual mutation or ambient state
    - stdlib-only (L0-safe)
    """

    message: str
    code: str
    cause: Optional[BaseException] = None

    def __post_init__(self) -> None:
        # Ensure Exception machinery is correctly populated deterministically.
        object.__setattr__(self, "args", (self.message,))
        if self.cause is not None:
            object.__setattr__(self, "__cause__", self.cause)

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


# ============================================================
# Kernel Errors
# ============================================================

class KernelFrozenError(CoreError):
    """Raised when mutation occurs after kernel freeze."""

    def __init__(self, message: str = "Kernel is frozen and cannot be modified"):
        super().__init__(message=message, code="KERNEL_FROZEN")


class InvariantViolationError(CoreError):
    """Raised when a kernel invariant is violated."""

    def __init__(self, message: str):
        super().__init__(message=message, code="INVARIANT_VIOLATION")


# ============================================================
# Validation Errors
# ============================================================

class ValidationError(CoreError):
    """Input or structural validation failure."""

    def __init__(self, message: str):
        super().__init__(message=message, code="VALIDATION_ERROR")


class GrammarViolationError(CoreError):
    """Raised when a grammar rule (regex authority) is violated."""

    def __init__(self, message: str):
        super().__init__(message=message, code="GRAMMAR_VIOLATION")


# ============================================================
# Authorization / Governance
# ============================================================

class AuthorizationError(CoreError):
    """Raised when access control denies execution."""

    def __init__(self, message: str = "Access denied"):
        super().__init__(message=message, code="AUTHORIZATION_DENIED")


class TenantIsolationError(CoreError):
    """Raised when cross-tenant access is attempted."""

    def __init__(self, message: str = "Tenant isolation violation"):
        super().__init__(message=message, code="TENANT_ISOLATION_VIOLATION")


# ============================================================
# Execution Discipline
# ============================================================

class StrictWriteViolationError(CoreError):
    """Raised when write operation occurs outside strict write-mode."""

    def __init__(self, message: str = "Write operation outside strict write mode"):
        super().__init__(message=message, code="STRICT_WRITE_VIOLATION")


class IdempotencyViolationError(CoreError):
    """Raised when idempotency constraints are violated."""

    def __init__(self, message: str):
        super().__init__(message=message, code="IDEMPOTENCY_VIOLATION")
