# Afritech Core — Documentation

This directory contains the **authoritative documentation** for the Afritech Core
decision and authorization system.

The Afritech Core is a **GA‑sealed, deterministic, test‑proven semantic system**.
Its meaning is defined by executable tests, not by prose alone.

Any semantic change to the core **requires an Architecture Decision Record (ADR)**.

---

## How to Read These Docs

Afritech Core documentation follows a **strict hierarchy of authority**:

1. **Executable tests** are the ultimate source of truth  
2. **Generated documentation** is derived from tests  
3. **Hand‑written docs** explain intent, rationale, and architecture  

If tests and documentation ever disagree, **tests win**.

---

## Directory Structure

```text
docs/
├── README.md              # This file
├── architecture/          # Global design laws and invariants
├── decisions/             # Architecture Decision Records (ADR)
├── generated/             # AUTO‑GENERATED — DO NOT EDIT
└── modules/               # Per‑module responsibilities



## Pre‑Commit Setup (Required for Contributors)

AfriTech uses pre‑commit to enforce architectural invariants locally.

Install once:

```bash
pip install pre-commit
pre-commit install
``
# AfriTech Governance & Certification

This directory contains the **constitutional documentation** governing the AfriTech platform.

It defines:
- What the Core is
- How it is frozen
- How it may evolve
- How correctness is proven continuously

This is **not developer documentation**.
This is **system law**.

---

## ✅ Core Re‑Certification Status

![Core Re-Certification](https://github.com/<ORG>/<REPO>/actions/workflows/core-recertification.yml/badge.svg)

➡️ [View Core Re-Certification Workflow](https://github.com/<ORG>/<REPO>/actions/workflows/core-recertification.yml)

### What This Badge Means

When the **Core Re‑Certification** badge is green ✅, all of the following are true:

- ✅ The Core is unchanged or lawfully amended under **ADR‑000**
- ✅ The Core checksum ledger matches exactly
- ✅ All re‑certification tests pass
- ✅ Core semantics are deterministic, immutable, and replay‑safe
- ✅ Amendments are explicitly documented and auditable

When the badge is red ❌:

- The Core has drifted, or
- A Core amendment failed re‑certification, or
- An invariant was violated

There is **no partial success state**.

---

## 📘 Core Governance Documents

### Constitutional Decisions (ADRs)

Located in:

``
docs/decisions/

Key files include:

- **ADR‑000 — Core Freeze**  
  Defines the immutable boundary of the AfriTech Core.

- **ADR‑000A‑\*** — Core Amendments  
  Explicit, versioned amendments to the frozen Core.
  Each amendment requires full re‑certification.

---

## 🔐 Core Integrity Ledger

Located at:


docs/constitution/core_checksums.json

This ledger contains **cryptographic checksums** of every Core file.

CI verifies the ledger on every run.
Any mismatch fails the build unless a valid **ADR‑000A amendment** is present.

> The Core cannot drift quietly.
> History must record why it changed.

---

## 🧪 Re‑Certification Tests

Re‑certification tests live in:


tests/core/recertification/

These tests do **not** test features.
They prove **invariants**, including:

- Identity immutability
- Deterministic construction
- Semantic equality
- Replay safety
- Stability of edge cases
- Correct behavior under real Core APIs

All tests are structural, semantic, and ontology‑aware.

---

## 🚦 Enforcement Order (CI)

On every commit to `main`, the following occurs **in this order**:

1. Core Freeze enforcement (ADR‑000)
2. Core checksum verification
3. Core re‑certification tests
4. Remaining platform tests

If Core validation fails, **nothing else runs**.

---

## 🏛️ Final Principle

> **The Core defines truth.  
> Truth does not change quietly.  
> Correctness must be continuously proven.**

This repository enforces that principle mechanically.

---


✅ What to do next

Create or update:
docs/README.md


Replace <ORG> and <REPO> with your GitHub values
Commit

Once merged:

The docs folder becomes your constitutional index
The badge signals governance health
Auditors know exactly where to look

