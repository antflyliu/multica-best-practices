---
name: multica-platform-jenkins
description: 平台层 skill（占位壳）：CI/CD 系统（Jenkins 类）的读写能力——触发带参构建、轮询状态、取控制台日志。参数自动发现，禁止硬编码。凭据由运行时 env 注入。具体 CI 地址、Job 清单在 config.yaml 配置，不写进角色提示词。
metadata:
  layer: platform
  replaces: 任何 CI/CD 系统（Jenkins / GitLab CI / GitHub Actions / 自建流水线 等）
  runtime:
    python: ">=3.10"
---

# Platform · Jenkins（占位壳）

> 这是一个**平台层占位壳**。公开的 multica-best-practices 不绑定任何具体公司的内网地址与凭据。
> 团队接入自己的 CI/CD 系统时，只改本 skill 的 `config.yaml` 与 `scripts/`，所有上层编排 skill 无需改动。

## Purpose

CI/CD 系统 **读 + 写** 能力：触发 Job、轮询构建、取 `consoleText`、回传构建 URL。

> **参数自动发现**：连 CI 系统 API 读取每个 Job 的必填参数，禁止 Agent 硬编码参数名。

默认 CI 地址在 `config.yaml` → `cicd.base_url` 配置（占位：`http://<your-cicd-host>`）。

## Agent 标准流程（必读）

```text
1. 解析 service（jobs-catalog / issue_service_map）+ **deploy branch**（Issue「Git 分支」区块，非 feature）
2. discover（必做）— 默认从 lastSuccessfulBuild 复制参数，仅覆盖 deploy branch
3. ready=false → 补 missing 参数或 BLOCKED 问人类
4. 触发：multica-artifact-cicd-sync → trigger 脚本
```

**参数优先级**：`--param` > **分支 hint**（branchName 等）> **上次 SUCCESS 构建参数** > CI 默认值

## Files（建议结构）

```text
multica-platform-jenkins/
├── SKILL.md
├── config.yaml
├── jobs-catalog.yaml     # 各 env Job 清单（service → Job 名）
├── .env.example
└── scripts/
    ├── trigger_env.py    # 按 env + service 触发
    ├── list_jobs.py      # 列出 / 查询 Job
    ├── cicd_cli.py       # 底层 API
    └── lib/
```

## 安装依赖（一次）

```bash
pip install -r scripts/requirements.txt
```

## 列出 Job

```bash
python scripts/list_jobs.py --env dev
python scripts/list_jobs.py --env sit --service <service>
```

## 发现参数（连 CI 系统，按 Job 实时拉取）

```bash
python scripts/cicd_cli.py discover-params --env sit --service <service> --branch release/<ISSUE>-<slug> --json
```

返回示例（节选）：

```json
{
  "ready": true,
  "last_success": {
    "number": 795,
    "url": "http://<your-cicd-host>/job/<service>-sit/795/",
    "params": { "env": "sit", "deployVersion": "1.0.0_795", "branchName": "release/<ISSUE>-<slug>" }
  },
  "parameters": [
    { "name": "branchName", "last_success_value": "release/...", "resolved": "release/<ISSUE>-<slug>", "source": "hint:branch" }
  ]
}
```

## 触发构建（默认 auto-params）

```bash
python scripts/trigger_env.py --env sit --service <service> --branch release/<ISSUE>-<slug> --json

# 补缺失参数
python scripts/trigger_env.py --env sit --service <service> --branch release/<ISSUE>-<slug> --param deployVersion=1.0.0_795 --json
```

## 凭据

| 变量 | 说明 |
| --- | --- |
| `CICD_USER` / `CICD_PASSWORD` | CI 系统账号（运行时 env 注入，不写进角色提示词） |
| `CICD_TOKEN` | 可选 token 方式 |

## 成功标准

- 脚本 exit code `0`
- 每个 build `result=SUCCESS`
- 回传构建 URL 列表

## 与编排 skill 的关系

| 编排 skill | 调用 |
| --- | --- |
| `multica-artifact-cicd-sync` | `trigger_cicd.py` → 内部调用本 skill 的 Python 脚本 |

## 为什么有效

参数发现：不同项目参数名不同，Agent 先 discover 再 trigger，避免写死 branchName。Job 名清单在 `jobs-catalog.yaml`。平台层可替换是「复制即用」的核心。
