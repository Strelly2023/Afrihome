
import pytest
import inspect

def test_health_has_no_io():
    try:
        from core.health import registry as health_registry
        import inspect as _i
        src = _i.getsource(health_registry)
    except ModuleNotFoundError:
        pytest.skip('health not implemented.')
    forbidden = ['open(', 'socket.', 'requests.', 'httpx.', 'subprocess.', 'os.system(']
    assert not any(t in src for t in forbidden), 'Health must be in-memory only'
