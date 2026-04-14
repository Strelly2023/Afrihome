from __future__ import annotations
"""
GA Enterprise Core â€” Time Value Types
------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.errors only
Deterministic: YES
Side effects: NONE
"""
from typing import NewType

from afritech.platform.core.errors import ValidationError


UnixMillis = NewType("UnixMillis", int)


def unix_millis(value: int) -> UnixMillis:
    if not isinstance(value, int) or value < 0:
        raise ValidationError("UnixMillis must be a non-negative integer")
    return UnixMillis(value)
