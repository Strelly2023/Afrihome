
"""
GA Enterprise Core — Saga State (Immutable, Pure)
-------------------------------------------------

LAYER: L2
Dependencies:
- core.typing
- core.kernel.invariants
- core.errors

Rules:
- Immutable dataclasses
- Pure transitions (return new instances)
- No timers, no scheduling (time injected)
- No IO/logging/threads
"""


from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, Mapping, Any

from core.typing import AggregateId, Version, UnixMillis, CorrelationId, CausationId
from core.kernel.invariants import assert_not_none
from core.errors import InvariantViolationError


class StepStatus(Enum):
    PENDING = auto()
    DONE = auto()
    FAILED = auto()
    COMPENSATING = auto()
    COMPENSATED = auto()
    SKIPPED = auto()


class SagaStatus(Enum):
    INIT = auto()
    RUNNING = auto()
    FAILED = auto()
    COMPENSATING = auto()
    COMPLETED = auto()


@dataclass(frozen=True, slots=True)
class SagaStep:
    name: str
    status: StepStatus = StepStatus.PENDING

    def __post_init__(self) -> None:
        if not self.name:
            raise InvariantViolationError("SagaStep.name must not be empty")


@dataclass(frozen=True, slots=True)
class SagaSnapshot:
    saga_id: AggregateId
    status: SagaStatus
    version: Version
    steps: Tuple[SagaStep, ...]
    started_ms: UnixMillis
    updated_ms: UnixMillis
    correlation_id: CorrelationId
    causation_id: CausationId
    error: Optional[str] = None
    context: Optional[Mapping[str, Any]] = None

    def __post_init__(self) -> None:
        assert_not_none(self.saga_id, "saga_id")
        assert_not_none(self.status, "status")
        assert_not_none(self.version, "version")
        assert_not_none(self.steps, "steps")
        assert_not_none(self.started_ms, "started_ms")
        assert_not_none(self.updated_ms, "updated_ms")
        assert_not_none(self.correlation_id, "correlation_id")
        assert_not_none(self.causation_id, "causation_id")
        if int(self.version) < 0:
            raise InvariantViolationError("version cannot be negative")
        if self.started_ms < 0 or self.updated_ms < 0:
            raise InvariantViolationError("timestamps cannot be negative")
        if self.updated_ms < self.started_ms:
            raise InvariantViolationError("updated_ms cannot be earlier than started_ms")

    def _with(
        self,
        *,
        status: Optional[SagaStatus] = None,
        steps: Optional[Tuple[SagaStep, ...]] = None,
        updated_ms: Optional[UnixMillis] = None,
        error: Optional[Optional[str]] = None,
        context: Optional[Optional[Mapping[str, Any]]] = None,
        bump_version: bool = True,
    ) -> "SagaSnapshot":
        v = Version(int(self.version) + 1) if bump_version else self.version
        return SagaSnapshot(
            saga_id=self.saga_id,
            status=status if status is not None else self.status,
            version=v,
            steps=steps if steps is not None else self.steps,
            started_ms=self.started_ms,
            updated_ms=updated_ms if updated_ms is not None else self.updated_ms,
            correlation_id=self.correlation_id,
            causation_id=self.causation_id,
            error=(error if error is not None else self.error),
            context=(context if context is not None else self.context),
        )

    def _replace_step(self, name: str, new_status: StepStatus) -> Tuple[SagaStep, ...]:
        found = False
        new_steps = []
        for s in self.steps:
            if s.name == name:
                new_steps.append(SagaStep(name=s.name, status=new_status))
                found = True
            else:
                new_steps.append(s)
        if not found:
            raise InvariantViolationError(f"Step {name!r} not found in saga")
        return tuple(new_steps)

    def start(self, now_ms: UnixMillis) -> "SagaSnapshot":
        if self.status != SagaStatus.INIT:
            raise InvariantViolationError("Saga can only start from INIT")
        return self._with(status=SagaStatus.RUNNING, updated_ms=now_ms)

    def step_done(self, name: str, now_ms: UnixMillis) -> "SagaSnapshot":
        if self.status != SagaStatus.RUNNING:
            raise InvariantViolationError("step_done only allowed in RUNNING")
        steps = self._replace_step(name, StepStatus.DONE)
        new_status = SagaStatus.COMPLETED if all(s.status == StepStatus.DONE for s in steps) else SagaStatus.RUNNING
        return self._with(status=new_status, steps=steps, updated_ms=now_ms)

    def step_failed(self, name: str, error: str, now_ms: UnixMillis) -> "SagaSnapshot":
        if self.status not in (SagaStatus.RUNNING, SagaStatus.COMPENSATING):
            raise InvariantViolationError("step_failed allowed only in RUNNING/COMPENSATING")
        steps = self._replace_step(name, StepStatus.FAILED)
        return self._with(status=SagaStatus.FAILED, steps=steps, updated_ms=now_ms, error=error)

    def begin_compensation(self, now_ms: UnixMillis) -> "SagaSnapshot":
        if self.status != SagaStatus.FAILED:
            raise InvariantViolationError("begin_compensation only allowed from FAILED")
        return self._with(status=SagaStatus.COMPENSATING, updated_ms=now_ms)

    def mark_compensating(self, name: str, now_ms: UnixMillis) -> "SagaSnapshot":
        if self.status != SagaStatus.COMPENSATING:
            raise InvariantViolationError("mark_compensating only allowed in COMPENSATING")
        steps = self._replace_step(name, StepStatus.COMPENSATING)
        return self._with(steps=steps, updated_ms=now_ms)

    def step_compensated(self, name: str, now_ms: UnixMillis) -> "SagaSnapshot":
        if self.status != SagaStatus.COMPENSATING:
            raise InvariantViolationError("step_compensated only allowed in COMPENSATING")
        steps = self._replace_step(name, StepStatus.COMPENSATED)
        new_status = SagaStatus.COMPLETED if all(s.status in (StepStatus.COMPENSATED, StepStatus.PENDING, StepStatus.SKIPPED) for s in steps) else SagaStatus.COMPENSATING
        return self._with(status=new_status, steps=steps, updated_ms=now_ms)

    def with_context(self, ctx: Mapping[str, Any], now_ms: UnixMillis) -> "SagaSnapshot":
        return self._with(context=ctx, updated_ms=now_ms)

    def with_correlation(self, correlation_id: CorrelationId, causation_id: CausationId, now_ms: UnixMillis) -> "SagaSnapshot":
        return SagaSnapshot(
            saga_id=self.saga_id,
            status=self.status,
            version=Version(int(self.version) + 1),
            steps=self.steps,
            started_ms=self.started_ms,
            updated_ms=now_ms,
            correlation_id=correlation_id,
            causation_id=causation_id,
            error=self.error,
            context=self.context,
        )


def new_saga(
    *,
    saga_id: AggregateId,
    steps: Tuple[str, ...],
    started_ms: UnixMillis,
    correlation_id: CorrelationId,
    causation_id: CausationId,
    context: Optional[Mapping[str, Any]] = None,
) -> SagaSnapshot:
    assert_not_none(saga_id, "saga_id")
    if started_ms < 0:
        raise InvariantViolationError("started_ms cannot be negative")
    step_objs = tuple(SagaStep(name=s) for s in steps)
    return SagaSnapshot(
        saga_id=saga_id,
        status=SagaStatus.INIT,
        version=Version(0),
        steps=step_objs,
        started_ms=started_ms,
        updated_ms=started_ms,
        correlation_id=correlation_id,
        causation_id=causation_id,
        error=None,
        context=context,
    )
