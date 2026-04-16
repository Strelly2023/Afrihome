from pathlib import Path
import yaml
import pytest

"""
This test enforces a core governance invariant:

    Every Architectural Decision Record (ADR) MUST declare
    how it is enforced.

An ADR without enforcement is a "paper law" and is forbidden.

This test is intentionally structural:
- It verifies presence, not correctness, of enforcement
- It allows incremental development
- It prevents silent introduction of ungoverned laws
"""


ADR_DIR = Path("adr")


def test_every_adr_declares_enforcement():
    """
    Ensure that every ADR explicitly declares an enforcement section.

    Enforcement may be:
    - tooling
    - tests (test-only)
    - process / manual (explicitly stated)

    Absence of enforcement is a governance failure.
    """
    assert ADR_DIR.exists(), "ADR directory does not exist"

    adrs = sorted(ADR_DIR.glob("ADR-*.yaml"))

    # Guard against accidental deletion or rename
    assert adrs, "No ADR files found (ADR-*.yaml)"

    for adr in adrs:
        try:
            data = yaml.safe_load(adr.read_text())
        except Exception as exc:
            pytest.fail(f"{adr.name} is not valid YAML: {exc}")

        assert isinstance(
            data, dict
        ), f"{adr.name} must contain a YAML mapping"

        assert (
            "enforcement" in data
        ), f"{adr.name} missing required 'enforcement' section"