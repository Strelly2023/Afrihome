from core.time.clock import FixedClock
from core.typing import UnixMillis, RequestId, CorrelationId, CausationId
from core.context.request_context import RequestContext
from core.identity.uuid import DeterministicUUIDProvider
from core.execution.execution_context import ExecutionContext

from control_plane.application.tenancy.tenant_service import TenantService
from tests.helpers.memory_tenant_repo import MemoryTenantRepository


# Build deterministic execution context
ctx = ExecutionContext(
    request_context=RequestContext(
        request_id=RequestId("req-1"),
        correlation_id=CorrelationId("corr-1"),
        causation_id=CausationId("cause-1"),
        timestamp_ms=UnixMillis(1000),
    ),
    clock=FixedClock(UnixMillis(1000)),
    uuid_provider=DeterministicUUIDProvider(seed="afrihome"),
)

repo = MemoryTenantRepository()
svc  = TenantService(ctx=ctx, repo=repo)

tenant = svc.create_tenant(
    slug="acme",
    data_region="AU",
    regulatory_profile="GDPR",
    display_name="Acme Inc",
)
assert tenant.active is True
tenant = svc.suspend(tenant.tenant_id)
assert tenant.active is False
tenant = svc.activate(tenant.tenant_id)
assert tenant.active is True
tenant = svc.rename(tenant.tenant_id, "Acme International")
assert tenant.name == "Acme International"