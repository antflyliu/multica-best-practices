---
name: multica-artifact-design-sync
description: Orchestrate technical design artifact publication and return a stable reference; concrete platforms are provided by adapters.
category: orchestration
owner: Architect
version: 1.0
inputs:
  - Technical design artifact
  - Issue key
  - Target platform adapter
outputs:
  - Stable design artifact reference
side_effects:
  - Creates or updates design artifacts
requires:
  - multica-technical-design
  - multica-platform-* adapter
forbidden:
  - Embedding credentials in Agent Instructions
  - Owning Gate PASS decisions
idempotent: true
platform_dependent: true
---

# Artifact · Technical Design Sync

## Purpose

Land technical design docs to the team's agreed location and let downstream retrieve them via a stable reference.

> This skill decouples platform integration from the role prompt. The role only says "produce technical design"; this skill handles publication.

## Default platform

- Git repo or Confluence, according to team convention.
- Output: technical design with current architecture, proposed change, affected components, steps, verification plan, and risks.
- Retrieve: downstream roles consume the file path or page link.

## Usage

> @Architect: "Produce technical design, land it via `multica-artifact-design-sync`, and return the stable reference."

## Boundaries

- `multica-technical-design`: design content.
- This skill: artifact publication orchestration.
- `multica-platform-*`: concrete platform adapter.
- `multica-verification`: Leader-owned Gate decisions.
