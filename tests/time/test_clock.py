
import pytest
from afritech.platform.control_plane.time.clock import Clock, FixedClock, SystemClock
from core.typing import UnixMillis


def test_fixed_clock():
    c = FixedClock(UnixMillis(123456))
    assert c.now_ms() == 123456


def test_clock_protocol():
    class DummyClock:
        def now_ms(self) -> UnixMillis:
            return UnixMillis(1)
    d = DummyClock()
    assert isinstance(d, Clock)


def test_system_clock_returns_ms():
    s = SystemClock()
    a = s.now_ms(); b = s.now_ms()
    assert isinstance(a, int) and isinstance(b, int)
