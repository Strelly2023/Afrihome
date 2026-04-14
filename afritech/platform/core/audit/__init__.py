"""
GA Enterprise Core â€” Audit Engine
--------------------------------

LAYER: L2 (Pure Engine)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose the frozen public API of the audit engine
- Provide immutable, replay-safe audit artifacts
- Enable explainable authorization decisions

Rules:
- Public API is defined ONLY via __all__
- No kernel or foundation dependencies
- No IO, persistence, verification, or identity mapping
"""

from afritech.platform.core.audit.decision import AuditDecision
from afritech.platform.core.audit.trace import AuditTrace
from afritech.platform.core.audit.explanation import AuditExplanation
from afritech.platform.core.audit.composer import AuditComposer
from afritech.platform.core.audit.governance_record import GovernanceRecord
from afritech.platform.core.audit.errors import (
    AuditError,
    InvalidAuditDecisionError,
    InvalidAuditTraceError,
    AuditCompositionError,
)

# ============================================================
# Audit Public ABI (Frozen)
# ============================================================

__all__ = [
    # Core audit artifacts
    "AuditDecision",
    "AuditTrace",
    "AuditExplanation",
    "GovernanceRecord",

    # Composition
    "AuditComposer",

    # Errors
    "AuditError",
    "InvalidAuditDecisionError",
    "InvalidAuditTraceError",
    "AuditCompositionError",
]
