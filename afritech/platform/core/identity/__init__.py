"""
AfriHome Core â€” Identity (GA v1)
--------------------------------

LAYER: L1 (Foundation)
Deterministic: YES
Side effects: NONE

Purpose:
- Expose GAâ€‘stable identity domain primitives
- Describe *who* an actor is, not *what they can do*

GA RULES:
- Identity MUST NOT depend on RBAC or policy
- Identity MUST NOT define permissions
"""

# ---------------------------------------------------------------------
# Core identity models (value objects)
# ---------------------------------------------------------------------

from afritech.platform.core.identity.model import (
    IdentityId,
    Identity,
    Principal,
)

from afritech.platform.core.identity.identity_snapshot import (
    IdentityRef,
)

from afritech.platform.core.identity.user import (
    User,
)

from afritech.platform.core.identity.user_id import (
    UserId,
)

# ---------------------------------------------------------------------
# Identity relationships and resolution contracts
# ---------------------------------------------------------------------

from afritech.platform.core.identity.binding import (
    IdentityBinding,
)

from afritech.platform.core.identity.resolver import (
    IdentityResolver,
)

from afritech.platform.core.identity.identity_provider import (
    IdentityProvider,
)

from afritech.platform.core.identity.identity_status import (
    IdentityStatus,
)

# ---------------------------------------------------------------------
# Deterministic UUID infrastructure
# ---------------------------------------------------------------------

from afritech.platform.core.identity.uuid import (
    UUIDProvider,
    UuidProvider,
    DeterministicUUIDProvider,
)

# ---------------------------------------------------------------------
# Invariants & validation
# ---------------------------------------------------------------------

from afritech.platform.core.identity.identity_invariants import (
    validate_email,
    normalize_display_name,
)

# ---------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------

from afritech.platform.core.identity.errors import (
    IdentityError,
    InvalidEmailError,
    InvalidDisplayNameError,
    InvalidIdentityTransitionError,
)

# ---------------------------------------------------------------------
# Public GA exports (EXPLICIT & FROZEN)
# ---------------------------------------------------------------------

__all__ = [
    # Core identity models
    "IdentityId",
    "IdentityRef",
    "Identity",
    "Principal",
    "User",
    "UserId",

    # Identity structure & providers
    "IdentityBinding",
    "IdentityProvider",
    "IdentityResolver",
    "IdentityStatus",

    # UUID infrastructure
    "UUIDProvider",
    "UuidProvider",
    "DeterministicUUIDProvider",

    # Invariants
    "validate_email",
    "normalize_display_name",

    # Errors
    "IdentityError",
    "InvalidEmailError",
    "InvalidDisplayNameError",
    "InvalidIdentityTransitionError",
]
