from __future__ import annotations
"""
GA Enterprise Core â€” Identity Resolver Contract
-----------------------------------------------

LAYER: L1 (Foundation)
Dependencies: core.identity + stdlib
Deterministic: BY CONTRACT
Side effects: NONE (interface only)

Purpose:
- Define the pure identity resolution contract
- Bridge identity identifiers to canonical IdentityBinding snapshots

Responsibilities:
- Resolve an IdentityId into an IdentityBinding
- Expose the SINGLE authoritative source of RBAC roles

Nonâ€‘Responsibilities:
- Authentication
- Credential parsing
- Persistence
- Caching
- Authorization decisions
- Policy evaluation
"""


from typing import Optional, Protocol, runtime_checkable

from afritech.platform.core.identity.binding import IdentityBinding
from afritech.platform.core.identity.model import IdentityId


@runtime_checkable
class IdentityResolver(Protocol):
    """
    Pure identity resolution contract.

    Implementations:
    - MUST be deterministic for the same inputs
    - MUST NOT perform authorization decisions
    - MAY live in infrastructure or application layers

    Core consumes this interface; it never implements it.
    """

    def resolve(self, identity_id: IdentityId) -> Optional[IdentityBinding]:
        """
        Resolve an identity identifier into its canonical binding.

        Args:
            identity_id: Stable identity reference

        Returns:
            IdentityBinding if identity exists,
            None if identity is unknown or not resolvable.
        """
        ...
