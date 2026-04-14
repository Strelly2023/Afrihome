
## 📘 ADR‑BI‑006 — Lazy Global Cache Prohibition

**Canonical location**

```text
docs/decisions/ADR-BI-006-lazy-global-cache-prohibition.md
```

***

````markdown
# ADR-BI-006 — Lazy Global Cache Prohibition

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | BI — Boundary & Isolation |
| ADR ID | ADR-BI-006 |
| Constitutional Level | Structural |
| Breaking Change | No |
| Requires Migration | No |
| Enforced By Tests | ✅ Yes |

---

## 1. Boundary Rule

AfriTech MUST NOT contain **lazy global caches**.

A *lazy global cache* is any pattern where:
- a module‑level name is declared with an immutable or null sentinel, AND
- that name is later assigned or mutated at runtime, AND
- the resulting object is reused across calls or execution contexts.

Lazy global caches create hidden global state while evading detection at import time.

They are constitutionally forbidden.

---

## 2. Rationale

Lazy global caches violate the same architectural invariants as explicit singletons,
but in a more subtle and dangerous form.

They:

- hide state creation until execution begins,
- make behavior dependent on execution order,
- defeat replay and deterministic reasoning,
- bypass explicit dependency ownership,
- conceal cross‑layer coupling.

Because their mutation is deferred, they evade review and static reasoning.
AfriTech treats this pattern as an intentional form of hidden global state.

---

## 3. Canonical Forbidden Patterns

The following patterns are **constitutionally illegal**.

### 3.1 Sentinel‑Based Lazy Cache

```python
_cache = None

def get_user(id):
    global _cache
    if _cache is None:
        _cache = {}
    return _cache[id]
````

***

### 3.2 Deferred Global Initialization

```python
_result = None

def compute():
    global _result
    if _result is None:
        _result = expensive()
    return _result
```

***

### 3.3 Default‑Dict / Accumulating Cache

```python
_registry = {}

def register(key, value):
    _registry[key] = value
```

***

### 3.4 Function‑Attribute Cache (Hidden Global)

```python
def parse(x):
    if not hasattr(parse, "_cache"):
        parse._cache = {}
    return parse._cache[x]
```

Function attributes are global state by another name.

***

## 4. Explicitly Allowed

The following patterns are **explicitly permitted**.

### 4.1 Explicit Ownership via Instances

```python
class Cache:
    def __init__(self):
        self._data = {}
```

Ownership is instance‑scoped, not global.

***

### 4.2 Dependency Injection

```python
def handler(cache):
    ...
```

***

### 4.3 Factory‑Constructed State

```python
def make_cache():
    return {}
```

Each call produces a new object.

***

### 4.4 Type‑Level or Semantic Constructs

```python
UserId = NewType("UserId", str)
Permission = Enum("Permission", ["READ", "WRITE"])
```

Type‑level semantics are not state.

***

## 5. Invariants

The following MUST always hold:

*   [ ] No module‑level name transitions from immutable → mutable
*   [ ] No deferred mutation of global bindings
*   [ ] No execution‑order‑dependent state creation
*   [ ] All state has explicit, local ownership
*   [ ] Deterministic execution and replay preserved

Violation of any invariant constitutes a constitutional breach.

***

## 6. Forbidden

The following are explicitly forbidden:

*   lazy global caches
*   sentinel‑to‑state patterns
*   deferred initialization of mutable objects
*   function‑attribute caches
*   “compute once” globals
*   “just an optimization” caches

There is no exception process.

***

## 7. Enforcement Mechanism

This ADR is enforced via static analysis by:

```text
tools/check_global_mutable_state.py
```

The checker MUST detect:

*   global sentinels (`None`, `()`, empty literals),
*   followed by later mutation or reassignment,
*   inside functions or execution paths.

Enforcement is fail‑closed and CI‑enforced.

***

## 8. Relationship to Other ADRs

This ADR supplements and completes:

*   **ADR‑BI‑004 — Global Mutable State Prohibition**
*   **ADR‑BI‑005 — Forbidden Singleton Pattern**
*   **ADR‑FT‑001 — Fail‑Closed Semantics**
*   **ADR‑KE‑001 — Deterministic Execution Order**

Together they seal AfriTech’s state discipline.

***

## 9. Consequences

### Positive

*   deterministic behavior
*   honest tests
*   replay safety
*   explicit state ownership
*   stable architectural boundaries

### Trade‑off

*   explicit passing of cache/state objects
*   no “free” optimizations at global scope

This trade‑off is intentional and accepted.

***

## 10. Final Law

> **State that appears later is still state.**  
> **Deferred global mutation is forbidden.**

***

## Status

✅ **Accepted and Binding**

This ADR is constitutional law for all present and future AfriTech code.

```

---

### What this completes

With **ADR‑BI‑006**, AfriTech now forbids **all three** forms of hidden state:

1. Global mutable containers ✅  
2. Singleton objects ✅  
3. **Lazy / deferred global caches ✅**

There are now **no remaining ways** to smuggle global state into the system.

If you want to proceed next, the clean successors are:

- **Runtime mutation outside constructors (OP / FT)**
- **Lazy cache detection implementation (AST‑level)**
- **Pure‑function boundary enforcement (DS / BI)**

Say the word when ready.
```
