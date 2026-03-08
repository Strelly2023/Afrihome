# control_plane/application/organisations/service.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, Tuple

from control_plane.application.auditing.writer import (
    AuditWriter,  # NEW: audit orchestrator (pure)  # noqa
)
from control_plane.application.event_handlers.builder import (
    EventBuilder,  # NEW: event envelopes (pure)  # noqa
)
from control_plane.application.execution.models import ExecutionFrame
from control_plane.governance.organisations.organisation import Organisation, OrganisationId
from control_plane.repositories.organisation_repository import OrganisationRepository
from core.errors import ValidationError
from core.events import EventEnvelope  # for return type of wrappers
from core.kernel.invariants import assert_not_none


@dataclass(frozen=True, slots=True)
class OrganisationService:
    repo: OrganisationRepository

    # NEW: deterministic builders and audit orchestrator (no IO here)
    evt_created: EventBuilder
    evt_updated: EventBuilder
    audit: AuditWriter

    # ---------------- Existing API (unchanged) ----------------
    def create(
        self,
        frame: ExecutionFrame,
        *,
        org_id: OrganisationId,
        tenant_id,
        name: str,
        slug: str,
        owner_user_id: str,
        attributes: Optional[Mapping[str, str]] = None,
    ) -> Organisation:
        """Deterministic create: validates, persists via repo, returns snapshot."""
        assert_not_none(frame, "frame")
        candidate = Organisation(
            id=org_id,
            tenant_id=tenant_id,
            name=name,
            slug=slug,
            owner_user_id=owner_user_id,
            attributes=(attributes or {}),
        )
        existing = self.repo.get_by_slug(candidate.slug)
        if existing is not None:
            raise ValidationError("Organisation slug already in use")
        saved = self.repo.save(candidate)
        return saved

    def update_profile(
        self,
        frame: ExecutionFrame,
        *,
        org_id: OrganisationId,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        attributes: Optional[Mapping[str, str]] = None,
    ) -> Organisation:
        assert_not_none(frame, "frame")
        current = self.repo.get_by_id(org_id)
        if current is None:
            raise ValidationError("Organisation not found")

        new = Organisation(
            id=current.id,
            tenant_id=current.tenant_id,
            name=(name if name is not None else current.name),
            slug=(slug if slug is not None else current.slug),
            owner_user_id=current.owner_user_id,
            active=current.active,
            attributes=(attributes if attributes is not None else current.attributes or {}),
        )
        if new.slug != current.slug and self.repo.get_by_slug(new.slug):
            raise ValidationError("Organisation slug already in use")
        return self.repo.save(new)

    # ---------------- New wrappers (envelopes + audit) ----------------
    def create_with_events(
        self,
        frame: ExecutionFrame,
        *,
        org_id: OrganisationId,
        tenant_id,
        name: str,
        slug: str,
        owner_user_id: str,
        attributes: Optional[Mapping[str, str]] = None,
    ) -> Tuple[Organisation, EventEnvelope]:
        """
        Create org, build `organisation.created` envelope, and append an audit entry.
        NOTE: App layer remains IO-free; envelope is returned, audit goes via repository port.
        """
        saved = self.create(
            frame,
            org_id=org_id,
            tenant_id=tenant_id,
            name=name,
            slug=slug,
            owner_user_id=owner_user_id,
            attributes=attributes,
        )

        env = self.evt_created.build(
            tenant_id=frame.tenant_id,
            correlation_id=frame.correlation_id,
            causation_id=frame.causation_id,
            timestamp_ms=frame.timestamp_ms,
            uuid_new_event_id=frame.ctx.uuid_provider.new_event_id,
            payload={
                "organisation_id": str(saved.id),
                "tenant_id": str(saved.tenant_id),
                "slug": saved.slug,
                "name": saved.name,
                "owner_user_id": saved.owner_user_id,
                "attributes": dict(saved.attributes or {}),
            },
        )

        self.audit.write(
            frame,
            category="organisation",
            action="created",
            data={
                "organisation_id": str(saved.id),
                "tenant_id": str(saved.tenant_id),
                "slug": saved.slug,
                "name": saved.name,
                "owner_user_id": saved.owner_user_id,
            },
        )
        return saved, env

    def update_profile_with_events(
        self,
        frame: ExecutionFrame,
        *,
        org_id: OrganisationId,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        attributes: Optional[Mapping[str, str]] = None,
    ) -> Tuple[Organisation, EventEnvelope]:
        """
        Update org, build `organisation.updated` envelope, and append an audit entry.
        """
        saved = self.update_profile(
            frame, org_id=org_id, name=name, slug=slug, attributes=attributes
        )

        env = self.evt_updated.build(
            tenant_id=frame.tenant_id,
            correlation_id=frame.correlation_id,
            causation_id=frame.causation_id,
            timestamp_ms=frame.timestamp_ms,
            uuid_new_event_id=frame.ctx.uuid_provider.new_event_id,
            payload={
                "organisation_id": str(saved.id),
                "tenant_id": str(saved.tenant_id),
                "slug": saved.slug,
                "name": saved.name,
                "attributes": dict(saved.attributes or {}),
            },
        )

        self.audit.write(
            frame,
            category="organisation",
            action="updated",
            data={
                "organisation_id": str(saved.id),
                "tenant_id": str(saved.tenant_id),
                "slug": saved.slug,
                "name": saved.name,
            },
        )
        return saved, env
