# Issue Template

> Copy into a new Issue, fill it in, then hand it to the Squad.

```markdown
# Feature

## Background
<!-- Why are we doing this? -->

## Goal
<!-- What problem should this feature solve? -->

## Scope
<!-- The Leader routes by this: ends not checked get no role; their artifacts are skipped -->
- Affected ends (check):
  - [ ] Design (needs Architect to propose a plan)
  - [ ] Frontend (needs FrontendDev)
  - [ ] Backend (needs BackendDev + API contract)
- What to change: <!-- What should change? -->

## Non-goals
<!-- What explicitly won't be done? -->

## Acceptance criteria (must be testable)
- [ ]
- [ ]
- [ ]

## Requirements traceability matrix (recommended, prevents broken links)
<!-- Map REQ → DESIGN → API → CODE → CASE → TEST so every acceptance criterion traces to an artifact and a test -->
| Acceptance criterion (AC) | Design (DESIGN-ID) | API (API-ID) | Code | Case (CASE-ID) | Test result |
| --- | --- | --- | --- | --- | --- |
| AC-1 | | | | | |

## Technical context
<!-- Existing architecture, modules, APIs, constraints, etc. -->

## Constraints
<!-- Compatibility, performance, security, deadlines, etc. -->

## Verification method
- [ ] Build
- [ ] Unit tests
- [ ] CI/CD deploy to test env (check if scope includes CI/CD; G2.5)
- [ ] Automated test (after G2.5, T3)
- [ ] Manual verification (if applicable)

## Git Branch
<!-- Declared by Leader at G0; all implementations merge to this deploy branch, @DevOps triggers CI/CD on it only. Feature branches are not used for CI/CD -->
- Deploy branch: `release/<ISSUE-KEY>-<slug>`
- Feature branch (optional): `<ISSUE-KEY>-<desc>`

## References
<!-- Docs, Issues, screenshots, code locations -->

## Notes
<!-- Anything else the squad needs to know -->
```

---

## Why it's written this way

- **The "affected ends" in the scope is the routing input**: the Leader's G0 uses it to decide which roles to dispatch. Missing or vague scope → G0 FAIL, instead of the Leader guessing.
- **Goal / Scope / Non-goals separated**: prevents agents from freewheeling and expanding the scope.
- **Acceptance criteria must be testable**: without testable criteria, gatekeeping can't execute (the multica-verification skill has nothing to map against), and the whole gate system breaks.

## Common failure

- Only writing "please build this feature for me" → the squad either guesses or gets stuck at G0.
- Not checking "affected ends" → the Leader doesn't know whether to dispatch Frontend / Backend, and the flow runs as full-stack by default.
- Writing requirement details into Agent Instructions instead of the Issue → those instructions are dead the moment the task changes.
