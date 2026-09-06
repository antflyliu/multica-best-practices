---
name: multica-platform-jenkins
description: CI/CD platform adapter: trigger parameterized builds, poll status, read build logs, and return deployment evidence. Concrete URLs, Jobs, and credentials are runtime configuration, never Agent Instructions.
category: platform
owner: Platform Adapter
version: 1.0
inputs:
  - environment
  - service
  - deploy_branch
  - optional_parameters
outputs:
  - build_status
  - build_urls
  - deployment_version
side_effects:
  - triggers CI/CD builds
requires:
  - multica-artifact-cicd-sync
forbidden:
  - hardcode platform URL or credentials in Agent Instructions
  - make Gate PASS/FAIL decisions
idempotent: false
platform_dependent: true
---

# Platform · Jenkins

## Purpose

Provide CI/CD read/write capability: trigger Jobs, poll builds, read `consoleText`, and return build URLs plus deployment version.

> This is the platform adapter layer. Concrete Jenkins URL, Job names, accounts, and tokens live only in `config.yaml` / runtime environment / secret store. Upstream Agents, Squads, and methodology skills must not carry these details.

## Standard flow

```text
1. Resolve service + deploy branch
2. discover (required) — read parameters from the target Job, reusing lastSuccessfulBuild params where appropriate
3. ready=false → fill missing parameters; if they cannot be resolved, BLOCKED
4. trigger → poll → return build/deployment evidence
```

**Parameter priority**: `--param` > branch hint > last SUCCESS build params > platform default.

## Files

```text
multica-platform-jenkins/
├── SKILL.md
├── config.yaml
├── jobs-catalog.yaml
├── reference.md
├── .env.example
└── scripts/
    ├── trigger_env.py
    ├── list_jobs.py
    ├── jenkins_cli.py
    └── lib/
```

## Runtime configuration

- `config.yaml`: CI/CD base URL, environments, and logical service → Job mapping.
- `.env` / secret store: runtime accounts, tokens, and other secrets.
- `jobs-catalog.yaml`: logical service-to-Job mapping; do not copy it into Agent Instructions.

Use one credential naming convention. Prefer `JENKINS_USER` / `JENKINS_PASSWORD` or the organization's standard token variables; do not mix unrelated `ATLASSIAN_*` and `JENKINS_*` names.

## Discover

```bash
python scripts/jenkins_cli.py discover-params --env sit --service <service> --branch release/<ISSUE-KEY>-<slug> --json
```

Discover first, then trigger; Agents must not hardcode parameters such as `branchName`.

## Trigger

```bash
python scripts/trigger_env.py --env sit --service <service> --branch release/<ISSUE-KEY>-<slug> --json
python scripts/trigger_env.py --env sit --service <service> --branch release/<ISSUE-KEY>-<slug> --param deployVersion=<VERSION> --json
```

## Success criteria

- script exit code `0`
- target build returns `SUCCESS`
- return a traceable build URL
- when deployment produces an artifact, return stable `deployment_version`

> Platform success is not G2.5 PASS. G2.5 is independently decided by the Leader using `multica-verification`.

## Relationship to orchestration

`multica-artifact-cicd-sync` owns workflow orchestration; this skill owns platform execution and evidence return. After execution, return deployment version/evidence to the orchestration layer, then let the Leader decide G2.5.
