---
name: multica-platform-jenkins
description: "Platform-layer skill (placeholder shell): read/write capability for CI/CD systems (Jenkins-class) — trigger parameterized builds, poll status, fetch console logs. Parameters are auto-discovered; never hardcode. Credentials injected via runtime env. Concrete CI URL / Job list in config.yaml, never in role prompts."
metadata:
  layer: platform
  replaces: any CI/CD system (Jenkins / GitLab CI / GitHub Actions / self-hosted pipeline / etc.)
  runtime:
    python: ">=3.10"
---

# Platform · Jenkins (placeholder shell)

> This is a **platform-layer placeholder shell**. The public multica-best-practices binds to no specific company's internal URLs or credentials.
> To onboard your own CI/CD platform, only edit this skill's `config.yaml` and `scripts/`; all upstream roles and orchestration skills stay untouched.

## Purpose

Provide **read + write** capability for CI/CD systems:

- **Read**: discover jobs, parameters, build status, console output and artifacts.
- **Write**: trigger parameterized builds and return a stable build identifier / URL.

Concrete CI endpoints and job mappings belong in `config.yaml`; credentials are injected at runtime and never embedded in role prompts.

## Files (suggested structure)

```text
multica-platform-jenkins/
├── SKILL.md
├── config.yaml
├── .env.example
└── scripts/
    ├── credentials.py
    ├── discover_jobs.py
    ├── trigger_env.py
    ├── poll_build.py
    ├── promote_prod.py
    └── validate.py
```

## Read

Use the supplied scripts to discover the target job, inspect parameters, poll build state and fetch console evidence. Do not hardcode job names or parameters in Agent Instructions.

## Write

Trigger only the job and parameters resolved from the team configuration. Return the build identifier and stable URL when the platform provides one.

## Success criteria

- Discovery returns the intended job and supported parameters.
- Trigger operations return a build identifier and/or stable build URL.
- Polling confirms the final build result from the target CI system.
- Console/log evidence can be retrieved and tied to the same build.
- On failure, scripts exit non-zero with diagnosable output; never fabricate build IDs, URLs, or PASS results.

## Agent Compatibility

- Credentials are injected through runtime environment variables; never print secrets or place them in role prompts.
- Platform-specific URLs, job names, parameters and tokens belong in `config.yaml` / runtime environment only.
- Prefer the supplied `scripts/`; do not call REST APIs directly from role prompts.

## Adapting To A New Team

1. Edit `config.yaml` with the team's placeholder-safe CI settings.
2. Provide runtime credentials through the environment.
3. Run `scripts/validate.py` before using the shell in a real environment.

## Why it works

CI/CD details vary by team; isolating them in a platform skill keeps Agent Instructions stable while allowing Jenkins or another CI provider to be swapped behind the same artifact-orchestration contract.
