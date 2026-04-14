from __future__ import annotations
"""
AfriTech Core Registry â€” Protocol Metadata (GA-Sealed)

This module declares protocol/type references exposed by core
decision engines. It exists solely for **static typing and metadata**
consumption by the L3 control plane.

RULES:
- STATIC METADATA ONLY
- NO instantiation
- NO execution
- NO orchestration
- NO imports of concrete engine implementations

Any modification requires an ADR.
"""


# ---------------------------------------------------------------------
# Protocol / type references (metadata only)
# ---------------------------------------------------------------------
# NOTE:
# These are references to *protocols* or *interfaces*, not implementations.
# They must never be instantiated or invoked in core.registry.
# ---------------------------------------------------------------------

from afritech.platform.core.policy.protocol import PolicyVersionResolver


# ---------------------------------------------------------------------
# Engine â†’ protocol mapping
# ---------------------------------------------------------------------
# Keys:
#   Symbolic engine names (strings)
#
# Values:
#   Protocol/type objects only (never instances)
# ---------------------------------------------------------------------

ENGINE_PROTOCOLS: dict[str, object] = {
    # Policy engine exposes a protocol for version resolution
    "policy": PolicyVersionResolver,
}


# ---------------------------------------------------------------------
# Registry invariants (must always hold)
# ---------------------------------------------------------------------

# Engine names must be symbolic strings
assert all(isinstance(name, str) for name in ENGINE_PROTOCOLS.keys()), (
    "ENGINE_PROTOCOLS keys must be symbolic engine name strings"
)

# Protocol values must be type-like (not instances)
assert all(
    isinstance(proto, type) or hasattr(proto, "__call__")
    for proto in ENGINE_PROTOCOLS.values()
), (
    "ENGINE_PROTOCOLS values must be protocol or type references only"
)


# ---------------------------------------------------------------------
# Public ABI (frozen)
# ---------------------------------------------------------------------

__all__ = [
    "ENGINE_PROTOCOLS",
]
