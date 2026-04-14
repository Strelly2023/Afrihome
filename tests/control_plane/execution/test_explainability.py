import pytest
from afritech.platform.control_plane.execution.authorization import UnexplainableDecision
from afritech.platform.core.decision import Decision
from afritech.platform.core.typing.enums import DecisionVerdictType


def test_silent_allow_is_rejected(
    handler, context, rbac_allow
):
    silent_decision = Decision(
        verdict=DecisionVerdictType.ALLOW,
        reasons=(),
        traces=(),
    )

    with pytest.raises(UnexplainableDecision):
        handler.authorize(
            decision=silent_decision,
            outcomes=(rbac_allow,),
            context=context,
        )