---
name: multica-technical-design
description: Produce a minimal technical plan from the PRD / Issue and existing code. Owns design content only; platform publishing, JIRA/Confluence operations, and credentials belong elsewhere.
category: methodology
owner: Architect
version: 1.0
inputs:
  - Issue / PRD
  - Acceptance Criteria
  - Existing Code
outputs:
  - Technical Design Artifact
  - Verification Plan
side_effects:
  - Creates or updates the technical-design artifact
requires:
  - Stable Issue scope and Acceptance Criteria
  - Access to relevant source code
forbidden:
  - Platform publishing
  - JIRA / Confluence operations
  - Credential management
  - Declaring Gate PASS
idempotent: true
platform_dependent: false
---

# Technical Design

## Purpose

Produce the smallest viable technical design from the PRD / Issue, acceptance criteria, and existing code.

This Skill answers "what, why, how, and how to verify". It does not own platform publishing. `multica-artifact-design-sync` publishes the artifact, while downstream platform adapters handle concrete platforms.

## Process

1. Read the PRD / Issue and Acceptance Criteria.
2. Inspect the current implementation using existing patterns and focused searches.
3. Identify affected modules, dependencies, and boundaries.
4. Determine the smallest viable change and state non-goals.
5. Mark risks as `RISK-*`.
6. Define verification methods mapped to the Acceptance Criteria.
7. If information is insufficient, return `BLOCKED` rather than guessing.

## Principles

```text
Existing patterns > new abstractions
Small changes     > big refactors
Reuse             > new dependencies
```

## Output Contract

```text
docs/design/<ISSUE-KEY>/design.md
```

Required sections:

| Section | Content |
| --- | --- |
| Understanding | Current behavior and context |
| Proposed Changes | Smallest viable solution |
| Affected Components | Files / modules / services |
| Implementation Steps | Actionable steps for implementation roles |
| Verification Plan | Verification mapped to `AC-*` |
| Risks & Boundaries | `RISK-*` and non-goals |

## Handoff

After the draft is complete, hand it to `multica-artifact-design-sync`. That orchestration Skill publishes the local Artifact to the team's platform; platform URLs, page IDs, tokens, and credentials belong only to `multica-platform-*`.

Do not put concrete platform URLs, page IDs, tokens, accounts, or platform API details in this Skill.

## Gate Boundary

- This Skill: produces the technical design.
- Reviewer: evaluates professional design quality.
- Leader + `multica-verification`: independently judges the Gate.
- `multica-artifact-design-sync`: publishes and synchronizes the Artifact.
- `multica-platform-*`: handles concrete platform adapters.

If the design Artifact is modified, all downstream Gates immediately become invalid and must be re-verified.
