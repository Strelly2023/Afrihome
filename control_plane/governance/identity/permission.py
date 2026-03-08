from dataclasses import dataclass

from core.rbac.grammar import validate_permission_name


@dataclass(frozen=True, slots=True)
class Permission:
    """
    Pure permission value object.

    - Normalized & validated by core.rbac.grammar (single authority)
    - Represents a concrete permission (not a pattern)
    """

    name: str  # canonical, e.g., "inventory.item.read"

    def __post_init__(self) -> None:
        n = validate_permission_name(self.name)
        object.__setattr__(self, "name", n)

    def __str__(self) -> str:
        return self.name
