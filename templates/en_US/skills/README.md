# Skills Index (en_US)

This directory contains reusable Skills that can be mounted into Multica. Each subdirectory is one Skill; `SKILL.md` is the Agent-facing contract, while script-backed Skills may also include a `README.md` for human setup.

## 1. Skill Contract

Every Skill `SKILL.md` should use the same frontmatter contract:

```yaml
---
name:
description:
category: methodology | orchestration | platform | gate
owner:
version:
inputs:
outputs:
side_effects:
requires:
forbidden:
idempotent: true | false
platform_dependent: true | false
---
```

`Agent` defines role responsibilities; `Skill` defines the concrete method. Gate status is produced only by the Leader using `multica-verification`.

## 2. Platform

Platform Skills may contain team-specific URL / credential placeholders, but real credentials must never be committed.

| Skill | Purpose |
|---|---|
| `multica-platform-confluence` | Confluence publishing / query adapter |
| `multica-platform-jira` | JIRA Issue read/write and workflow adapter |
| `multica-platform-jenkins` | Jenkins build, release, and promotion adapter |

## 3. Orchestration

Orchestration Skills route and publish Artifacts through platform Skills without embedding platform implementation in role prompts.

| Skill | Purpose |
|---|---|
| `multica-artifact-req-sync` | PRD / requirements Artifact sync |
| `multica-artifact-cicd-sync` | Orchestrate review results into CI/CD |
| `multica-artifact-api-sync` | API contract Artifact sync |
| `multica-artifact-design-sync` | Technical design Artifact sync |
| `multica-artifact-test-sync` | Test Artifact sync |
| `multica-artifact-ui-sync` | UI Artifact sync |

## 4. Methodology

| Skill | Purpose |
|---|---|
| `multica-implementation` | Implementation methodology |
| `multica-requirement-analysis` | Requirement analysis |
| `multica-technical-design` | Technical design |
| `multica-test-design` | T1/T2 test design and coverage analysis |
| `multica-test-automation` | T3 runtime automation after G2.5 |
| `multica-review-architect` | Architecture professional review |
| `multica-review-backend` | Backend professional review |
| `multica-review-product` | Product professional review |
| `multica-review-test` | Test professional review |

## 5. Gate / Setup

| Skill | Purpose |
|---|---|
| `multica-verification` | Leader-owned independent G1/G2/G3 gate decision |
| `multica-gate-setup` | CI / branch-protection gate templates |
| `multica-manage-skills` | Multica Skill management adapter; platform management, not core development methodology |

## 6. Mounting Rules

1. Copy the required Skill directories into the Multica workspace `skills/` directory.
2. For script-backed Skills, follow their `README.md` / `.env.example` setup instructions.
3. Platform URLs, tokens, accounts, and credentials belong only in `multica-platform-*` or the relevant adapter configuration, never in Agent Instructions.
4. If any Artifact changes, all downstream Gates immediately become invalid and must be re-verified.
5. T3 must not trigger before `G2.5 = PASS`; when CI is unavailable, T3 automation remains `BLOCKED` rather than being treated as PASS.

## 7. Naming

- Use the `multica-` prefix with lowercase hyphen-separated names.
- `SKILL.md` `name` must match its directory name.
- `category` must be one of `methodology` / `orchestration` / `platform` / `gate`.
