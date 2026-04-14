# tests/test_authorization_service.py
import pytest
from core.errors import AuthorizationError
from core.typing import TenantId, RoleName, Permission
from control_plane.application.execution.models import ExecutionFrame, Actor, ActorKind
from control_plane.application.authorization.models import AccessDecision, DecisionStage
from control_plane.application.authorization.service import AuthorizationService
from control_plane.application.authorization.policies import PolicyProvider, GovernancePolicy

class _AllowAllPolicyProvider:
    def policy_for(self, tenant_id: TenantId):
        # Minimal Policy stub: one role with allow "demo.read"
        from core.rbac.roles import Role
        from core.rbac.policy_engine import Policy
        role = Role(name=RoleName("demo_reader"), allow=("demo.read",), deny=())
        return Policy(roles={"demo_reader": role})

class _NoGov:
    def evaluate(self, *, tenant_id: TenantId, permission: str):
        return None

def _frame_with_roles(*roles: str) -> ExecutionFrame:
    from core.execution import ExecutionContext
    from core.context import RequestContext
    from afritech.platform.control_plane.time.clock import FixedClock
    from core.identity.uuid import DeterministicUUIDProvider
    from core.typing import RequestId, CorrelationId, CausationId, UnixMillis
    rc = RequestContext(
        request_id=RequestId("r1"),
        correlation_id=CorrelationId("c1"),
        causation_id=CausationId("k1"),
        timestamp_ms=UnixMillis(0),
        tenant_id=TenantId("t1"),
        user_id=None,
    )
    ctx = ExecutionContext(rc, FixedClock(UnixMillis(0)), DeterministicUUIDProvider("seed"))
    actor = Actor(kind=ActorKind.USER, user_id=None, roles=tuple(RoleName(r) for r in roles))
    return ExecutionFrame(
        ctx=ctx, request_id=rc.request_id, correlation_id=rc.correlation_id,
        causation_id=rc.causation_id, timestamp_ms=rc.timestamp_ms,
        tenant_id=TenantId("t1"), tenant_slug="t1", actor=actor,
        feature_snapshot={}, headers={}
    )

def test_decide_allows_when_role_matches():
    svc = AuthorizationService(policy_provider=_AllowAllPolicyProvider(), governance_policies=(_NoGov(),))
    frame = _frame_with_roles("demo_reader")
    dec = svc.decide(frame, "demo.read")
    assert dec.allowed is True
    assert dec.stage is DecisionStage.RBAC

def test_require_raises_on_deny():
    svc = AuthorizationService(policy_provider=_AllowAllPolicyProvider(), governance_policies=(_NoGov(),))
    frame = _frame_with_roles()  # no roles
    with pytest.raises(AuthorizationError):
        svc.require(frame, "demo.read")

def test_invalid_permission_short_circuits():
    svc = AuthorizationService(policy_provider=_AllowAllPolicyProvider(), governance_policies=(_NoGov(),))
    frame = _frame_with_roles("demo_reader")
    dec = svc.decide(frame, "BadPermissionName")  # uppercase should fail grammar
    assert dec.allowed is False
    assert dec.stage is DecisionStage.DEFAULT_DENY