---
name: multica-platform-jira
description: JIRA platform adapter for reading and updating Issue-tracking state and returning stable artifact references.
category: platform
owner: Platform Adapter
version: 1.0
inputs:
  - JIRA operation
  - Issue or payload parameters
  - Runtime platform configuration
outputs:
  - JIRA response or stable artifact reference
side_effects:
  - Reads or mutates JIRA state
requires:
  - Runtime JIRA URL and credentials
  - Team-specific platform configuration
forbidden:
  - Storing real credentials in source
  - Putting platform credentials into Agent Instructions
  - Making Gate decisions
idempotent: false
platform_dependent: true
---

# Platform · JIRA (placeholder shell)

> This is a **platform-layer placeholder shell**. The public multica-best-practices binds to no specific company's internal URLs or credentials.

## Purpose

Provide read/write capability for JIRA-class Issue-tracking systems:

- **Read**: query Issues, search by project or condition, and parse artifact references.
- **Write**: create or update Issues, transition state, schedule work, write back stable artifact references, and notify.

## Configuration boundary

Concrete URLs, projects, fields, and credentials belong to runtime platform configuration such as `config.yaml` and environment variables. They must not appear in Agent Instructions or methodology Skills.

## Execution rules

1. Validate required Issue identifiers and payload fields before writes.
2. Use the platform adapter scripts rather than calling REST directly from Agent Instructions.
3. Return the platform response or a stable artifact reference; never fabricate URLs or IDs.
4. On failure, exit non-zero with diagnosable error output.

## Gate boundary

This Skill is a platform adapter only. It does not execute or approve G0–G4 Gates. Gate decisions are owned by Leader through `multica-verification`.
