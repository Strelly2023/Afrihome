from typing import Protocol, runtime_checkable, Mapping, Optional
from core.typing import TenantId, UserId
from core.guards.rate_limit import TokenBucketPolicy, TokenBucketState  # pure core model & logic

@runtime_checkable
class RateKeyDeriver(Protocol):
    """
    Deterministic derivation of tenant-scoped rate-limit keys.
    Must be pure (no IO, no randomness).
    """
    def derive(
        self,
        *,
        tenant_id: TenantId,
        actor_kind: str,
        actor_user_id: Optional[UserId],
        actor_principal: Optional[str],
        headers: Mapping[str, str],
        # optional extra scoping (e.g., per-endpoint or custom tags)
        scope: Mapping[str, str] | None = None,
    ) -> str: ...

@runtime_checkable
class RatePolicyProvider(Protocol):
    """
    Pure provider of TokenBucketPolicy for a key.
    Infra adapters bind concrete sources later (Phase 5/8).
    """
    def policy_for(self, tenant_id: TenantId, key: str) -> TokenBucketPolicy: ...

@runtime_checkable
class RateLimitStore(Protocol):
    """
    Pure interface for reading/updating bucket state for a key.
    Implementations persist state (DB/cache) in infra layers; app stays orchestration-only.
    """
    def get(self, key: str) -> TokenBucketState | None: ...
    def put(self, key: str, state: TokenBucketState) -> None: ...
