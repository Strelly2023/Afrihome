
# ADR-BI-005 — Forbidden Singleton Pattern

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | BI — Boundary & Isolation |
| ADR ID | ADR-BI-005 |
| Constitutional Level | Structural |
| Breaking Change | No |
| Requires Migration | No |
| Enforced By Tests | ✅ Yes |

---

## 1. Boundary Rule

AfriTech MUST NOT contain **singleton objects** that hold or expose
**runtime‑mutable state**.

A **singleton** is defined as:

- a module‑level instantiated object, AND
- intended for global reuse or access, AND
- capable of holding or mutating state during execution.

Singletons create hidden global coupling, violate isolation boundaries,
and undermine determinism, replayability, and testability.

---

## 2. Rationale

Hidden global state is one of the most fragile architectural failures.

Singletons:

- bypass dependency injection
- prevent explicit ownership of state
- make execution order observable
- collapse isolation between modules
- break replay and reproducibility guarantees

AfriTech’s architecture requires that **all mutable state has explicit ownership**.
Singletons violate this requirement by construction.

---

## 3. Forbidden Patterns

The following patterns are **constitutionally illegal**.

### 3.1 Explicit Singleton Instances

```python
ENGINE = Engine()
registry = Registry()
client = HttpClient()
````

### 3.2 Hidden Singletons

```python
_instance = SomeClass()

def get_instance():
    return _instance
```

### 3.3 Lazy / Deferred Singletons

```python
_engine = None

def engine():
    global _engine
    if _engine is None:
        _engine = Engine()
    return _engine
```

### 3.4 Module‑Scoped Service Objects

```python
service = AuthorizationService()
manager = ResourceManager()
provider = IdentityProvider()
```

***

## 4. Explicitly Allowed

The following are **explicitly allowed and NOT considered singletons**.

### 4.1 Type‑Level Constructs

*   typing aliases
*   identity value objects
*   permission and role types
*   covariance / variance helpers

```python
TenantId = NewType("TenantId", str)
Permission = Enum("Permission", ["READ", "WRITE"])
ID_co = TypeVar("ID_co", covariant=True)
```

### 4.2 Immutable / Stateless Objects

*   enums
*   frozen dataclasses
*   regex patterns
*   pure constants

```python
EMAIL_RE = re.compile(r"...")
MAX_RETRIES = 5
```

### 4.3 Factories and Dependency Injection

```python
def make_engine() -> Engine:
    return Engine()

def handler(engine: Engine):
    ...
```

Each call produces an independent instance.
Ownership is explicit.

***

## 5. Invariants

The following invariants MUST hold:

*   [ ] No globally shared runtime state
*   [ ] No implicit reuse of stateful objects
*   [ ] No hidden object lifetime
*   [ ] All state ownership is explicit
*   [ ] Deterministic execution and replay preserved

Violation of any invariant invalidates compliance.

***

## 6. Forbidden

The following are **explicitly forbidden**:

*   singleton instance reuse
*   global service objects
*   lazy initialization of mutable state
*   “one instance per process” assumptions
*   implicit caches or registries at module scope

There is **no exception process**.

***

## 7. Enforcement Mechanism

Enforcement is performed by static analysis via:

```text
tools/check_global_mutable_state.py
```

The checker MUST detect:

*   explicit singleton instantiation
*   hidden singleton patterns
*   lazy global caches
*   stateful module‑level objects

Enforcement is **fail‑closed** and **CI‑enforced**.

***

## 8. Relationship to Other ADRs

This ADR works in combination with:

*   **ADR‑BI‑004** — Global Mutable State Prohibition
*   **ADR‑FT‑001** — Fail‑Closed Semantics
*   **ADR‑KE‑001** — Deterministic Execution Order

Together they ensure:

*   no hidden state
*   no execution‑order dependence
*   no architectural ambiguity

***

## 9. Consequences

### Positive

*   deterministic execution
*   replayable behavior
*   explicit dependency boundaries
*   honest tests
*   simpler reasoning

### Trade‑off

*   additional plumbing via dependency injection
*   no convenience singletons

This trade‑off is **intentional and accepted**.

***

## 10. Final Law

> **If an object holds state, it must not be global.**  
> **If an object is global, it must hold no state.**

***

## Status

✅ **Accepted and Binding**

This ADR is constitutional law for all present and future AfriTech code.

```

---

## ✅ What This Completes

With **ADR‑BI‑005**, AfriTech now has **sealed state discipline**:

- ❌ no global mutable objects
- ❌ no hidden singletons
- ❌ no lazy global caches
- ✅ explicit ownership everywhere
- ✅ deterministic execution
- ✅ replay safety

This closes one of the **hardest-to-enforce architectural loopholes**.

---

### Legitimate Next Steps (Optional)
Only proceed if you want to keep encoding law:

- **Lazy cache detection (specialized singleton subclass)**
- **Runtime mutation ban outside constructors (OP / FT)**
- **Pure‑function boundary enforcement (DS / BI)**

Just name the next rule to encode.
```
