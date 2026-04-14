from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True, slots=True)
class PolicyRule:
    """
    Declarative hint for policy evaluation (optional for call-sites that want one-liners).
    If provided, the engine will check in order:
      1) RBAC 'permission'
      2) optional 'feature_key'
      3) optional 'entitlement_key'
      4) optional ABAC (subject/resource injected at call)
    """
    permission: str
    feature_key: Optional[str] = None
    entitlement_key: Optional[str] = None