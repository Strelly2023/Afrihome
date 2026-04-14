Below is a **complete, practical refactoring guide** specifically designed to accompany  
**ADR‑OP‑001 — Runtime Mutation Ban Outside Constructors**.

This guide is **not theoretical**. It shows **exact refactoring patterns** you should apply when migrating code to comply with the ADR—without weakening correctness, determinism, or auditability.

You can commit this as a companion document.

***

## 📘 `docs/guides/refactoring-under-ADR-OP-001.md`

````markdown
# Refactoring Guide — ADR‑OP‑001
## Runtime Mutation Ban Outside Constructors

This guide explains how to **safely refactor existing code** to comply with:

> **ADR‑OP‑001 — Runtime Mutation Ban Outside Constructors**

The rule is simple:

> **State may be created only at construction time.  
> State must not change afterward.**

This guide shows how to convert common mutation patterns into compliant, deterministic designs.

---

## 1. Recognizing Illegal Patterns

### ❌ Post‑construction mutation

```python
obj.value = 42
obj.items.append(x)
del obj.flag
````

### ❌ Stateful methods

```python
def increment(self):
    self.count += 1
```

### ❌ Lazy initialization

```python
if self.cache is None:
    self.cache = {}
```

### ❌ Runtime configuration

```python
self.timeout = new_timeout
```

If you see any of the above outside `__init__`, the code **violates ADR‑OP‑001**.

***

## 2. Canonical Refactoring Patterns

### ✅ Pattern 1 — Move State to the Constructor

**Before (illegal):**

```python
class Engine:
    def start(self):
        self.ready = True
```

**After (legal):**

```python
class Engine:
    def __init__(self, ready: bool):
        self.ready = ready
```

**Key idea:**  
If state is needed, it must be known **at construction time**.

***

### ✅ Pattern 2 — Functional Replacement (Object Recreation)

**Before (illegal mutation):**

```python
def with_value(self, v):
    self.value = v
```

**After (legal replacement):**

```python
def with_value(self, v):
    return X(v)
```

You do not mutate objects — you **replace them**.

> Think: *values, not variables*.

***

### ✅ Pattern 3 — Explicit State Objects (Encapsulation)

If state must evolve, move it **outside the Core** or **into a separate state container**.

**Before:**

```python
class Counter:
    def inc(self):
        self.count += 1
```

**After:**

```python
@dataclass
class CounterState:
    count: int


class Counter:
    def __init__(self, state: CounterState):
        self.state = state
```

Mutation happens on `CounterState`, not on the Core object.

***

### ✅ Pattern 4 — Constructor Composition

**Before:**

```python
self.a = compute_a()
self.b = compute_b()
```

**After:**

```python
def __init__(self, a, b):
    self.a = a
    self.b = b
```

Call `compute_a()` and `compute_b()` **before construction**, not during runtime.

***

## 3. Handling Container State

### ❌ Illegal

```python
self.items.append(x)
self.map[k] = v
```

### ✅ Legal alternatives

#### Option A — Recreate container

```python
def with_item(self, x):
    return X(self.items + [x])
```

#### Option B — Immutable containers

```python
from frozenset import frozenset

self.items = frozenset(items)
```

***

## 4. Replacing `__setattr__` / `__delattr__`

### ❌ Forbidden

```python
def __setattr__(self, k, v): ...
def __delattr__(self, k): ...
```

### ✅ Correct alternative

Remove overrides entirely.

If immutability must be enforced, rely on:

*   frozen dataclasses
*   no mutator methods
*   static analysis (CI)

***

## 5. Properties and Descriptors

### ❌ Forbidden

```python
@x.setter
def x(self, value):
    self._x = value
```

### ✅ Allowed

```python
@property
def x(self):
    return self._x
```

For changes, use **replacement constructors**:

```python
def with_x(self, value):
    return X(value)
```

***

## 6. Class and Metaclass State

### ❌ Forbidden

```python
Class.attr = v
cls.attr = v
type(self).attr = v
```

### ✅ Legal approach

If configuration is needed:

*   pass it explicitly
*   inject it at construction
*   store it outside Core (e.g. Control Plane)

***

## 7. Migration Strategy (Safe Order)

1.  **Freeze the Core** (ADR‑000 enforced)
2.  Identify mutations with CI (`check_runtime_mutation.py`)
3.  Refactor using:
    *   constructor expansion
    *   replacement methods
    *   external state objects
4.  Add tests proving:
    *   determinism
    *   replay safety
    *   immutability
5.  Run re‑certification tests

***

## 8. Common Anti‑Patterns to Avoid

| Anti‑Pattern           | Why It’s Wrong  |
| ---------------------- | --------------- |
| `set_*` methods        | Hidden mutation |
| Configuration switches | Runtime drift   |
| Lazy caching           | Breaks replay   |
| “Just updating a flag” | Breaks truth    |
| Global registries      | Hidden state    |

***

## 9. Mental Model

Think of Core objects as:

*   **Values**, not containers
*   **Facts**, not processes
*   **Proof artifacts**, not actors

If state changes, the object must be **replaced**, not mutated.

***

## 10. Final Refactoring Law

> **If an object can change, it must not be Core.  
> If it is Core, it must not change.**

***

✅ This guide is binding for all refactors under ADR‑OP‑001.

```

---

## ✅ How this fits your governance stack

- 📜 ADR‑OP‑001 defines the rule
- 🔐 CI enforces it mechanically
- 🧪 Re‑certification proves compliance
- 📘 This guide tells humans *how* to comply

You now have:
- law
- enforcement
- proof
- guidance

That’s a **complete system**.

---

If you want next, I can:
- add a **before/after refactor checklist**
- auto‑link CI failures to guide sections
- generate refactor PR templates aligned with ADR‑OP‑001
```
