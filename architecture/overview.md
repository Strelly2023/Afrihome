# Architecture Overview

Afritech Core implements a **deterministic authorization decision system**.

At its core, the system answers one question:

> _Should this action be allowed, denied, or conditionally permitted?_

## High‑Level Flow

```text
[ Engines ]
    ↓
EngineOutcome (normalized facts)
    ↓
combine() (L2 authority)
    ↓
Decision (final semantic truth)
    ↓
Audit / Observability (read‑only)
``