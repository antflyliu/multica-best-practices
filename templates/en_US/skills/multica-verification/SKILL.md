---
name: multica-verification
description: "Gatekeeping function: objectively check whether an artifact satisfies the acceptance criteria. Triggered by the Leader to rerun at gate points (G1/G2/G3); producers may provide evidence but cannot execute formal gatekeeping or issue the gate verdict. Used for design review / implementation acceptance / test-report review."
---

# Verification (gatekeeping)

## What this is

Verification is a **function**, not a role. It answers one question:

> For every acceptance criterion, is there objective evidence that it is satisfied?

The key: verification must be an **objectively decidable action** (run commands, read output, map item by item), not "I feel it's fine."
It doesn't rely on anyone's character — it relies on the evidence itself. Whoever runs it, the result is the same.

## Who executes it

- **Gatekeeping**: the **Leader** triggers this Skill at the gate points (G1 / G2 / G3) and reruns independently. Leader produces no artifacts, so it's naturally a third party.
- **Producer responsibility**: producers provide the artifact and supporting evidence; they do not execute the formal gatekeeping action and cannot issue the gate verdict.

> The gate issuer must be a different party from the gated. Authors cannot stamp "PASS" on themselves.

## Process

1. Read the Issue's acceptance criteria.
2. Map every criterion to evidence (which test / which command / which output).
3. **Rerun** the verification commands; don't cite someone else's described output.
4. Check the change scope: does the diff only touch this requirement?
5. Give PASS / FAIL for each criterion (individual check result).
6. Normalize the gate outcome to APPROVED / APPROVED_NA / REJECTED / BLOCKED.

## Result

Use these four values for the formal gate verdict:

**APPROVED** — every applicable criterion has sufficient evidence; downstream may open.

**APPROVED_NA** — the artifact / branch is explicitly confirmed by the Leader to be not applicable; record the N/A reason and do not silently skip it.

**REJECTED** — at least one applicable criterion is unmet. Must provide: the problem, why it matters, where, the fix direction, and a verifiable pass condition.

**BLOCKED** — missing information / environment / dependency prevents verification. Report honestly; it is not a pass.

> Individual evidence may still use PASS / FAIL, but the final gate verdict must use the four values above so it stays consistent with `gates-and-evidence`.

## Known failure case

A typical failure mode is a producer treating "the local command passed" as gate evidence, with the Leader accepting that output without independently rerunning or checking the diff. A later review can reveal uncovered files and invalidate downstream verification. The rule is explicit: the Leader must rerun independently and check the diff; producer-supplied evidence is never sufficient by itself for the formal gate verdict.

## Relationship to CI hard gates

This Skill is the verification function's form in the agent world (soft gate), suitable for getting started, no CI, or an exploration phase.
The same function's machine form is the CI hard-gate template carried by the `multica-gate-setup` skill. If it can run in CI, run it in CI; the soft gate is transitional.

## Why this works

"Verification" is the easiest thing to turn into a formality. Writing verification as a rerunnable action checklist and requiring the non-producing Leader to execute it blocks producers from turning their own evidence into a formal gate verdict.