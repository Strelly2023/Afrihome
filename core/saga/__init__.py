"""
GA Enterprise Core — Saga (Deterministic Coordination)

LAYER: L2

Purpose:
- Immutable saga state model
- Pure state transitions
- Deterministic coordination (no timers/scheduling)
"""

from .manager import (
    AbortSaga,
    BeginCompensation,
    SagaEffects,
    SagaManager,
    SagaSignal,
    StartSaga,
    StepCompensated,
    StepFailed,
    StepSucceeded,
)
from .state import (
    SagaSnapshot,
    SagaStatus,
    SagaStep,
    StepStatus,
    new_saga,
)

__all__ = [
    "SagaStatus",
    "StepStatus",
    "SagaStep",
    "SagaSnapshot",
    "new_saga",
    "SagaSignal",
    "StartSaga",
    "StepSucceeded",
    "StepFailed",
    "BeginCompensation",
    "StepCompensated",
    "AbortSaga",
    "SagaEffects",
    "SagaManager",
]
