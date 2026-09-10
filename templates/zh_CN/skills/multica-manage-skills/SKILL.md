---
name: multica-manage-skills
description: "Multica 平台管理与统计适配层：查询 workspace / agent 及运行统计。仅用于平台数据访问，不属于业务方法论，不参与交付 Gate。"
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

提供 Multica 平台管理 / 统计查询能力，例如 workspace 列表、agent 列表、运行次数、30 天活动明细与汇总报表。

> 这是平台适配层，不是 methodology skill。真实 API 地址、token、workspace 标识和认证信息只通过运行时参数 / 环境变量 / secret store 注入。

## Authentication & Configuration

- API URL：优先使用运行时 `--url`，其次 `MULTICA_API_URL`。
- Token：优先使用运行时 `--token`，其次 `MULTICA_API_TOKEN`。
- Workspace：通过运行时 `--workspace` 指定。
- 不把真实 URL、token、账号写入 Agent Instructions、Squad 或 methodology skill。

如果具体 API endpoint、header 或认证机制发生变化，应以部署环境的 Multica 官方文档 / 实际服务契约为准；本 best-practices 不臆造平台 API 细节。

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

本 skill 可以读取平台数据，但不能：

- 修改 PRD / Design / API / Code / Test 等业务产物
- 代替 Reviewer 做专业质量判断
- 代替 Leader 执行 `multica-verification`
- 将平台查询成功解释为任何 Gate PASS

## Resources

- `scripts/multica_api.py` — 平台查询 CLI / client
- `references/api_reference.md` — 部署环境对应的 API 契约说明

若平台契约不可得或与本地脚本不一致，停止猜测，需查官方文档或部署方提供的契约。
