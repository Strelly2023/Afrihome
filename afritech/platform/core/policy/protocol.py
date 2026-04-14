from __future__ import annotations
"""
GA Enterprise Core â€” Policy Protocols
------------------------------------

LAYER: L2 (Pure Engine)
Dependencies: stdlib + core.policy.version
Deterministic: YES
Side effects: NONE
IO / Time / Network: NONE

Purpose:
- Define contracts for resolving active policy versions
- Enable deterministic policy selection by higher layers

Rules:
- Protocols only (no implementation)
- No kernel or foundation dependencies
- Uses primitive types exclusively
"""

from typing import Optional, Protocol, runtime_checkable

from afritech.platform.core.policy.version import PolicyVersion


@runtime_checkable
class PolicyVersionResolver(Protocol):
    """
    Contract for resolving which policy version was active
    at a given point in time.

    Implementations are expected to live in:
    - control plane
    - infrastructure
    - test harnesses

    The core.policy engine depends only on this contract,
    never on concrete implementations.
    """

    def resolve(
        self,
        *,
        policy_id: str,
        at_ms: int,
    ) -> Optional[PolicyVersion]:
        """
        Resolve the PolicyVersion active for the given policy
        at the specified timestamp (milliseconds since epoch).

        Returns:
            PolicyVersion if one is applicable,
            None if no policy was active.
        """
        ...


# ============================================================
# Policy Protocol ABI (explicit, frozen)
# ============================================================

__all__ = [
    "PolicyVersionResolver",
]
