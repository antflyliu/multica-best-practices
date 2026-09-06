# Issue Template

> Copy into a new Issue, fill it in, then hand it to the Squad.

```markdown
# Bug

## Issue source (required, pick one)
- [ ] External system link (lightweight)
      - Link: https://jira.example.com/browse/<ISSUE-KEY>
      - Summary: <!-- one line on the symptom -->
- [ ] Fully self-contained (default): this Issue is the requirement; fill in all sections below

## Severity (required)
- [ ] S0 — production blocker / data or security impact / broad outage
- [ ] S1 — severe impact to a core function, needs priority fix
- [ ] S2 — normal functional issue with clear impact and an acceptable workaround
- [ ] S3 — low-impact issue / edge-case experience problem

## Change Type (required)
- [ ] Bug Fix
- [ ] Regression
- [ ] Performance
- [ ] Security
- [ ] Data / Migration
- [ ] Other: <!-- explain -->

## Repro steps
1.
2.
3.

## Expected behavior
<!-- What should happen -->

## Actual behavior
<!-- What actually happened -->

## Impact area
- Affected ends (check; unchecked means no role dispatched):
  - [ ] Frontend
  - [ ] Backend
- Affected users / modules / versions:

## Root-cause hypothesis
<!-- If known, write it here; if unknown, write "TBD" instead of guessing -->

## Fix requirements
- [ ] Locate the root cause
- [ ] Minimal-scope fix
- [ ] Regression test (or explain why it can't be automated)

## Acceptance criteria
- [ ] The issue no longer reproduces with the repro steps
- [ ] Existing behavior doesn't regress
- [ ]

## References
<!-- Logs, screenshots, error messages, relevant code locations -->
```

---

## Why it's written this way

A Bug Issue must state **Severity + Change Type** in addition to being reproducible. Severity drives escalation and verification intensity; Change Type prevents security, data-migration, and performance risks from being disguised as ordinary bug fixes.

Repro steps + expected/actual behavior let the implementer locate the root cause without guessing. If the root cause is unknown, "TBD" is valid; fabrication is not.

## Common failure modes

- **No Severity**: production blockers and low-priority UX issues follow the same path.
- **No Change Type**: security / data / performance risk can be hidden inside an ordinary fix.
- **One-line description with no repro steps**: the implementer can only guess-and-patch.
- **Missing environmental conditions** (version, data, auth state): others can't reproduce, so the gate can't reach PASS.
- **A solution given instead of a root-cause hypothesis**: the Issue should record facts and hypotheses, not prescribe a patch.
- **Regression verification skipped**: without regression evidence, the team can't prove the trigger won't recur.
