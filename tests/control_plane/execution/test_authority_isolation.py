import pytest
from afritech.platform.control_plane.execution.authorization import AuthorityNotGranted


def test_policy_allow_without_rbac_blocks(
    handler, context, allow_decision, policy_allow
):
    with pytest.raises(AuthorityNotGranted):
        handler.authorize(
            decision=allow_decision,
            outcomes=(policy_allow,),
            context=context,
        )