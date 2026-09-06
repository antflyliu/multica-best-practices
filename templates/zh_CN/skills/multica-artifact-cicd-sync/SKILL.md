---
name: multica-artifact-cicd-sync
description: CI/CD 产物编排：G2 PASS 且代码已 push 后调用 multica-platform-jenkins 触发 dev/sit 构建，回写 JIRA 并回传部署 URL。Python 实现，Windows / Linux 通用。
metadata:
  orchestrates:
    - multica-platform-jenkins
    - multica-platform-jira
  runtime:
    python: ">=3.10"
---

# Artifact · CI/CD Sync（编排）

## Purpose

G2 PASS + push 后，调用 `multica-platform-jenkins` 触发 dev/sit Job。**参数由 Jenkins API 自动发现**，编排层不硬编码参数名。

## Agent 流程

```text
1. discover-only（推荐先跑，检查 missing）：
   python scripts/trigger_cicd.py --issue <ISSUE_KEY> --env sit --branch release/<ISSUE_KEY>-slug --discover-only --json
2. 触发（**只用 Issue deploy branch，不用 feature 分支**）：
   python scripts/trigger_cicd.py --issue <ISSUE_KEY> --env sit --branch release/<ISSUE_KEY>-slug --json
3. missing 参数：追加 --param name=value（trigger_cicd 需扩展传参时走 trigger_env --param）
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
  --issue <ISSUE_KEY> \
  --env dev \
  --service <service> \
  --branch release/<ISSUE_KEY>-slug \
  --json
```

## Workflow B：sit 部署（G2.5 → Tester T3）

```bash
python scripts/trigger_cicd.py \
  --issue <ISSUE_KEY> \
  --env sit \
  --branch release/<ISSUE_KEY>-slug \
  --json
```

`<ISSUE_PREFIX_A>` / `<ISSUE_PREFIX_B>` / `<ISSUE_PREFIX_C>` / `<ISSUE_PREFIX_D>` 等前缀已在 `config.yaml` → `issue_service_map` 配置，可省略 `--service`。

## Workflow C：多服务

```bash
python scripts/trigger_cicd.py --env sit --service <service1>,<service2> --branch release/<ISSUE_KEY>-xxx --json
```

## 用法（角色侧）

```text
G2 PASS 且代码已 push 后，用 multica-artifact-cicd-sync 触发 Jenkins 并回传部署链接。
```

## 平台不可用时的降级路径

1. 先执行一次 discover / trigger；确认 CI/CD 平台不可用后停止重复触发。
2. 将 G2.5 标记为 `BLOCKED`，记录平台、Job / 环境、尝试的操作、时间 / 错误信息，以及缺失的 build URL / deploy URL / build ID。
3. 不得伪造构建、部署或环境 URL；旧构建、旧部署或本地命令输出不能冒充当前 commit 的 G2.5 证据。
4. CI/CD 不可用时，**不得放行 T3**。只有真实测试环境部署证据使 G2.5 PASS 后，Tester 才能执行部署环境 T3；否则流程停在 G2.5 `BLOCKED`。
5. 平台恢复并产生当前 deploy branch / commit 对应的构建部署证据后，Leader 重新判 G2.5。若代码、部署产物或关联引用发生修改，其下游门禁立即失效，必须重新验证。

## 为什么有效

编排层只依赖 Python；Issue 前缀自动映射到 `jobs-catalog.yaml` 中的 logical service。



