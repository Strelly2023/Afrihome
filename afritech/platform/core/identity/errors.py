"""
GA Enterprise Core â€” Identity Errors
-----------------------------------

LAYER: L1 (Foundation)
Dependencies: core.errors.base
Deterministic: YES
Side effects: NONE

Purpose:
- Define identityâ€‘specific governance and validation errors
- Provide clear semantic failures for identity domain logic

Rules:
- All identity errors MUST derive from CoreError
- Errors are deterministic and immutable by convention
- No kernel imports
- No business logic
"""

from afritech.platform.core.errors.base import CoreError


# ============================================================
# Base Identity Error
# ============================================================

class IdentityError(CoreError):
    """
    Base error for identity domain violations.
    """

    def __init__(self, message: str):
        super().__init__(message=message, code="IDENTITY_ERROR")


# ============================================================
# Validation Errors
# ============================================================

class InvalidEmailError(IdentityError):
    """
    Raised when an email address fails identity validation.
    """

    def __init__(self, message: str = "Invalid email address"):
        super().__init__(message=message)


class InvalidDisplayNameError(IdentityError):
    """
    Raised when a display name fails validation rules.
    """

    def __init__(self, message: str = "Invalid display name"):
        super().__init__(message=message)


# ============================================================
# Lifecycle / Transition Errors
# ============================================================

class InvalidIdentityTransitionError(IdentityError):
    """
    Raised when an invalid identity lifecycle transition is attempted.
    """

    def __init__(self, message: str = "Invalid identity state transition"):
        super().__init__(message=message)
