"""
ADR-000A — Identity Ontology Re-Certification
Ensures deterministic identity construction.
"""

from afritech.platform.core.identity import IdentityId


def test_identity_construction_is_deterministic():
    identities = [IdentityId("tenant:alpha") for _ in range(10)]

    for i in identities[1:]:
        assert i == identities[0]
        assert hash(i) == hash(identities[0])
