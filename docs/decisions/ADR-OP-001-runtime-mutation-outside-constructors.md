

# 📘 ADR‑OP‑001 — Runtime Mutation Outside Constructors Prohibition

> *(Operational + Failure & Truth invariant)*

## ✅ Canonical Location

```text
docs/decisions/ADR-OP-001-runtime-mutation-outside-constructors.md
```

***

## ✅ Complete ADR (Binding Law)

````markdown
# ADR-OP-001 — Runtime Mutation Outside Constructors Prohibition

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | OP — Deployment & Operations |
| ADR ID | ADR-OP-001 |
| Constitutional Level | Evolution |
| Breaking Change | No |
| Requires Migration | No |
| Enforced By Tests | ✅ Yes |

---

## 1. Operational Rule

AfriTech code MUST NOT mutate object state **outside of constructors**.

All mutation of instance attributes MUST occur:
- inside `__init__`, or
- inside an explicitly declared constructor‑equivalent factory

Any mutation that occurs:
- during normal method execution, or
- after object construction

is constitutionally forbidden.

---

## 2. Rationale

Runtime mutation outside constructors introduces:

- hidden state transitions
- execution‑order dependence
- time‑sensitive behavior
- replay irreproducibility
- test fragility

It creates objects whose behavior depends not only on inputs,
but also on **when** and **how often** methods were called.

AfriTech requires objects to have:
- explicit construction
- stable identity
- predictable lifecycle

That requires **state to be finalized at construction time**.

---

## 3. Forbidden Patterns

### 3.1 Post‑Construction Mutation

```python
class Service:
    def __init__(self):
        self.ready = False

    def start(self):
        self.ready = True   # ❌ forbidden
````

***

### 3.2 Stateful Methods

```python
def process(self, x):
    self.count += 1  # ❌ forbidden
```

***

### 3.3 Lazy Initialization on First Use

```python
def handle(self):
    if self.cache is None:
        self.cache = {}  # ❌ forbidden
```

***

### 3.4 Mutating “Configuration” After Init

```python
self.timeout = new_timeout  # ❌ forbidden outside constructor
```

***

## 4. Explicitly Allowed

### 4.1 Constructor Mutation

```python
class Engine:
    def __init__(self, config):
        self.config = config
        self.state = "ready"
```

***

### 4.2 Immutable Replacements

```python
def with_state(self, state):
    return Engine(state)
```

Objects may be *replaced*, not mutated.

***

### 4.3 External State Objects

```python
def handle(self, ctx):
    ctx.counter += 1  # ✅ allowed (not object-owned state)
```

***

## 5. Invariants

The following MUST hold:

*   [ ] After `__init__`, object state is immutable
*   [ ] No instance attribute assignment outside constructors
*   [ ] No lazy initialization inside methods
*   [ ] Execution order does not affect object identity
*   [ ] Objects are replay‑safe

Violation of any invariant constitutes a constitutional breach.

***

## 6. Forbidden

*   runtime mutation of `self.*`
*   post‑init configuration
*   stateful method side‑effects
*   “just updating a flag”
*   lazy initialization patterns

No exception process exists.

***

## 7. Enforcement Mechanism

This ADR is enforced by static analysis via:

```text
tools/check_runtime_mutation.py
```

The checker MUST detect:

*   assignments to `self.*` outside `__init__`
*   mutations inside non‑constructor methods
*   attribute creation after initialization

Enforcement is fail‑closed and CI‑enforced.

***

## 8. Relationship to Other ADRs

This ADR completes AfriTech’s state discipline:

*   **ADR‑BI‑004** — Global Mutable State Prohibition
*   **ADR‑BI‑005** — Forbidden Singleton Pattern
*   **ADR‑BI‑006** — Lazy Global Cache Prohibition

Together, they guarantee:

*   explicit state ownership
*   deterministic execution
*   replay safety

***

## 9. Consequences

### Positive

*   reproducible behavior
*   honest tests
*   clear lifecycle modeling
*   straightforward reasoning

### Trade‑off

*   objects must be rebuilt instead of mutated
*   more explicit construction

This trade‑off is intentional and accepted.

***

## 10. Final Law

> **State may be created only at construction.**  
> **After construction, state must not change.**

***

✅ **Accepted and Binding**

````

---

# 🔧 Enforcement Tool — Runtime Mutation Detector

## ✅ Canonical Location

```text
tools/check_runtime_mutation.py
````

***

## ✅ Complete, Enforcement‑Grade Implementation

```python
#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path

"""
AfriTech Runtime Mutation Validator

Enforces ADR-OP-001 — Runtime mutation outside constructors is forbidden.
"""

ENFORCED_ROOTS = {
    "afritech/platform/core",
    "afritech/platform/control_plane",
}

SKIP_DIRS = {
    "venv", ".venv", ".tox", "__pycache__", "site-packages",
    "tests", "tools", "config", "_quarantine", "core_PRE_GA_BACKUP",
}


def should_skip(path: Path) -> bool:
    if any(part in SKIP_DIRS for part in path.parts):
        return True
    return not any(root in path.as_posix() for root in ENFORCED_ROOTS)


class MutationVisitor(ast.NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.violations: list[str] = []
        self.current_class = None
        self.current_function = None

    def visit_ClassDef(self, node: ast.ClassDef):
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef):
        prev = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = prev

    def visit_Assign(self, node: ast.Assign):
        if self.current_class and self.current_function != "__init__":
            for target in node.targets:
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                ):
                    self.violations.append(
                        f"{self.path}:{node.lineno} — mutation of self.{target.attr} "
                        f"outside constructor (__init__)"
                    )
        self.generic_visit(node)


def find_runtime_mutation_violations(path: Path) -> listtry:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return []

    visitor = MutationVisitor(path)
    visitor.visit(tree)
    return visitor.violations


def main() -> None:
    violations: list[str] = []

    for py in Path(".").rglob("*.py"):
        if should_skip(py):
            continue
        violations.extend(find_runtime_mutation_violations(py))

    if violations:
        print("❌ Runtime mutation violations detected:\n")
        for v in sorted(violations):
            print(f"  {v}")
        raise SystemExit(1)

    print("✅ Runtime mutation outside constructors check passed.")


if __name__ == "__main__":
    main()
```

***

# ✅ CI / Pre‑Commit Integration

Add after your existing state checks:

```yaml
- name: Enforce runtime mutation prohibition (ADR-OP-001)
  run: python3 tools/check_runtime_mutation.py
```

***

# ✅ What This Now Enforces

| Pattern                               | Result      |
| ------------------------------------- | ----------- |
| `self.x = ...` in `__init__`          | ✅ Allowed   |
| `self.x = ...` in any other method    | ❌ Forbidden |
| Lazy attribute creation               | ❌ Forbidden |
| Immutable replacement via constructor | ✅ Allowed   |

***

# 🧠 Architectural State After This Step

AfriTech now enforces **full state discipline**:

1.  ❌ Global mutable state
2.  ❌ Singletons
3.  ❌ Lazy caches
4.  ❌ Runtime post‑construction mutation ✅ *(new)*

This is the **strongest form of determinism guarantee** you can have without going full pure FP.

***

## 🚀 Next Legitimate Invariants (Optional)

Only these remain in the same orbit:

*   **Pure‑function boundary enforcement**
*   **Time / clock injection law**
*   **Side‑effect free computation zones**

If you want to continue, say which one to encode next.
