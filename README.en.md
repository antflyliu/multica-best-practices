# Multica Best Practices

[中文](./README.md) | English

> Practical Agent · Squad · Skill · Issue templates for [Multica](https://github.com/multica-ai/multica).
> **Copy. Paste. Run.**

Multica is powerful, but the first run can be surprisingly hard:

- What should go into Instructions?
- Does this rule belong in Agent Instructions or Squad Instructions?
- What does the Leader do? How do members hand off work?
- What should an Issue contain?
- How do you stop agents from skipping steps?
- How do verification and testing divide the work?

This repo gives you ready-to-reuse practices that continue to be validated on real tasks.

## What this is

In one sentence: **a set of Multica squad configurations continuously refined through real tasks** — each agent owns one thing, the Leader owns orchestration and gatekeeping, and every step must produce evidence.

```text
You create: Agents (roles) + Squad (orchestration) + Skills (practices) + Issue (task)
                  ↓
       Leader runs the squad: design → implement → test
                  ↓
   Gate each step (rerun via the multica-verification skill) → Human final acceptance
```

## 5-minute quick start

### Prerequisites

A **Multica environment** where you can create Agents / Squads / Skills / Issues.
Don't have one yet? Read the [Multica docs](https://www.multica.ai/docs) or [How Multica works](https://www.multica.ai/docs/how-multica-works) (3 minutes).

### Copy the software-development Starter

👉 **[`templates/en_US/squad/software-development/README.md`](./templates/en_US/squad/software-development/README.md)**

You get:

- 1 Squad Leader (orchestration + gatekeeping)
- 6 Agents: Architect / Designer / FrontendDev / BackendDev / Tester / Reviewer
- 6 Skills (`multica-verification` is the mandatory gatekeeping Skill)
- 1 Issue template (with the "affected ends" scope declaration)
- 1 software-development workflow (conditional routing where any role can be missing)

### Step 1 — Create Agents

In Multica, create 5 Agents (naming follows [`docs/en_US/naming-conventions.md`](./docs/en_US/naming-conventions.md)) and copy the code block from the matching file under [`templates/en_US/agents/`](./templates/en_US/agents/) into each Agent's Instructions:

| Agent | Copy |
| --- | --- |
| Architect | `architect.md` |
| FrontendDev | `frontend-developer.md` |
| BackendDev | `backend-developer.md` |
| Tester | `tester.md` |
| Reviewer | `reviewer.md` |

> `leader.md` does not need a separate Agent: Squad Instructions only inject the Leader, and `squad.md` is its behavior config.

### Step 2 — Create Skills

In Multica, create 6 Skills, copying the code block from the matching `SKILL.md`:

| Skill | Source | Mount to |
| --- | --- | --- |
| `multica-verification` (gatekeeping, required) | [`templates/en_US/skills/multica-verification/SKILL.md`](./templates/en_US/skills/multica-verification/SKILL.md) | **Leader** |
| `multica-gate-setup` | [`templates/en_US/skills/multica-gate-setup/SKILL.md`](./templates/en_US/skills/multica-gate-setup/SKILL.md) | Leader (when integrating CI hard gates) |
| `multica-test-design` | [`templates/en_US/skills/multica-test-design/SKILL.md`](./templates/en_US/skills/multica-test-design/SKILL.md) | Tester |
| `multica-requirement-analysis` | [`templates/en_US/skills/multica-requirement-analysis/SKILL.md`](./templates/en_US/skills/multica-requirement-analysis/SKILL.md) | Leader / Architect |
| `multica-technical-design` | [`templates/en_US/skills/multica-technical-design/SKILL.md`](./templates/en_US/skills/multica-technical-design/SKILL.md) | Architect |
| `multica-implementation` | [`templates/en_US/skills/multica-implementation/SKILL.md`](./templates/en_US/skills/multica-implementation/SKILL.md) | FrontendDev / BackendDev |

> All 6 Skills are shared under `templates/en_US/skills/` with the unified `multica-` prefix namespace (`multica-verification` is the gatekeeper and is also used by Bug Fix; `multica-gate-setup` installs CI hard gates into a repo and lets gatekeeping read the CI verdict; `multica-test-design` has the Tester generate cases and test reports). Skills mount **by name** — whoever needs one writes "use the xxx skill" in their Instructions, independent of repo paths.

### Step 3 — Create the Squad

Create a Squad and copy `templates/en_US/squad/software-development/squad.md` into the Squad Instructions.

### Step 4 — Create the Issue

Copy `templates/en_US/squad/software-development/issue.md` into a new Issue and fill in your requirement.

### Step 5 — Assign

Assign the Issue to this Squad.

### Step 6 — Run

During implementation, dispatch API test cases in parallel as soon as the API contract is ready; the test report follows the relevant implementation and API-test gates.

```text
Issue → [Design] → [API contract ∥ feature cases] → [Frontend ∥ Backend implementation] → [Testing] → Human
```

The Leader gatekeeps every artifact with the multica-verification skill; only PASS moves to the next stage. Roles outside the scope are skipped; design and critical changes get a business review from the Reviewer.
That's it. Run one real requirement, then tune it to your team.

## Agent Matrix

| Agent | Should do | Should NOT do |
| --- | --- | --- |
| Architect | Design the solution | Write lots of code |
| FrontendDev | Frontend implementation (works with the UI design) | Change requirements / self-approve / invent APIs |
| BackendDev | Backend implementation + API contract | Change requirements / self-approve / touch UI |
| Tester | Feature cases / API test cases / verify acceptance criteria | Change requirements |
| Reviewer | Business review (design / critical changes) | Replace objective verification / replace human acceptance |
| Leader | Orchestration and gatekeeping (multica-verification skill) | Implement personally / rubber-stamp itself |

## Where does an instruction go?

| I want to tell the agent… | Put it in |
| --- | --- |
| "What we're doing this time" | Issue |
| "What background does this project have" | Project Instructions |
| "What role are you" | Agent Instructions |
| "Who is responsible for what" | Squad Instructions |
| "How to do a certain kind of check" | Skill |
| "Tests must pass" | CI (engineering system) |
| "Who decides what ships" | Human |

```text
Issue   = What are we doing?
Project = What should we know?
Agent   = What is my job?
Squad   = Who does what?
Skill   = How do I do it?
CI / PR = What must actually pass?
```

## Principles

1. Keep agent responsibilities narrow.
2. Don't copy routing logic into every Agent.
3. Let the Squad Leader do the coordination.
4. Never let the completer approve their own work (the gatekeeping action is standardized as the multica-verification skill, executed by the non-producing Leader or CI).
5. Require evidence instead of a verbal "it's done".
6. Don't use natural-language instructions as hard constraints.
7. Try a simple flow before a complex multi-agent one.
8. Retry on transient failures.
9. Restart a new session on wrong direction; don't push through.
10. Keep human approval at important irreversible boundaries.

> **Instructions are guidance, not a safety boundary.** Rules that must be obeyed live outside the LLM: tests, lint, build, CI, branch protection, PR approval. Don't rely on "the agent was asked not to do this."

## Starters

| Starter | Use | Status |
| --- | --- | --- |
| [Software Development](./templates/en_US/squad/software-development/README.md) | Regular feature development (frontend/backend routed by scope; any role can be missing) | Recommended |
| [Bug Fix](./templates/en_US/squad/bug-fix/README.md) | Root cause / fix / regression (routed by impact, skips Architect) | Experimental |

More starters (Technical Research, etc.) will be added after being validated on real tasks. **Don't pretend best practices are finished.**

## Repository structure

```text
AGENTS.md     ⭐ Agent entry: project conventions and change rules
templates/  ⭐ Start here: all copy-paste-ready configs
├── zh_CN/                Chinese templates (default; copy the whole subdirectory and run)
│   ├── agents/            Shared Agent Instructions (6 role definitions)
│   ├── skills/            Shared Skills (6, unified multica- prefix: gatekeeping / CI integration / test design / requirement analysis / technical design / implementation)
│   │   └── multica-gate-setup/  CI hard-gate templates ship inside this Skill (delivery-gate.yml, etc.)
│   └── squad/             Squad starters
│       ├── software-development/  Regular development (squad / issue / README incl. workflow)
│       └── bug-fix/              Minimal fix combination (only the orchestration changes)
└── en_US/                English templates (same structure as zh_CN/)
docs/          ⭐ Read first: where instructions go / gates & evidence / common mistakes / adapt & scale
├── zh_CN/                Chinese methodology
└── en_US/                English methodology
```

Details:

| Doc | Content |
| --- | --- |
| [where-to-put-things](docs/en_US/where-to-put-things.md) | Where instructions belong — cheat sheet (most worth reading) |
| [artifact-conventions](docs/en_US/artifact-conventions.md) | Collaboration artifact landing: where each stage artifact goes, how downstream reads it |
| [gates-and-evidence](docs/en_US/gates-and-evidence.md) | Gates G0–G4 and evidence requirements |
| [common-mistakes](docs/en_US/common-mistakes.md) | Bad → Good examples |
| [adapt-and-scale](docs/en_US/adapt-and-scale.md) | Cut down, extend, pilot, roll out |
| [naming-conventions](docs/en_US/naming-conventions.md) | Agent naming rules (role + project + member-id) |

## Relationship to related projects

| Project | Relationship |
| --- | --- |
| [Multica](https://github.com/multica-ai/multica) | The runtime and collaboration foundation (Issue, Agent, Squad, Runtime) |
| [multica-agent-workflow-template](https://github.com/wksudud/multica-agent-workflow-template) | Methodology on Agent/Skill count and routing design; can be used together |
| [oh-my-multica](https://github.com/xiaohei-info/oh-my-multica) | Production-grade deterministic DAG / Loop; this repo focuses on the Squad and gate-convention layer |

## Contributing

Please don't submit "sounds nice" prompts. A valuable contribution includes:

1. The problem it solves
2. The scenarios it fits
3. The complete template
4. At least one real example
5. Known failure cases

Real-world experience is worth more than prompt complexity. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Resources

- [Multica GitHub](https://github.com/multica-ai/multica)
- [Multica docs](https://www.multica.ai/docs)
- [How Multica works](https://www.multica.ai/docs/how-multica-works)
- [Agents](https://www.multica.ai/docs/agents)
- [Squads](https://www.multica.ai/docs/squads)
- [Tasks](https://www.multica.ai/docs/tasks)

## Security

Read [SECURITY.md](SECURITY.md) before sharing configs: never upload tokens, absolute paths, or real workspaces / emails.

## License

[MIT](LICENSE)
