"""
ADR-000A — Identity Ontology Re-Certification
Ensures identity equality semantics are correct.
"""

from afritech.platform.core.identity import IdentityId


def test_identity_equal_for_same_logical_identity():
    id1 = IdentityId("user:123")
    id2 = IdentityId("user:123")

    assert id1 == id2
    assert hash(id1) == hash(id2)


def test_identity_not_equal_for_different_logical_identity():
    id1 = IdentityId("user:123")
    id2 = IdentityId("user:456")

    assert id1 != id2