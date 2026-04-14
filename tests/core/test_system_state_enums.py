"""
GA Core â€” System State Enum Tests
================================

Purpose:
- Enforce canonical behavior of system-level enums
- Prevent string drift or semantic ambiguity
- Guarantee determinism and replay safety
- Validate boundary normalization rules

These tests validate SEMANTIC CONTRACTS, not implementations.
"""

import pytest

from afritech.platform.core.typing.enums import (
    SystemLifecycleState,
    KernelState,
    ExecutionMode,
    SystemHealthStatus,
    FeatureFlagState,
    DataLifecycleState,
)


# ============================================================
# Helper â€” generic enum contract checks
# ============================================================

def assert_enum_contract(enum_cls):
    """
    Shared invariant checks for all canonical enums.
    """
    # Closed set: values are non-empty strings
    values = enum_cls.values()
    assert values
    assert all(isinstance(v, str) and v for v in values)

    # Determinism: repeated calls are identical
    assert values == enum_cls.values()

    # Round-trip normalization
    for v in values:
        assert enum_cls.normalize(v) == v
        assert enum_cls.is_valid(v) is True

    # Enum instance normalization
    for member in enum_cls:
        assert enum_cls.normalize(member) == member.value
        assert enum_cls.is_valid(member) is True

    # Invalid values are rejected
    assert enum_cls.is_valid("INVALID") is False
    assert enum_cls.is_valid("") is False

    with pytest.raises(ValueError):
        enum_cls.normalize("INVALID")


# ============================================================
# System Lifecycle
# ============================================================

def test_system_lifecycle_state_contract():
    assert_enum_contract(SystemLifecycleState)
    assert set(SystemLifecycleState.values()) == {
        "initializing",
        "active",
        "suspended",
        "decommissioned",
    }


# ============================================================
# Kernel State
# ============================================================

def test_kernel_state_contract():
    assert_enum_contract(KernelState)
    assert set(KernelState.values()) == {
        "open",
        "frozen",
        "sealed",
    }


# ============================================================
# Execution Mode
# ============================================================

def test_execution_mode_contract():
    assert_enum_contract(ExecutionMode)
    assert set(ExecutionMode.values()) == {
        "development",
        "test",
        "staging",
        "production",
    }


# ============================================================
# System Health Status
# ============================================================

def test_system_health_status_contract():
    assert_enum_contract(SystemHealthStatus)
    assert set(SystemHealthStatus.values()) == {
        "ok",
        "degraded",
        "unavailable",
    }


# ============================================================
# Feature Flag State
# ============================================================

def test_feature_flag_state_contract():
    assert_enum_contract(FeatureFlagState)
    assert set(FeatureFlagState.values()) == {
        "disabled",
        "enabled",
        "gated",
    }


# ============================================================
# Data Lifecycle State
# ============================================================

def test_data_lifecycle_state_contract():
    assert_enum_contract(DataLifecycleState)
    assert set(DataLifecycleState.values()) == {
        "active",
        "archived",
        "deleted",
    }
