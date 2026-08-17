# Naming Convention: Role + Name

> Purpose: one role definition can be instantiated as multiple Agents, distinguished by name instead of edited instructions — so the flow stays reusable.

## Rules

1. Agent name = `<role>-<instance>`, where the role comes from a fixed vocabulary.
2. Role vocabulary: `Leader / Architect / Designer / FrontendDev / BackendDev / Tester / Reviewer`
3. `<instance>` = domain / service / project name (lowercase hyphenated), e.g. `user-service`, `web`, `order`.
4. The name only distinguishes instances; it carries no responsibility. Responsibilities always come from Agent Instructions / Squad Instructions.
5. `Architect` is technical architecture design (change plan / files / verification); `Designer` is UI / interaction design (Figma visuals & specs). Different expertise and artifacts — don't merge them.

## Examples

| Role | Example name | Meaning |
| --- | --- | --- |
| BackendDev | `BackendDev-user-service` | User-service backend |
| FrontendDev | `FrontendDev-web` | Web frontend |
| Tester | `Tester-order` | Order-domain testing |
| Architect | `Architect-core` | Core architecture design |
| Designer | `Designer-web` | Web UI / interaction design (Figma) |
| Leader | `Leader-core` | Core squad Leader |

## Squad instance suffix & prefix wildcard

Squad Instructions refer to members by the **role prefix** (`@Architect` / `@FrontendDev` / …), not a hardcoded full Agent name — that's what keeps `squad.md` copy-paste-ready. But a workspace routinely hosts multiple instances of the same role (e.g. `FrontendDev-web`, `FrontendDev-mobile`); the orchestrator must be able to pin the one that belongs to *this* squad. Rules:

1. Each squad declares its **instance suffix** `suffix` (e.g. `payment`, `order`) at startup, bound to all its roles.
2. Wherever the Squad Instructions write `@role`, the orchestrator resolves it to `@role-<squad suffix>` before dispatching the precise @mention.
   - Example: with `suffix = payment`, `@FrontendDev` → actually dispatched to `FrontendDev-payment`, `@Architect` → `Architect-payment`.
3. If a role is out of the squad's scope (the Issue 【Scope】 doesn't include that layer), skip its artifact per the existing rule — don't resolve, don't dispatch.
4. `suffix` is set once in the squad configuration, never written into `squad.md`; `squad.md` always shows only the role prefix, staying copy-paste-ready.

> Thus the "role prefix" is the logical name inside the Squad, and `@role-suffix` is the physical name inside the workspace; the two are bridged by the squad configuration.

## Why

- In Multica, Agent names must be unique; multiple instances of the same role are the norm (multi-service / multi-domain), so names must be distinguishable.
- The role is in the name, so `@mention` routing is readable and unambiguous — `@BackendDev-user-service` tells you who it is at a glance.
- **Changing the name doesn't change behavior; changing behavior means editing Instructions, not the name**: switching instances only changes `<instance>`, and the template is reused as-is.
- Naming is the last piece that makes "reusable flows" work: the same `squad.md`, with a different set of instance names, is a brand-new squad.
- **The prefix wildcard solves "coexisting instances"**: Squad instructions only write the role prefix (reusable); the squad configuration supplies the suffix (locatable). Separating the two keeps reuse intact while still letting the orchestrator dispatch precisely to this squad's members in a crowded workspace.
