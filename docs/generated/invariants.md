# Core Decision System — Semantic Invariants

> ⚠️ **GENERATED FILE — DO NOT EDIT**
>
> This document is generated directly from executable tests.
> Tests are the source of truth; this file is a derived view.

---

## `test_consent_denial_is_absolute`

**Source test:** `test_core_cross_engine_invariants.py`

Invariant:
Any consent denial results in a final DENY,
regardless of other engine outcomes.

---

## `test_decision_combination_is_deterministic`

**Source test:** `test_core_cross_engine_invariants.py`

Invariant:
Combining the same EngineOutcomes always produces
the same final Decision.

---

## `test_engine_order_independence`

**Source test:** `test_core_cross_engine_invariants.py`

Invariant:
The order in which EngineOutcomes are combined
must not affect the final Decision.

---

## `test_global_deny_wins_over_allows`

**Source test:** `test_core_cross_engine_invariants.py`

Invariant:
DENY always dominates ALLOW across all decision engines.

---

## `test_multiple_denials_preserve_all_reasons`

**Source test:** `test_core_cross_engine_invariants.py`

Invariant:
When multiple engines deny, all denial reasons
must be preserved in the final Decision.

---

## `test_quota_denial_is_authoritative`

**Source test:** `test_core_cross_engine_invariants.py`

Invariant:
Quota denial overrides all authorization ALLOW decisions.

---

## `test_soft_deleted_tenant_blocks_all_access`

**Source test:** `test_core_cross_engine_invariants.py`

Invariant:
A soft-deleted tenant results in a system-wide DENY,
regardless of other authorization signals.

---
