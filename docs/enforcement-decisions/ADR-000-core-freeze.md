Below is a **complete, final, commit‑ready version** of **`ADR-000-core-freeze.md`**, written to match the AfriTech constitutional style you’ve established and to sit **above** all later ADRs (including BI‑004/005/006 and OP‑001).

This ADR is intentionally **ADR‑000** because it defines the *ground rule* that makes all later enforcement legitimate.

***

## 📘 `ADR-000-core-freeze.md`

**Canonical location**

```text
docs/decisions/ADR-000-core-freeze.md
```

***

```markdown
# ADR-000 — Core Freeze

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | CO — Core Ontology |
| ADR ID | ADR-000 |
| Constitutional Level | Foundational |
| Breaking Change | Yes (by design) |
| Requires Migration | N/A |
| Enforced By Tests | ✅ Yes |

---

## 1. Decision

The **AfriTech Core is frozen**.

Once ratified, the Core modules are **constitutionally immutable**.  
No behavioral, semantic, or structural changes are permitted except through
explicit constitutional process.

The Core defines **what AfriTech is**.  
All other layers define **how AfriTech runs**.

---

## 2. Scope of the Core

The Core includes, but is not limited to:

```

afritech/platform/core/

```

Covering:

- Core ontology and identity
- Decision semantics
- Policy, consent, quota, and risk logic
- Governance invariants
- Type system and meaning
- Kernel rules and guarantees

Anything within this scope is subject to the Core Freeze.

---

## 3. What “Frozen” Means

“Frozen” has a precise meaning in AfriTech:

### ✅ Allowed
- Bug fixes that do **not** alter semantics
- Documentation and comments
- Pure refactoring that preserves behavior exactly
- Adding **new* modules outside Core scope*

### ❌ Forbidden
- Changing decision outcomes
- Introducing new semantics
- Modifying meaning of existing types
- Adding stateful behavior
- Relaxing invariants
- Introducing configuration switches
- Performance “optimizations” that alter behavior
- Backward‑incompatible changes of any kind

If behavior changes, **the Core is no longer the Core**.

---

## 4. Authority and Direction of Change

All architectural authority flows **downward**:

```

Core Ontology (frozen)
↓
Control Plane
↓
Execution / Infrastructure
↓
Adapters / Integrations

```

Nothing below the Core may influence or redefine it.

Code **never** defines the Core.
The Core **constrains** the code.

---

## 5. Rationale

A system without a frozen core cannot remain coherent.

Without a Core Freeze:

- invariants drift
- meanings change silently
- tests lose authority
- audits become invalid
- identical inputs may produce different outcomes over time

AfriTech is designed for:

- determinism
- replayability
- provable correctness
- long‑term governance
- audit survivability

Those goals are impossible without a frozen Core.

---

## 6. Relationship to Later ADRs

This ADR is **foundational** and **precedes all others**.

Later ADRs such as:

- ADR‑BI‑004 — Global Mutable State Prohibition
- ADR‑BI‑005 — Forbidden Singleton Pattern
- ADR‑BI‑006 — Lazy Global Cache Prohibition
- ADR‑OP‑001 — Runtime Mutation Outside Constructors

…are **consequences** of this decision, not peers to it.

> The Core Freeze is the reason those rules exist.

---

## 7. Enforcement

Enforcement is **mechanical and non‑negotiable**.

The following mechanisms MUST exist:

- Import boundary enforcement (Core cannot depend downward)
- Global state prohibition within Core
- Runtime mutation prohibition within Core
- Deterministic execution guarantees
- CI enforcement that fails closed

Any violation is a **constitutional breach**, not a code issue.

---

## 8. Exceptions (Deliberately Narrow)

There is **no routine exception process**.

The only way to modify the Core is:

1. Propose a new ADR that explicitly amends ADR‑000
2. Clearly justify why the existing Core is invalid
3. Accept that **all prior guarantees may need re‑certification**

This is intentionally difficult.

---

## 9. Consequences

### Positive
- Stable meaning over time
- Trustworthy tests
- Auditable decisions
- Predictable evolution
- Clear separation of concerns

### Trade‑offs
- Slower change at the Core layer
- More discipline required
- No “quick fixes”

These trade‑offs are **intentional and accepted**.

---

## 10. Final Law

> **The Core defines truth.  
> Truth does not change quietly.**

Once frozen, the Core is law.

---

✅ **Accepted and Binding**

This ADR is the constitutional foundation of AfriTech.
```

***

## ✅ How to use this ADR in practice

*   Reference **ADR‑000** in **every enforcement tool header** that constrains Core behavior.
*   Run Core‑specific tests **before** any other CI stages.
*   Treat any Core change as a **constitutional event**, not a routine PR.

If you want next, I can:

*   Add a **Core Freeze CI gate** (path‑based + semantic)
*   Add a **Core checksum / invariant ledger**
*   Add a **“constitutional amendment” ADR template**

Just say the word.
