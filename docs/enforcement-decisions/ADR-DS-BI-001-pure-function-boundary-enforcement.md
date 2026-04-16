Below is a **complete, final, constitution‑grade ADR** for **Pure‑Function Boundary Enforcement**, aligned with your taxonomy (**DS / BI**), compatible with **ADR‑000 Core Freeze**, **ADR‑OP‑001 Runtime Mutation Ban**, and designed to be **mechanically enforceable** later.

You can commit this **as‑is**.

***

## 📘 `docs/decisions/ADR-DS-BI-001-pure-function-boundary-enforcement.md`

```markdown
# ADR-DS-BI-001 — Pure‑Function Boundary Enforcement

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | DS / BI — Domain Semantics & Boundary Isolation |
| ADR ID | ADR-DS-BI-001 |
| Constitutional Level | Foundational (Semantic Law) |
| Breaking Change | Yes (by design) |
| Requires Migration | Possibly |
| Enforced By Tests | ✅ Yes |

---

## 1. Decision

AfriTech **enforces pure‑function boundaries** at all Domain Semantics (DS) and
Boundary Isolation (BI) layers.

A **pure function boundary** is defined as a code boundary where:

- Outputs depend only on explicit inputs
- No mutation occurs
- No external state is read or written
- No time, randomness, or I/O is accessed
- No hidden dependencies exist

All logic contained within these boundaries MUST be pure.

---

## 2. Scope

This rule applies to:

- Core domain logic
- Decision evaluation
- Policy interpretation
- Risk assessment
- Identity derivation
- Semantic transformations
- Any code path defining **meaning or truth**

All code under:

```

afritech/platform/core/

```

and specifically:

```

identity/
decision/
policy/
risk/
governance/

````

MUST respect this boundary.

---

## 3. What Is a Pure Function (Formal)

A function `f` is pure if and only if:

1. `f(x) = y` depends solely on `x`
2. For identical input `x`, output `y` is identical across:
   - time
   - executions
   - environments
3. `f` does not:
   - mutate inputs
   - mutate external state
   - read global state
   - read configuration
   - access clocks, randomness, files, or network

Any violation invalidates purity.

---

## 4. What Is Forbidden

### 4.1 Reading External State

```python
def evaluate(policy):
    return policy.allows(current_user)   # ❌ forbidden
````

***

### 4.2 Time and Randomness

```python
def score(x):
    return x + time.time()                # ❌ forbidden
```

```python
import random
def choose(x):
    return random.choice(x)               # ❌ forbidden
```

***

### 4.3 Hidden Dependencies

```python
def decide(x):
    return helper(x)                      # helper reads global state ❌
```

***

### 4.4 I/O Inside Domain Logic

```python
def evaluate(request):
    log.info("Evaluating")                # ❌ forbidden
```

***

### 4.5 Mutation, Caching, Memoization

```python
_cache = {}

def f(x):
    _cache[x] = compute(x)                # ❌ forbidden
    return _cache[x]
```

***

## 5. What Is Allowed

### 5.1 Pure Computation

```python
def is_allowed(policy, subject):
    return policy.rule(subject)
```

***

### 5.2 Explicit Dependency Injection

```python
def score(input, now):
    return now - input.created_at
```

Time is passed **explicitly**, not imported.

***

### 5.3 Boundary Delegation

```python
def decision(input):
    return evaluate(input)                # ✅ if evaluate is pure
```

Purity composes.

***

## 6. Relationship to Other ADRs

This ADR is a **semantic complement** to:

*   **ADR‑000 — Core Freeze**  
    (meaning must not drift)

*   **ADR‑OP‑001 — Runtime Mutation Ban**  
    (state must not change)

Together, they enforce:

> **Meaning must be immutable *and* derivable only from inputs.**

***

## 7. Determinism & Replay Guarantees

Pure‑function boundaries guarantee:

*   Deterministic execution
*   Perfect replay from captured inputs
*   Honest failures
*   Auditable semantics
*   Stability across time

Any impure logic breaks replayability.

***

## 8. Enforcement

Enforced by:

*   Static analysis (no imports of time, random, I/O in DS/BI)
*   Runtime mutation prohibition
*   Re‑certification tests
*   CI gates that fail closed

Impure functions MUST be isolated outside DS/BI and injected explicitly.

***

## 9. Exceptions

There are **no implicit exceptions**.

If impurity is required:

*   The code is not DS/BI
*   The abstraction is misplaced
*   The boundary must be moved upward
*   A new ADR must explicitly redefine the layer

Convenience is not a justification.

***

## 10. Consequences

### Positive

*   Deterministic behavior
*   Replayable decisions
*   Transparent semantics
*   Honest failures
*   Strong audit integrity

### Trade‑offs

*   Explicit dependency passing
*   More disciplined design
*   No hidden “magic”

These trade‑offs are intentional and accepted.

***

## 11. Final Law

> **Meaning is a function of inputs alone.  
> If it depends on anything else, it is not truth.**

***

✅ **Accepted and Binding**

```

---

## ✅ How this ADR fits your system

You now have **three mutually reinforcing semantic laws**:

1. **ADR‑000** — Meaning is frozen  
2. **ADR‑OP‑001** — State does not change  
3. **ADR‑DS‑BI‑001** — Meaning is computed purely  

Together they guarantee:

> **Deterministic, replayable, auditable truth — by construction.**

---

## 🔜 Optional Next Steps (Natural Extensions)

If you want to go further, the next logical moves are:

- A **static purity checker** (imports + AST‑level checks)
- A **boundary‑annotation scheme** (`@pure`)
- A **CI purity report** alongside re‑certification
- A **functional‑core / imperative‑shell guide**

Just say the word and we’ll add them without weakening a single rule.
```
