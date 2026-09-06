---
name: multica-technical-design
description: 基于 PRD / Issue 与现有代码产出最小技术方案。只负责设计内容，不负责平台发布、JIRA/Confluence 操作或凭据管理。
category: methodology
owner: Architect
version: 1.0
inputs:
  - Issue / PRD
  - Acceptance Criteria
  - Existing Code
outputs:
  - Technical Design Artifact
  - Verification Plan
side_effects:
  - Creates or updates the technical-design artifact
requires:
  - Stable Issue scope and Acceptance Criteria
  - Access to relevant source code
forbidden:
  - Platform publishing
  - JIRA / Confluence operations
  - Credential management
  - Declaring Gate PASS
idempotent: true
platform_dependent: false
---

# Technical Design

## Purpose

基于 PRD / Issue、验收标准与现有代码，产出**最小可行技术设计**。

本 Skill 只负责回答「改什么、为什么、怎么改、如何验证」，不负责「发布到哪个平台」。产物发布由 `multica-artifact-design-sync` 负责，再由其下游 platform adapter 处理具体平台。

## Process

1. 读取 PRD / Issue 与 Acceptance Criteria。
2. 检查当前实现，优先使用现有代码模式与局部搜索。
3. 识别受影响模块、依赖与边界。
4. 确定最小可行改动，并明确非目标。
5. 标记风险 `RISK-*`。
6. 定义与 Acceptance Criteria 对齐的验证方式。
7. 信息不足时输出 `BLOCKED`，不猜测。

## Principles

```text
现有模式 > 新抽象
小改动   > 大重构
复用     > 新依赖
```

## Output Contract

```text
docs/design/<ISSUE-KEY>/design.md
```

必须包含：

| 章节 | 内容 |
| --- | --- |
| 理解 | 当前系统行为与上下文 |
| 建议改动 | 最小可行方案 |
| 受影响组件 | 文件 / 模块 / 服务 |
| 实现步骤 | 给实现角色的可执行步骤 |
| 验证计划 | 与 `AC-*` 对齐的验证方法 |
| 风险与边界 | `RISK-*` 及非目标 |

## Handoff

设计草稿完成后交给 `multica-artifact-design-sync`。该编排 Skill 负责把本地 Artifact 发布到团队平台；平台 URL、page ID、token 等只存在于 `multica-platform-*` 层。

不要在本 Skill 中写入具体平台 URL、page ID、token、账号或平台 API 调用细节。

## Gate Boundary

- 本 Skill：产出技术设计。
- Reviewer：评价设计专业质量。
- Leader + `multica-verification`：在 Gate 点独立判门。
- `multica-artifact-design-sync`：负责 Artifact 发布与同步。
- `multica-platform-*`：负责具体平台适配。

任何设计 Artifact 修改后，其下游 Gate 立即失效，必须重新验证。
