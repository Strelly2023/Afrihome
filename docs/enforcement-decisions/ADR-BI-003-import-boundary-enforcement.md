# ADR-BI-003 — Import Boundary Enforcement

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | BI — Boundary & Isolation |
| ADR ID | ADR-BI-003 |
| Constitutional Level | Structural |
| Breaking Change | No |
| Requires Migration | No |
| Enforced By Tests | ✅ Yes |

---

## 1. Boundary Rule

AfriTech modules MUST NOT import across architectural boundaries
in a way that violates layer isolation.

Specifically:

- Core MUST NOT import from:
  - control_plane
  - infrastructure
  - tools
- Control Plane MUST NOT import from:
  - infrastructure
- Infrastructure MUST NOT import from:
  - core
  - control_plane

---

## 2. Architectural Layers

| Layer | Root |
|------|------|
| Core | `afritech.platform.core` |
| Control Plane | `afritech.platform.control_plane` |
| Infrastructure | `afritech.platform.infrastructure` |
| Tools | `tools.*` |

---

## 3. Invariants

- [ ] No upward imports (lower → higher authority)
- [ ] No lateral leakage
- [ ] Core is pure and dependency‑free
- [ ] Boundaries are statically enforceable

---

## 4. Forbidden

- Core importing execution or audit logic
- Control plane importing persistence or IO
- Infrastructure importing decision semantics
- Runtime or conditional imports to bypass boundaries

---

## 5. Test Requirements

- Import boundary violation test
- CI‑enforced static analysis

---

## 6. Final Law

> **If two layers are isolated, they must not import each other — ever.**

---

✅ **Accepted and Binding**