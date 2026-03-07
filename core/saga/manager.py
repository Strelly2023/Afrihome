
"""
GA Enterprise Core — Saga Manager (Pure Coordinator)
----------------------------------------------------

LAYER: L2
Dependencies:
- core.saga.state
- core.typing
- core.kernel.invariants
- core.errors

Rules:
- Pure state machine (no IO/threads/async)
- No timers or scheduling (time injected via now_ms)
- Deterministic effects (pure data only)
"""


from dataclasses import dataclass
from typing import Mapping, Any, Tuple, List

from core.saga.state import (
    SagaSnapshot,
    SagaStatus,
)
from core.typing import UnixMillis
from core.kernel.invariants import assert_not_none
from core.errors import InvariantViolationError


class SagaSignal:
    pass


@dataclass(frozen=True, slots=True)
class StartSaga(SagaSignal):
    pass


@dataclass(frozen=True, slots=True)
class StepSucceeded(SagaSignal):
    step_name: str


@dataclass(frozen=True, slots=True)
class StepFailed(SagaSignal):
    step_name: str
    error: str


@dataclass(frozen=True, slots=True)
class BeginCompensation(SagaSignal):
    pass


@dataclass(frozen=True, slots=True)
class StepCompensated(SagaSignal):
    step_name: str


@dataclass(frozen=True, slots=True)
class AbortSaga(SagaSignal):
    reason: str


@dataclass(frozen=True, slots=True)
class SagaEffects:
    emitted: Tuple[Mapping[str, Any], ...] = ()

    @staticmethod
    def emit(event_type: str, payload: Mapping[str, Any]) -> "SagaEffects":
        return SagaEffects(emitted=({"type": event_type, "payload": dict(payload)},))

    @staticmethod
    def combine(*effects: "SagaEffects") -> "SagaEffects":
        acc: List[Mapping[str, Any]] = []
        for e in effects:
            acc.extend(e.emitted)
        return SagaEffects(emitted=tuple(acc))


class SagaManager:
    def apply(self, state: SagaSnapshot, signal: SagaSignal, now_ms: UnixMillis) -> Tuple[SagaSnapshot, SagaEffects]:
        assert_not_none(state, "state")
        assert_not_none(signal, "signal")
        assert_not_none(now_ms, "now_ms")
        if isinstance(signal, StartSaga):
            return self._start(state, now_ms)
        if isinstance(signal, StepSucceeded):
            return self._step_succeeded(state, signal.step_name, now_ms)
        if isinstance(signal, StepFailed):
            return self._step_failed(state, signal.step_name, signal.error, now_ms)
        if isinstance(signal, BeginCompensation):
            return self._begin_compensation(state, now_ms)
        if isinstance(signal, StepCompensated):
            return self._step_compensated(state, signal.step_name, now_ms)
        if isinstance(signal, AbortSaga):
            return self._abort(state, signal.reason, now_ms)
        raise InvariantViolationError(f"Unknown signal: {type(signal).__name__}")

    def _start(self, s: SagaSnapshot, now_ms: UnixMillis) -> Tuple[SagaSnapshot, SagaEffects]:
        ns = s.start(now_ms)
        eff = SagaEffects.emit("saga.started", {"saga_id": str(s.saga_id), "ts": int(now_ms)})
        return ns, eff

    def _step_succeeded(self, s: SagaSnapshot, name: str, now_ms: UnixMillis) -> Tuple[SagaSnapshot, SagaEffects]:
        ns = s.step_done(name, now_ms)
        evt = SagaEffects.emit("saga.step.succeeded", {"saga_id": str(s.saga_id), "step": name, "ts": int(now_ms)})
        if ns.status == SagaStatus.COMPLETED and s.status != SagaStatus.COMPLETED:
            done = SagaEffects.emit("saga.completed", {"saga_id": str(s.saga_id), "ts": int(now_ms)})
            return ns, SagaEffects.combine(evt, done)
        return ns, evt

    def _step_failed(self, s: SagaSnapshot, name: str, error: str, now_ms: UnixMillis) -> Tuple[SagaSnapshot, SagaEffects]:
        ns = s.step_failed(name, error, now_ms)
        evt = SagaEffects.emit("saga.step.failed", {"saga_id": str(s.saga_id), "step": name, "error": error, "ts": int(now_ms)})
        return ns, evt

    def _begin_compensation(self, s: SagaSnapshot, now_ms: UnixMillis) -> Tuple[SagaSnapshot, SagaEffects]:
        ns = s.begin_compensation(now_ms)
        evt = SagaEffects.emit("saga.compensation.started", {"saga_id": str(s.saga_id), "ts": int(now_ms)})
        return ns, evt

    def _step_compensated(self, s: SagaSnapshot, name: str, now_ms: UnixMillis) -> Tuple[SagaSnapshot, SagaEffects]:
        ns = s.step_compensated(name, now_ms)
        evt = SagaEffects.emit("saga.step.compensated", {"saga_id": str(s.saga_id), "step": name, "ts": int(now_ms)})
        if ns.status == SagaStatus.COMPLETED and s.status != SagaStatus.COMPLETED:
            done = SagaEffects.emit("saga.completed", {"saga_id": str(s.saga_id), "ts": int(now_ms)})
            return ns, SagaEffects.combine(evt, done)
        return ns, evt

    def _abort(self, s: SagaSnapshot, reason: str, now_ms: UnixMillis) -> Tuple[SagaSnapshot, SagaEffects]:
        ns = s._with(status=SagaStatus.FAILED, updated_ms=now_ms, error=reason)
        evt = SagaEffects.emit("saga.aborted", {"saga_id": str(s.saga_id), "reason": reason, "ts": int(now_ms)})
        return ns, evt
