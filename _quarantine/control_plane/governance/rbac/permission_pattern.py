from dataclasses import dataclass

from core.rbac.grammar import validate_permission_pattern


@dataclass(frozen=True, slots=True)
class PermissionPattern:
    """
    Canonical permission pattern (e.g., "inventory.*", "orders.**").

    - Validated/normalized by core.rbac.grammar (single authority)
    - Immutable VO, no side effects
    """
    pattern: str

    def __post_init__(self) -> None:
        p = validate_permission_pattern(self.pattern)
        object.__setattr__(self, "pattern", p)

    def __str__(self) -> str:
        return self.pattern