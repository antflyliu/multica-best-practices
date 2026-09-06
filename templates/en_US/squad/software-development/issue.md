# Issue Template

> Copy into a new Issue, fill it in, then hand it to the Squad.

```markdown
# Feature

## Issue source (required, pick one)
- [ ] External system link (lightweight): only fill "link / one-line summary / affected ends"; other sections omitted
      - Link: https://jira.example.com/browse/<ISSUE-KEY>
      - Summary: <!-- one line on what to do -->
- [ ] Fully self-contained (default): this Issue is the requirement; fill in all sections below

## Change Type (required)
- [ ] Feature
- [ ] Bug Fix
- [ ] Refactor
- [ ] Performance
- [ ] Security
- [ ] Documentation
- [ ] Infrastructure
- [ ] Other: <!-- explain -->

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

## References
<!-- Docs, Issues, screenshots, code locations -->

## Notes
<!-- Anything else the squad needs to know -->
```

---

## Why it's written this way

- **Change Type comes before routing**: Feature, Bug Fix, Refactor, Performance, Security, etc. have different risk and verification needs; declare the type first so the Squad can select the right flow.
- **Affected ends in Scope are routing input**: the Leader's G0 uses them to decide which roles to dispatch. Missing or vague scope → G0 FAIL, instead of guessing.
- **Goal / Scope / Non-goals separated**: prevents agents from freewheeling and expanding scope.
- **Acceptance criteria must be testable**: without testable AC, `multica-verification` has nothing objective to check and the gate system breaks.
- **An Issue is a requirement contract, not an implementation blueprint**: technical context, constraints, traceability, verification, and Git branch are produced by the Squad during execution, not front-loaded onto the requester.

## Common failure modes

- **No Change Type**: every task gets treated as a Feature, causing routing and verification strength to drift.
- **Only writing "please build this feature"**: the squad either guesses or gets stuck at G0.
- **Not checking affected ends**: the Leader cannot tell whether to dispatch Frontend / Backend, so the flow may default to full-stack.
- **Writing requirement details into Agent Instructions instead of the Issue**: those instructions become wrong as soon as the task changes.
