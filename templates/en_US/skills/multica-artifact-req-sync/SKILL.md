---
name: multica-artifact-req-sync
description: Orchestrate PRD artifact landing through requirement-platform adapters and return a stable reference.
category: orchestration
owner: ProductManager
version: 1.0
inputs:
  - Structured PRD
  - Issue key
outputs:
  - Published PRD reference
side_effects:
  - Creates or updates requirement artifacts
requires:
  - multica-requirement-analysis
  - multica-platform-* requirement adapter
forbidden:
  - Embedding platform credentials in Agent Instructions
  - Redefining PRD content rules owned by multica-requirement-analysis
idempotent: true
platform_dependent: true
---

# Artifact · Requirement Sync

## Purpose

Land product requirement artifacts to the team's unified requirement platform and let downstream retrieve them via a stable reference.

> This skill decouples "platform integration" from "role prompt": the role prompt only says "produce PRD", not which platform. Changing companies means editing only this skill, not the @ProductManager prompt.

## Workflow

1. `multica-requirement-analysis` structures the PRD.
2. This skill orchestrates the configured requirement platform adapter(s).
3. Return the stable artifact reference and version to the Leader.
4. If the artifact version changes, downstream Gates must be re-verified.

## Default platform: Confluence

- Output: PRD artifact with stable G-/FR-/BR-/AC-/KPI-/OP-/RISK- ids.
- Upload: create or update the configured requirement page.
- Retrieve: downstream roles consume the stable page reference.

## Usage

> @ProductManager: "Produce PRD, land it via `multica-artifact-req-sync`, and return the stable reference."

## Boundaries

- `multica-requirement-analysis`: requirement content.
- This skill: artifact publication orchestration.
- `multica-platform-*`: concrete platform integration.
- `multica-verification`: Leader-owned Gate decisions.
