
from __future__ import annotations
"""
GA Enterprise Core â€” Permission Typing
--------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.errors, core.typing.primitives
Deterministic: YES
Side effects: NONE
"""

from typing import NewType

from afritech.platform.core.errors import ValidationError
from .primitives import assert_non_empty_str


Permission = NewType("Permission", str)


def permission(value: str) -> Permission:
    assert_non_empty_str(value, name="Permission")

    if "." not in value:
        raise ValidationError(
            "Permission must use dotted notation (e.g. 'invoice.read')"
        )

    return Permission(value)
