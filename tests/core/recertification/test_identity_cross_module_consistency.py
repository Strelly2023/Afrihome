#test_identity_cross_module_consistency.py
"""
from afritech.platform.core.identity import IdentityId
from afritech.platform.core.decision.trace import DecisionTrace
from afritech.platform.core.audit.trace import AuditTrace


def test_identity_is_consistent_across_decision_and_audit():
    actor = IdentityId("user:123")

    decision_trace = DecisionTrace(
        actor,
        effect=None,
        metadata={}
    )

    audit_trace = AuditTrace.from_decision_trace(decision_trace)

    assert audit_trace.actor == decision_trace.actor
    """