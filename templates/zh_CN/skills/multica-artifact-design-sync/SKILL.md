---
name: multica-artifact-design-sync
description: 把技术设计文档落地到 Confluence（默认父页面 <CONFLUENCE_DESIGN_PAGE_ID>）并回写 JIRA 链接。用于 @Architect 发布设计，供实现与测试下游消费。
metadata:
  orchestrates:
    - multica-platform-confluence
    - multica-platform-jira
  landing:
    confluence_parent_page_id: "<CONFLUENCE_DESIGN_PAGE_ID>"
    local_draft: "docs/design/<ISSUE-KEY>/design.md"
---

# Artifact · Technical Design Sync

## Purpose

编排 **Confluence 发布 + JIRA 描述回写**，把 @Architect 的技术设计变成下游可引用的稳定链接。

> 平台能力在 `multica-platform-confluence` 与 `multica-platform-jira`；本 skill 只管「设计产物」编排，不换平台时不动 Architect 提示词。

## 前置

- 内容已通过 `multica-technical-design` 写入本地：`docs/design/<ISSUE-KEY>/design.md`
- 凭据：`ATLASSIAN_USER` / `ATLASSIAN_PASS`（见 SECURITY.md）
- 可选：`export MULTICA_SKILLS_ROOT="/path/to/templates/skills"`

## 默认落点

| 步骤 | 平台 | 位置 |
| --- | --- | --- |
| 发布 | Confluence | 父页面 **`<CONFLUENCE_DESIGN_PAGE_ID>`** 下 upsert 子页面 |
| 回写 | JIRA | Issue 描述追加「设计文档」Wiki 块 + 链接 |

设计目录页：[pageId=<CONFLUENCE_DESIGN_PAGE_ID>](http://<CONFLUENCE_URL>/pages/viewpage.action?pageId=<CONFLUENCE_DESIGN_PAGE_ID>)

## Workflow（来自 dev-workflow design publish）

1. **发布 Markdown → Confluence**（同 title 则更新版本，title 加 `[AI]` 后缀）：

```bash
export MULTICA_SKILLS_ROOT="<path-to>/templates/skills"
pip install -r "$MULTICA_SKILLS_ROOT/multica-platform-confluence/scripts/requirements.txt"
python "$MULTICA_SKILLS_ROOT/multica-platform-confluence/scripts/publish_design.py" \
  <ISSUE-KEY> docs/design/<ISSUE-KEY>/design.md --json
```

2. 从 JSON 取 `url` 与 `title`。

3. **回写 JIRA 描述**：

```bash
bash "$MULTICA_SKILLS_ROOT/multica-platform-jira/scripts/jira.sh" append-description \
  <ISSUE-KEY> $'h3. 设计文档 (Design Document)\n* [<title>|<url>]\n* _Auto-published from: design.md_\n'
```

4. 向 Leader 回传 **Confluence 链接**（稳定引用）。

或使用本 skill 编排脚本：

```bash
bash scripts/publish-design.sh <ISSUE-KEY> docs/design/<ISSUE-KEY>/design.md
```

## 产物内容规范

依据 `multica-technical-design`：当前架构、最小改动、受影响组件、实现步骤、验证计划、风险；保留稳定标题。

## 用法（角色侧只写这一句）

> @Architect：「先用 `multica-technical-design` 写 `docs/design/<ISSUE-KEY>/design.md`，再用本 skill 发布到 Confluence 并回传链接。」

## 替换平台

换 Wiki / 语雀时改 `multica-platform-confluence` 实现；JIRA 回写改 `multica-platform-jira`；本 skill 编排步骤不变。

## 平台不可用时的降级路径

1. 先执行一次发布 / 回写；确认 Confluence 或 JIRA 不可用后停止重复写入。
2. 将受影响产物或同步步骤标记为 `BLOCKED`，记录平台、尝试的操作、时间 / 错误信息，以及缺失的稳定 URL / page ID / Issue 引用。
3. 若下游只需要设计内容草稿且当前门禁不要求稳定平台引用，Leader 可明确接受 `docs/design/<ISSUE-KEY>/design.md` 作为**临时引用**；不得伪造 Confluence 页面或 JIRA 链接。
4. 若 G1 或下游要求稳定引用，则保持 `BLOCKED`，不得用截图、猜测 URL 或旧页面冒充当前版本。
5. 平台恢复后重新发布并回写；任何设计内容或稳定引用发生修改，其下游门禁立即失效，必须重新判门。

## 为什么有效

dev-workflow 已验证「本地 md → Confluence upsert → JIRA 挂链接」链路；platform skill 按名挂载 + `MULTICA_SKILLS_ROOT`，PRD / 设计 / API 文档可复用 Confluence 能力而不重复脚本。


