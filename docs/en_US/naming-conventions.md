# Naming Convention: Role + Name

> Purpose: one role definition can be instantiated as multiple Agents, distinguished by name instead of edited instructions — so the flow stays reusable.

## Rules

1. Agent name = `<role>-<instance>`, where the role comes from a fixed vocabulary.
2. Role vocabulary: `Leader / Architect / FrontendDev / BackendDev / Tester / Reviewer`
3. `<instance>` = domain / service / project name (lowercase hyphenated), e.g. `user-service`, `web`, `order`.
4. The name only distinguishes instances; it carries no responsibility. Responsibilities always come from Agent Instructions / Squad Instructions.

## Examples

| Role | Example name | Meaning |
| --- | --- | --- |
| BackendDev | `BackendDev-user-service` | User-service backend |
| FrontendDev | `FrontendDev-web` | Web frontend |
| Tester | `Tester-order` | Order-domain testing |
| Architect | `Architect-core` | Core architecture design |
| Leader | `Leader-core` | Core squad Leader |

## Why

- In Multica, Agent names must be unique; multiple instances of the same role are the norm (multi-service / multi-domain), so names must be distinguishable.
- The role is in the name, so `@mention` routing is readable and unambiguous — `@BackendDev-user-service` tells you who it is at a glance.
- **Changing the name doesn't change behavior; changing behavior means editing Instructions, not the name**: switching instances only changes `<instance>`, and the template is reused as-is.
- Naming is the last piece that makes "reusable flows" work: the same `squad.md`, with a different set of instance names, is a brand-new squad.
