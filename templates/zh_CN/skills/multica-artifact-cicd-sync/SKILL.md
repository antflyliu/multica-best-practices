---
name: multica-artifact-cicd-sync
description: CI/CD 产物编排 skill（占位壳）：G2 PASS 且代码已 push 后调用底层 CI/CD 平台 skill 触发 dev/sit 构建，回写 Issue 并回传部署 URL。参数由 CI 系统 API 自动发现，编排层不硬编码参数名。具体平台在 multica-platform-* 层配置。
metadata:
  layer: orchestration
  orchestrates:
    - multica-platform-jenkins
    - multica-platform-jira
  runtime:
    python: ">=3.10"
---

# Artifact · CI/CD Sync（编排，占位壳）

## Purpose

G2 PASS + push 后，调用底层 CI/CD 平台 skill 触发构建部署。**参数由 CI 系统 API 自动发现**，编排层不硬编码参数名。

## Agent 流程

```text
1. discover-only（推荐先跑，检查 missing）：
   python scripts/trigger_cicd.py --issue <ISSUE-KEY> --env sit --branch release/<ISSUE-KEY>-<slug> --discover-only --json
2. 触发（**只用 Issue deploy branch，不用 feature 分支**）：
   python scripts/trigger_cicd.py --issue <ISSUE-KEY> --env sit --branch release/<ISSUE-KEY>-<slug> --json
3. missing 参数：追加 --param name=value
```

## 参数解析策略

默认（`use_last_success=true`）：

1. 读取 `lastSuccessfulBuild` 的全部构建参数
2. **仅**将分支类参数（branchName / branch / gitBranch …）替换为 `--branch`
3. `--param` 可覆盖任意项；`--no-last-success` 关闭此行为

---

## Workflow A：dev 部署

```bash
python scripts/trigger_cicd.py \
  --issue <ISSUE-KEY> \
  --env dev \
  --service <service> \
  --branch release/<ISSUE-KEY>-<slug> \
  --json
```

## Workflow B：sit 部署（G2.5 → Tester T3）

```bash
python scripts/trigger_cicd.py \
  --issue <ISSUE-KEY> \
  --env sit \
  --branch release/<ISSUE-KEY>-<slug> \
  --json
```

Issue 前缀 → logical service 的映射在 `config.yaml` → `issue_service_map` 配置，可省略 `--service`。

## Workflow C：多服务

```bash
python scripts/trigger_cicd.py --env sit --service svc-a,svc-b --branch release/<ISSUE-KEY>-<slug> --json
```

## 用法（角色侧）

```text
G2 PASS 且代码已 push 后，用 multica-artifact-cicd-sync 触发 CI/CD 并回传部署链接。
```

## 为什么有效

编排层只依赖脚本；Issue 前缀自动映射到 `jobs-catalog.yaml` 中的 logical service。底层 CI 系统（Jenkins / GitLab CI / GitHub Actions 等）由 `multica-platform-*` 层封装，本 skill 不感知具体平台。
