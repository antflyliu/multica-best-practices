# Gates & Evidence

The most common failure mode in multi-Agent collaboration: **an Agent says "done," but nobody knows whether it is actually done.**

The solution is one system: **each stage has a gate, each gate requires evidence, and critical evidence is rerun by a party other than the producer.**

## What is a gate?

A gate is a checkpoint that can answer "pass / not pass" unambiguously. In the software-development Starter, the stages are G0–G4:

| Gate | Content | Decider |
| --- | --- | --- |
| G0 | Requirements ready: goal + testable acceptance criteria | Leader / Human |
| G1 | Design approved: design aligned with acceptance criteria + business acceptance | Leader (multica-verification skill) + Reviewer (business review in default software-development; dedicated Reviewer per artifact in reviewed) |
| G2 | Implementation acceptance: prefer CI verdict; rerun verification if CI is absent | Leader (multica-verification / multica-gate-setup) |
| G2.5 | CI/CD deployment: after G2 PASS and code push, build/deploy to test env and return environment URL | Leader (checks CI evidence, triggered by @DevOps) |
| G3 | Test passed: T3 automation report maps item-by-item to acceptance criteria (depends on G2.5 deployment) | Leader (reviews report) |
| G4 | Human acceptance: delivery decision | Human |

A gate must be **decidable**: each gate maps to a question that can be answered with evidence. If it cannot be decided, it is not a gate; it is a wish.

## Gatekeeping action: multica-verification skill

Verification is a **function**, not a role. It is standardized as `templates/en_US/skills/multica-verification/SKILL.md`, triggered by the **Leader** at G1 / G2 / G3:

- Leader produces no artifact → the decider and producer are independent
- Gatekeeping = rerun verification commands + map evidence item-by-item to acceptance criteria; when CI is configured, **prefer the CI verdict** (e.g. `[G2 PASS · CI #123]`) instead of rerunning it (see `multica-gate-setup` for the mechanics)
- Producer self-checks do not count as gate evidence; critical commands must be rerun by the gatekeeper

## Verification vs. review

| | Verification | Review |
| --- | --- | --- |
| Question | Is the artifact valid? Is there evidence? | Is the solution/change acceptable from a business/professional perspective? |
| Decision | Objective: command output, item-by-item mapping | Judgment: business intent, risk, maintainability |
| Executor | Leader (multica-verification skill) / CI | Reviewer (independent role) / Human |

Verification can be standardized as a Skill and automated; review needs an independent business/professional perspective.

## Two layers: generic gate + specialist artifact review

`software-development` has **one generic gate layer** (Leader reruns multica-verification at G1/G2/G3). `software-development-reviewed` adds a **second layer: specialist artifact review**, forming "generic gate + professional review" with different standards, triggers, and purposes.

### Why two layers?

The generic gate answers **"is it correct?"**: does the artifact satisfy acceptance criteria and has the process been completed? It does not judge professional depth. But that is not enough: a frontend implementation can satisfy AC while its unit tests are ineffective; a test report can pass acceptance while covering low-risk paths and missing critical branches. These **professional quality issues** need independent domain reviewers.

Specialist artifact review answers **"is it professional?"**: it analyzes the artifact using requirements, upstream artifacts, and domain materials (design quality, unit-test adequacy, case/coverage depth).

### Fixed order

```text
Producer completes artifact
  → Layer 1 generic gate (Leader): multica-verification reruns acceptance/process checks (correctness)
  → if PASS:
      Layer 2 specialist review (dedicated Reviewer): multica-review-* (professional quality)
        → if PASS: release artifact and advance
        → if FAIL: Reviewer reports conclusion + fix list to Leader
             → Leader assigns producer to fix
             → same dedicated Reviewer re-reviews
             → max 3 rounds; escalate to human after round 3
  → if FAIL: return to producer; count generic-gate failures (escalate after 3)
```

Either layer can block release. Review-round and generic-gate failure counts are independent, but both share the 3-attempt escalation threshold.

### Specialist Reviewer mapping (reviewed)

| Producer | Dedicated Reviewer | Review Skill | Focus |
| --- | --- | --- | --- |
| @ProductManager (PRD) | @ProductReviewer | multica-review-product | scope/goals/AC clarity and completeness |
| @Architect (design) | @ArchReviewer | multica-review-architect | architecture, extensibility, alignment, technical risk |
| @Designer (UI) | @DesignReviewer | multica-review-designer | interaction, accessibility, design-system/acceptance alignment |
| @FrontendDev | @FrontendReviewer | multica-review-frontend | UI/API contract fit, component quality, unit-test adequacy |
| @BackendDev (implementation + API contract) | @BackendReviewer | multica-review-backend | contract quality, design fit, error handling, unit-test adequacy |
| @Tester (cases / report) | @TestReviewer | multica-review-test | coverage depth, report quality, item-by-item acceptance mapping |

> Leader and DevOps have **no** dedicated Reviewer: Leader is the orchestrator and must not be both generic gatekeeper and specialist reviewer; DevOps produces deployment evidence already covered by the CI hard gate. All other regular producer roles are covered.

### Three hard constraints

1. **Dedicated Reviewers do not modify the producer's artifact**: they output conclusions + fix lists and report to Leader; Leader assigns the producer to fix. This separates review authority from modification authority.
2. **Leader cannot replace the generic gate with a specialist review**: the generic gate is always rerun by Leader via multica-verification; a Reviewer PASS never substitutes for it.
3. **Reviewer and producer must be independent**: re-review of the same artifact uses the same dedicated Reviewer for continuity; producers cannot review themselves, and Leader must not act as both generic gatekeeper and specialist reviewer.

## What counts as evidence

"Done" has no evidentiary value. Valuable evidence:

- List of changed files (git diff summary)
- Commands actually executed + full output
- Item-by-item mapping to acceptance criteria (each criterion → the test or check covering it)
- Test / check results
- Known limitations and risks

## How to prevent author self-certification

The rule is simple: **don't let the person who did the work judge whether the work is acceptable.**

- Implementers don't pass themselves
- Gatekeeping is done by the Leader rerunning the multica-verification skill (or citing the CI verdict), not by citing the implementer's description
- The gatekeeper personally reruns the automated verification output

## Soft gates vs. hard gates

LLM instructions are guidance, not a safety boundary. **Rules that must be obeyed live outside the LLM:**

```text
Tests / Lint / Build / CI / branch protection / PR approval
```

- **Soft gate**: Leader gatekeeps inside the Squad with multica-verification (G1–G3), constrained by instructions and evidence — useful when starting, without CI, or during exploration.
- **Hard gate**: unforgeable checks produced by CI (templates and practices live in `multica-gate-setup`). If a critical check can be enforced in CI, enforce it there.

Soft and hard gates are two execution environments of the same verification function. Don't rely on "the agent was asked not to do this."

## Full walkthrough

Using "add a CSV export feature" as an example:

1. **G0**: The Issue states acceptance criteria, e.g. "after calling the export API, the returned CSV contains all filtered results."
2. **G1**: Architect gives a minimal-change plan. Leader verifies that the plan covers the acceptance criteria; Reviewer checks business acceptability.
3. **Implementation**: Frontend / BackendDev (per Issue scope) submit code + unit tests + changed-file list + verification output (self-check).
4. **G2**: Leader prefers the CI verdict; if there is no CI, Leader reruns verification commands and checks the diff. PASS.
5. **G2.5**: @DevOps, after G2 PASS and code push, triggers CI/CD, builds and deploys to the test environment, and returns the environment URL. Leader verifies the CI evidence. **If there is no @DevOps or no triggerable CI/CD, G2.5 remains BLOCKED and T3 is forbidden.**
6. **G3**: Tester creates cases with multica-test-design. **T3 automation may start only after G2.5 is PASS and real deployment evidence tied to the current commit exists.** Then multica-test-automation runs against the deployed environment, verifies "filter → export → inspect CSV content," and produces the report; Leader checks item-by-item coverage.
7. **G4**: Human reviews the evidence and decides whether to merge / ship.

If any G2/G3 FAILs, the task returns to the responsible implementer and **previous gate conclusions are void — they must be rerun.** More generally: **once any artifact is modified, its downstream gates become invalid immediately and must be re-judged.** Design, API contract, or test-case changes invalidate downstream implementation/testing/acceptance gates too. N/A must be explicit, justified, and confirmed by Leader; an unconfirmed N/A is a scope gap.

### Gate verdict values

Use four final gate values:

- **APPROVED**: the artifact stands; downstream may open.
- **APPROVED_NA**: Leader confirms the artifact is out of scope; no artifact is produced and the downstream follows the explicit N/A route.
- **REJECTED**: return to the producer with blocking issue, evidence location, owner, and verifiable pass condition.
- **BLOCKED**: waiting on missing information/environment/dependency; never treated as a pass.

### Join gates

Parallel branches may join only when all applicable gates are `APPROVED` or explicitly Leader-confirmed `APPROVED_NA`. Any `REJECTED` / `BLOCKED` blocks the join.

### Verdict mapping

Specialist Review Skills report check results; they do not directly issue the Leader's final gate verdict:

- Review `PASS` → after Leader confirms applicability and evidence, may become `APPROVED`
- Review `N/A` → becomes `APPROVED_NA` only after explicit Leader confirmation
- Review `FAIL` → artifact cannot be released; Leader should issue `REJECTED`
- Missing critical evidence / unavailable environment → Leader should issue `BLOCKED`
