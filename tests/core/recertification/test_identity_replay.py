"""
ADR-000A — Identity Ontology Re-Certification
Ensures replay safety.
"""

from afritech.platform.core.identity import IdentityId


def test_identity_replay_from_historical_value():
    historical_identity_value = "user:123"

    past = IdentityId(historical_identity_value)
    replay = IdentityId(historical_identity_value)

    assert past == replay