import hashlib
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple

from core.typing import TenantId, UserId


class ActorKind(Enum):
    USER = auto()
    API_KEY = auto()
    SYSTEM = auto()
    OPERATOR = auto()


class RuleEffect(Enum):
    DISABLE = 0  # deny-wins precedence
    ENABLE = 1


@dataclass(frozen=True, slots=True)
class FlagRule:
    """
    Immutable feature rule with deterministic evaluation.

    Fields
    ------
    rule_id: str                        — unique ID for audit/debug
    priority: int                       — lower number = higher priority
    effect: RuleEffect                  — ENABLE or DISABLE (deny-wins)
    tenant_slugs: Tuple[str, ...]       — optional whitelist of tenant slugs
    tenant_ids: Tuple[TenantId, ...]    — optional whitelist of tenant IDs
    user_ids: Tuple[UserId, ...]        — optional whitelist of users
    actor_kinds: Tuple[ActorKind, ...]  — optional whitelist of actor kinds
    percentage: Optional[int]           — 0..100 (deterministic rollout)
    salt: Optional[str]                 — salt for hashing (required if percentage set)

    Notes
    -----
    - All conditions are conjunctive *within* a category (e.g. tenant_ids matches if target's tenant is IN the set);
      across categories, conditions are combined with AND (i.e. all specified categories must match).
    - Percentage applies only if ALL other specified conditions match, and it is evaluated deterministically using SHA-256.
    """

    rule_id: str
    priority: int
    effect: RuleEffect

    tenant_slugs: Tuple[str, ...] = ()
    tenant_ids: Tuple[TenantId, ...] = ()
    user_ids: Tuple[UserId, ...] = ()
    actor_kinds: Tuple[ActorKind, ...] = ()

    percentage: Optional[int] = None
    salt: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.rule_id or not isinstance(self.rule_id, str):
            raise ValueError("rule_id must be a non-empty string")
        if not isinstance(self.priority, int) or self.priority < 0:
            raise ValueError("priority must be a non-negative integer")
        if self.percentage is not None:
            p = int(self.percentage)
            if p < 0 or p > 100:
                raise ValueError("percentage must be within 0..100")
            if self.salt is None or not isinstance(self.salt, str) or not self.salt.strip():
                raise ValueError("salt is required when percentage is set")

    # ---------- Evaluation (pure, deterministic) ----------

    def matches(
        self,
        *,
        feature_key: str,
        tenant_slug: Optional[str],
        tenant_id: Optional[TenantId],
        user_id: Optional[UserId],
        actor_kind: ActorKind,
    ) -> bool:
        """
        Returns True if the target matches the rule's non-percentage conditions.
        """
        # Tenant slug filter (if provided)
        if self.tenant_slugs:
            if tenant_slug is None or tenant_slug not in self.tenant_slugs:
                return False

        # Tenant ID filter (if provided)
        if self.tenant_ids:
            if tenant_id is None or tenant_id not in self.tenant_ids:
                return False

        # User filter (if provided)
        if self.user_ids:
            if user_id is None or user_id not in self.user_ids:
                return False

        # Actor kind filter (if provided)
        if self.actor_kinds:
            if actor_kind not in self.actor_kinds:
                return False

        return True

    def percentage_hit(
        self,
        *,
        feature_key: str,
        tenant_slug: Optional[str],
        tenant_id: Optional[TenantId],
        user_id: Optional[UserId],
    ) -> bool:
        """
        Deterministic percentage rollout using SHA-256.

        Hash input combines (feature_key | tenant | user | salt)
        and maps into [0..99]. A hit occurs if value < percentage.
        """
        if self.percentage is None:
            return True  # if no percentage constraint, it's a hit by definition

        # Construct a stable identity string
        parts = [
            feature_key,
            tenant_slug or "",
            str(tenant_id) if tenant_id is not None else "",
            str(user_id) if user_id is not None else "",
            self.salt or "",
        ]
        blob = "|".join(parts).encode("utf-8")
        digest_hex = hashlib.sha256(blob).hexdigest()
        # Take first 8 hex chars → int
        value = int(digest_hex[:8], 16) % 100
        return value < int(self.percentage)

    def evaluate(
        self,
        *,
        feature_key: str,
        tenant_slug: Optional[str],
        tenant_id: Optional[TenantId],
        user_id: Optional[UserId],
        actor_kind: ActorKind,
    ) -> bool:
        """
        Returns True if the rule BOTH matches (non-percentage conditions)
        AND the percentage test (if present) is a hit.
        """
        if not self.matches(
            feature_key=feature_key,
            tenant_slug=tenant_slug,
            tenant_id=tenant_id,
            user_id=user_id,
            actor_kind=actor_kind,
        ):
            return False
        return self.percentage_hit(
            feature_key=feature_key,
            tenant_slug=tenant_slug,
            tenant_id=tenant_id,
            user_id=user_id,
        )
