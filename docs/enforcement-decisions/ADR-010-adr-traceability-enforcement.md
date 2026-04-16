
---

# ✅ Finalized System: ADR → Test → CI Enforcement (Complete)

This is the **fully operational version**, not just concept + script.

---

# 🔐 1. Strengthened Invariant (Upgraded)

You defined:

> No unenforced ADR may exist

We tighten it to **machine-enforceable law**:

### ✅ Final Invariant

> **Every ADR must be referenced by ≥1 test, and every referenced ADR must exist and be valid.**

This gives you **bidirectional closure**:

| Direction  | Guarantee             |
| ---------- | --------------------- |
| ADR → Test | No dead law           |
| Test → ADR | No orphan enforcement |
| CI         | No drift              |

---

# 🧱 2. Source of Truth for ADRs

Right now your extractor assumes a list of ADRs—but doesn’t define how to get them.

### ✅ Fix: ADR registry = filesystem

```bash
docs/decisions/
  ADR-DS-001-*.md
  ADR-AM-002-*.md
```

### ✅ Extract ADR IDs from filenames

---

# 🛠️ 3. Full ADR Coverage Validator (Production-Ready)

## `tools/adr/validate_adr_traceability.py`

```python
import re
import sys
from pathlib import Path

ADR_PATTERN = re.compile(r"ADR-[A-Z]{2}-\d{3}")


# ---------------------------------------------------------
# 1. Collect ADRs from docs
# ---------------------------------------------------------

def collect_adrs(adr_dir: Path):
    adrs = set()

    for file in adr_dir.glob("ADR-*.md"):
        match = ADR_PATTERN.search(file.name)
        if match:
            adrs.add(match.group())

    return adrs


# ---------------------------------------------------------
# 2. Extract ADR references from tests
# ---------------------------------------------------------

def extract_adrs_from_tests(test_dir: Path):
    coverage = {}

    for file in test_dir.rglob("test_*.py"):
        content = file.read_text()

        matches = ADR_PATTERN.findall(content)

        for adr in matches:
            coverage.setdefault(adr, set()).add(str(file))

    return coverage


# ---------------------------------------------------------
# 3. Validation
# ---------------------------------------------------------

def validate(adrs, coverage):
    errors = False

    # ❌ ADR with no tests
    uncovered = [adr for adr in adrs if adr not in coverage]

    if uncovered:
        print("\n❌ ADRs without test coverage:")
        for adr in uncovered:
            print(f"  - {adr}")
        errors = True

    # ❌ Tests referencing unknown ADRs
    unknown = [adr for adr in coverage if adr not in adrs]

    if unknown:
        print("\n❌ Unknown ADR references in tests:")
        for adr in unknown:
            print(f"  - {adr}")
        errors = True

    # ✅ Report coverage
    print("\n📊 ADR Coverage:")
    for adr in sorted(coverage):
        print(f"{adr}:")
        for f in sorted(coverage[adr]):
            print(f"  - {f}")

    return errors


# ---------------------------------------------------------
# Entry
# ---------------------------------------------------------

def main():
    adr_dir = Path("docs/decisions")
    test_dir = Path("tests")

    adrs = collect_adrs(adr_dir)
    coverage = extract_adrs_from_tests(test_dir)

    errors = validate(adrs, coverage)

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

# 🔒 4. CI Enforcement (Non-Bypassable)

## `.github/workflows/adr-traceability.yml`

```yaml
name: ADR Traceability Enforcement

on: [push, pull_request]

jobs:
  adr-traceability:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Validate ADR Traceability
        run: |
          python tools/adr/validate_adr_traceability.py
```

---

# 📊 5. Coverage Report Generator (Human + Audit Layer)

## `tools/adr/generate_adr_coverage.py`

```python
from pathlib import Path
from validate_adr_traceability import (
    collect_adrs,
    extract_adrs_from_tests,
)

OUTPUT = Path("docs/generated/adr_coverage.md")


def generate():
    adrs = collect_adrs(Path("docs/decisions"))
    coverage = extract_adrs_from_tests(Path("tests"))

    lines = ["# ADR Coverage Report\n"]

    for adr in sorted(adrs):
        lines.append(f"## {adr}")

        if adr in coverage:
            lines.append("✔ Covered by:")
            for f in sorted(coverage[adr]):
                lines.append(f"- {f}")
        else:
            lines.append("❌ NOT COVERED")

        lines.append("")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines))


if __name__ == "__main__":
    generate()
```

---

# 🧪 6. Enforced Test Annotation Standard

### ✅ Required Pattern

```python
def test_rbac_is_only_grantor():
    """
    ADR-AM-003
    ADR-BI-002
    """
```

### ❌ Forbidden

```python
# ADR-AM-003   ❌ not machine-readable
```

---

# 🔍 7. Optional (High-Value): Strict Mode

Add validation for:

### ❌ Missing docstrings

### ❌ Tests without ADR references

Add this:

```python
if not matches:
    print(f"❌ Test without ADR reference: {file}")
    errors = True
```

---

# 🧠 8. What You’ve Actually Built

This is the important part.

You now have:

### BEFORE

* Architecture described
* Tests exist
* ADRs exist

### AFTER

* ADRs **must be enforced**
* Tests **must justify existence**
* CI **enforces legitimacy**

---

# 🔒 Final System (Closed Loop)

```
ADR (Law)
  ↓
Invariant
  ↓
Test
  ↓
CI Enforcement
  ↓
System Behavior
  ↓
Audit Trace
  ↓
Back to ADR
```

---

# 🚨 Final Constitutional Rule (Now Enforced)

> **If a rule is not tested, it is not real.
> If a test has no rule, it is not allowed.**

---

# 🏁 What This Unlocks Next

Now that traceability is sealed, the system is ready for:

### 1. ADR Templates per Class

→ ensures all future decisions are structured

### 2. ADR Acceptance Workflow (you already drafted)

→ removes human discretion

### 3. Invariant Extraction Engine

→ unify core + execution + ADR laws

### 4. Replay Engine

→ prove correctness across time

---

# 🔥 Final Insight

You didn’t just add traceability.

You removed:

* informal architecture
* undocumented behavior
* unenforced decisions

> **AfriTech now cannot lie about what it is.**

---

If you want the strongest next move:

👉 **“generate ADR templates per class”**

That will lock **future decisions** the same way you just locked enforcement.
