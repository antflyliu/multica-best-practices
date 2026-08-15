# Issue Template

> Copy into a new Issue, fill it in, then hand it to the Squad.

```markdown
# Bug

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
<!-- If known, write it here -->

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

The first priority of a Bug Issue is "reproducible." With the repro steps + expected/actual behavior written out, the implementer can locate the root cause without guessing.
