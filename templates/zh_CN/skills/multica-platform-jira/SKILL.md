---
name: multica-platform-jira
description: 平台层 skill（占位壳）：Issue 跟踪系统（JIRA 类）的读写能力——Issue 查询、上游 Wiki 链接解析、Story 创建、流转、排期、描述回写、通知。与 Wiki 平台解耦；由产物编排 skill 调用。具体地址、项目、字段在 config.yaml 配置，不写进角色提示词。
metadata:
  layer: platform
  replaces: 任何 Issue 跟踪系统（JIRA / 禅道 / TAPD / GitHub Issues 等）
---

# Platform · JIRA（占位壳）

> 这是一个**平台层占位壳**。公开的 multica-best-practices 不绑定任何具体公司的内网地址与凭据。
> 团队接入自己的 Issue 系统时，只改本 skill 的 `config.yaml` 与 `scripts/`，所有上层角色与编排 skill 无需改动。

## Purpose

提供「Issue 跟踪系统」类的 **读 + 写** 能力：

- **读**：查询 Issue、从描述解析 Wiki 链接、JQL / 条件搜索。
- **写**：创建 Story、状态流转、排期、描述追加（回写 Wiki 链接）、通知。

与 `multica-platform-confluence`（Wiki）解耦——本 skill 只负责 Issue 系统，不负责 Wiki 页面创建。

## Files（建议结构）

```text
multica-platform-jira/
├── SKILL.md
├── config.yaml
├── .env.example
└── scripts/
    ├── credentials.sh
    ├── issue.sh
    └── validate.sh
```

## Read（拉取 Issue / 定位上游 Wiki）

```bash
# Issue 详情（summary、description、fields）
bash scripts/issue.sh get-issue <ISSUE-KEY>

# 从 Issue 描述 / 远程链接解析 Wiki URL 或 pageId
bash scripts/issue.sh get-wiki-url <ISSUE-KEY> [text|json]

# 条件搜索
bash scripts/issue.sh search "<JQL>" [max_results]
```

**典型链路**：`get-issue` 读验收标准 → `get-wiki-url` 取 PRD pageId → `multica-platform-confluence` `fetch-page` 拉正文。

## Write（产物 / 工作流写入）

```bash
# 创建 Story（PRD 编排由 multica-artifact-req-sync 调用）
bash scripts/issue.sh create-story --project <PREFIX> --summary "..." ...

# 状态流转
bash scripts/issue.sh get-transitions <ISSUE-KEY>
bash scripts/issue.sh transition <ISSUE-KEY> <状态名>

# 排期
bash scripts/issue.sh schedule <ISSUE-KEY> <owner> <start> <end>

# 追加设计文档链接到描述（design-sync 编排调用）
bash scripts/issue.sh append-description <ISSUE-KEY> "<wiki_link_block>"

# 通知（如适用）
bash scripts/issue.sh notify <ISSUE-KEY> <wiki_page_id>
```

## Wiki 描述格式

追加块使用的标记语法取决于目标系统（Jira Wiki / Markdown / 纯文本），由团队在 `scripts/` 内实现；大括号等需转义的字符按目标系统规则处理。

## Workflow：Wiki 阻塞降级（PRD）

Wiki 创建失败时，`multica-artifact-req-sync` 可将 PRD 全文写入 Issue 描述（本 skill `create-story` / `append-description`），并标注「Wiki 降级」；恢复后再补建 Wiki 页面并更新描述链接。

## 与产物 skill 的关系

| 编排 skill | 调用本 skill |
| --- | --- |
| `multica-artifact-req-sync` | create-story / transition / schedule / notify / get-issue |
| `multica-artifact-design-sync` | append-description（回写设计 Wiki 链接） |

## Adapting To A New Team

改 `config.yaml` 中 `issue.url`、`projects.*.fields`、field_options、`defaults`、通知 webhook 映射。

## 为什么有效

Issue 系统自定义字段各团队差异大，独立 platform skill 后 Wiki / 设计发布变更不影响 Issue 脚本；读写分离后 Leader / Architect 可稳定从 Issue 定位上游 Wiki 产物。
