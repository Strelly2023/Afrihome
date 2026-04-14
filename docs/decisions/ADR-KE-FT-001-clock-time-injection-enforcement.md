Below is a **complete, constitution‑grade ADR** for **Clock / Time Injection Enforcement**, aligned with your taxonomy (**KE / FT**) and designed to integrate cleanly with:

*   **ADR‑000 — Core Freeze**
*   **ADR‑OP‑001 — Runtime Mutation Ban**
*   **ADR‑DS‑BI‑001 — Pure‑Function Boundary Enforcement**
*   Your CI gates, purity report, and re‑certification model

You can commit this **as‑is**.

***

## 📘 `docs/decisions/ADR-KE-FT-001-clock-time-injection-enforcement.md`

```markdown
# ADR-KE-FT-001 — Clock / Time Injection Enforcement

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | KE / FT — Kernel Environment & Failure/Truth |
| ADR ID | ADR-KE-FT-001 |
| Constitutional Level | Foundational (Kernel Law) |
| Breaking Change | Yes (by design) |
| Requires Migration | Possibly |
| Enforced By Tests | ✅ Yes |

---

## 1. Decision

AfriTech **forbids all implicit access to system time** within Core, Domain Semantics (DS),
and Boundary Isolation (BI) code.

All access to time MUST be:
- explicit
- injectable
- deterministic
- test‑controlled

Any use of clocks, timestamps, “now”, or wall‑time values without explicit injection
is constitutionally forbidden.

---

## 2. Scope

This rule applies to **all code defining meaning or truth**, including:

```

afritech/platform/core/

````

and specifically:
- identity
- decision
- policy
- risk
- governance
- audit semantics

Lower layers (execution, adapters, infra) may access system time,
but MUST pass it explicitly across boundaries.

---

## 3. What Is Forbidden

### 3.1 Direct System Time Access

```python
import time
time.time()            # ❌ forbidden
````

```python
from datetime import datetime
datetime.now()         # ❌ forbidden
```

```python
datetime.utcnow()      # ❌ forbidden
```

***

### 3.2 Hidden Time Dependencies

```python
def evaluate(x):
    return x.expires_at < datetime.now()   # ❌ forbidden
```

***

### 3.3 Time‑Based Defaults

```python
def f(now=datetime.now()):  # ❌ forbidden
    ...
```

***

### 3.4 Implicit Clocks in Libraries

Any Core function that indirectly reads time via:

*   third‑party libraries
*   global clocks
*   environment variables

is forbidden unless time is explicitly injected.

***

## 4. What Is Allowed

### 4.1 Explicit Time Injection

```python
def evaluate(policy, now):
    return now < policy.expires_at
```

Time is an **input**, not an ambient fact.

***

### 4.2 Clock Abstractions (Injected)

```python
class Clock:
    def now(self): ...
```

```python
def decide(input, clock):
    return input.expires_at < clock.now()
```

The clock itself may be impure — but **must live outside DS/BI boundaries**.

***

### 4.3 Pure Time Values

```python
DecisionTrace(
    engine=engine_id,
    effect=effect,
    metadata={"at": at_time}
)
```

Captured timestamps are allowed as immutable data.

***

## 5. Rationale (FT — Failure & Truth)

Implicit time access breaks **Failure Truth**:

*   Identical inputs yield different results over time
*   Replay becomes impossible
*   Debugging lies about causality
*   Audits cannot be trusted
*   Tests become flaky and dishonest

Time is **the most dangerous hidden input**.

Therefore:

> **If time influences meaning, it must be explicit.**

***

## 6. Determinism & Replay Guarantees

This ADR guarantees:

*   Deterministic semantics
*   Replayable decisions
*   Time‑controlled testing
*   Audit reproducibility
*   Honest failure diagnosis

All guarantees collapse if time is accessed implicitly.

***

## 7. Relationship to Other ADRs

This ADR completes the semantic enforcement triangle:

*   **ADR‑000 — Core Freeze**  
    (meaning must not drift)

*   **ADR‑OP‑001 — Runtime Mutation Ban**  
    (state must not change)

*   **ADR‑DS‑BI‑001 — Pure‑Function Boundary Enforcement**  
    (outputs depend only on inputs)

Together, these require:

> **Time must be an explicit input, never an ambient dependency.**

***

## 8. Enforcement

Enforced by:

*   Static analysis (imports of `time`, `datetime.now`, etc.)
*   CI purity checks (time access is a violation)
*   Re‑certification tests
*   CI failure decision tree

Any violation is **fail‑closed**.

***

## 9. Exceptions

There are **no implicit exceptions**.

If code “needs” time:

*   The boundary is wrong
*   The abstraction is wrong
*   The code is not DS/BI
*   Time must be injected

Convenience is not a justification.

***

## 10. Consequences

### Positive

*   Deterministic behavior
*   Replay safety
*   Honest tests
*   Auditable semantics
*   Stable time‑based logic

### Trade‑offs

*   Extra parameters
*   Explicit propagation of time
*   No ambient “now”

These trade‑offs are deliberate and accepted.

***

## 11. Final Law

> **Time is data.  
> If it affects meaning, it must be passed, not read.**

***

✅ **Accepted and Binding**

```

---

## ✅ How this fits your system

You now have **four mutually reinforcing kernel truths**:

| Law | Meaning |
|----|-------|
ADR‑000 | Meaning is frozen |
ADR‑OP‑001 | State does not change |
ADR‑DS‑BI‑001 | Meaning is pure |
ADR‑KE‑FT‑001 | Time is explicit |

Together they guarantee:

> **Deterministic, replayable, auditable truth — by construction.**

---

## 🔜 Natural Next Steps (Optional)

You may want to add:
- a **static time‑access checker** emitting purity violations
- a `Clock` interface in a non‑Core layer
- a **time injection section** in the refactoring guide
- CI annotations that link time violations to this ADR

If you want, I can generate those next without weakening a single rule.

Just say the word.
```
