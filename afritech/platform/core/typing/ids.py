
from __future__ import annotations
"""
GA Enterprise Core â€” Identifier Types
-------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.errors, core.typing.primitives
Deterministic: YES
Side effects: NONE
"""

from typing import NewType

from afritech.platform.core.errors import ValidationError
from .primitives import assert_non_empty_str


TenantId = NewType("TenantId", str)
UserId = NewType("UserId", str)
AggregateId = NewType("AggregateId", str)
RoleName = NewType("RoleName", str)


def tenant_id(value: str) -> TenantId:
    assert_non_empty_str(value, name="TenantId")
    return TenantId(value)


def user_id(value: str) -> UserId:
    assert_non_empty_str(value, name="UserId")
    return UserId(value)


def aggregate_id(value: str) -> AggregateId:
    assert_non_empty_str(value, name="AggregateId")
    return AggregateId(value)


def role_name(value: str) -> RoleName:
    assert_non_empty_str(value, name="RoleName")
    return RoleName(value)
