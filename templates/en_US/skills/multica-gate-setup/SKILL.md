---
name: multica-gate-setup
description: Install CI hard-gate templates into a target repository and provide the machine-evidence path for G2.5.
category: orchestration
owner: Leader
version: 1.0
inputs:
  - Target repository
  - CI workflow commands
  - Branch protection policy
outputs:
  - Installed CI gate configuration
  - Machine-verifiable G2.5 evidence path
side_effects:
  - Creates or updates CI workflow and branch protection configuration
requires:
  - Target repository CI capability
  - multica-verification for Leader-side gate decisions
forbidden:
  - Treating human-pasted CI claims as machine evidence
  - Allowing T3 before G2.5 PASS
idempotent: true
platform_dependent: true
---

# Gate Setup (CI gate integration)

## Positioning

Install CI as the machine gate for G2.5 and make the CI evidence traceable to the current Artifact Version. This Skill handles installation and integration; it does not replace Leader-owned `multica-verification`.

## Template files

- `delivery-gate.yml`: CI workflow.
- `branch-protection.json`: branch protection template.
- `apply-branch-protection.sh`: protection-rule application script.

## Deployment

1. Replace workflow placeholders with the target repository's real commands.
2. Configure branch protection / rulesets so `delivery-gate` is a merge gate.
3. Verify that the workflow produces a machine-readable result.
4. Record how the CI result is associated with the current Artifact Version.

Concrete GitHub API, Jenkins, or other platform details belong in platform adapters; this Skill is not tied to one platform.

## G2.5 boundary

The canonical state machine is:

```text
G2 PASS
  ↓
G2.5 CI/CD
  ↓
G2.5 PASS
  ↓
T3
  ↓
G3
```

- Missing CI or unreadable CI evidence → `G2.5 = BLOCKED`; never turn it into PASS.
- Manual verification may exist, but it cannot substitute for G2.5 machine evidence.
- **T3 automation may trigger only after G2.5 PASS.**

## Relationship to multica-verification

- `multica-gate-setup`: installs the CI hard gate and exposes machine evidence.
- `multica-verification`: Leader independently executes Gate decisions.
- Reviewer: judges professional quality and does not own Gate authority.

If any Artifact changes, all downstream Gates become invalid and must be re-verified.
