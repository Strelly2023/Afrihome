Below is a **complete, final, constitution‑grade ADR** for the **Runtime Mutation Ban Outside Constructors**, aligned with **OP (Operations)** and **FT (Failure & Truth)**, and consistent with your existing governance (ADR‑000 Core Freeze, ADR‑000A amendments, checksum gate, re‑certification).

You can commit this **as‑is**.

***

## 📘 `docs/decisions/ADR-OP-001-runtime-mutation-ban.md`

````markdown
# ADR-OP-001 — Runtime Mutation Ban Outside Constructors

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | OP / FT — Operations & Failure/Truth |
| ADR ID | ADR-OP-001 |
| Constitutional Level | Foundational (Operational Law) |
| Breaking Change | Yes (by design) |
| Requires Migration | Possibly |
| Enforced By Tests | ✅ Yes |

---

## 1. Decision

AfriTech **forbids all runtime mutation of state outside of constructors**.

After an object is constructed, its state MUST NOT change by any mechanism.
State may only be *created* at construction time, not *modified* afterward.

This applies to **instances, classes, descriptors, and metaclasses**.

---

## 2. Scope

This rule applies to:

- All code under `afritech/platform/core`
- Any code path executed as part of core semantics
- Any object participating in decisions, identity, audit, policy, or governance

Lower layers MUST NOT weaken this rule.

---

## 3. What Is Forbidden (Non‑Exhaustive)

### 3.1 Instance Mutation After Construction

```python
class X:
    def __init__(self):
        self.value = 1

    def mutate(self):
        self.value = 2   # ❌ forbidden
````

### 3.2 Attribute Deletion After Construction

```python
def cleanup(self):
    del self.value      # ❌ forbidden
```

### 3.3 Container Mutation on Object State

```python
self.items.append(x)   # ❌ forbidden
self.map[key] = value  # ❌ forbidden
```

### 3.4 `__setattr__` and `__delattr__` Overrides

```python
def __setattr__(self, k, v): ...
def __delattr__(self, k): ...
```

Any override is forbidden, regardless of delegation or guards.

***

### 3.5 Descriptor Setters

```python
@property
def x(self): ...

@x.setter
def x(self, v):         # ❌ forbidden
```

```python
def __set__(self, obj, value):  # ❌ forbidden
```

***

### 3.6 Class Attribute Mutation at Runtime

```python
Class.attr = value      # ❌ forbidden
```

```python
cls.attr = value        # ❌ forbidden
```

```python
type(self).attr = value # ❌ forbidden
```

***

### 3.7 Metaclass Mutation

```python
class Meta(type):
    def __setattr__(cls, k, v):  # ❌ forbidden
        ...
```

***

## 4. What Is Allowed

### 4.1 Construction‑Time Assignment Only

```python
class X:
    def __init__(self, value):
        self.value = value  # ✅ allowed
```

### 4.2 Pure, Read‑Only Behavior

```python
def compute(self):
    return self.value * 2  # ✅ allowed
```

### 4.3 Functional Replacement (New Instance)

```python
def with_value(self, v):
    return X(v)            # ✅ allowed
```

***

## 5. Rationale (FT — Failure & Truth)

Runtime mutation violates **Failure Truth**:

*   Hidden state changes make failures non‑reproducible
*   Debugging lies about the cause of failure
*   Replay diverges from original execution
*   Audits cannot be trusted

If state may change after construction, **truth is no longer stable**.

Therefore:

> **State must be fixed at the moment of construction.**

***

## 6. Determinism and Replay Guarantees

This ADR guarantees:

*   Deterministic execution
*   Referentially stable objects
*   Replay safety from historical logs
*   Audit consistency
*   Test reproducibility

These guarantees cannot be achieved if mutation is allowed.

***

## 7. Relationship to Other ADRs

This ADR is a direct operational consequence of:

*   **ADR‑000 — Core Freeze** (immutability of meaning)
*   **ADR‑000A — Core Amendments** (explicit correction only)
*   Core checksum ledger (cryptographic integrity)

It is enforced mechanically and continuously.

***

## 8. Enforcement

Enforced by static analysis and CI gates:

*   `tools/check_runtime_mutation.py`
*   Descriptor, class, and metaclass mutation detection
*   Fail‑closed CI policy

Violations **block merges**.

***

## 9. Exceptions

There is **no exception mechanism**.

If mutation is required:

1.  The design is incorrect, or
2.  The state belongs outside the Core, or
3.  A new ADR must explicitly amend this rule

Convenience is not a justification.

***

## 10. Consequences

### Positive

*   Strong determinism
*   Honest failures
*   Replayable history
*   Auditable semantics
*   Stable governance

### Trade‑offs

*   No in‑place updates
*   Requires functional or construction‑based patterns
*   May require refactors

These trade‑offs are deliberate and accepted.

***

## 11. Final Law

> **State is created, not changed.  
> If it changes, truth breaks.**

This rule is binding for all present and future Core code.

***

✅ **Accepted and Enforced**

```

---

## ✅ Where this fits in your system

- Pairs with the **Core Freeze** (meaning immutability)
- Ensures **Failure & Truth** are preserved operationally
- Backed by **mechanical CI enforcement**
- Proven by **re‑certification tests**

If you want next, I can:
- add a short **“How to refactor safely under ADR‑OP‑001”** guide
- generate an **exception decision template** (even though exceptions are discouraged)
- link this ADR explicitly from `docs/README.md` under Governance

Just say the word.
```
