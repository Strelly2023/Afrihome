
import inspect
import pytest

def test_identity_uuid_is_protocol_only():
    try:
        import core.identity.uuid as uuid_mod
    except ModuleNotFoundError:
        pytest.skip('identity.uuid not implemented.')
    assert hasattr(uuid_mod, 'UUIDProvider')
    src = inspect.getsource(uuid_mod)
    forbidden = ('uuid.uuid4(', 'random.', 'from random', 'secrets.rand', 'datetime.now(')
    assert not any(f in src for f in forbidden)


def test_hlc_is_pure_and_deterministic():
    try:
        from core.time.hlc import HLC
        from core.typing import UnixMillis
    except ModuleNotFoundError:
        pytest.skip('time.hlc not implemented.')
    h1 = HLC(UnixMillis(0), 0)
    h2 = HLC(UnixMillis(0), 0)
    for _ in range(10):
        h1 = h1.tick(UnixMillis(100))
        h2 = h2.tick(UnixMillis(100))
    assert h1 == h2
