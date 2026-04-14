import pytest

from afritech.platform.control_plane.execution.authorization import (
    AuthorizeActionHandler,
    ExecutionContext,
)
from afritech.platform.core.decision import Decision
from afritech.platform.core.decision.engine_outcome import EngineOutcome
from afritech.platform.core.decision.reason import DecisionReason
from afritech.platform.core.typing.enums import EngineId, DecisionVerdictType


def r(code: str) -> DecisionReason:
    return DecisionReason(
        engine=EngineId.COMBINED,
        code=code,
        metadata={},
    )


@pytest.fixture
def handler():
    return AuthorizeActionHandler()


@pytest.fixture
def context():
    return ExecutionContext(
        actor="user-123",
        action="delete",
        resource="document-456",
        environment="production",
    )


@pytest.fixture
def rbac_allow():
    return EngineOutcome(
        engine=EngineId.RBAC,
        verdict=DecisionVerdictType.ALLOW,
        reasons=("rbac.allow",),
        traces=(),
    )


@pytest.fixture
def policy_allow():
    return EngineOutcome(
        engine=EngineId.POLICY,
        verdict=DecisionVerdictType.ALLOW,
        reasons=("policy.allow",),
        traces=(),
    )


@pytest.fixture
def allow_decision():
    return Decision(
        verdict=DecisionVerdictType.ALLOW,
        reasons=(r("rbac.allow"),),
        traces=(),
    )


@pytest.fixture
def deny_decision():
    return Decision(
        verdict=DecisionVerdictType.DENY,
        reasons=(r("policy.deny"),),
        traces=(),
    )


@pytest.fixture
def conditional_decision():
    return Decision(
        verdict=DecisionVerdictType.CONDITIONAL,
        reasons=(r("policy.requires_review"),),
        traces=(),
    )
