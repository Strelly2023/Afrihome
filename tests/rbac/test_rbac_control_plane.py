from core.typing import RoleName, Permission, UserId
from control_plane.governance.rbac import RoleDefinition, RBACState

def test_rbac_state_happy_path():
    state = RBACState()
    admin = RoleDefinition(name=RoleName("admin"), allow=("inventory.**",), deny=())
    state = state.register_role(admin)

    uid = UserId("u-1")
    state = state.assign_role(uid, RoleName("admin"))

    assert state.evaluate_for_user(uid, Permission("inventory.item.read")) is True
    assert state.evaluate_for_user(uid, Permission("billing.read")) is False