"""
GA Enterprise Core â€” Risk Engine
--------------------------------

LAYER: L2 (Pure Engine)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose the frozen public API of the risk engine
- Provide deterministic, replay-safe risk scoring primitives

Rules:
- Public API is defined ONLY via __all__
- No kernel or foundation dependencies
- No IO, persistence, clocks, or randomness
"""

from afritech.platform.core.risk.grammar import (
    SIGNALS,
    SCORE_MIN,
    SCORE_MAX,
    BANDS,
    validate_signal,
    validate_score,
    validate_band,
)

from afritech.platform.core.risk.signal import RiskSignal
from afritech.platform.core.risk.definition import RiskDefinition
from afritech.platform.core.risk.snapshot import RiskSnapshot
from afritech.platform.core.risk.decision import RiskDecision
from afritech.platform.core.risk.evaluation import RiskEvaluator
from afritech.platform.core.risk.errors import (
    RiskError,
    InvalidRiskDefinitionError,
    InvalidRiskSnapshotError,
    RiskEvaluationError,
)

# ============================================================
# Risk Public ABI (Frozen)
# ============================================================

__all__ = [
    # Grammar
    "SIGNALS",
    "SCORE_MIN",
    "SCORE_MAX",
    "BANDS",
    "validate_signal",
    "validate_score",
    "validate_band",

    # Risk models
    "RiskSignal",
    "RiskDefinition",
    "RiskSnapshot",
    "RiskDecision",

    # Evaluation engine
    "RiskEvaluator",

    # Errors
    "RiskError",
    "InvalidRiskDefinitionError",
    "InvalidRiskSnapshotError",
    "RiskEvaluationError",
]
