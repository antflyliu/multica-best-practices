---
name: multica-review-backend
description: Backend implementation professional review framework that reports quality findings to the Leader.
category: methodology
owner: BackendReviewer
version: 1.0
inputs:
  - API Contract Artifact
  - Backend implementation changes
  - Acceptance Criteria
  - Previous review findings when applicable
outputs:
  - Professional review result
  - Blocking and non-blocking findings
side_effects:
  - None; review only
requires:
  - multica-artifact-api-sync
forbidden:
  - Modifying reviewed code or API artifacts
  - Declaring Leader Gate PASS
idempotent: true
platform_dependent: false
---

# Backend Implementation Professional Review (BackendReviewer)

Structured professional review framework for **backend implementation artifacts (API contract + implementation)**. Called by `BackendReviewer`; reviews the links `BackendDev` returns via `multica-artifact-api-sync` and code changes, plus the architecture design ref Leader passes.

## When to use
- BackendReviewer receives a "review backend implementation" dispatch from Leader.
- Entering a re-review round after implementation changes (check previous round's fix list item by item).

## Review dimensions (conclusion per item)
1. **Contract quality**: field naming, status codes, error model, versioning clear & self-consistent.
2. **Design fit**: implementation aligned with Architect plan, deviations explained.
3. **Error handling**: exception branches, timeouts, idempotency, boundaries covered.
4. **Unit-test sufficiency**: key paths, boundaries, exception branches covered; invalid tests are blocking.
5. **Acceptance mapping**: implementation truly satisfies every AC-.

## Output format
```
【Backend Review】<change link>
Conclusion: PASS / FAIL
Blocking items (required on FAIL, each: rationale / involved point / fix direction):
- ...
Suggestions (non-blocking):
- ...
Previous fix-list check (re-review): resolved X / unresolved Y
Round: N / 3
```
Conclusion + fix list **reported to Leader**; don't modify code or notify BackendDev yourself.

## Boundaries
- Review only backend contract & implementation, unit tests; not frontend, UI, requirements, architecture design itself, or test cases.
- Don't replace Leader's generic gate (multica-verification skill).
- Architecture-level disagreement goes to ArchReviewer; you own implementation-layer quality.
- Still FAIL at round 3 → mark "escalate to human", hand to Leader, stop looping.
