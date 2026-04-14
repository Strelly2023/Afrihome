Below is the **complete, ratifiable ADR** for the **AfriTech Future Import Validator**, written to your constitutional standards and ready to commit.

It formally elevates the tool from “lint script” to **binding architectural law**, with class, invariants, enforcement, and CI hooks.

***

# 📘 ADR-TV-002 — AfriTech Future Import Validator

| Field                    | Value                       |
| ------------------------ | --------------------------- |
| **Status**               | ✅ Accepted                  |
| **Class**                | TV — Testing & Verification |
| **ADR ID**               | ADR-TV-002                  |
| **Constitutional Level** | Evolution                   |
| **Breaking Change**      | No                          |
| **Requires Migration**   | No                          |
| **Enforced By Tests**    | ✅ Yes                       |

***

## 1. Enforcement Rule

AfriTech source files that alter Python parsing or semantic behavior via  
`from __future__ import …` **MUST declare that change immediately and visibly**.

Specifically:

> Any `from __future__ import …` statement MUST appear:
>
> *   at the top of the file, or
> *   immediately after the module docstring (if present).

Delayed future imports are **constitutionally forbidden**.

***

## 2. Rationale

`from __future__ import …` statements alter how Python code is parsed and interpreted.
Allowing them to appear later in a file causes:

*   semantic ambiguity
*   reader misdirection
*   tool misanalysis
*   version‑dependent behavior
*   silent drift in meaning

In AfriTech, **source files are contracts**.  
Any file that opts into future semantics must do so **explicitly and immediately**.

This rule upholds:

*   **Truth over convenience** (FT)
*   **Provable semantics** (TV)
*   **Non‑ambiguous intent** (BI)

***

## 3. Invariants

The following invariants MUST hold:

*   [ ] Future imports appear before all executable code
*   [ ] Future imports are visible to readers and tools immediately
*   [ ] No future import may appear after side‑effects
*   [ ] Violations fail CI (fail‑closed)

***

## 4. Forbidden

The following are **explicitly illegal**:

*   Delayed `from __future__ import …` statements
*   Conditional or runtime‑dependent future imports
*   Hiding future imports after imports, assignments, or logic
*   Allowing semantic drift “for readability”

No exception process exists.

***

## 5. Enforcement Mechanism

Enforcement is performed by the **AfriTech Future Import Validator**:

*   **Tool:** `tools/check_future_imports.py`
*   **Scope:** All Python files excluding virtual environments
*   **Mode:** Fail‑closed
*   **Authority:** CI enforced, non‑bypassable

Any violation causes immediate CI failure.

***

## 6. Test Requirements

At minimum, the following behaviors must be enforced:

*   ✅ File with future import at top → pass
*   ✅ File with future import after docstring → pass
*   ❌ File with future import after code → fail
*   ❌ File with future import buried deep → fail

These tests are enforced indirectly via CI, not mocks.

***

## 7. CI Integration

This ADR is enforced by adding:

```yaml
- name: Enforce future import placement
  run: python tools/check_future_imports.py
```

to the AfriTech CI pipeline.

CI failure = architectural illegality.

***

## 8. Architectural Classification

This ADR is classified as:

*   **Primary Class:** TV — Testing & Verification
*   **Secondary Constraints Enforced:** FT — Failure & Truth, BI — Boundary & Isolation

***

## 9. Consequences

### Positive

*   Eliminates semantic ambiguity
*   Makes parsing behavior explicit
*   Prevents silent meaning drift
*   Improves human and tool comprehension

### Trade‑off

*   Slightly stricter formatting requirements

This trade‑off is intentional and accepted.

***

## 10. Final Law

> **If a file changes the language, it must say so immediately.**  
> **Hidden semantics are forbidden.**

***

## 📌 Canonical Location (Required)

Save this ADR at:

    docs/decisions/ADR-TV-002-future-import-validator.md

***

## ✅ Status Summary

*   ✅ Rule defined
*   ✅ Tool implemented
*   ✅ CI‑enforced
*   ✅ Constitutionally classified
*   ✅ Drift prevented

***

If you want to continue legitimately, the next aligned steps would be:

*   **ADR-BI-003 — Import Boundary Enforcement**
*   **ADR-TV-003 — Global State Prohibition**
*   **ADR-FT-002 — Parser Determinism Guarantee**

