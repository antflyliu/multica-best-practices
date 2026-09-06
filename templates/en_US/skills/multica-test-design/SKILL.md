---
name: multica-test-design
description: Produce test cases and a coverage matrix from requirements, design, and API contracts. Owns T1/T2 test design and gap analysis; it does not gate G3 or execute post-deployment T3 automation.
category: methodology
owner: Tester
version: 1.0
inputs:
  - Issue / PRD
  - Acceptance Criteria
  - Technical Design
  - API Contract
  - Implemented Code for T2
outputs:
  - T1 test cases
  - T2 coverage matrix
  - Test gaps
side_effects:
  - Creates or updates test-design artifacts
requires:
  - Stable Acceptance Criteria
  - Design available for T1
forbidden:
  - Executing T3 runtime automation
  - Declaring G3 PASS
  - Replacing Leader Verification
idempotent: true
platform_dependent: false
---

# Test Design

## Positioning

Test design is a **production function**, not a gatekeeping role. It makes Acceptance Criteria testable before implementation and identifies coverage gaps after implementation.

## Execution

- **Tester**: runs this Skill and produces T1/T2 test design and coverage analysis.
- **Leader + `multica-verification`**: owns independent G3 gatekeeping. Tester must not stamp Gate PASS on its own result.
- **`multica-test-automation`**: owns only T3 runtime automation after G2.5 PASS.

## Workflow

### T1 — Test Design (before G1)

Input: PRD / Issue + technical design.

Output:

- At least one test scenario for every `AC-*`.
- Happy-path, boundary, negative, and regression scenarios.
- API scenarios covering method, path, parameters, and expected response.
- Mark which cases are automatable and which require manual verification.

### T2 — Coverage & Gap Analysis (before G2)

Input: implemented code, T1 test design, and Acceptance Criteria.

Output:

- `AC-*` → test case → implementation coverage matrix.
- Uncovered items and reasons.
- Automation gaps.
- Recommended additional test cases.

T2 does not execute T3 runtime automation and does not claim G3 PASS.

## Test Case Contract

Each key case should contain at least:

```yaml
id: TC-001
acceptance_criteria: [AC-001]
scenario: <scenario>
type: positive | negative | boundary | regression
preconditions: []
steps: []
expected: <expected_behavior>
automatable: true | false
```

## Result

- `READY`: test design is complete for the current stage.
- `GAP`: coverage is incomplete; resolve the gap or explicitly accept the risk.
- `BLOCKED`: required requirements, design, data, or environment information is missing.

## Boundaries

- `multica-test-design`: T1/T2 design, coverage, and gap analysis.
- `multica-test-automation`: **only after G2.5 PASS**, execute T3 runtime automation.
- `multica-verification`: Leader independently gates G3.
- `multica-artifact-test-sync`: publishes/synchronizes the test Artifact.

If a test-design Artifact is modified, all downstream Gates immediately become invalid and must be re-verified.
