---
name: multica-artifact-ui-sync
description: Orchestrate publication of UI and interaction design artifacts and return a stable reference through a replaceable design-platform adapter.
category: orchestration
owner: Designer
version: 1.0
inputs:
  - UI design artifact
  - Issue key
  - Target design platform adapter
outputs:
  - Stable UI artifact reference
side_effects:
  - Publishes or updates UI design artifacts
requires:
  - Configured design platform adapter
forbidden:
  - Embed platform credentials in Agent Instructions
  - Declare Gate PASS
idempotent: true
platform_dependent: true
---

# Artifact · UI Design Sync

## Purpose

Publish UI design artifacts through the team's design-platform adapter and return a stable reference for downstream consumers.

The role prompt describes what Designer produces; platform-specific integration belongs here or in the platform adapter. Swapping Figma, Zeplin, MasterGo, or an internal design library must not require changing the Designer role contract.

## Platform boundary

This skill defines the orchestration interface only:
- receive the completed UI artifact;
- call the configured design-platform adapter;
- return the stable artifact reference and publication evidence.

Do not hard-code vendor URLs, credentials, tokens, or account configuration in this methodology/orchestration contract.

## Content requirements

Regardless of platform, the UI artifact should include:
- Page/module structure aligned with PRD information architecture
- Empty, loading, error, and no-permission states
- Entry, navigation, and validation-feedback interactions
- Size, spacing, color, typography, and component-boundary annotations

## Output

Return the stable UI artifact reference to Leader and downstream consumers. This skill does not grant any Gate PASS.
