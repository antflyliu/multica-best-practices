---
name: multica-platform-jenkins
description: CI/CD 平台适配层：触发带参构建、轮询状态、读取构建日志并回传部署信息。具体 URL、Job、凭据只从运行时配置注入，不写入 Agent Instructions。
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

提供 CI/CD 平台的读写能力：触发 Job、轮询构建、读取 `consoleText`、回传构建 URL 与部署版本。

> 这是平台适配层。具体 Jenkins URL、Job 名、账号和 token 只存在于 `config.yaml` / runtime environment / secret store；上游 Agent、Squad、methodology skill 不携带这些细节。

## Agent 标准流程

```text
1. 解析 service + deploy branch
2. discover（必做）— 从目标 Job 获取参数，并优先复用 lastSuccessfulBuild 参数
3. ready=false → 补齐缺失参数；无法补齐则 BLOCKED
4. trigger → poll → return build/deployment evidence
```

**参数优先级**：`--param` > branch hint > last SUCCESS build params > platform default。

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

## 运行时配置

- `config.yaml`：CI/CD base URL、环境与 logical service → Job 映射。
- `.env` / secret store：运行时账号、token 等敏感凭据。
- `jobs-catalog.yaml`：服务与 Job 的逻辑映射，不应被 Agent Instructions 复制。

凭据命名应保持单一规范；推荐使用 `JENKINS_USER` / `JENKINS_PASSWORD` 或组织统一的 token 变量，避免 `ATLASSIAN_*` 与 `JENKINS_*` 混用造成歧义。

## Discover

```bash
python scripts/jenkins_cli.py discover-params --env sit --service <service> --branch release/<ISSUE_KEY>-<slug> --json
```

发现参数后再触发，不在 Agent 中硬编码 `branchName` 等具体参数名。

## Trigger

```bash
python scripts/trigger_env.py --env sit --service <service> --branch release/<ISSUE_KEY>-<slug> --json
python scripts/trigger_env.py --env sit --service <service> --branch release/<ISSUE_KEY>-<slug> --param deployVersion=<VERSION> --json
```

## 成功标准

- 脚本 exit code `0`
- 目标 build 返回 `SUCCESS`
- 回传可追踪的 build URL
- 如产生部署产物，回传稳定的 `deployment_version`

> 本 skill 的 SUCCESS 只描述平台调用结果，不等于 G2.5 PASS。G2.5 由 Leader 使用 `multica-verification` 独立判定。

## 与编排层关系

`multica-artifact-cicd-sync` 负责流程编排；本 skill 只负责平台执行与证据回传。平台执行完成后，必须把 deployment version/evidence 交回编排层，由 Leader 决定 G2.5。
