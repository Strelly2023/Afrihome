"""
GA Core â€” ABI Snapshot Tests
===========================

Purpose:
- Freeze the public ABI of GA-sealed core modules
- Detect accidental symbol additions, removals, or renames
- Force architectural intent (ADR) for any surface change

RULES:
- Public ABI is defined ONLY via __all__
- Any mismatch is a BREAKING CHANGE
- Changes MUST be intentional and ADR-gated
"""

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def assert_api(module, expected):
    actual = getattr(module, "__all__", None)
    assert actual is not None, (
        f"{module.__name__} must define __all__"
    )

    assert sorted(actual) == sorted(expected), (
        f"\nABI MISMATCH in {module.__name__}\n"
        f"Expected: {sorted(expected)}\n"
        f"Actual:   {sorted(actual)}\n"
        f"\nTHIS IS A BREAKING CHANGE.\n"
        f"Update requires an ADR.\n"
    )


# ============================================================
# core.typing.enums (Semantic Authority â€” GA-Sealed)
# ============================================================

def test_core_typing_enums_abi_snapshot():
    import afritech.platform.core.typing.enums as enums

    assert_api(
        enums,
        [
            "EngineId",
            "Effect",
            "DecisionVerdictType",
            "ConsentState",
            "ReasonCategory",
            "SystemLifecycleState",
            "KernelState",
            "ExecutionMode",
            "SystemHealthStatus",
            "FeatureFlagState",
            "DataLifecycleState",
        ],
    )


# ============================================================
# core.typing.system (Alias Module â€” GA-Sealed)
# ============================================================

def test_core_typing_system_abi_snapshot():
    import afritech.platform.core.typing.system as system

    assert_api(
        system,
        [
            "SystemLifecycleState",
            "KernelState",
            "ExecutionMode",
            "SystemHealthStatus",
            "FeatureFlagState",
            "DataLifecycleState",
        ],
    )


# ============================================================
# core.decision (Canonical Decision Surface â€” GA-Sealed)
# ============================================================

def test_core_decision_abi_snapshot():
    import afritech.platform.core.decision as decision

    assert_api(
        decision,
        [
            "Decision",
            "DecisionVerdict",
            "DecisionReason",
            "DecisionTrace",
            "EngineOutcome",
            "combine",
        ],
    )


# ============================================================
# core.audit (Projection Layer â€” GA-Sealed)
# ============================================================

def test_core_audit_abi_snapshot():
    import afritech.platform.core.audit as audit

    assert_api(
        audit,
        [
            "AuditDecision",
            "AuditTrace",
            "AuditExplanation",
            "GovernanceRecord",
            "AuditComposer",
            "AuditError",
            "InvalidAuditDecisionError",
            "InvalidAuditTraceError",
            "AuditCompositionError",
        ],
    )


# ============================================================
# core.consent (L2 Engine â€” GA-Sealed)
# ============================================================

def test_core_consent_abi_snapshot():
    import afritech.platform.core.consent as consent

    assert_api(
        consent,
        [
            "CONSENT_STATES",
            "CONSENT_SCOPES",
            "LEGAL_BASES",
            "validate_consent_state",
            "validate_consent_scope",
            "validate_legal_basis",
            "ConsentDefinition",
            "ConsentSnapshot",
            "ConsentDecision",
            "ConsentEvaluator",
            "ConsentError",
            "InvalidConsentDefinitionError",
            "InvalidConsentSnapshotError",
            "ConsentEvaluationError",
        ],
    )


# ============================================================
# core.contracts (Declarative Constitution â€” GA-Sealed)
# ============================================================

def test_core_contracts_abi_snapshot():
    import afritech.platform.core.contracts as contracts

    assert_api(
        contracts,
        [
            "DecisionEngineContract",
            "DecisionContract",
            "ContractDecisionVerdict",
            "DecisionInputContract",
            "EffectContract",
            "ENGINE_RETURNS_DECISION_CONTRACT",
            "DETERMINISTIC_DECISIONS_REQUIRED",
            "NO_SIDE_EFFECTS_IN_ENGINES",
            "NO_INFRASTRUCTURE_DEPENDENCY",
        ],
    )
