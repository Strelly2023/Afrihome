import pytest
from afritech.platform.control_plane.execution.authorization import AuthorizationDenied


def test_deny_blocks_execution(
    handler, context, deny_decision, rbac_allow
):
    with pytest.raises(AuthorizationDenied):
        handler.authorize(
            decision=deny_decision,
            outcomes=(rbac_allow,),
            context=context,
        )
