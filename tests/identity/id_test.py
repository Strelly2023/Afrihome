from core.typing import UnixMillis, TenantId, RoleName
from core.identity.uuid import DeterministicUUIDProvider
from control_plane.governance.identity import UserId, User, Role, Permission, validate_email

uuidp = DeterministicUUIDProvider(seed="afrihome")
uid = UserId.new(uuidp)
tid = TenantId("t-1")

u = User.create(
    user_id=uid,
    tenant_id=tid,
    email="alice@example.com",
    display_name="Alice",
    now_ms=UnixMillis(1000),
)
assert u.active and u.email == "alice@example.com"
u = u.assign_role(RoleName("admin"), UnixMillis(1010))
u = u.grant_permission("inventory.read", UnixMillis(1011))