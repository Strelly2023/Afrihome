"""
ADR-000A — Identity Ontology Re-Certification
Verifies identity normalization behavior is stable and deterministic.
"""

from afritech.platform.core.identity import IdentityId


def test_identity_edge_inputs_are_stable_and_deterministic():
    values = [None, "", "   ", "user:", ":123", "user:123"]

    results = [IdentityId(v) for v in values]

    # Determinism: same input yields same output every time
    for v, result in zip(values, results):
        assert IdentityId(v) == result