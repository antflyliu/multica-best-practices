---
name: multica-platform-confluence
description: 平台层 skill（占位壳）：Confluence / Wiki 类系统的读写能力——拉取已有页面供 Agent 消费，把 PRD / 设计等产物落地并回传稳定页面链接。与 JIRA 类系统解耦；由产物编排 skill 调用。具体平台地址、空间、父页面在 config.yaml 配置，不写进角色提示词。
metadata:
  layer: platform
  replaces: 任何 Wiki / 知识库平台（Confluence / 语雀 / 飞书文档 / 蓝湖文档 等）
---

# Platform · Confluence（占位壳）

> 这是一个**平台层占位壳**。公开的 multica-best-practices 不绑定任何具体公司的内网地址与凭据。
> 团队接入自己的 Wiki 时，只改本 skill 的 `config.yaml` 与 `scripts/`，所有上层角色与编排 skill 无需改动。

## Purpose

提供「知识库 / Wiki」类平台的 **读 + 写** 能力：

- **读**：按 pageId / 标题拉取已有页面为 Markdown，供下游 Agent 消费。
- **写**：把 PRD / 技术设计等产物落地到团队 Wiki，并回传**稳定页面链接**。

与 `multica-platform-jira`（Issue 系统）解耦——本 skill 只负责 Wiki，不负责 Issue 字段写入。角色提示词不写 Wiki URL / pageId；换平台只换本 skill。

## 默认落点（团队自配）

| 产物类型 | Wiki 父页面（config.yaml 配置） | 本地草稿（Agent 先写） |
| --- | --- | --- |
| PRD | `config.yaml` → `wiki.default_parent_page_id` | 由 `multica-requirement-analysis` 结构化后交 req-sync 编排 |
| 技术设计 | `config.yaml` → `wiki.design_parent_page_id` | `docs/design/<ISSUE-KEY>/design.md` |

## Files（建议结构）

```text
multica-platform-confluence/
├── SKILL.md
├── config.yaml
├── .env.example
└── scripts/
    ├── credentials.sh
    ├── wiki.sh            # Read/Write CLI
    ├── fetch_page.py      # Wiki → local Markdown
    ├── publish_design.py  # Markdown 设计 upsert
    └── lib/
```

## Read（下游 / Leader 拉取上游产物）

```bash
# 按 pageId 拉取为 Markdown
bash scripts/wiki.sh fetch-page <page_id> [output_dir] [issue_key]

# 获取页面元数据 / 原始 storage（调试）
bash scripts/wiki.sh get-page <page_id>

# 按标题搜索
bash scripts/wiki.sh find-page "<title>" [space_key]
```

## Write（产物落地）

### PRD 页面

```bash
bash scripts/wiki.sh create-page "<title>" "<parent_page_id>" "<html_or_md>" "<space_key>"
```

由 `multica-artifact-req-sync` 编排调用。

### 技术设计（Markdown → Wiki）

1. @Architect 用 `multica-technical-design` 写本地：`docs/design/<ISSUE-KEY>/design.md`。
2. 发布到设计父页面下：

```bash
python scripts/publish_design.py <ISSUE-KEY> docs/design/<ISSUE-KEY>/design.md \
  [--space SPACE] [--parent PAGE_ID] [--title "标题"] [--json]
```

3. 回传 JSON 中的 `url` / `page_id`；`multica-artifact-design-sync` 再调用 Issue 平台 skill 把链接写回 Issue。

**Upsert 规则**：同 space + 同 title 则更新版本；title 自动加 `[AI]` 后缀（可选，团队自定）。

## Agent Compatibility

- 凭据由运行时环境变量注入（`.env.example` 给出变量名模板），禁止打印密码，不写进角色提示词。
- 外部写入前确认：space、parent pageId、标题。
- 优先用 `scripts/`，不要裸调 REST。

## Adapting To A New Team

1. 改 `config.yaml`：`wiki.url`、`default_space`、`*_parent_page_id`。
2. 设计文档父页面 ID 改为团队 Wiki 目录页。
3. 空间 / 目录列表维护在 `spaces.json`（如适用）。

## 为什么有效

Wiki 认证、space、父页面各团队不同；独立 platform skill 后，Issue 系统 / 通知 / Git 变更不影响 Wiki 脚本，PRD 与设计共用同一套读写能力。平台层可替换是「复制即用」的核心：角色提示词永远只写 `multica-artifact-*-sync`，真正的内网细节收敛在本层。
