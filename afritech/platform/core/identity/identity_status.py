"""
GA Enterprise Core â€” Identity Status (Derived)
----------------------------------------------

LAYER: L1 (Foundation)
Dependencies: stdlib only
Deterministic: YES
Side effects: NONE

Purpose:
- Provide a derived, humanâ€‘readable identity lifecycle status
- Bridge core identity state to presentation / reporting layers

GA v1 Rules:
- IdentityStatus is NOT authoritative
- The source of truth is:
    User.active: bool

Mapping (GA v1):
    User.active == True  â†’ IdentityStatus.ACTIVE
    User.active == False â†’ IdentityStatus.SUSPENDED

IMPORTANT:
- Do NOT persist IdentityStatus
- Do NOT mutate IdentityStatus
- Do NOT use this enum for decisionâ€‘making
- GA v2 may introduce a firstâ€‘class Identity aggregate
"""

from enum import Enum


class IdentityStatus(str, Enum):
    """
    Derived identity lifecycle status.

    This enum exists purely for representation and interoperability.
    """

    ACTIVE = "active"
    SUSPENDED = "suspended"

__all__ = ["IdentityStatus"]
