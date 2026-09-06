---
name: multica-manage-skills
description: Multica platform management and usage adapter: query workspaces, agents, and runtime statistics. Platform-only capability; it does not participate in delivery Gates.
category: platform
owner: Platform Adapter
version: 1.0
inputs:
  - api_url
  - api_token
  - optional_workspace
outputs:
  - workspace_data
  - agent_data
  - usage_report
side_effects: []
requires: []
forbidden:
  - embed real API URL or token in Agent Instructions
  - make Gate PASS/FAIL decisions
  - modify business artifacts
idempotent: true
platform_dependent: true
---

# Platform · Multica Management

## Purpose

Provide Multica platform management and usage queries, such as workspace lists, agent lists, run counts, 30-day activity details, and summary reports.

> This is a platform adapter, not a methodology skill. Real API URLs, tokens, workspace identifiers, and authentication data are injected only at runtime through arguments, environment variables, or a secret store.

## Authentication & Configuration

- API URL: runtime `--url`, then `MULTICA_API_URL`.
- Token: runtime `--token`, then `MULTICA_API_TOKEN`.
- Workspace: runtime `--workspace`.
- Never put real URLs, tokens, accounts, or secrets into Agent Instructions, Squad definitions, or methodology skills.

If API endpoints, headers, or authentication mechanisms differ in a deployment, follow that deployment's Multica official documentation / service contract. This best-practices repository does not invent platform API details.

## CLI Examples

```bash
python scripts/multica_api.py workspaces
python scripts/multica_api.py agents --workspace <workspace-slug>
python scripts/multica_api.py run-counts --workspace <workspace-slug> --json
python scripts/multica_api.py activity --workspace <workspace-slug>
python scripts/multica_api.py report
python scripts/multica_api.py report --workspace <workspace-slug> --json
```

## Boundary

```text
Agent / Operator request
        ↓
multica-manage-skills
        ↓
Multica platform API
        ↓
management / usage evidence
```

This skill may read platform data, but must not:

- modify PRD / Design / API / Code / Test business artifacts
- replace Reviewer professional judgment
- replace the Leader's `multica-verification` Gate execution
- interpret successful platform queries as any Gate PASS

## Resources

- `scripts/multica_api.py` — platform query CLI / client
- `references/api_reference.md` — deployment-specific API contract

If the platform contract is unavailable or conflicts with the local script, stop guessing and consult the official documentation or the deployment owner.
