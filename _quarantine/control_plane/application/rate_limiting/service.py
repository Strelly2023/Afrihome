from dataclasses import dataclass
from core.kernel.invariants import assert_not_none
from core.errors import ValidationError, AuthorizationError
from core.guards.rate_limit import TokenBucketPolicy, TokenBucketState, try_consume  # pure core logic
from control_plane.application.execution.models import ExecutionFrame
from control_plane.application.actors.models import ActorKind
from .protocols import RateKeyDeriver, RatePolicyProvider, RateLimitStore
from .models import RateDecision

@dataclass(frozen=True, slots=True)
class RateLimiter:
    """
    Deterministic token-bucket orchestration:
      1) Derive a stable, tenant-actor-scoped key (pure)
      2) Load TokenBucketPolicy via provider (pure interface)
      3) Read current TokenBucketState via store (pure interface)
      4) Apply core token-bucket try_consume(now, policy, cost) (pure)
      5) Return immutable RateDecision and the new state (store.put is caller-controlled)
    NOTE: No IO here; infra binds store/provider in later phases.
    """
    deriver: RateKeyDeriver
    policies: RatePolicyProvider
    store: RateLimitStore

    def enforce(
        self,
        frame: ExecutionFrame,
        *,
        cost: int = 1,
        scope: dict[str, str] | None = None,
        persist: bool = True,
    ) -> tuple[RateDecision, TokenBucketState, str]:
        """
        Enforce a rate limit for the current tenant+actor+scope.
        Returns (decision, new_state, key). The caller may choose to persist new_state later.
        """
        assert_not_none(frame, "frame")
        if cost <= 0:
            raise ValidationError("rate limit cost must be positive")

        key = self._derive_key(frame, scope or {})
        policy: TokenBucketPolicy = self.policies.policy_for(frame.tenant_id, key)

        now = frame.ctx.now()
        prev = self.store.get(key)
        if prev is None:
            # New bucket begins full at first observation, last_refill=now (pure deterministic init)
            prev = TokenBucketState(tokens=float(policy.capacity), last_refill_ms=int(now))

        new_state, allowed = try_consume(prev, int(now), policy, cost)  # pure, deterministic transitions
        reason = "allow: under token bucket" if allowed else "deny: rate limit exceeded"

        decision = RateDecision(
            key=key,
            allowed=bool(allowed),
            reason=reason,
            cost=int(cost),
            tokens_before=float(prev.tokens),
            tokens_after=float(new_state.tokens),
            last_refill_ms_before=prev.last_refill_ms,
            last_refill_ms_after=new_state.last_refill_ms,
        )

        # No IO if persist=False; caller can persist later in a write boundary/event handler
        if persist:
            self.store.put(key, new_state)

        return decision, new_state, key

    def require(
        self,
        frame: ExecutionFrame,
        *,
        cost: int = 1,
        scope: dict[str, str] | None = None,
        persist: bool = True,
    ) -> None:
        """
        Exception-style guard. Raises AuthorizationError when the bucket rejects the request.
        """
        decision, _, _ = self.enforce(frame, cost=cost, scope=scope, persist=persist)
        if decision.allowed:
            return
        raise AuthorizationError(decision.reason)

    # ---------- internals ----------

    def _derive_key(self, frame: ExecutionFrame, scope: dict[str, str]) -> str:
        actor = frame.actor
        return self.deriver.derive(
            tenant_id=frame.tenant_id,
            actor_kind=actor.kind.name.lower(),
            actor_user_id=actor.user_id if actor.kind is ActorKind.USER else None,
            actor_principal=actor.principal if actor.kind is not ActorKind.USER else None,
            headers=frame.headers,
            scope=scope,
        )