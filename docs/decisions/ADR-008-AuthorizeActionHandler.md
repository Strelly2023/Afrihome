

# ADR‑008 — AuthorizeActionHandler (Execution‑Layer Authorization Gate)

| Field               | Value                                                                           |
| ------------------- | ------------------------------------------------------------------------------- |
| **Status**          | ✅ Accepted (Constitutionally Bound)                                             |
| **Date**            | 2026-04-13                                                                      |
| **Decision Driver** | Enforce execution-time authorization without violating decision core invariants |
| **Related ADRs**    | ADR-001, ADR-004, ADR-006, Authority Model, Generational Invariants             |



***

## 1. Context

The AfriTech platform defines a **pure Decision Core** whose sole responsibility is to compute semantic authorization outcomes (`ALLOW`, `DENY`, `CONDITIONAL`) based on engine inputs (RBAC, Policy, Consent, Risk, etc.).

Through extensive testing and invariant enforcement, the following principles are now sealed:

*   The decision core is **deterministic, immutable, and authority‑agnostic**
*   The decision core **does not interpret meaning**, only aggregates outcomes
*   The decision core **does not enforce execution policy**
*   Authority isolation, explainability, and conditional blocking are **not core invariants**

As a result, there is a deliberate architectural gap between:

*   **Decision computation** (what the system thinks)
*   **Action execution** (what the system allows to happen)

This gap must be closed **without violating core purity**.

***

## 2. Problem Statement

We need a mechanism that:

1.  Consumes a computed `Decision` and its contributing `EngineOutcome`s
2.  Determines whether an action may actually execute
3.  Enforces execution‑time rules such as:
    *   Fail‑closed behavior
    *   Authority isolation (RBAC is the only grantor)
    *   Conditional blocking
    *   Explainability requirements
4.  Does **not** modify or reinterpret the decision core
5.  Remains testable, auditable, and composable

Embedding these rules directly into the decision core would violate established layering invariants and reintroduce domain coupling.

***

## 3. Decision

We introduce an **execution‑layer component** named:

> **`AuthorizeActionHandler`**

### Definition

`AuthorizeActionHandler` is a **pure execution gate** that authorizes or rejects the execution of an action *based on* a precomputed `Decision`, its contributing `EngineOutcome`s, and an execution context.

It **does not compute decisions**.  
It **does not mutate decisions**.  
It **enforces execution‑time rules only**.

***

## 4. Responsibilities

`AuthorizeActionHandler` is responsible for enforcing **execution‑time authorization laws** that intentionally do **not** exist in the decision core.

### 4.1 Enforced Laws

#### Law 1 — Fail‑Closed Execution

*   Only `DecisionVerdictType.ALLOW` may pass
*   `DENY` and `CONDITIONAL` block execution

#### Law 2 — Authority Isolation

*   RBAC is the **only** engine that may grant execution authority
*   Policy, Consent, Risk, and others may influence the decision
*   They may **never** independently grant execution

#### Law 3 — Conditional Blocking

*   `CONDITIONAL` is an explicit execution‑blocking state
*   Conditional decisions require resolution elsewhere before execution

#### Law 4 — Explainability Enforcement

*   Executed actions must be explainable
*   Silent decisions (`reasons == ()`) are rejected at execution time
*   The core may be silent; execution may not

***

## 5. Non‑Responsibilities

`AuthorizeActionHandler` explicitly **does not**:

*   Compute or aggregate decisions
*   Reorder or reinterpret engine outcomes
*   Modify the `Decision` object
*   Invent reasons or explanations
*   Encode domain‑specific policy semantics
*   Persist audit logs (delegated to downstream components)

***

## 6. Design Rationale

### 6.1 Why Not in the Decision Core?

The decision core is constitutionally sealed to be:

*   Authority‑agnostic
*   Domain‑agnostic
*   Pure and deterministic

Embedding execution semantics there would:

*   Break composability
*   Introduce implicit meaning
*   Violate established ADRs and invariants

### 6.2 Why a Dedicated Handler?

A dedicated handler:

*   Preserves clean layering
*   Allows different execution policies per interface (API, batch, UI)
*   Simplifies auditing and troubleshooting
*   Enables enforcement evolution without touching core semantics

***

## 7. Interface Contract (Conceptual)

```text
Inputs:
- Decision
- Tuple[EngineOutcome]
- ExecutionContext (actor, action, resource, environment)

Outputs:
- AuthorizedAction  (success)
- AuthorizationException (failure)
```

Execution always returns **either**:

*   A valid, authorized action
*   A typed, explicit exception

No booleans. No partial success.

***

## 8. Error Model

The handler uses **typed execution errors**, never silent failures.

Examples:

*   `AuthorizationDenied`
*   `AuthorizationConditional`
*   `AuthorityNotGranted`
*   `UnexplainableDecision`

This makes failures:

*   Machine‑actionable
*   Auditable
*   API‑safe
*   Log‑friendly

***

## 9. Consequences

### Positive

*   Clean separation of concerns
*   No regression risk to the decision core
*   Strong security posture (fail‑closed)
*   Clear audit and compliance boundaries
*   Flexible execution policies

### Trade‑offs

*   Slight increase in components
*   Requires explicit orchestration
*   Requires discipline to keep execution rules out of core

These trade‑offs are intentional and accepted.

***

## 10. Final Architectural Rule

> **The decision core decides what the system believes.  
> The AuthorizeActionHandler decides what the system allows to happen.**

This division is **intentional, enforced, and permanent**.

***

## 11. Status

✅ **Accepted**  
This ADR is binding for all future authorization execution paths.

***

### Next Steps (Explicitly Out of Scope for This ADR)

*   AuthorizeActionHandler test suite
*   Execution‑layer audit logging
*   API integration
*   Conditional resolution workflows

These will be covered in subsequent ADRs or implementation documents.

***

If you say **“next”**, the logical continuation is:

*   **AuthorizeActionHandler test design (execution‑layer invariants)**
