
import pytest
from core.time.hlc import HLC
from core.typing import UnixMillis
from core.errors import InvariantViolationError


def test_hlc_tick_determinism():
    h1 = HLC(UnixMillis(0), 0)
    h2 = HLC(UnixMillis(0), 0)
    for _ in range(5):
        h1 = h1.tick(UnixMillis(100))
        h2 = h2.tick(UnixMillis(100))
    assert h1 == h2


def test_hlc_merge():
    local = HLC(UnixMillis(100), 0)
    remote = HLC(UnixMillis(90), 5)
    merged = local.merge(remote, UnixMillis(50))
    assert merged.physical == 100 and merged.logical == 1
    m2 = local.merge(remote, UnixMillis(150))
    assert m2.physical == 150 and m2.logical == 0


def test_hlc_guards():
    with pytest.raises(InvariantViolationError):
        HLC(UnixMillis(-1), 0)
    with pytest.raises(InvariantViolationError):
        HLC(UnixMillis(0), -1)
    x = HLC(UnixMillis(0), 0)
    with pytest.raises(InvariantViolationError):
        x.tick(UnixMillis(-1))
