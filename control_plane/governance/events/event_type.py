from dataclasses import dataclass

from core.errors import InvariantViolationError
from core.kernel.invariants import assert_not_none


@dataclass(frozen=True, slots=True)
class EventType:
    """
    Canonical platform event type (e.g., "billing.invoice.created").
    """

    name: str

    def __post_init__(self) -> None:
        assert_not_none(self.name, "name")
        n = self.name.strip().lower()
        if "." not in n or n.startswith(".") or n.endswith("."):
            raise InvariantViolationError("event type must be dot-separated segments")
        object.__setattr__(self, "name", n)
