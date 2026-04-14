from dataclasses import dataclass
from typing import Mapping, Any, Tuple
from core.kernel.invariants import assert_not_none
from core.events import DomainEvent, EventHeaders, EventEnvelope
from control_plane.application.execution.models import ExecutionFrame
from .models import TemplateRef, NotificationPlan, RenderedMessage, ChannelTarget
from .protocols import TemplateRepository, TemplateBinder, ChannelRouter

@dataclass(frozen=True, slots=True)
class NotificationEmitter:
    """
    Orchestration-only notification sender:
      1) Fetch template via TemplateRepository (protocol)
      2) Render via TemplateBinder (pure)
      3) Route via ChannelRouter (pure)
      4) Emit one EventEnvelope per target ('notification.outbound.requested')
    NOTE: No IO/SDK calls; infra adapters will deliver messages later.
    """
    event_type: str = "notification.outbound.requested"

    def plan(
        self,
        frame: ExecutionFrame,
        *,
        template: TemplateRef,
        variables: Mapping[str, Any],
        attributes: Mapping[str, Any],
        repo: TemplateRepository,
        binder: TemplateBinder,
        router: ChannelRouter,
    ) -> NotificationPlan:
        assert_not_none(frame, "frame")
        assert_not_none(template, "template")
        assert_not_none(repo, "repo")
        assert_not_none(binder, "binder")
        assert_not_none(router, "router")

        payload = repo.get(template)  # protocol only, no IO in app
        rendered: RenderedMessage = binder.bind(template_payload=payload, variables=variables)
        targets: Tuple[ChannelTarget, ...] = router.route(
            tenant_slug=frame.tenant_slug,
            attributes=attributes,
            variables=variables,
        )
        return NotificationPlan(
            template=template,
            rendered=rendered,
            targets=targets,
            attributes=dict(attributes),
        )

    def emit(self, frame: ExecutionFrame, plan: NotificationPlan) -> Tuple[EventEnvelope, ...]:
        """
        Build pure event envelopes (one per target). Outbox persist/dispatch happens later.
        """
        assert_not_none(frame, "frame")
        assert_not_none(plan, "plan")

        envelopes: list[EventEnvelope] = []
        for t in plan.targets:
            evt = DomainEvent(
                event_id=frame.ctx.uuid_provider.new_event_id(),
                event_type=self.event_type,
                payload={
                    "tenant_id": str(frame.tenant_id),
                    "channel": t.channel.name.lower(),
                    "address": t.address,
                    "metadata": dict(t.metadata),
                    "template": {
                        "id": plan.template.template_id,
                        "language": plan.template.language,
                    },
                    "message": {
                        "subject": plan.rendered.subject,
                        "body_text": plan.rendered.body_text,
                        "body_html": plan.rendered.body_html,
                        "variables": dict(plan.rendered.variables),
                    },
                    "attributes": dict(plan.attributes),
                },
            )
            hdr = EventHeaders(
                correlation_id=frame.correlation_id,
                causation_id=frame.causation_id,
                timestamp_ms=frame.timestamp_ms,
                tenant_id=frame.tenant_id,
            )
            envelopes.append(EventEnvelope.create(event=evt, headers=hdr))
        return tuple(envelopes)