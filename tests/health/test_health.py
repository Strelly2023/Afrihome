
from core.health import HealthStatus, HealthCheckResult, HealthRegistry, run_diagnostics
from core.typing import UnixMillis


def _ok(now_ms: UnixMillis) -> HealthCheckResult:
    return HealthCheckResult(name='ok', status=HealthStatus.OK, timestamp_ms=now_ms, details={'v': 1})

def _warn(now_ms: UnixMillis) -> HealthCheckResult:
    return HealthCheckResult(name='warn', status=HealthStatus.WARN, timestamp_ms=now_ms, details={})

def _fail(now_ms: UnixMillis) -> HealthCheckResult:
    return HealthCheckResult(name='fail', status=HealthStatus.FAIL, timestamp_ms=now_ms, details={'err': 'x'})


def test_health_registry_and_diagnostics():
    reg = HealthRegistry()
    reg.register('ok', _ok)
    reg.register('warn', _warn)
    reg.register('fail', _fail)
    report = run_diagnostics(reg, UnixMillis(1234))
    assert report.overall == HealthStatus.FAIL
    assert report.counts == {'OK': 1, 'WARN': 1, 'FAIL': 1}
    d = report.to_dict()
    assert d['overall'] == 'FAIL'
    assert d['generated_ms'] == 1234
    assert [r['name'] for r in d['results']] == ['ok', 'warn', 'fail']
