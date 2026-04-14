from __future__ import annotations
"""
GA Enterprise Core â€” Policy Condition
------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: core.policy.grammar + stdlib
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Represent a single atomic policy condition
- Provide pure condition evaluation against attribute dictionaries

Rules:
- Pure value object
- Grammar validation delegated to policy.grammar
- No kernel or foundation dependencies
"""


from dataclasses import dataclass
from typing import Any

from afritech.platform.core.policy.grammar import (
    validate_operator,
    validate_attribute,
)


@dataclass(frozen=True, slots=True)
class Condition:
    """
    A single policy condition.

    Attributes:
        attribute:
            Name of the attribute to inspect.
        operator:
            Operator applied to the attribute.
        value:
            Optional comparison value (ignored for 'exists').
    """

    attribute: str
    operator: str
    value: Any | None = None

    def __post_init__(self) -> None:
        # Grammar validation
        object.__setattr__(
            self,
            "attribute",
            validate_attribute(self.attribute),
        )
        object.__setattr__(
            self,
            "operator",
            validate_operator(self.operator),
        )

    def matches(self, attributes: dict[str, Any]) -> bool:
        """
        Evaluate this condition against a set of attributes.

        Returns:
            True if the condition matches, False otherwise.
        """

        if self.operator == "exists":
            return self.attribute in attributes

        if self.attribute not in attributes:
            return False

        actual = attributes[self.attribute]

        if self.operator == "eq":
            return actual == self.value

        if self.operator == "neq":
            return actual != self.value

        if self.operator == "in":
            return actual in self.value  # type: ignore[arg-type]

        if self.operator == "not_in":
            return actual not in self.value  # type: ignore[arg-type]

        # Should never be reached due to grammar validation
        return False


# ============================================================
# Policy Condition ABI (explicit, frozen)
# ============================================================

__all__ = [
    "Condition",
]
