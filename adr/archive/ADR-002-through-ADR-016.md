# ADR-002 → ADR-016: Semantic Consolidation

This document consolidates multiple architectural decisions that were
validated through implementation and test enforcement.

## Recorded Decisions

- EngineOutcome normalizes all facts
- Raw strings are forbidden in decision logic
- Enums define semantic truth
- Deny always wins
- Audit is observational
- No ABSTAIN verdict
- DecisionReason identity is code‑based
- Combinator is the sole precedence authority

These decisions are final and enforced by tests.