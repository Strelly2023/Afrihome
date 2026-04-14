Below is a **complete, practical CI Failure Guide** designed to accompany your governance stack (ADR‑000, ADR‑000A, ADR‑OP‑001, checksum ledger, re‑certification tests).

This guide tells **exactly what a red CI means, why it happened, and what to do next**—without weakening any rule.

You can commit this verbatim.

***

## 📘 `docs/guides/ci-failure-guide.md`

```markdown
# CI Failure Guide — AfriTech Core Governance

This guide explains how to **interpret and respond to CI failures** in the AfriTech platform.

CI failures in this repository are **not generic test failures**.
They are **constitutional signals** that indicate a governance rule has been violated.

This document tells you:
- What failed
- Why it failed
- What actions are permitted
- What actions are forbidden

---

## 1. General Rule

> **If CI fails, the system is protecting truth.**

CI is designed to fail **early, loudly, and non‑negotiably** when:
- Core meaning drifts
- Invariants are violated
- State mutation sneaks in
- Amendments are incomplete or unauthorized

There is no “temporary ignore” or “just this once”.

---

## 2. Failure: Core Freeze Gate (ADR‑000)

### ❌ Error Signal

```

❌ Core Freeze violation detected
Changed core files:
afritech/platform/core/...
No Core Amendment ADR found

```

### ✅ Meaning

You modified files under:

```

afritech/platform/core/

```

without an explicit **ADR‑000A amendment**.

This is a constitutional violation.

---

### ✅ Allowed Actions

1. Revert the Core change  
**or**
2. Create a Core Amendment ADR:
```

docs/decisions/ADR-000A-<reason>.md

```
3. Justify why the Core was incorrect
4. Re‑certify invariants

---

### ❌ Forbidden Actions

- Bypassing CI
- Moving files to “hide” the change
- Re‑labeling as a refactor
- Editing the Core Freeze script

---

## 3. Failure: Core Checksum Ledger

### ❌ Error Signal

```

❌ Core Freeze violation (checksum mismatch)
Checksum mismatch: afritech/platform/core/identity/...

````

### ✅ Meaning

The **byte‑level contents** of the Core differ from the approved checksum ledger.

Even whitespace changes are intentional signals.

---

### ✅ Allowed Actions

- If the change is accidental → revert
- If intentional → you MUST:
  1. Add an ADR‑000A amendment
  2. Regenerate:
     ```
     docs/constitution/core_checksums.json
     ```
  3. Re‑certify the Core

---

### ❌ Forbidden Actions

- Editing the checksum file manually
- Disabling the checksum gate
- Claiming “no semantic change” without amendment

---

## 4. Failure: Core Re‑Certification Tests (ADR‑000A)

### ❌ Error Signal

````

FAILED tests/core/recertification/...

```

### ✅ Meaning

A Core amendment was proposed, but **invariants are no longer proven**.

This does NOT mean:
- “tests are wrong”
- “pytest is flaky”

It means:
> **The amendment is incomplete or incorrect.**

---

### ✅ Allowed Actions

- Fix the amendment logic
- Adjust expectations to match real Core semantics
- Remove invalid invariants (do NOT invent new ones)
- Re‑run re‑certification

---

### ❌ Forbidden Actions

- Weakening tests to “make CI green”
- Reintroducing runtime mutation
- Adding convenience abstractions to Core
- Tightening semantics without amending ADR‑000A

---

## 5. Failure: Runtime Mutation Ban (ADR‑OP‑001)

### ❌ Error Signal

```

❌ Runtime mutation violations detected
mutation of self.x outside **init**

```

### ✅ Meaning

State is being mutated after construction.

This breaks:
- determinism
- replay safety
- failure truth

---

### ✅ Allowed Actions

Refactor using:
- constructor expansion
- functional replacement (`with_*` methods)
- external state objects (outside Core)

See:
```

docs/guides/refactoring-under-ADR-OP-001.md

```

---

### ❌ Forbidden Actions

- Adding `__setattr__`
- Using property setters
- Mutating containers
- Claiming “harmless” mutation

---

## 6. Failure: Import Boundary / Global State Checks

### ❌ Error Signal

```

global mutable state detected
forbidden singleton detected

```

### ✅ Meaning

Hidden state or lifecycle‑dependent behavior exists.

This violates Core determinism.

---

### ✅ Allowed Actions

- Remove global state
- Pass dependencies explicitly
- Move mutable state outside Core

---

### ❌ Forbidden Actions

- Lazy caches
- Singletons
- Module‑level registries

---

## 7. Correct Debugging Order

When CI fails, investigate **in this order**:

1. Core Freeze gate
2. Checksum ledger
3. Re‑certification tests
4. Runtime mutation checks
5. Other platform tests

**If Core validation fails, nothing else matters.**

---

## 8. Mental Model for CI

CI is not a build system.
It is **constitutional enforcement**.

- Green ✅ means “truth holds”
- Red ❌ means “truth was violated”

There is no override.

---

## 9. Final Law

> **The Core defines truth.  
> CI enforces truth.  
> When CI fails, truth is being protected.**

---

✅ This guide is binding for all contributors.
```

***

## ✅ What this gives you

You now have:

*   📜 ADRs (law)
*   🔐 Checksum ledger (proof)
*   🧪 Re‑certification tests (evidence)
*   🚦 CI gates (enforcement)
*   📘 **A failure guide that explains exactly what happens when things go red**

This closes the loop between **governance and day‑to‑day engineering**.

***

If you want next, I can:

*   add **links from CI logs directly to guide sections**
*   add a **“CI Failure Decision Tree” diagram**
*   generate a **PR template** tied to this guide

Just say the word.
