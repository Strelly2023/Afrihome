# ADR-BI-004 — Global Mutable State Prohibition

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | BI — Boundary & Isolation |
| ADR ID | ADR-BI-004 |
| Constitutional Level | Structural |
| Breaking Change | No |
| Requires Migration | No |
| Enforced By Tests | ✅ Yes |

---

## 1. Boundary Rule

AfriTech code MUST NOT define or mutate **global mutable state**.

All mutable state MUST be:
- explicitly passed
- locally scoped
- owned by a clear abstraction

Global variables that hold mutable data create hidden coupling and undermine determinism.

---

## 2. Definition

**Global mutable state** is any top‑level variable that:
- is not a constant, AND
- is mutated or intended to be mutated at runtime

Examples of **forbidden global state**:
- lists, dicts, sets
- objects with mutable attributes
- counters or caches
- module‑level accumulators

---

## 3. Allowed Global Declarations (Explicit)

The following are permitted:

- Constants (UPPERCASE, immutable)
- Enums
- Dataclasses or objects marked immutable
- Module‑level functions
- Type aliases

Mutability MUST be explicit and local.

---

## 4. Invariants

- [ ] No runtime‑mutable globals
- [ ] No hidden shared state
- [ ] Determinism is preserved
- [ ] State ownership is explicit

---

## 5. Forbidden

- Mutable collections at module scope
- Lazy‑initialized globals
- Global caches
- Singleton state holders
- “Temporary” global state

No exception process exists.

---

## 6. Test Requirements

- Static analysis enforcement
- CI‑enforced failure on violation

---

## 7. Final Law

> **State is only legitimate where ownership is explicit.**  
> **Hidden global state is forbidden.**

---

✅ **Accepted and Binding**