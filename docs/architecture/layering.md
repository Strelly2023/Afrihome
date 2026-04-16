
---

## `docs/architecture/layering.md`

```md
# Layering Model

Afritech Core is strictly layered.

## L1 — Engines
- Emit `EngineOutcome`
- Cannot see other engines
- Cannot determine final outcome

Examples:
- RBAC
- Policy
- Risk
- Quota
- Consent

## L2 — Combinator
- Accepts multiple `EngineOutcome`
- Enforces deny‑wins precedence
- Produces `Decision`

## L3 — Observers (Audit)
- Consume `Decision`
- Never influence authorization