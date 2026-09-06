---
name: multica-artifact-api-sync
description: Orchestrate API contract artifact landing through an API-platform adapter and return a stable reference.
category: orchestration
owner: BackendDev
version: 1.0
inputs:
  - API contract artifact
  - Issue key
  - Target platform adapter
outputs:
  - Stable API artifact reference
side_effects:
  - Creates or updates API contract artifacts
requires:
  - Valid API contract
  - Configured platform adapter
forbidden:
  - Embedding platform credentials in Agent Instructions
  - Declaring Gate PASS
idempotent: true
platform_dependent: true
---

# Artifact · API Contract Sync

## Purpose

Land API contract artifacts to the team's unified API platform and let downstream (frontend / test) retrieve them via a stable reference.

> This skill decouples "platform integration" from "role prompt": the role prompt only says "produce API contract", not which platform.

## Default platform: Apifox

- Output: API contract (endpoints, in/out params, error codes, auth, state-machine boundaries).
- Upload: maintain interface definitions and return the project / interface-group link as the artifact reference.
- Retrieve: downstream roles consume the stable link.

## Usage

> @BackendDev: "Produce API contract, land it via `multica-artifact-api-sync`, and return the stable reference."

## Boundaries

- This skill: artifact publication orchestration.
- `multica-platform-*`: concrete API platform adapter.
- `multica-verification`: Leader-owned Gate decisions.
