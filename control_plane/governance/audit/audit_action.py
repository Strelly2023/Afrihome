from dataclasses import dataclass
from core.kernel.invariants import assert_not_none

@dataclass(frozen=True, slots=True)
class AuditAction:
    """
    Action taxonomy for audit (category + verb).
    Example: category="subscription", action="plan.change.requested"
    """
    category: str
    action: str

    def __post_init__(self) -> None:
        assert_not_none(self.category, "category")
        assert_not_none(self.action, "action")
        object.__setattr__(self, "category", self.category.strip().lower())
        object.__setattr__(self, "action", self.action.strip().lower())