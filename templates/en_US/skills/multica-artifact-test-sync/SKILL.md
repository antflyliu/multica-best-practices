---
name: multica-artifact-test-sync
description: Orchestrate test case and report artifact publication through a case-management adapter and return a stable reference.
category: orchestration
owner: Tester
version: 1.0
inputs:
  - Test artifact
  - Issue key
  - Target platform adapter
outputs:
  - Stable test artifact reference
side_effects:
  - Creates or updates test artifacts
requires:
  - multica-test-design
  - Configured case-management adapter
forbidden:
  - Embedding platform credentials in Agent Instructions
  - Declaring G3 PASS
idempotent: true
platform_dependent: true
---

# Artifact · Test Case Sync

## Purpose

Land test case / report artifacts to the team's unified case-management platform and let downstream retrieve them via a stable reference.

> This skill decouples platform integration from the role prompt. The role only says "produce test cases"; this skill handles publication.

## Default platform

Local XMind → Jira, replaceable by TestRail / Zephyr / ZenTao / an internal case library.

- Output: feature cases / API cases / test report per `multica-test-design`.
- Upload: publish the test artifact and return the case-set reference.
- Retrieve: downstream roles consume the stable reference.

## Usage

> @Tester: "Produce cases / report, land them via `multica-artifact-test-sync`, and return the stable reference."

## Boundaries

- `multica-test-design`: T1/T2 test content.
- This skill: artifact publication orchestration.
- `multica-verification`: Leader-owned Gate decisions.
