---
name: multica-requirement-analysis
description: Turn an Issue or request into structured, reviewable, testable PRD content for ProductManager requirement clarification, scope confirmation, and acceptance criteria; hand off to multica-artifact-req-sync for publication.
category: methodology
owner: ProductManager
version: 1.0
inputs:
  - issue
  - business_context
  - stakeholder_input
outputs:
  - structured_requirements
  - acceptance_criteria
  - open_questions
  - risks
side_effects: []
requires: []
forbidden:
  - write platform URLs, credentials, tokens, or page IDs into requirements
  - publish to external platforms directly
  - make Gate PASS/FAIL decisions
idempotent: true
platform_dependent: false
---

# Requirement Analysis

## Purpose

Turn an Issue, meeting decisions, and scattered requests into **clear, reviewable, decomposable, testable** PRD content.

This skill owns “what to write”, not “where to publish it”. `multica-artifact-req-sync` owns Artifact publication and platform adaptation.

## Process

1. Identify business goals (`G-` / `KPI-`).
2. Identify expected behavior and user roles / permissions.
3. Define explicit scope (in / out).
4. Define non-goals.
5. Identify constraints (compatibility / performance / security / time).
6. Define testable acceptance criteria (`AC-`).
7. Record ambiguities as `OP-` open questions; never pretend they are confirmed.
8. Identify dependencies and risks (`RISK-`).

## Requirement Structure

| Section | ID |
| --- | --- |
| One-line definition / background | — |
| Goals / success criteria | G- + KPI- |
| User stories | U- |
| Functional requirements | FR- |
| Business rules | BR- |
| Acceptance criteria | AC- |
| Open questions | OP- |
| Risks | RISK- |

A formal PRD should include: definition, background, goals, users/permissions, scope, FR-/BR-/AC-, field semantics, empty/error/unauthorized states, RISK-/OP-, and revision history.

## Output

- **Goals (`G-`)**: what problem to solve
- **Scope**: what will change
- **Non-goals**: what explicitly will not change
- **Acceptance criteria (`AC-`)**: testable checks
- **Constraints**: compatibility / performance / security / time
- **Dependencies**: prerequisites
- **Open questions (`OP-`)**: unresolved material questions
- **Risks (`RISK-`)**: risks requiring attention

## Ambiguity Rule

Do not silently digest ambiguous requirements.

If an ambiguity materially affects implementation:

→ `BLOCKED`
→ state what is missing and who must provide it
→ ask only the single most important question

`BLOCKED` is not Gate PASS and does not mean the requirement is ready.

## Handoff

When the structure is ready, `multica-artifact-req-sync` publishes the requirement Artifact to the team's platform and returns a stable reference.

```text
Issue
  ↓
multica-requirement-analysis
  ↓
structured PRD + AC + OP/RISK
  ↓
multica-artifact-req-sync
  ↓
requirement Artifact
```

## Why it works

Separating content methodology from platform adaptation means changing Confluence, Notion, Feishu, or another requirement platform does not require changing requirement analysis, Agent Instructions, or Gate rules.
