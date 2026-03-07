from dataclasses import dataclass
from core.kernel.invariants import assert_not_none

@dataclass(frozen=True, slots=True)
class ApiKeyId:
    """
    Stable identifier of an API key (NOT the secret token).
    """
    value: str

    def __post_init__(self) -> None:
        assert_not_none(self.value, "value")
        object.__setattr__(self, "value", self.value.strip().lower())