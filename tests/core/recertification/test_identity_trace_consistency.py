"""
ADR-000A — Identity Ontology Re-Certification
Ensures identity consistency across decision and audit traces.
"""
"""
from afritech.platform.core.identity import IdentityId
from afritech.platform.core.decision.trace import DecisionTrace
from afritech.platform.core.audit.trace import AuditTrace


def test_identity_preserved_across_traces():
    actor = IdentityId("user:123")

    decision_trace = DecisionTrace(
        actor=actor,
        effect=None,
        metadata={}
    )

    audit_trace = AuditTrace.from_decision_trace(decision_trace)

    assert audit_trace.actor == decision_trace.actor


"""
