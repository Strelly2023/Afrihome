
"""
GA Enterprise Core — Health Diagnostics (Deterministic)
-------------------------------------------------------

LAYER: L3
Dependencies:
- core.health.registry
- core.typing
- core.kernel.invariants

Rules:
- No IO / No logging / No threads / No async
- Pure summarization; timestamps injected by caller
"""


from dataclasses import dataclass
from typing import Mapping, Dict, Tuple

from core.health.registry import HealthStatus, HealthCheckResult, HealthRegistry
from core.typing import UnixMillis
from core.kernel.invariants import assert_not_none


_STATUS_RANK = {
    HealthStatus.OK: 0,
    HealthStatus.WARN: 1,
    HealthStatus.FAIL: 2,
}


def summarize_status(results: Tuple[HealthCheckResult, ...]) -> HealthStatus:
    worst = HealthStatus.OK
    for r in results:
        if _STATUS_RANK[r.status] > _STATUS_RANK[worst]:
            worst = r.status
            if worst is HealthStatus.FAIL:
                break
    return worst


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    generated_ms: UnixMillis
    overall: HealthStatus
    results: Tuple[HealthCheckResult, ...]
    counts: Dict[str, int]

    def to_dict(self) -> Dict[str, object]:
        return {
            "generated_ms": int(self.generated_ms),
            "overall": self.overall.name,
            "counts": dict(self.counts),
            "results": [
                {
                    "name": r.name,
                    "status": r.status.name,
                    "timestamp_ms": int(r.timestamp_ms),
                    "details": dict(r.details),
                }
                for r in self.results
            ],
        }


def run_diagnostics(registry: HealthRegistry, now_ms: UnixMillis) -> DiagnosticReport:
    assert_not_none(registry, "registry")
    results = registry.run_all(now_ms)
    overall = summarize_status(results)
    counts: Dict[str, int] = {"OK": 0, "WARN": 0, "FAIL": 0}
    for r in results:
        counts[r.status.name] += 1
    return DiagnosticReport(generated_ms=now_ms, overall=overall, results=results, counts=counts)
