import pytest
from core.events.headers import EventHeaders
from core.errors import InvariantViolationError

def test_event_headers_negative_timestamp():
    with pytest.raises(InvariantViolationError):
        EventHeaders(correlation_id="c", causation_id="k", timestamp_ms=-1)  # type: ignore[arg-type]