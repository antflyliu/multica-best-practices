---
name: multica-artifact-cicd-sync
description: "CI/CD 产物编排：在 G2 PASS 且代码已 push 后调用平台适配层执行部署，回传 deployment version 与证据。编排层不拥有 G2.5/G3 Gate。"
category: orchestration
owner: Leader
version: 1.0
inputs:
  - issue
  - g2_result
  - commit_or_artifact_version
  - environment
  - deploy_branch
outputs:
  - deployment_version
  - deployment_evidence
  - deployment_url
side_effects:
  - triggers deployment through platform adapter
requires:
  - multica-verification
  - multica-platform-jenkins
forbidden:
  - trigger T3 before G2.5 PASS
  - make G2.5 or G3 PASS decisions
  - hardcode platform credentials or URLs
idempotent: false
platform_dependent: true
---

# Artifact · CI/CD Sync（编排）

## Purpose

在 **G2 PASS + code push** 后编排 CI/CD 部署，调用 `multica-platform-*` 适配层，并回传部署产物版本与证据。

> 本 skill 负责“怎么编排部署”，不负责“判 G2.5”。G2.5 必须由 Leader 使用 `multica-verification` 独立判定。

## Preconditions

必须同时满足：

- G2 = `PASS`
- G2 PASS 绑定的 Artifact Version / commit 未发生变化
- deploy branch 已由 Issue 明确
- 所需 platform adapter 可用

任一条件不满足 → `BLOCKED`，不得触发后续 T3。

## Workflow

```text
G2 PASS
  ↓
code push / artifact version fixed
  ↓
multica-artifact-cicd-sync
  ↓
multica-platform-* discover → trigger → poll
  ↓
deployment_version + evidence
  ↓
Leader / multica-verification 判定 G2.5
  ↓
G2.5 PASS
  ↓
允许 Tester 触发 T3
```

## Workflow A：dev

```bash
python scripts/trigger_cicd.py \
  --issue <ISSUE_KEY> \
  --env dev \
  --service <service> \
  --branch release/<ISSUE_KEY>-slug \
  --json
```

## Workflow B：sit

```bash
python scripts/trigger_cicd.py \
  --issue <ISSUE_KEY> \
  --env sit \
  --branch release/<ISSUE_KEY>-slug \
  --json
```

## Workflow C：多服务

```bash
python scripts/trigger_cicd.py --env sit --service <service1>,<service2> --branch release/<ISSUE_KEY>-xxx --json
```

## Parameter policy

平台参数由 `multica-platform-*` 适配层 discover；编排层不硬编码 Job 参数名。

- deploy branch 只能来自 Issue / 已确认的部署上下文
- 缺少必填参数 → 补齐或 `BLOCKED`
- platform build SUCCESS → 只是平台执行成功，不自动等价于 G2.5 PASS

## Artifact Contract

成功部署后至少回传：

```yaml
artifact:
  type: deployment
  issue_key: <ISSUE_KEY>
  version: <DEPLOYED_VERSION>
  location:
    type: cicd
    url: <DEPLOY_URL>
  source:
    commit: <COMMIT_SHA>
  status: deployed
```

`<DEPLOYED_VERSION>` 必须能唯一对应实际部署内容。若部署后产物版本变化，下游 Gate 立即失效并重新验证。

## T3 Boundary

本 skill **不能直接触发 T3**。只有 Leader 判定 `G2.5 = PASS` 后，Tester 才能使用 `multica-test-automation` 执行 T3。

## Why it works

平台差异被封装在 `multica-platform-*`；编排只处理 Issue、版本、环境和证据。这样更换 Jenkins / GitLab CI / GitHub Actions 时，不需要修改 Agent Instructions 或 Gate 逻辑。
