---
name: multica-technical-design
description: Produce a minimal technical plan based on the PRD and existing code. Used for architecture analysis, impact assessment, and implementation-plan design; once structured, hand off to multica-artifact-design-sync for publication.
---

# Technical Design

## Purpose

Produce the smallest viable technical plan based on the PRD (or Issue) and the existing codebase, without coupling the design content to a specific platform.

> This Skill works with `multica-artifact-design-sync`: **technical-design owns structure and content; design-sync owns platform publication**.

## Process

1. Read the PRD / Issue and acceptance criteria (AC-).
2. Inspect the current implementation (prefer codegraph / existing patterns; avoid broad repository scans).
3. Identify relevant modules and existing patterns.
4. Determine the smallest viable change and state non-goals.
5. Identify dependencies and risks (RISK-).
6. Define the verification method and map it to AC-.
7. Missing information → BLOCKED; do not guess.

## Principles

```text
Existing patterns > new abstractions
Small changes     > big refactors
Reuse             > new dependencies
```

## Local Draft

Write a Markdown draft first, then hand it to design-sync for publication:

```text
docs/design/<ISSUE-KEY>/design.md
```

The section baseline is defined by `multica-platform-confluence`'s `scripts/templates/design-template.md`.

## Output (required)

| Section | Content |
| --- | --- |
| Understanding | What the system currently does |
| Proposed changes | Smallest viable solution |
| Affected components | Files / modules / services |
| Implementation steps | Executable steps for @FrontendDev / @BackendDev |
| Verification plan | How to verify, mapped to AC- |
| Risks and boundaries | RISK- IDs |

## Handoff

Once the draft is complete, use `multica-artifact-design-sync` to publish it and return a stable reference to the Leader.

```text
First use multica-technical-design to write docs/design/<ISSUE-KEY>/design.md,
then use multica-artifact-design-sync to publish it and return the stable reference.
```

Do not put platform credentials, concrete platform URLs, or page IDs in this Skill; those belong in the `multica-platform-*` placeholder shells.

## Why this works

A local Markdown draft is diffable and reviewable before publication. Separating design content from platform integration keeps the workflow portable while giving @FrontendDev / @BackendDev / @Tester a stable downstream reference after publication.
