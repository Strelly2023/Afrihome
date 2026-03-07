
import os
import sys
import pytest

# Ensure project root is importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

@pytest.fixture(scope="session")
def core_root():
    return os.path.join(PROJECT_ROOT, "core")

@pytest.fixture(scope="session")
def canonical_order():
    return {
        # PHASE 0
        "errors": 1,
        "typing": 2,
        "kernel.freeze": 3,
        "kernel.invariants": 4,
        "identity.uuid": 5,
        "time.clock": 6,
        "time.hlc": 7,
        # PHASE 1
        "context.request_context": 8,
        "context.accessors": 9,
        "execution.execution_context": 10,
        "execution.strict_write": 11,
        "execution.transaction": 12,
        # PHASE 2
        "events.event": 13,
        "events.headers": 14,
        "events.envelope": 15,
        "events.bus": 16,
        "outbox.topic_grammar": 17,
        "outbox.model": 18,
        "outbox.store_protocol": 19,
        "outbox.backoff": 20,
        "outbox.writer": 21,
        "outbox.dispatcher": 22,
        "outbox.memory_store": 23,
        "audit.audit_record": 24,
        "audit.chain": 25,
        "audit.merkle": 26,
        "audit.storage_protocol": 27,
        "audit.audit_writer": 28,
        "saga.state": 29,
        "saga.manager": 30,
        # PHASE 3
        "tenancy.grammar": 31,
        "tenancy.tenant": 32,
        "tenancy.tenant_context": 33,
        "tenancy.resolver": 34,
        "rbac.grammar": 35,
        "rbac.permissions": 36,
        "rbac.roles": 37,
        "rbac.policy_engine": 38,
        "guards.preconditions": 39,
        "guards.idempotency": 40,
        "guards.rate_limit": 41,
        "guards.circuit_breaker": 42,
        "health.registry": 43,
        "health.diagnostics": 44,
        # REGISTRY (LAST)
        "registry.base": 45,
        "registry.scopes": 46,
        "registry.services": 47,
        "registry.handlers": 48,
        "registry.registry": 49,
        "registry.freeze_guard": 50,
    }
