import pytest
from afritech.platform.control_plane.execution.authorization import (
    MissingDecision,
    AuthorizationDenied,
)


def test_missing_decision_blocks(handler, context, rbac_allow):
    with pytest.raises(MissingDecision):
        handler.authorize(
            decision=None,
            outcomes=(rbac_allow,),
            context=context,
        )


def test_missing_outcomes_blocks(
    handler, context, allow_decision
):
    with pytest.raises(AuthorizationDenied):
        handler.authorize(
            decision=allow_decision,
            outcomes=(),
            context=context,
        )