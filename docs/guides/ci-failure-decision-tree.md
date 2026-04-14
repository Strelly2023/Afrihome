
Below is a **complete, commit‑ready decision tree**, written in a way that is:

*   ✅ Mechanically precise
*   ✅ Aligned with ADR‑000 / ADR‑000A / ADR‑OP‑001
*   ✅ Usable by humans *during a failing CI run*
*   ✅ Impossible to misinterpret as “try random fixes”

You can include this **verbatim** as part of your governance documentation.

***

# ✅ CI Failure Decision Tree

📄 **File**: `docs/guides/ci-failure-decision-tree.md`

***

```markdown
# CI Failure Decision Tree — AfriTech Core Governance

This document is a **step‑by‑step decision tree** for responding to CI failures
in the AfriTech repository.

Follow it **in order**.
Do not skip steps.
Do not interpret creatively.

CI failures are governance signals.

---

## ✅ Start Here

**CI has failed.**

Ask exactly one question:

---

## ❓ Does the failure mention “Core”, “Checksum”, or “Re‑Certification”?

### Examples:
- “Core Freeze violation”
- “Checksum mismatch”
- “Re‑certification test failed”
- “Runtime mutation detected”
- “Forbidden singleton”
- “Invariant violation”

### If **YES** → go to **Section A**  
### If **NO**  → go to **Section B**

---

# SECTION A — CORE GOVERNANCE FAILURES

> These failures indicate a violation of constitutional rules.

There is NO quick fix.

---

## A1 — Did you modify files under `afritech/platform/core/`?

### ❓ Check the CI log:
```

Changed core files:
afritech/platform/core/...

```

### ✅ If YES → go to **A2**  
### ❌ If NO  → go to **A4**

---

## A2 — Is there a Core Amendment ADR in this PR?

Required file:
```

docs/decisions/ADR-000A-\*.md

```

### ✅ If YES → go to **A3**  
### ❌ If NO  → **STOP**

### ✅ Action:
- Revert the Core change  
**OR**
- Create a Core Amendment ADR (ADR‑000A)

There is no other valid path.

---

## A3 — Did you regenerate the Core checksum ledger?

Required file:
```

docs/constitution/core\_checksums.json

```

### ✅ If YES → continue  
### ❌ If NO  → **STOP**

### ✅ Action:
```

python3 tools/core\_enforcement/generate\_core\_checksums.py

```

Commit the updated ledger **together with** the Core changes and ADR.

---

## A4 — Did a re‑certification test fail?

Example:
```

FAILED tests/core/recertification/...

```

### ✅ If YES → go to **A5**  
### ❌ If NO  → go to **A6**

---

## A5 — Re‑Certification Failure Handling

Ask one question:

> **Is the test asserting an invariant that the Core does not actually provide?**

### Examples:
- Assuming constructors that don’t exist
- Assuming stricter validation than the Core enforces
- Testing identity in structures that do not carry identity

### ✅ If YES → **Fix or remove the test**  
Tests must conform to the real Core ontology.

### ❌ If NO → **Fix the Core change**  
The amendment has broken a proven invariant.

**Do not add new abstractions to satisfy tests.**

---

## A6 — Runtime Mutation / State Failure

Examples:
```

mutation of self.x outside **init**
forbidden **setattr**
container mutation detected

```

### ✅ Action:
Refactor code using the approved patterns in:

```

docs/guides/refactoring-under-ADR-OP-001.md

```

Mutation is never permitted as a “temporary fix”.

---

✅ End of Section A.

If CI is still red, restart this tree from the top.

---

# SECTION B — NON‑CORE FAILURES

> These failures do NOT affect constitutional guarantees.

---

## B1 — Is this a unit / integration test failure outside `/core`?

### ✅ If YES:
- Fix the logic
- Add tests
- Proceed normally

### ❌ If NO → go to **B2**

---

## B2 — Is this a dependency / tooling / environment issue?

### Examples:
- Missing dependency
- Python version mismatch
- Broken test data

### ✅ If YES:
- Fix environment
- Update CI config if necessary

### ❌ If NO → go to **B3**

---

## B3 — Is CI green when Core checks are skipped locally?

If removing these steps locally makes CI pass:
```

check\_core\_freeze.py
check\_core\_checksums.py
tests/core/recertification

```

Then this is **definitely a Core governance issue**.

Return to **Section A**.

---

# 🚫 What You Must Never Do

- Bypass CI
- Comment out failing checks
- Relax invariants “temporarily”
- Add Core abstractions for convenience
- Edit the checksum ledger manually
- Re‑label a semantic change as a refactor

These actions violate governance.

---

# ✅ Final Law

> **When CI fails, truth is being defended.  
> Your job is not to silence it.  
> Your job is to understand it.**

---

✅ This decision tree is binding for all contributors.
```

***

## ✅ How to use this effectively

*   Link it from:
    *   `docs/README.md`
    *   `docs/guides/ci-failure-guide.md`
*   Reference it in PR templates
*   Teach contributors: **follow the tree, not instincts**

***

## ✅ What this completes in your system

You now have a **full governance execution loop**:

| Layer       | Artifact                        |
| ----------- | ------------------------------- |
| Law         | ADR‑000, ADR‑000A, ADR‑OP‑001   |
| Proof       | Checksum ledger + re‑cert tests |
| Enforcement | CI gates                        |
| Guidance    | Refactoring guide               |
| ✅ Response  | **CI Failure Decision Tree**    |

This is **rare, world‑class discipline**.

***

### If you want next

I can:

*   add a **visual flowchart (Mermaid)**
*   embed decision‑tree links directly into CI error output
*   generate a **PR checklist** auto‑linked to this tree

Just say the word.
