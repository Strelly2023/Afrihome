# ADR-TV-003 — Source HTML Entity Normalization

| Field | Value |
|------|------|
| Status | ✅ Accepted |
| Class | TV — Testing & Verification |
| ADR ID | ADR-TV-003 |
| Constitutional Level | Evolution |
| Breaking Change | No |
| Requires Migration | No |
| Enforced By Tests | ✅ Yes |

---

## 1. Enforcement Rule

AfriTech source code MUST NOT contain HTML-escaped entities
that alter the **semantic readability or correctness** of code.

Specifically, the following entities are forbidden in Python source
when used to represent code tokens:

- `-&amp;gt;` instead of `->`
- `&amp;lt;` instead of `<`
- `&amp;gt;` instead of `>`
- `&amp;quot;` instead of `"`
- `&amp;#39;` instead of `'`

Such entities are considered **semantic corruption**, not formatting.

---

## 2. Rationale

HTML entity escapes may be introduced by:
- copy/paste from rendered documentation
- automated converters
- markdown pipelines
- code review tools

When they appear in source code, they:
- obscure meaning
- mislead reviewers
- degrade tool analysis
- risk silent behavioral divergence

AfriTech treats **source files as semantic contracts**.
Any corruption of code tokens is constitutionally illegal.

---

## 3. Scope of Enforcement

This ADR applies to:

- Python source files (`.py`)
- Under AfriTech authority boundaries only
- Excluding:
  - virtual environments
  - third‑party code
  - generated artifacts (unless explicitly ratified)

The tool MUST skip:
- HTML or template files
- Lines that clearly represent HTML markup
- Any directory outside AfriTech’s ownership

---

## 4. Normalization Rules

The following transformations are **permitted and intentional**:

| Encoded | Normalized |
|------|-----------|
| `-&amp;gt;` | `->` |
| `&amp;lt;` | `<` |
| `&amp;gt;` | `>` |
| `&amp;quot;` | `"` |
| `&amp;#39;` | `'` |

Normalization MUST be:
- deterministic
- idempotent
- context‑aware (code‑only)

---

## 5. Invariants

The following invariants MUST hold:

- [ ] Semantic meaning is preserved
- [ ] No HTML markup is modified
- [ ] Fix is idempotent
- [ ] Only code‑context replacements occur
- [ ] No runtime behavior is introduced
- [ ] No dependency on execution state

Violations of these invariants invalidate the tool.

---

## 6. Forbidden

The following are explicitly illegal:

- Blind global replace
- Runtime mutation of code
- HTML document rewriting
- CI‑time auto‑modification of source
- Silent normalization without visibility
- Fixing code outside AfriTech ownership

This tool is **never** allowed to modify code during production execution.

---

## 7. Enforcement Mechanism

Enforcement is provided by the tool:

```text
tools/fix_html_entities.py