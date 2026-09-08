---
name: multica-artifact-cicd-sync
description: "CI/CD artifact orchestration: after G2 PASS and code push, invoke the platform adapter for deployment and return deployment version/evidence. This skill never owns G2.5/G3 Gate decisions."
category: orchestration
owner: Leader
version: 1.0
inputs:
  - issue
  - g2_result
  - commit_or_artifact_version
  - environment
  - deploy_branch
outputs:
  - deployment_version
  - deployment_evidence
  - deployment_url
side_effects:
  - triggers deployment through platform adapter
requires:
  - multica-verification
  - multica-platform-jenkins
forbidden:
  - trigger T3 before G2.5 PASS
  - make G2.5 or G3 PASS decisions
  - hardcode platform credentials or URLs
idempotent: false
platform_dependent: true
---

# Artifact · CI/CD Sync (orchestration)

## Purpose

After **G2 PASS + code push**, orchestrate CI/CD deployment through the `multica-platform-*` adapter and return deployment version/evidence.

> This skill owns deployment orchestration, not the G2.5 decision. G2.5 must be independently decided by the Leader using `multica-verification`.

## Preconditions

All must hold:

- G2 = `PASS`
- the Artifact Version / commit bound to G2 has not changed
- the deploy branch is explicit in the Issue / confirmed deployment context
- the required platform adapter is available

If any condition is missing → `BLOCKED`; do not trigger downstream T3.

## Workflow

```text
G2 PASS
  ↓
code push / artifact version fixed
  ↓
multica-artifact-cicd-sync
  ↓
multica-platform-* discover → trigger → poll
  ↓
deployment_version + evidence
  ↓
Leader / multica-verification decides G2.5
  ↓
G2.5 PASS
  ↓
Tester may trigger T3
```

## Workflow A: dev

```bash
python scripts/trigger_cicd.py \
  --issue <ISSUE-KEY> \
  --env dev \
  --service <service> \
  --branch release/<ISSUE-KEY>-<slug> \
  --json
```

## Workflow B: sit

```bash
python scripts/trigger_cicd.py \
  --issue <ISSUE-KEY> \
  --env sit \
  --branch release/<ISSUE-KEY>-<slug> \
  --json
```

## Workflow C: multi-service

```bash
python scripts/trigger_cicd.py --env sit --service <service1>,<service2> --branch release/<ISSUE-KEY>-<slug> --json
```

## Parameter policy

Platform parameters are discovered by `multica-platform-*`; this orchestration layer never hardcodes Job parameter names.

- deploy branch must come from the Issue / confirmed deployment context
- missing required parameters → fill them or `BLOCKED`
- platform build `SUCCESS` is platform execution evidence, not automatically G2.5 PASS

## Artifact Contract

A successful deployment must return at least:

```yaml
artifact:
  type: deployment
  issue_key: <ISSUE-KEY>
  version: <DEPLOYED_VERSION>
  location:
    type: cicd
    url: <DEPLOY_URL>
  source:
    commit: <COMMIT_SHA>
  status: deployed
```

`<DEPLOYED_VERSION>` must uniquely identify the deployed content. If the deployment artifact version changes, downstream Gates become invalid and must be re-verified.

## T3 Boundary

This skill **must not trigger T3 directly**. Only after the Leader records `G2.5 = PASS` may Tester use `multica-test-automation` for T3.

## Why it works

Platform differences stay inside `multica-platform-*`; orchestration handles Issue, version, environment, and evidence. Swapping Jenkins / GitLab CI / GitHub Actions therefore does not require changes to Agent Instructions or Gate logic.
