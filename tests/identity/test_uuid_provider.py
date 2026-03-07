
import uuid
import inspect
import pytest

from core.identity.uuid import DeterministicUUIDProvider, UUIDProvider


def test_uuid_provider_determinism_and_format():
    p1 = DeterministicUUIDProvider(seed='alpha')
    p2 = DeterministicUUIDProvider(seed='alpha')
    p3 = DeterministicUUIDProvider(seed='beta')

    e1 = p1.new_event_id()
    e2 = p2.new_event_id()
    e3 = p3.new_event_id()

    assert e1 == e2
    assert e1 != e3
    uuid.UUID(str(e1))


def test_uuid_provider_protocol():
    p = DeterministicUUIDProvider(seed='x')
    assert isinstance(p, UUIDProvider)


def test_uuid_module_no_randomness():
    import core.identity.uuid as mod
    src = inspect.getsource(mod)
    forbidden = ('uuid.uuid4(', 'random.', 'from random', 'secrets.rand', 'datetime.now(')
    assert not any(tok in src for tok in forbidden)
