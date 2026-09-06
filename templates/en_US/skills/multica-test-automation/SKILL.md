---
name: multica-test-automation
description: Tester T3 runtime automation: run automated tests only after G2.5 CI/CD PASS and the deployment environment is ready, producing G3 input. The concrete test tool is provided by a team adapter; this Skill is vendor-neutral.
category: methodology
owner: Tester
version: 1.0
inputs:
  - Issue
  - Deployed Artifact Version
  - Deploy Base URL
  - Test Suite
  - G2.5 PASS evidence
outputs:
  - Machine-readable T3 test result
  - Runtime test evidence
side_effects:
  - Executes runtime tests against the deployed environment
requires:
  - G2.5 PASS
  - Deployment environment ready
  - Team test adapter / runner
forbidden:
  - Running T3 before G2.5 PASS
  - Declaring G3 PASS
  - Hard-coding vendor-specific credentials in this Skill
idempotent: true
platform_dependent: false
metadata:
  runtime:
    python: ">=3.10"
---

# Test Automation (T3)

## Purpose

Run post-deployment runtime automation against the target environment and produce machine-readable evidence for G3.

**Hard prerequisite: `G2.5 = PASS`.** T3 must not start before G2.5 PASS.

## Input Contract

```yaml
t3:
  issue: <ISSUE_KEY>
  artifact_version: <DEPLOYED_VERSION>
  base_url: <DEPLOY_BASE_URL>
  test_suite: <TEST_SUITE>
  g2_5: PASS
```

If `g2_5` is not `PASS`, the result must be `BLOCKED` and no tests may run.

## Execution

Use the team's adapter-provided test runner, for example:

```bash
python scripts/run_tests.py \
  --issue <ISSUE_KEY> \
  --base-url "<deploy_base_url>" \
  --suite <TEST_SUITE> \
  --json
```

Concrete CLI names, scenario IDs, environment IDs, tokens, and platform details belong to the adapter / platform configuration. They must not be embedded in Tester Agent Instructions or the generic Skill.

## Output Contract

```yaml
test_run:
  issue: <ISSUE_KEY>
  artifact_version: <DEPLOYED_VERSION>
  gate_prerequisite: G2.5:PASS
  result: PASS | FAIL | BLOCKED
  total: <N>
  passed: <N>
  failed: <N>
  blocked: <N>
  evidence: <MACHINE_READABLE_REPORT>
```

## Failure Rules

- Environment not ready / G2.5 not PASS → `BLOCKED`.
- Test failure → `FAIL`, retaining reproducible steps and machine evidence.
- A passing T3 run means only T3 execution passed; it does not mean G3 passed.
- G3 is independently gated by the Leader using `multica-verification`.

## Boundaries

- `multica-test-design`: T1/T2 test design and coverage gaps.
- `multica-test-automation`: T3 runtime execution after G2.5.
- `multica-artifact-test-sync`: publishes/synchronizes test Artifacts.
- `multica-verification`: independent Gate decision by the Leader.

If the tested Artifact or test Artifact is modified, all downstream Gates immediately become invalid and must be re-verified.
