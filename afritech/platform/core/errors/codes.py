from __future__ import annotations

"""
GA Enterprise Core â€” Error Codes (GA-Sealed)
-------------------------------------------

This module defines the canonical, machine-readable error codes used
throughout afritech.platform.core.

Error codes are:
- Stable identifiers (never change meaning)
- Used for programmatic handling, audit, and telemetry
- Independent of human-readable messages
- Shared across engines, governance, and control-plane layers

RULES:
- Constants ONLY (no functions, no classes)
- NO execution
- NO IO
- NO time
- NO imports outside stdlib
- Values MUST remain stable unless changed via ADR

Any change to this file requires an ADR.
"""

from typing import Final


# ============================================================
# Generic / Cross-Cutting Errors
# ============================================================

INVARIANT_VIOLATION: Final[str] = "INVARIANT_VIOLATION"
VALIDATION_ERROR: Final[str] = "VALIDATION_ERROR"
GRAMMAR_VIOLATION: Final[str] = "GRAMMAR_VIOLATION"


# ============================================================
# Authorization / Governance Errors
# ============================================================

AUTHORIZATION_DENIED: Final[str] = "AUTHORIZATION_DENIED"
TENANT_ISOLATION_VIOLATION: Final[str] = "TENANT_ISOLATION_VIOLATION"


# ============================================================
# Execution Discipline Errors
# ============================================================

STRICT_WRITE_VIOLATION: Final[str] = "STRICT_WRITE_VIOLATION"
IDEMPOTENCY_VIOLATION: Final[str] = "IDEMPOTENCY_VIOLATION"


# ============================================================
# RBAC Errors
# ============================================================

RBAC_INVALID_ROLE: Final[str] = "RBAC_INVALID_ROLE"
RBAC_PERMISSION_DENIED: Final[str] = "RBAC_PERMISSION_DENIED"
RBAC_INVALID_ASSIGNMENT: Final[str] = "RBAC_INVALID_ASSIGNMENT"


# ============================================================
# Policy Errors
# ============================================================

POLICY_INVALID_DEFINITION: Final[str] = "POLICY_INVALID_DEFINITION"
POLICY_EVALUATION_FAILED: Final[str] = "POLICY_EVALUATION_FAILED"


# ============================================================
# Quota Errors
# ============================================================

QUOTA_INVALID_DEFINITION: Final[str] = "QUOTA_INVALID_DEFINITION"
QUOTA_INVALID_SNAPSHOT: Final[str] = "QUOTA_INVALID_SNAPSHOT"
QUOTA_LIMIT_EXCEEDED: Final[str] = "QUOTA_LIMIT_EXCEEDED"


# ============================================================
# Risk Errors
# ============================================================

RISK_INVALID_DEFINITION: Final[str] = "RISK_INVALID_DEFINITION"
RISK_INVALID_SNAPSHOT: Final[str] = "RISK_INVALID_SNAPSHOT"
RISK_EVALUATION_FAILED: Final[str] = "RISK_EVALUATION_FAILED"


# ============================================================
# Consent Errors
# ============================================================

CONSENT_INVALID_DEFINITION: Final[str] = "CONSENT_INVALID_DEFINITION"
CONSENT_INVALID_SNAPSHOT: Final[str] = "CONSENT_INVALID_SNAPSHOT"
CONSENT_EVALUATION_FAILED: Final[str] = "CONSENT_EVALUATION_FAILED"


# ============================================================
# Audit Errors
# ============================================================

AUDIT_INVALID_DECISION: Final[str] = "AUDIT_INVALID_DECISION"
AUDIT_INVALID_TRACE: Final[str] = "AUDIT_INVALID_TRACE"
AUDIT_COMPOSITION_FAILED: Final[str] = "AUDIT_COMPOSITION_FAILED"


# ============================================================
# Frozen Public ABI
# ============================================================

__all__ = [
    # Generic
    "INVARIANT_VIOLATION",
    "VALIDATION_ERROR",
    "GRAMMAR_VIOLATION",

    # Authorization / Governance
    "AUTHORIZATION_DENIED",
    "TENANT_ISOLATION_VIOLATION",

    # Execution discipline
    "STRICT_WRITE_VIOLATION",
    "IDEMPOTENCY_VIOLATION",

    # RBAC
    "RBAC_INVALID_ROLE",
    "RBAC_PERMISSION_DENIED",
    "RBAC_INVALID_ASSIGNMENT",

    # Policy
    "POLICY_INVALID_DEFINITION",
    "POLICY_EVALUATION_FAILED",

    # Quota
    "QUOTA_INVALID_DEFINITION",
    "QUOTA_INVALID_SNAPSHOT",
    "QUOTA_LIMIT_EXCEEDED",

    # Risk
    "RISK_INVALID_DEFINITION",
    "RISK_INVALID_SNAPSHOT",
    "RISK_EVALUATION_FAILED",

    # Consent
    "CONSENT_INVALID_DEFINITION",
    "CONSENT_INVALID_SNAPSHOT",
    "CONSENT_EVALUATION_FAILED",

    # Audit
    "AUDIT_INVALID_DECISION",
    "AUDIT_INVALID_TRACE",
    "AUDIT_COMPOSITION_FAILED",
]
