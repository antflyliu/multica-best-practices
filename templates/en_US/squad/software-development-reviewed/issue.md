# Issue Template

> Copy to a new Issue, fill it, and hand it to the Squad.

```markdown
# Feature

## Issue Source (required, pick one)
<!-- Decides how deep this Issue is filled. For "external link", fill only the link + summary + involved ends; other sections jump to Notes referencing the KEY. Full requirements live in Jira/Tapd etc.; Squad pulls by KEY -->
- [ ] External system link (lightweight): only "link / one-line summary / involved ends", other sections omitted
      - Link: https://jira.example.com/browse/<ISSUE-KEY>
      - Summary: <!-- one line on what to do -->
- [ ] Fully self-contained (default): this Issue is the requirement; fill all sections below

## Background
<!-- Why do this? -->

## Goal
<!-- What problem does this solve? -->

## Scope
<!-- Leader routes by this; missing ends aren't dispatched, their artifacts skipped -->
- Involved ends (check):
  - [ ] Design (needs Architect)
  - [ ] Frontend (needs FrontendDev)
  - [ ] Backend (needs BackendDev + API contract)
  - [ ] CI/CD deployment (needs DevOps)
- Changes: <!-- what should change? -->

## Non-goals
<!-- Explicitly what NOT to do -->

## Acceptance Criteria (must be testable)
- [ ] AC-1:
- [ ] AC-2:
- [ ] AC-3:

## References
<!-- docs, issues, screenshots, code locations -->

## Notes
<!-- other context the Squad needs -->
```

---

## Why it's written this way

- **"Involved ends" in Scope is the routing input**: Leader's G0 uses it to decide which roles to dispatch. Missing or vague scope → G0 FAIL, not a guess.
- **Goal / Scope / Non-goals separated**: prevents Agents from freely expanding scope.
- **Acceptance Criteria must be testable and use AC- numbering**: dedicated Reviewers and multica-verification need stable references to each criterion.
- **"Source: pick one" lightens link-type Issues**: when the source is Jira/Tapd, full requirements live externally; this Issue only needs "link + involved ends + one-line summary" to drive G0 routing and gating. Both forms share the same `<ISSUE-KEY>`; gate system unchanged.
- **Issue is a requirements contract, not an implementation blueprint**: technical context, constraints, traceability, verification, and Git branches are produced by the Squad at runtime—not pre-loaded as PM burden.

## Common failures

- Only "help me build this feature" → Squad either guesses or stalls at G0.
- Not checking "involved ends" → Leader doesn't know whether to dispatch Frontend / Backend; flow defaults to full-stack.
- Putting requirement detail into Agent Instructions instead of the Issue → those instructions become invalid for the next task.
