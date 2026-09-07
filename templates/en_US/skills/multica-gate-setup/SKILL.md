---
name: multica-gate-setup
description: Integrate CI hard gates into the target repository and let gatekeeping consume CI evidence. Used for deploying gates, reading check-runs for G2, and falling back to soft gates when CI is unavailable.
---

# Gate Setup (CI gate integration)

## What this is

An integration Skill that upgrades "verification" from agent self-discipline to machine-executed CI evidence.
Core idea (`multica-gatekit`): **the gate issuer must be a different party from the gated** — authors can't stamp "tests passed" on themselves; CI's actual run results are evidence, while the Leader is the only formal gate verifier.

This Skill answers two questions:

1. **How do you install gates into a repository?** (one-time deployment)
2. **How does gatekeeping consume CI evidence?** (G2 on every task)

## Template files it carries

The 3 template files needed for deployment live in the same directory as this SKILL.md (the Skill is self-contained; copy them together with the skill):

| File | Purpose |
| --- | --- |
| `delivery-gate.yml` | CI workflow: runs lint + test + build on PRs and writes a structured gate conclusion |
| `branch-protection.json` | Branch protection rules: require the `delivery-gate` status check to pass + independent approval before merging |
| `apply-branch-protection.sh` | Applies the protection rules to the repo with the `gh` CLI (edit the placeholders, then run) |

Fit: you already have runnable test / lint / build commands; you don't want "Worker self-certifies done" to leave room for cheating; multiple squads in parallel need a unified merge gate.

## Capability prerequisites (route by environment)

The Leader only has the Skill + MCP, no shell. So branch by the runtime environment:

| Capability | Gatekeeping (G2) | Deployment (one-time) |
| --- | --- | --- |
| Has GitHub MCP (read) | **Real integration**: query check-runs and collect CI evidence | — |
| Has GitHub MCP (write) | — | **Real integration**: create the workflow + set branch protection |
| No MCP | **Weak integration**: read CI evidence humans paste into the PR comment | Human runs the script; the Leader verifies the output |

## Deployment flow (one-time)

1. Read the 3 template files in this Skill's directory: `delivery-gate.yml` / `branch-protection.json` / `apply-branch-protection.sh`.
2. Replace the placeholders for the target repository:

| File | Placeholder | Replace with |
| --- | --- | --- |
| `delivery-gate.yml` | `pnpm install --frozen-lockfile` | The repo's real install command |
| | `pnpm lint` / `pnpm test` / `pnpm build` | The repo's real verification commands |
| `branch-protection.json` | `"delivery-gate"` (context) | Keep (unless you renamed the workflow job) |
| | `required_approving_review_count` | Independent approval count (default 1) |
| `apply-branch-protection.sh` | `YOUR_OWNER` | GitHub org / username |
| | `YOUR_REPO` | Repository name |

> This branch-protection API can require an approval count, but it cannot use a team slug to require approval from a specific team. For team-level approval, configure `CODEOWNERS` with required code-owner reviews or use GitHub Rulesets; this template does not create those repository policies automatically.

3. Install into the target repository:
   - **With write-capable MCP**: create `.github/workflows/delivery-gate.yml`; set branch protection with the GitHub API `PUT /repos/{owner}/{repo}/branches/main/protection` (equivalent to the script's action; body from `branch-protection.json`).
   - **Without MCP**: give the human an explicit checklist — copy `delivery-gate.yml` into `.github/workflows/`; edit the placeholders in both files; after `gh auth login` with admin rights, run `bash apply-branch-protection.sh`.
4. Verify it took effect: query the branch protection rules `GET /repos/{owner}/{repo}/branches/main/protection` and confirm `required_status_checks.contexts` contains `delivery-gate`; or have the human paste the script output.

## Gatekeeping flow (G2, every task)

1. Query the PR's check-runs via GitHub MCP: `GET /repos/{owner}/{repo}/commits/{sha}/check-runs`.
2. Find the check named `delivery-gate` and record its completed result as **CI evidence** (`success` / `failure` / `cancelled` / `pending`). Do not turn the CI result directly into the formal gate verdict.
3. The **Leader** runs the formal G2 verification with `multica-verification`, using the current-commit CI evidence plus diff scope as inputs:
   - **Valid completed CI evidence** → verify the evidence is bound to the current commit SHA and the diff is in scope; then issue the formal verdict.
   - **CI missing** → use the soft-gate path in `multica-verification` to perform the required verification.
   - **CI unreachable or evidence cannot be bound to the current commit** → formal verdict is `BLOCKED`.
4. Do not rerun commands already covered by valid CI evidence merely to manufacture another result. The Leader verifies the evidence and scope; `multica-verification` owns the formal verdict vocabulary.

## Formal result

The formal gate result issued by the Leader via `multica-verification` is one of:

**APPROVED** — required evidence is valid and the gate criteria are satisfied.

**APPROVED_NA** — the gate criterion is explicitly not applicable, with the Leader recording the reason.

**REJECTED** — evidence or scope does not satisfy the gate. Must provide: the problem, why it matters, where, the fix direction, and a re-verifiable pass condition.

**BLOCKED** — required evidence or verification capability is unavailable. Report honestly; never turn it into an approval.

`PASS` / `FAIL` may be used for individual checks or CI evidence summaries, but they are not the formal gate verdict.

## Known failure case

A CI check once passed, but the Leader used an old PR comment rather than the check-run for the latest commit and incorrectly marked G2 as passed while the newest build was still pending. The rule is now explicit: bind CI evidence to the current commit SHA and a valid completed check-run; if that evidence cannot be read, return `BLOCKED` rather than substituting an old comment or build.

## Relationship to the multica-verification skill

The two Skills have different responsibilities:

- `multica-verification`: the Leader-owned formal gate verification and verdict issuance.
- `multica-gate-setup`: CI hard-gate deployment and collection of machine-generated evidence for the Leader's verification.

**If it can run in CI, run it in CI**; CI supplies evidence, while the Leader remains the formal gate verifier. They complement each other; CI does not bypass `multica-verification`.

## Why this works

If the gate is only "the agent was asked to check," two kinds of cheating remain: authors pretending they verified, and authors stamping themselves PASS. CI makes the evidence machine-generated, while the Leader remains independent from the producing role and issues the formal verdict through `multica-verification`. This Skill encodes that handoff into the flow — a clear deployment checklist, a commit-bound evidence source, and a clear fallback when CI is unavailable. No improvisation required.
