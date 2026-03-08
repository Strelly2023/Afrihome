"""
GA Enterprise Core — Health Registry (In-Memory)
------------------------------------------------

LAYER: L3
Dependencies:
- core.typing
- core.errors
- core.kernel.invariants

Rules:
- In-memory only
- Deterministic ordering (registration order)
- No IO / No logging / No threads / No async
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Mapping, Optional, Protocol, Tuple, runtime_checkable

from core.errors import InvariantViolationError
from core.kernel.invariants import assert_not_none
from core.typing import UnixMillis


class HealthStatus(Enum):
    OK = auto()
    WARN = auto()
    FAIL = auto()


@dataclass(frozen=True, slots=True)
class HealthCheckResult:
    name: str
    status: HealthStatus
    timestamp_ms: UnixMillis
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        assert_not_none(self.name, "name")
        assert_not_none(self.status, "status")
        assert_not_none(self.timestamp_ms, "timestamp_ms")
        if self.timestamp_ms < 0:
            raise InvariantViolationError("timestamp_ms cannot be negative")


@runtime_checkable
class HealthCheck(Protocol):
    def __call__(self, now_ms: UnixMillis) -> HealthCheckResult: ...


class HealthRegistry:
    def __init__(self) -> None:
        self._checks: Dict[str, HealthCheck] = {}

    def register(self, name: str, check: HealthCheck) -> None:
        assert_not_none(name, "name")
        assert_not_none(check, "check")
        if name in self._checks:
            raise InvariantViolationError(f"Health check {name!r} already registered")
        self._checks[name] = check

    def unregister(self, name: str) -> None:
        assert_not_none(name, "name")
        if name not in self._checks:
            raise InvariantViolationError(f"Health check {name!r} not found")
        del self._checks[name]

    def get(self, name: str) -> Optional[HealthCheck]:
        return self._checks.get(name)

    def names(self) -> Tuple[str, ...]:
        return tuple(self._checks.keys())

    def run_all(self, now_ms: UnixMillis) -> Tuple[HealthCheckResult, ...]:
        if now_ms < 0:
            raise InvariantViolationError("now_ms cannot be negative")
        results = []
        for name in self._checks.keys():
            check = self._checks[name]
            res = check(now_ms)
            if res.name != name:
                raise InvariantViolationError(
                    f"Health check result name {res.name!r} does not match registered name {name!r}"
                )
            results.append(res)
        return tuple(results)
