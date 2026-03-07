
"""
GA Enterprise Core — Saga (Deterministic Coordination)

LAYER: L2

Purpose:
- Immutable saga state model
- Pure state transitions
- Deterministic coordination (no timers/scheduling)
"""

from .state import (
    SagaStatus,
    StepStatus,
    SagaStep,
    SagaSnapshot,
    new_saga,
)

from .manager import (
    SagaSignal,
    StartSaga,
    StepSucceeded,
    StepFailed,
    BeginCompensation,
    StepCompensated,
    AbortSaga,
    SagaEffects,
    SagaManager,
)

__all__ = [
    "SagaStatus", "StepStatus", "SagaStep", "SagaSnapshot", "new_saga",
    "SagaSignal", "StartSaga", "StepSucceeded", "StepFailed", "BeginCompensation", "StepCompensated", "AbortSaga",
    "SagaEffects", "SagaManager",
]
