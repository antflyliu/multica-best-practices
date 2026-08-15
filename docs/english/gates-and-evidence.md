# Gates and Evidence

The most common way multi-agent collaboration falls apart: **an agent says "done", but nobody knows whether it's actually true.**

There is only one cure: **put a gate at every stage, require evidence at every gate, and have a non-producer rerun the key evidence.**

## What is a gate

A gate is a checkpoint that can clearly answer "pass / fail". In the software-development Starter these are G0–G4:

| Gate | Content | Who judges |
| --- | --- | --- |
| G0 | Requirements ready: goal + testable acceptance criteria | Leader / Human |
| G1 | Design approved: design aligns with acceptance criteria + acceptable from a business standpoint | Leader (multica-verification skill) + Reviewer |
| G2 | Implementation accepted: prefer the CI verdict; only rerun verification when CI is missing | Leader (multica-verification / multica-gate-setup) |
| G3 | Tests pass: test report maps every acceptance criterion | Leader (reviews the report) |
| G4 | Human acceptance: delivery decision | Human |

The key property of a gate is **decidability**: every gate maps to a question that can be answered PASS / FAIL. If you can't judge it, it's not a gate — it's a wish.

## The gatekeeping action: the multica-verification skill

Verification is a **function**, not a role. It is standardized as `templates/english/skills/multica-verification/` and triggered by the **Leader** at the gate points (G1 / G2 / G3):

- The Leader produces no artifacts → the gatekeeper and the gated are different parties
- Gatekeeping = rerun the verification commands + map each acceptance criterion item by item, without citing the producer's description; when the repo has CI configured, **prefer the CI verdict** (e.g. `[G2 PASS · CI #123]`) and don't rerun (how to read CI: the `multica-gate-setup` skill)
- Producer self-certification (running it yourself) doesn't count; key commands must be rerun

## Verification and review are two different kinds of checks

| | Verification | Review |
| --- | --- | --- |
| Question asked | Is the artifact acceptable? Is there evidence? | Is the design / change acceptable from a business standpoint? |
| How it's judged | Objectively decidable: command output, item-by-item mapping | Subjective judgment: business intent, risk, maintainability |
| Who runs it | Leader (multica-verification skill) / CI | Reviewer (independent role) / Human |

Verification can be standardized into a Skill and machine-run; review must be done by an independent person with a business perspective.

## What counts as evidence

"Done" has no evidentiary value. Valuable evidence:

- List of changed files (git diff summary)
- Commands actually executed + full output
- Item-by-item mapping to acceptance criteria (each criterion → the test or check covering it)
- Test / check results
- Known limitations and risks

## How to prevent "author self-certification"

The rule is simple: **don't let the person who did the work judge whether the work is acceptable.**

- Implementers don't pass themselves
- Gatekeeping is done by the Leader rerunning the multica-verification skill (or citing the CI verdict), not by citing the implementer's description
- The gatekeeper personally reruns the automated verification output

## Soft gates (agent world) vs. hard gates (CI)

LLM instructions are guidance, not a safety boundary. **Rules that must be obeyed live outside the LLM:**

```text
Tests / Lint / Build / CI / branch protection / PR approval
```

- **Soft gate**: the Leader gatekeeps inside the Squad with the multica-verification skill (G1–G3), constrained by instructions and evidence — good for getting started, no CI, or an exploration phase.
- **Hard gate**: unforgeable checks produced by CI (deployment templates and practices live in the `multica-gate-setup` skill: `templates/english/skills/multica-gate-setup/`). When you need results more trustworthy than manual checks, hand the critical gates to CI — the gate issuer must be a different party from the gated.

Soft and hard gates are **two execution environments of the same verification function**: the Skill in the agent world and CI in the engineering world. If it can run in CI, run it in CI.

Don't rely on "the agent was asked not to do this."

## A full walkthrough of a real requirement

Using "add a CSV export feature" as an example:

1. **G0**: The Issue states acceptance criteria, e.g. "after calling the export API, the returned CSV contains all filtered results."
2. **G1**: Architect gives a minimal-change plan (reuse the existing export middleware). The Leader uses the multica-verification skill to confirm the plan covers the acceptance criteria, and the Reviewer checks business acceptability.
3. **Implementation**: Frontend / BackendDev (per the Issue scope) submit code + unit tests + changed-file list + verification command output (self-claimed).
4. **G2**: The Leader prefers the CI verdict (or reruns the verification commands if there's no CI) and checks that the diff only touches this requirement. PASS.
5. **G3**: The Tester produces and executes feature / API cases per the multica-test-design skill, verifies "filter → export → inspect CSV content" against the acceptance criteria, and produces a test report; the Leader reviews whether the report covers every criterion.
6. **G4**: A human reviews the evidence and decides whether to merge / ship.

If any G2/G3 FAILs, the task returns to the responsible implementer and **previous gate conclusions are void — they must be rerun.** "It passed last time" doesn't excuse skipping the rerun.
