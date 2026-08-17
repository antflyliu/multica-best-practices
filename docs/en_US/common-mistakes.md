# Common Mistakes (Bad → Good)

> Every mistake comes from real usage. Read these and you'll understand why each template is written the way it is.

## 1. Agent prompt too all-round

**Bad**

```text
You are an all-round software development expert.
You need to analyze requirements, design the architecture, write code, test, review,
and make sure the final task is done.
```

**Good**

```text
You implement the confirmed technical design.
You don't change product requirements, and you don't do the final review.
```

Why: an all-round Agent occupies Agent / Squad / Skill / Issue at the same time, so changing the task breaks all of it; a narrow Agent can be reused as-is for the next task.

## 2. Squad is just an empty phrase

**Bad**

```text
Everyone collaborate to finish the task, help each other when needed.
```

**Good**

```text
Frontend implementation → FrontendDev (scope includes frontend)
Backend implementation + API contract → BackendDev (scope includes backend)
Gatekeeping → Leader reruns with the multica-verification skill
Business review → Reviewer
Testing → Tester

Gate FAIL → the responsible implementer
Test FAIL → the responsible implementer
```

Why: the value of a Squad is **explicit routing**. When routing is vague, every Agent guesses what to do next.

## 3. Issue has no acceptance criteria

**Bad**

```text
Please build this feature for me.
```

**Good**

```text
Goal: ...
Scope: ...
Non-goals: ...
Acceptance criteria: - [ ] ...
Constraints: ...
Verification method: ...
```

Why: without testable acceptance criteria, the gate system (G0–G4) breaks and Verification has nothing to judge.

## 4. Letting the completer self-certify

**Bad**

```text
After the implementer writes the code: review it yourself, and mark complete once it looks fine.
```

**Good**

```text
After the implementer writes the code: provide evidence (changed files + command output); the Leader reruns the multica-verification skill to gate it.
```

Why: authors instinctively make excuses for themselves. Gatekeeping must be done by a non-producer (Leader rerun or CI); producer self-certification doesn't count.

## 5. Writing hard constraints into the prompt

**Bad**

```text
The agent must ensure the code has no security issues and all tests pass before submitting.
```

**Good**

```text
Enforce passing tests with CI and require PR approval with branch protection. Agent instructions are only guidance.
```

Why: LLM instructions are not a safety boundary. Rules that truly "must" hold are enforced in the engineering system.

## 6. Using "it's done" instead of evidence

**Bad**

```text
The Squad Leader judges task completion by: members report done.
```

**Good**

```text
The Squad Leader judges task completion by: changed files + actual command output + item-by-item mapping to acceptance criteria.
```

Why: "done" is a verbal claim; evidence is a reproducible fact. Only trust the latter.

## 7. Blindly copying the five-Agent flow

**Bad**

```text
Every task goes through: Architect → Frontend/BackendDev → Tester → Leader gate.
Including changing one config line or fixing a typo.
```

**Good**

```text
Pick the smallest combination per task type: bugs use bug-fix (skip Architect),
small changes can be just BackendDev + Reviewer, and research tasks may not need a developer role at all.
```

Why: best practices aren't a fixed flow, they're **the smallest viable combination for the task**. The heavier the flow, the more context overhead.

## 8. Having the Leader do the work

**Bad**

```text
The Leader is the universal fallback: whatever others can't do, the Leader does.
```

**Good**

```text
The Leader only routes, gates, and escalates. Implementation is always delegated to the relevant member.
```

Why: the Leader is the conductor — conductors don't play the instruments.

## 9. Silently skipping an in-scope artifact as "not needed"

**Bad**

```text
Leader: let's skip the design this time, go straight to development.
(no reason recorded, no confirmation)
```

**Good**

```text
Leader: design judged N/A — reason is this change reuses the existing export
middleware with no new architecture decision; confirmed and recorded as N/A,
downstream gates follow the "no design" branch.
```

Why: when an in-scope artifact is judged not applicable, it must be marked N/A with the reason and the Leader's confirmation — otherwise it's a silent scope change. An unconfirmed N/A counts as a missing scope and should be written back to the Issue. Same logic in reverse: once an artifact is modified, its downstream gates must be invalidated and re-judged, not carried over as an old PASS; and when the same artifact fails your gate 3 times in a row, escalate to a Human instead of looping on rework forever.

---

## Diagnostic checklist

If your squad "looks like it's running, but results are unstable," check in order:

1. Does the Issue have testable acceptance criteria? (No → nothing else matters)
2. Does each Agent do exactly one thing? (Overlap → behavior drifts)
3. Is gatekeeping done by a non-producer? (Author self-judging → no real check)
4. Is the completion standard evidence? (Verbal reports → can't be reviewed)
5. Are hard constraints in CI / branch protection? (Only in the prompt → will eventually be bypassed)
6. When an in-scope artifact is N/A, is it marked with a reason and confirmed by the Leader? (Silent skip → equals a stealthy scope change)
7. After an upstream artifact is modified, are downstream gates invalidated and re-judged? (Carrying over an old PASS → gates are decorative)
8. Does the same artifact failing repeatedly get escalated to a Human? (Endless rework → consumes without converging)
