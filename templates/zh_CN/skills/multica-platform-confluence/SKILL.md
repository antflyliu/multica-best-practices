---
name: multica-platform-confluence
description: Confluence 平台适配：读取与发布知识库 Artifact，返回稳定页面引用。
category: platform
owner: Platform Adapter
version: 1.0
inputs:
  - Artifact content or page reference
  - Team platform configuration
outputs:
  - Stable page reference
  - Retrieved page content
side_effects:
  - Reads, creates, or updates Confluence pages
requires:
  - Runtime platform credentials/configuration
forbidden:
  - Printing credentials
  - Putting platform credentials into Agent Instructions
  - Making Gate decisions
idempotent: true
platform_dependent: true
---

# Platform · Confluence

## Purpose

Confluence **读 + 写**能力：拉取已有页面供 Agent 消费，把 PRD / 设计等产物落地并回传**稳定页面链接**。与 `multica-platform-jira` 解耦——只负责 Confluence，不负责 JIRA 字段写入。

> 角色提示词不写 Confluence URL / pageId；换 Wiki / 语雀 / 飞书只换本 skill。

## 默认落点

| 产物类型 | Confluence 父页面 | 本地草稿（Agent 先写） |
| --- | --- | --- |
| PRD | `config.yaml` → `confluence.default_parent_page_id` | 由 `multica-requirement-analysis` 结构化后交 req-sync 编排 |
| 技术设计 | `confluence.design_parent_page_id` | `docs/design/<ISSUE-KEY>/design.md` |

## Files

```text
multica-platform-confluence/
├── SKILL.md
├── config.yaml
├── spaces.json
├── .env.example
└── scripts/
    ├── credentials.sh
    ├── confluence.sh
    ├── fetch_page.py
    ├── publish_design.py
    └── templates/
```

## Read

```bash
bash scripts/confluence.sh fetch-page <page_id> [output_dir] [jira_key]
bash scripts/confluence.sh get-page <page_id>
bash scripts/confluence.sh find-page "<title>" [space_key]
```

## Write

PRD 和技术设计由对应 `multica-artifact-*-sync` 编排调用。本 skill 只提供平台能力。

```bash
bash scripts/confluence.sh create-page "<title>" "<parent_page_id>" "<html>" "<space_key>"
python scripts/publish_design.py <ISSUE-KEY> docs/design/<ISSUE-KEY>/design.md [--json]
```

## Agent Compatibility

- 凭据由 runtime env / `.env.example` 注入；禁止打印密码。
- 外部写入前确认 space、parent page、标题。
- 优先使用 `scripts/`，不要在上游角色中裸调 REST。

## Adapting To A New Team

通过 `config.yaml` 配置 URL、space、parent page 等团队参数；真实凭据不提交到仓库。
