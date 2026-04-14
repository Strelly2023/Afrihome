"""
GA Enterprise Core â€” Quota Engine
--------------------------------

LAYER: L2 (Pure Engine)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose the frozen public API of the quota engine
- Provide deterministic, replay-safe quota evaluation primitives

Rules:
- Public API is defined ONLY via __all__
- No kernel or foundation dependencies
- No IO, persistence, or clock access
"""

from afritech.platform.core.quota.grammar import (
    UNITS,
    SCOPES,
    DIMENSIONS,
    validate_unit,
    validate_scope,
    validate_dimension,
)

from afritech.platform.core.quota.definition import QuotaDefinition
from afritech.platform.core.quota.snapshot import QuotaSnapshot
from afritech.platform.core.quota.decision import QuotaDecision
from afritech.platform.core.quota.evaluation import QuotaEvaluator
from afritech.platform.core.quota.errors import (
    QuotaError,
    InvalidQuotaDefinitionError,
    InvalidQuotaSnapshotError,
    QuotaEvaluationError,
)

# ============================================================
# Quota Public ABI (Frozen)
# ============================================================

__all__ = [
    # Grammar
    "UNITS",
    "SCOPES",
    "DIMENSIONS",
    "validate_unit",
    "validate_scope",
    "validate_dimension",

    # Quota models
    "QuotaDefinition",
    "QuotaSnapshot",
    "QuotaDecision",

    # Evaluation engine
    "QuotaEvaluator",

    # Errors
    "QuotaError",
    "InvalidQuotaDefinitionError",
    "InvalidQuotaSnapshotError",
    "QuotaEvaluationError",
]
