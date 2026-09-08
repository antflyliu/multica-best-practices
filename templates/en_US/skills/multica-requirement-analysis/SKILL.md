---
name: multica-requirement-analysis
description: Turn an Issue into a clear, actionable engineering task. Used for requirement clarification, scope confirmation, and acceptance-criteria definition; once structured, hand off to multica-artifact-req-sync for publication.
---

# Requirement Analysis

## Purpose

Turn an Issue into a clear, actionable engineering task, producing structured requirement content without coupling the analysis to a specific platform.

> This Skill works with `multica-artifact-req-sync`: **requirement-analysis owns structure and content; req-sync owns platform publication**. Change the platform in req-sync, not here.

## Process

1. Identify the business goal and success metrics (G- + KPI-).
2. Identify expected behavior, user roles, and permissions.
3. Identify explicit scope and non-scope.
4. Identify non-goals.
5. Identify constraints (compatibility / performance / security / time).
6. Identify acceptance criteria (AC-, testable).
7. Identify ambiguities → record them as OP- open questions; never present assumptions as confirmed.
8. Identify dependencies and risks (RISK-).

## Requirement Structure

Structure the input as a PRD with Multica numbering:

| Section | ID |
| --- | --- |
| One-line definition / background | — |
| Goals and success criteria | G- + KPI- |
| User stories | U- |
| Functional requirements | FR- |
| Business rules | BR- |
| Acceptance criteria | AC- |
| Open questions | OP- |
| Risks | RISK- |

A formal PRD should include at least: one-line definition, background, goals G- + KPI-, users and permissions, scope, FR-/BR-/AC-, field definitions, empty / error / unauthorized states, RISK-/OP-, and revision history.

## Output

- **Goal (G-)**: what problem to solve
- **Scope**: what will change
- **Non-goals**: what explicitly won't change
- **Acceptance criteria (AC-)**: testable check items
- **Constraints**: compatibility / performance / security / time
- **Dependencies**: prerequisites
- **Open questions (OP-)**: centrally maintained; unresolved OP- blocks development
- **Risks (RISK-)**: risks requiring attention

## Rule

Don't silently digest ambiguous requirements.

If an ambiguity would materially affect the implementation:

→ BLOCKED
→ State what is missing and who must provide it; ask only the single most important question.

## Local Draft

Prepare the structured requirement content as a local Markdown draft before publication:

```text
docs/requirements/<ISSUE-KEY>/requirements.md
```

The draft is the reviewable source for the handoff; do not put platform credentials or concrete platform endpoints in this Skill.

## Handoff

Once the draft is ready, use `multica-artifact-req-sync` to publish it to the team's requirement platform and return a stable reference to the Leader.

```text
First use multica-requirement-analysis to structure docs/requirements/<ISSUE-KEY>/requirements.md,
then use multica-artifact-req-sync to publish it and return the stable link.
```

## Why this works

Ambiguity at the requirement stage gets amplified at every later stage. Blocking material ambiguity and using stable IDs makes downstream work consistent; separating content from platform integration also keeps the Skill portable.
