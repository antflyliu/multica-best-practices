---
name: multica-artifact-req-sync
description: PRD 产物编排：调用需求平台适配 Skill 落地 PRD 并回传稳定引用。
category: orchestration
owner: ProductManager
version: 1.0
inputs:
  - structured PRD
  - Issue key
outputs:
  - published PRD reference
side_effects:
  - creates or updates requirement artifacts
requires:
  - multica-requirement-analysis
  - multica-platform-confluence
  - multica-platform-jira
forbidden:
  - embedding platform credentials in role instructions
  - redefining PRD content rules owned by multica-requirement-analysis
idempotent: true
platform_dependent: true
---

# Artifact · Requirement Sync（编排）

## Purpose

**PRD 专用编排 skill**——不重复实现 Confluence / JIRA 脚本，而是调用两个独立 platform skill：

| Platform skill | 职责 |
| --- | --- |
| `multica-platform-confluence` | PRD HTML 页面、Markdown 设计发布、页面拉取 |
| `multica-platform-jira` | Story 创建、流转、排期、描述、钉钉、Issue 读取 |

> 内容结构由 `multica-requirement-analysis` 负责；本 skill 只编排落地。

## @ProductManager 标准流程

```text
1. multica-requirement-analysis  — 结构化 PRD
2. multica-artifact-req-sync     — 本 skill：Confluence + JIRA + 可选钉钉
   └─ 内部调用 multica-platform-confluence + multica-platform-jira
```

## Workflow A：完整 PRD（推荐）

1. 结构化 PRD 后，创建 Confluence 页面（或直接调用 platform skill）：

```bash
bash scripts/confluence.sh create-page \
  "<title>" "<parent_id>" "<html>" "<space>"
```

2. 创建 JIRA Story（描述含 Confluence 链接）：

```bash
bash scripts/jira.sh create-story \
  --project <KEY> --summary "<title>" --description "..." ...
```

3. 可选钉钉：`multica-platform-jira` → `notify-story`

或使用本目录编排脚本（需 platform skills 可解析）：

```bash
export MULTICA_SKILLS_ROOT="/path/to/templates/skills"
bash scripts/publish-prd.sh --project AAI --summary "..." --html-file prd.html \
  -- --need-user <user> --background "..." ...
```

## Workflow B–E

状态流转、排期、Confluence 阻塞降级等——直接使用对应 platform Skill；本 skill 不重复维护平台实现。

## 配置

- PRD 父页面 / space：`multica-platform-confluence/config.yaml`
- JIRA 字段 / 项目：`multica-platform-jira/config.yaml`
- 本目录 `config.yaml` 保留团队 PRD 默认值与钉钉映射（向后兼容；新团队以 platform config 为准）

## 用法（角色侧）

```text
先用 multica-requirement-analysis 结构化 PRD，
再用 multica-artifact-req-sync 落地并回传链接。
```

## 为什么有效

JIRA 与 Confluence 拆成独立 platform skill 后，Architect 的设计发布与 PM 的 PRD 落地共用同一套能力；编排脚本通过 skill 名称 + `MULTICA_SKILLS_ROOT` 定位，不依赖固定相对路径。
