
from __future__ import annotations
# afritech/platform/core/typing/enums.py
"""
GA Enterprise Core â€” Canonical Enums
----------------------------------

LAYER: L1.5 (Shared Semantic Types)
Dependencies: stdlib only
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define canonical, closed semantic domains used across the core
- Replace fragile string-based domains with type-safe enumerations
- Ensure consistency across decision, audit, consent, and contracts

Design Principles:
- Enums represent CLOSED sets (no runtime extension)
- Enums are STRING-backed for compatibility and serialization
- Enums contain NO business logic
- Validation remains grammar-authoritative where applicable

GA RULES:
- MUST remain stable once GA-sealed
- MUST be reused across modules (no duplication)
- MUST NOT introduce dependency cycles
- Strings are allowed ONLY at construction boundaries
"""

from enum import Enum
from typing import Final, Tuple, TypeVar


# ============================================================
# Base Enum (shared behavior)
# ============================================================

_S = TypeVar("_S", bound="_StrEnum")


class _StrEnum(str, Enum):
    """
    Base class for all string-backed canonical enums.

    Guarantees:
    - Stable string representation
    - Safe comparison with raw strings
    - Deterministic serialization
    - Closed semantic domain

    Allowed:
    - Boundary normalization
    - Fast validation helpers

    Forbidden:
    - Business logic
    - Side effects
    - External dependencies
    """

    # NOTE:
    # This cache is PER-SUBCLASS.
    # It is initialized lazily and MUST NOT be accessed directly.
    _VALUES: Final[set[str]]

    def __str__(self) -> str:
        return self.value

    # --------------------------------------------------------
    # Internal helpers (pure)
    # --------------------------------------------------------

    @classmethod
    def _value_set(cls) -> set[str]:
        """
        Cached set of valid enum values (O(1) membership).

        Safe because:
        - Initialized lazily
        - Scoped per enum subclass
        - Enum membership is immutable post-GA
        """
        if "_VALUES" not in cls.__dict__:
            cls._VALUES = {member.value for member in cls}
        return cls._VALUES

    # --------------------------------------------------------
    # Boundary normalization (PUBLIC, GA-FROZEN)
    # --------------------------------------------------------

    @classmethod
    def normalize(cls: type[_S], value: str | _S) -> str:
        """
        Normalize a boundary value to its canonical string form.

        Accepts:
        - enum instance
        - canonical string value

        Returns:
            canonical string value

        Raises:
            ValueError if the value is invalid

        NOTE:
        - Intended ONLY for boundary normalization
        - Internal code MUST operate on enum instances
        """
        if isinstance(value, cls):
            return value.value

        if isinstance(value, str):
            candidate = value.strip()
            if candidate in cls._value_set():
                return candidate

        raise ValueError(f"Invalid value for {cls.__name__}: {value!r}")

    @classmethod
    def is_valid(cls: type[_S], value: str | _S) -> bool:
        """
        Fast, non-throwing validation helper.
        """
        if isinstance(value, cls):
            return True

        if isinstance(value, str):
            return value.strip() in cls._value_set()

        return False

    @classmethod
    def values(cls) -> Tuple[str, ...]:
        """
        Deterministic ordered values.

        Intended for:
        - ABI snapshot tests
        - Documentation
        - Schema publication
        """
        return tuple(member.value for member in cls)


# ============================================================
# Engine Identity
# ============================================================

class EngineId(_StrEnum):
    """
    Canonical identifiers for decision engines.

    Used by:
    - decision layer (engine attribution)
    - audit layer (trace source)
    - contracts and registry metadata

    This is a CLOSED set and GA-sealed.
    """

    RBAC = "rbac"
    POLICY = "policy"
    QUOTA = "quota"
    RISK = "risk"
    CONSENT = "consent"
    AUDIT = "audit"
    COMBINED = "combined"


# ============================================================
# Effects (rule-level outcome)
# ============================================================

class Effect(_StrEnum):
    """
    Rule-level effect.

    Used by:
    - decision traces
    - audit traces

    NOTE:
    - This is NOT a final decision verdict
    - Effects describe *local rule outcomes*
    """

    ALLOW = "allow"
    DENY = "deny"


# ============================================================
# Decision Verdict (final outcome)
# ============================================================

class DecisionVerdictType(_StrEnum):
    """
    Canonical decision verdicts.

    Used by:
    - decision layer ONLY
    - combinator logic
    - replay and audit alignment

    MUST align with:
    afritech.platform.core.decision.DecisionVerdict
    """

    ALLOW = "allow"
    DENY = "deny"
    CONDITIONAL = "conditional"


# ============================================================
# Consent State
# ============================================================

class ConsentState(_StrEnum):
    """
    Consent lifecycle state.

    Mirrors consent grammar while providing type safety.

    NOTE:
    - Grammar remains authoritative for validation
    """

    GRANTED = "granted"
    REVOKED = "revoked"
    EXPIRED = "expired"


# ============================================================
# Optional: Reason Categories (NON-BINDING)
# ============================================================

class ReasonCategory(_StrEnum):
    """
    High-level categorization of decision reasons.

    Characteristics:
    - OPTIONAL
    - NON-BINDING
    - For analytics, grouping, and reporting only

    DO NOT enforce as a strict contract at GA.
    """

    RBAC = "rbac"
    POLICY = "policy"
    QUOTA = "quota"
    RISK = "risk"
    CONSENT = "consent"
    SYSTEM = "system"

# ============================================================
# System Lifecycle
# ============================================================

class SystemLifecycleState(_StrEnum):
    """
    High-level lifecycle state of the platform or subsystem.

    Used by:
    - control-plane
    - governance checks
    - operational gating

    NOT a decision verdict.
    """

    INITIALIZING = "initializing"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DECOMMISSIONED = "decommissioned"


# ============================================================
# Kernel State
# ============================================================

class KernelState(_StrEnum):
    """
    Kernel authority state.

    Reflects the GA sealing lifecycle of the kernel (L0).
    """

    OPEN = "open"
    FROZEN = "frozen"
    SEALED = "sealed"


# ============================================================
# Execution Mode
# ============================================================

class ExecutionMode(_StrEnum):
    """
    Runtime execution posture.

    Used for:
    - environment signaling
    - enforcement intensity
    - diagnostics vs production

    Must NOT branch business logic.
    """

    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


# ============================================================
# System Health
# ============================================================

class SystemHealthStatus(_StrEnum):
    """
    Coarse-grained health status indicator.

    Intended for observability and reporting ONLY.
    """

    OK = "ok"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


# ============================================================
# Feature Flag State
# ============================================================

class FeatureFlagState(_StrEnum):
    """
    Feature enablement state.

    This enum is declarative only.
    Rollout mechanics live outside core.
    """

    DISABLED = "disabled"
    ENABLED = "enabled"
    GATED = "gated"


# ============================================================
# Data Lifecycle
# ============================================================

class DataLifecycleState(_StrEnum):
    """
    Data governance lifecycle state.

    Used for:
    - retention logic
    - compliance signaling
    - audit classification
    """

    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
# ============================================================
# Public ABI (EXPLICIT + FROZEN)
# ============================================================
__all__ = [
    # Existing enums
    "EngineId",
    "Effect",
    "DecisionVerdictType",
    "ConsentState",
    "ReasonCategory",

    # System-level states (GA-safe additions)
    "SystemLifecycleState",
    "KernelState",
    "ExecutionMode",
    "SystemHealthStatus",
    "FeatureFlagState",
    "DataLifecycleState",
]
