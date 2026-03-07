from core.typing import TenantId, UserId, UnixMillis
from control_plane.governance.notifications import (
    NotificationTemplate, NotificationRule, Channel
)
from control_plane.governance.features.flag_rule import ActorKind

def test_template_and_rule_match():
    tmpl = NotificationTemplate(
        template_key="platform.tenant.created",
        version=1,
        channels=(Channel.EMAIL, Channel.WEBHOOK),
        subject_template="Welcome, {{tenant_name}}!",
        body_template="Hello {{tenant_name}}, your tenant is ready.",
        payload_template='{"tenant":"{{tenant_slug}}"}',
        placeholders=("tenant_name","tenant_slug"),
        description="Tenant created notice",
        locale="en-US",
    )
    rule = NotificationRule(
        rule_id="r1",
        priority=0,
        enabled=True,
        template_key="platform.tenant.created",
        match_events=("platform.tenant.created",),
        tenant_slugs=("acme",),
        channels=(Channel.EMAIL,),
        max_per_window=100,
        window_ms=3_600_000,
    )
    assert rule.matches(
        event_key="platform.tenant.created",
        tenant_slug="acme",
        tenant_id=TenantId("t-1"),
        user_id=UserId("u-1"),
        actor_kind=ActorKind.USER,
    )
    # rule selects only channels that are also permitted by the template
    assert rule.select_channels(tmpl.channels) == (Channel.EMAIL,)