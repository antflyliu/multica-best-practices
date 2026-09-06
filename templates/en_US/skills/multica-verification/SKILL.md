---
name: multica-verification
description: Independent gate verification: Leader reruns acceptance criteria at G1/G2/G3 and outputs PASS, FAIL, or BLOCKED. It judges delivery conditions and does not produce business, technical, or test artifacts.
category: gate
owner: Leader
version: 1.0
inputs:
  - Gate ID
  - Issue
  - Artifact
  - Artifact Version
  - Upstream Gates
  - Acceptance Criteria
  - Evidence
outputs:
  - Gate Result
  - Criterion-level evidence mapping
side_effects:
  - Records Gate status for the specified Artifact Version
requires:
  - Valid Issue and Acceptance Criteria
  - Valid upstream Gate results
forbidden:
  - Producing or modifying the Artifact under verification
  - Self-approving a producer's Artifact
  - Treating BLOCKED as PASS
idempotent: true
platform_dependent: false
---

# Verification (Independent Gate)

## Positioning

Verification is a **gate action**, not a role and not a production Skill. It answers only:

> Does the specified artifact version have objective evidence that it satisfies the current Gate's acceptance criteria?

**The only gate executor is the Leader.** A producer must not use this Skill to stamp PASS on their own artifact.

If a producer needs an early check, use a pre-submit checklist inside the producer's Skill. That check does not create Gate status and cannot replace Leader Verification.

## Gate Inputs

Before running this Skill, the Leader must identify at least:

- `Gate ID`: `G1` / `G2` / `G3`
- `Issue`
- `Artifact`
- `Artifact Version`
- `Upstream Gates`
- `Acceptance Criteria`
- `Evidence`

If a required input is missing, the result must be `BLOCKED`, never `PASS`.

## Process

1. Read the Issue's Acceptance Criteria.
2. Confirm the target Artifact and its current Version.
3. Confirm all Upstream Gates are still valid.
4. Map every Acceptance Criterion to rerunnable Evidence.
5. **Leader reruns the checks independently**; producer-reported or pasted output is not a substitute for rerun evidence.
6. Check the diff / change scope against the Issue Scope.
7. Record each check result and aggregate the Gate Result.

## Gate Result

### PASS

All current Gate Acceptance Criteria are satisfied and Upstream Gates are valid.

### FAIL

At least one Acceptance Criterion is unmet. Record:

- Problem
- Why it matters
- Evidence / location
- Fix direction

### BLOCKED

Required information, environment, evidence, or a valid upstream Gate is missing, so an objective decision cannot be made. **BLOCKED can never be converted to PASS until the blocking condition is resolved and verification is rerun.**

## Artifact Change Rule

**Whenever an artifact is modified, every downstream Gate immediately becomes invalid.**

The Leader must:

1. Identify downstream dependencies of the modified Artifact.
2. Mark affected downstream Gates as requiring re-verification.
3. Never reuse a Gate PASS or evidence from the previous artifact version.
4. Restart Verification from the earliest affected Gate.

Therefore, a Gate PASS is bound to a specific `Artifact Version`, not merely to an Issue.

## Boundaries

- **Reviewer**: judges professional quality and produces review findings.
- **Leader / Verification**: judges whether delivery Gate conditions are met and produces the Gate Result.
- **CI/PR**: provides machine-verifiable evidence; prose cannot replace it.
- **Human Acceptance**: decides final business/product acceptance; Verification does not replace it.

## Relationship to CI

`multica-verification` is the Agent-side Gate execution method; CI is the machine-side hard gate. They complement rather than replace each other:

- Checks that can be automated should be enforced in CI.
- At a Gate, Leader still confirms that CI evidence belongs to the current Artifact Version.
- T3 automated testing may trigger **only after G2.5 CI/CD PASS**.

## Result Contract

Leader should emit the following structure consistently:

```yaml
gate:
  id: G2
  issue: <ISSUE_KEY>
  artifact: <ARTIFACT_TYPE>
  artifact_version: <VERSION>
  upstream_gates: [G1]
  result: PASS | FAIL | BLOCKED
  checks:
    - criterion: <AC_ID>
      result: PASS | FAIL | BLOCKED
      evidence: <COMMAND_OR_EVIDENCE_REF>
  failures: []
```
