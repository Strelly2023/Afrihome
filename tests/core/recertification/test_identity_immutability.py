"""
ADR-000A — Identity Ontology Re-Certification
Ensures identity immutability.
"""

import pytest
from afritech.platform.core.identity import IdentityId


def test_identity_is_immutable():
    identity = IdentityId("user:123")

    with pytest.raises(Exception):
        identity.value = "user:456"


def test_identity_has_no_mutating_methods():
    identity = IdentityId("user:123")

    for attr in dir(identity):
        assert not attr.startswith("set_")
