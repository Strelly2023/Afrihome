from dataclasses import dataclass
import re
from typing import Tuple, Optional, Iterable, Any

from core.errors import InvariantViolationError
from core.typing import UnixMillis, TenantId, UserId

from .flag_rule import FlagRule, RuleEffect, ActorKind
from .feature_state_snapshot import FeatureStateSnapshot, DecisionSource


#_FEATURE_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_FEATURE_KEY_RE = re.compile(r'^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$')


def normalize_feature_key(key: str) -> str:
    if not isinstance(key, str):
        raise InvariantViolationError("feature key must be a string")
    k = key.strip().lower()
    if not _FEATURE_KEY_RE.match(k):
        raise InvariantViolationError(f"Invalid feature key: {key!r}")
    return k


@dataclass(frozen=True, slots=True)
class Target:
    """
    Evaluation target (pure carrier). No framework types here.
    """
    tenant_id: Optional[TenantId]
    tenant_slug: Optional[str]
    user_id: Optional[UserId]
    actor_kind: ActorKind


@dataclass(frozen=True, slots=True)
class FeatureFlag:
    """
    Immutable feature-flag definition + deterministic evaluator.

    Fields
    ------
    key: str                    — canonical feature key (validated)
    description: str            — optional human-friendly description
    enabled_default: bool       — fallback when no rule matches
    rules: Tuple[FlagRule, ...] — ordered rules; priority is authoritative

    Evaluation semantics
    --------------------
    - Find all rules that evaluate to True for the target.
    - Select the "best" rule deterministically by:
        1) lowest priority (higher precedence)
        2) deny-wins: DISABLE preferred over ENABLE when equal priority
        3) rule_id lexicographic tiebreak
    - If no rule matches, return enabled_default.
    """
    key: str
    enabled_default: bool
    rules: Tuple[FlagRule, ...] = ()
    description: str = ""

    def __post_init__(self) -> None:
        k = normalize_feature_key(self.key)
        object.__setattr__(self, "key", k)

    # ---------- Evaluation (pure, deterministic) ----------

    def evaluate(
        self,
        *,
        target: Target,
        now_ms: UnixMillis,
    ) -> FeatureStateSnapshot:
        """
        Evaluate flag deterministically for the given target.

        Arguments
        ---------
        target: Target                — tenant/user/actor-kind
        now_ms: UnixMillis            — injected timestamp (no reads here)

        Returns
        -------
        FeatureStateSnapshot
        """
        matches = []
        for r in self.rules:
            if r.evaluate(
                feature_key=self.key,
                tenant_slug=target.tenant_slug,
                tenant_id=target.tenant_id,
                user_id=target.user_id,
                actor_kind=target.actor_kind,
            ):
                # effect rank: DISABLE (0) before ENABLE (1) for deny-wins
                effect_rank = 0 if r.effect is RuleEffect.DISABLE else 1
                matches.append((r.priority, effect_rank, r.rule_id, r))

        if not matches:
            return FeatureStateSnapshot(
                feature_key=self.key,
                enabled=self.enabled_default,
                decision_source=DecisionSource.DEFAULT,
                tenant_id=target.tenant_id,
                tenant_slug=target.tenant_slug,
                user_id=target.user_id,
                actor_kind=target.actor_kind,
                timestamp_ms=now_ms,
                rule_id=None,
                reason="no_rule_matched",
            )

        # Deterministic selection
        matches.sort(key=lambda x: (x[0], x[1], x[2]))
        _, _, _, best = matches[0]
        enabled = (best.effect is RuleEffect.ENABLE)

        return FeatureStateSnapshot(
            feature_key=self.key,
            enabled=enabled,
            decision_source=DecisionSource.RULE,
            tenant_id=target.tenant_id,
            tenant_slug=target.tenant_slug,
            user_id=target.user_id,
            actor_kind=target.actor_kind,
            timestamp_ms=now_ms,
            rule_id=best.rule_id,
            reason=f"priority={best.priority},effect={best.effect.name}",
        )