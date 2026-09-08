---
name: multica-test-design
description: "Test design function: produce feature cases and API cases from the requirement / design / API contract, execute automation-first, and deliver a test report mapped item by item to the acceptance criteria. Used for feature cases / API test cases / test execution / test reports."
---

# Test Design

## What this is

Test design is a **function**, not a role. It answers one question:

> Have the acceptance criteria actually been verified? What is the evidence?

The key: testing shifts left — cases are prepared during the **design / coding stage**, not after the code is done. When implementation finishes, cases are ready and testing can run immediately.

## Who executes it

- **Production and execution**: the **Tester** triggers this Skill — feature cases at the design stage, API cases at the contract stage, then T3 execution and a test report only after the G2.5 deployment gate is formally approved.
- **Gatekeeping**: the test report is reviewed by the **Leader** at G3 (mapped item by item to the acceptance criteria); the Tester doesn't self-certify.

## Process

1. **Feature cases** (design stage; inputs: requirement + design):
   - Cover every acceptance criterion (each criterion → at least one case)
   - Add edge / exception / regression scenarios
2. **API test cases** (coding stage; input: API contract):
   - Positive / negative / boundary / auth / idempotency
   - Each marked with: method, path, parameters, expected status code and response
3. **Execution (T3)** (**only after G2.5 is formally APPROVED** and a real deployment environment tied to the current commit exists):
   - **Automation first**: scriptable cases become automated tests (merged into the repo's test suite, runnable by the team's CI / test automation tool)
   - Only cases that can't be automated run manually, and manual cases must give reproducible steps
   - If the deployment environment is unavailable or the evidence cannot be tied to the current commit, keep T3 `BLOCKED`; do not substitute a local mock for deployment evidence
4. **Test report**:
   - Mapped item by item to the acceptance criteria: PASS / FAIL / BLOCKED
   - A FAIL must provide: repro steps, expected behavior, actual behavior, evidence, severity

## Result

**PASS** — every acceptance criterion met with sufficient evidence.

**FAIL** — at least one criterion unmet. Must provide: repro steps, expected behavior, actual behavior, evidence, severity.

**BLOCKED** — missing environment / data / dependency, cannot verify. Report honestly; never turn it into PASS.

## Known failure case

A Tester once started T3 before G2.5 had passed and used a local mock environment as the deployment-environment test report. The report was green, but it did not prove that the actual deployed environment met the acceptance criteria. The rule is now explicit: T3 must wait for G2.5 PASS and record the actual test environment; if deployment-environment execution is impossible, report BLOCKED or use only an explicitly permitted non-T3 fallback.

## Relationship to the verification skill

- `multica-verification`: formal gatekeeping by the Leader at G1 / G2 / G2.5 / G3; CI supplies evidence but does not replace the formal verdict
- `multica-test-design`: produces cases + executes T3 + reports (the Tester)

The test report is the **input** to the G3 gate; the automated versions of the cases are part of the CI hard-gate evidence where configured. They complement each other: this Skill defines how cases are produced and run; the Leader defines the formal gate.

## Why this works

Testing is easiest to treat as "homework after the fact": only think about how to test once the code is written, and "ran it" equals "tested it." The three rules — shift left, item-by-item mapping, automation first — turn testing from "proof after the fact" into "part of the design," and give the gate rerunnable machine evidence.
