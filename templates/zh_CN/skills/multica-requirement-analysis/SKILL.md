---
name: multica-requirement-analysis
description: 把 Issue / 诉求结构化为带编号、可评审、可测试的 PRD 内容，用于 ProductManager 需求澄清、范围确认与验收标准定义；结构就绪后交 multica-artifact-req-sync 落地。
category: methodology
owner: ProductManager
version: 1.0
inputs:
  - issue
  - business_context
  - stakeholder_input
outputs:
  - structured_requirements
  - acceptance_criteria
  - open_questions
  - risks
side_effects: []
requires: []
forbidden:
  - write platform URLs, credentials, tokens, or page IDs into requirements
  - publish to external platforms directly
  - make Gate PASS/FAIL decisions
idempotent: true
platform_dependent: false
---

# Requirement Analysis

## Purpose

把 Issue、会议结论和零散诉求变成**清晰、可评审、可拆任务、可测试**的 PRD 内容。

本 skill 只管“写什么”，不管“落到哪个平台”。`multica-artifact-req-sync` 负责后续 Artifact 发布与平台适配。

## Process

1. 识别业务目标（`G-` / `KPI-`）。
2. 识别预期行为与用户角色 / 权限。
3. 明确范围（含 / 不含）。
4. 明确非目标。
5. 明确约束（兼容性 / 性能 / 安全 / 时间）。
6. 定义可测试的验收标准（`AC-`）。
7. 识别歧义，写入 `OP-` 待确认清单，不装作已确认。
8. 识别依赖与风险（`RISK-`）。

## Requirement Structure

| 章节 | 编号 |
| --- | --- |
| 一句话定义、背景 | — |
| 目标与成功标准 | G- + KPI- |
| 用户故事 | U- |
| 功能需求 | FR- |
| 业务规则 | BR- |
| 验收标准 | AC- |
| 待确认项 | OP- |
| 风险项 | RISK- |

正式 PRD 至少包含：一句话定义、背景、目标、用户与权限、范围、FR-/BR-/AC-、字段口径、空态 / 异常态 / 无权限态、RISK-/OP-、修订记录。

## Output

- **目标（G-）**：要解决什么问题
- **范围**：要改什么
- **非目标**：明确不改什么
- **验收标准（AC-）**：可测试的检查项
- **约束**：兼容性 / 性能 / 安全 / 时间
- **依赖**：前置条件
- **待确认项（OP-）**：未关闭的关键问题
- **风险（RISK-）**：需关注的风险

## Ambiguity Rule

不要默默消化有歧义的需求。

如果歧义会实质影响实现：

→ `BLOCKED`
→ 说明缺什么、谁提供
→ 只问 1 个最关键问题

`BLOCKED` 不是 Gate PASS，也不代表需求已就绪。

## Handoff

结构就绪后，由 `multica-artifact-req-sync` 负责把需求 Artifact 发布到团队平台并回传稳定链接。

```text
Issue
  ↓
multica-requirement-analysis
  ↓
structured PRD + AC + OP/RISK
  ↓
multica-artifact-req-sync
  ↓
requirement Artifact
```

## Why it works

内容方法与平台适配解耦：换 Confluence、语雀、飞书或其他需求平台时，不需要修改需求分析逻辑、Agent Instructions 或 Gate 规则。
