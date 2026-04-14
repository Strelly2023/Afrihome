import pytest
from afritech.platform.control_plane.execution.authorization import (
    AuthorizationConditional,
)


def test_conditional_blocks_execution(
    handler, context, conditional_decision, rbac_allow
):
    with pytest.raises(AuthorizationConditional):
        handler.authorize(
            decision=conditional_decision,
            outcomes=(rbac_allow,),
            context=context,
        )
