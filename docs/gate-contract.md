# Gate Contract

> Single Source of Truth for G0 → G1 → G2 → G2.5 → G3 → G4.

## Gate responsibilities

| Gate | Purpose | Required evidence | Decision owner |
|---|---|---|---|
| G0 | Issue / scope ready | Issue, scope, AC, non-goals | Leader |
| G1 | Design ready | PRD/design, review evidence, T1 test design | Leader |
| G2 | Implementation ready | implementation diff, T2 coverage/gap analysis, review/CI evidence | Leader |
| G2.5 | Deployment / CI ready | CI/CD result tied to current Artifact Version | CI + Leader |
| G3 | Runtime quality ready | T3 result + regression evidence | Leader |
| G4 | Final acceptance | business/product acceptance | Human |

## T1 / T2 / T3

- **T1**: test design before G1.
- **T2**: post-implementation coverage and test-gap analysis before G2.
- **T3**: runtime automation **only after G2.5 PASS**.

## Gate execution rule

All Agent-side Gate decisions are executed by **Leader** through `multica-verification`. Producer roles and Reviewer roles do not self-approve their own Gate.

Reviewer answers: "Is this professionally correct?"

Gate answers: "Is this deliverable eligible to move forward?"

CI answers: "Can a machine prove this check passed?"

Human acceptance answers: "Does the business accept the result?"

## Artifact versioning

Every Gate PASS must bind to:

- Issue
- Artifact type
- Artifact version
- Upstream Gate versions/results
- Acceptance Criteria
- Evidence

If any Artifact is modified, all downstream Gates immediately become invalid. The workflow must restart verification from the earliest affected Gate.

## T3 hard ordering

```text
G2 PASS
  ↓
G2.5 CI/CD
  ↓
G2.5 PASS
  ↓
T3 runtime automation
  ↓
G3 Leader verification
  ↓
G4 Human acceptance
```

T3 must never be triggered from G2 alone.

## Status values

- `PASS`: all required checks satisfied.
- `FAIL`: a required criterion is not satisfied.
- `BLOCKED`: objective verification cannot run because required input, environment, evidence, or upstream Gate is missing.

`BLOCKED` is not `PASS` and must be re-verified after the blocking condition is resolved.
