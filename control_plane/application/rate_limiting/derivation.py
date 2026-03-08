from dataclasses import dataclass
from typing import Mapping, Optional

from core.kernel.invariants import assert_not_none
from core.typing import TenantId, UserId

# Optional canonical header hints (all normalized to lowercase upstream)
HDR_METHOD = "x-method"  # e.g., GET/POST (Phase 4 routers can set)
HDR_ROUTE = "x-route"  # e.g., /v1/invoices/{id}
HDR_SCOPE = "x-rate-scope"  # optional, caller-supplied logical scope


@dataclass(frozen=True, slots=True)
class DefaultKeyDeriver:
    """
    Stable, tenant-first, actor-aware key grammar:
      rl:{tenant}:{actor-kind}:{actor-id-or-principal|anon}:{method}:{route}:{scope-kv...}
    Notes:
      - Deterministic: lowercased, trimmed, missing parts replaced by canonical tokens.
      - No IO, no randomness.
    """

    prefix: str = "rl"

    def derive(
        self,
        *,
        tenant_id: TenantId,
        actor_kind: str,
        actor_user_id: Optional[UserId],
        actor_principal: Optional[str],
        headers: Mapping[str, str],
        scope: Mapping[str, str] | None = None,
    ) -> str:
        assert_not_none(tenant_id, "tenant_id")
        ak = (actor_kind or "unknown").strip().lower()
        aid = (str(actor_user_id) if actor_user_id else (actor_principal or "anon")).strip().lower()
        method = (headers.get(HDR_METHOD) or "").strip().lower() or "-"
        route = (headers.get(HDR_ROUTE) or "").strip().lower() or "-"
        parts = [self.prefix, str(tenant_id), ak, aid, method, route]
        if scope:
            # Stable k=v join sorted by key for determinism
            for k in sorted(scope.keys()):
                v = str(scope[k]).strip().lower()
                parts.append(f"{k.strip().lower()}={v}")
        return ":".join(parts)
