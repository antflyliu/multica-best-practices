---
name: multica-artifact-design-sync
description: 技术设计产物编排：发布设计 Artifact 并回传稳定引用，具体平台由 adapter 提供。
category: orchestration
owner: Architect
version: 1.0
inputs:
  - Technical Design Artifact
  - Issue key
  - Target platform adapter
outputs:
  - Stable design Artifact reference
side_effects:
  - Publishes or updates design artifacts
requires:
  - multica-technical-design
  - multica-platform-* adapter
forbidden:
  - Embedding credentials in Agent Instructions
  - Owning Gate PASS decisions
idempotent: true
platform_dependent: true
---

# Artifact · Technical Design Sync

## Purpose

编排 **技术设计 Artifact 的发布与引用回传**。本 skill 只管产物编排，不重复实现具体平台能力。

> 平台能力由 `multica-platform-*` 提供；角色提示词只声明产出技术设计，不绑定平台。

## 前置

- 内容已通过 `multica-technical-design` 写入本地：`docs/design/<ISSUE-KEY>/design.md`
- 平台凭据只由对应 adapter / runtime 提供。

## Workflow

1. 校验本地 design Artifact 存在且对应 Issue。
2. 调用配置的平台 adapter 发布 / upsert。
3. 获取稳定 reference 与 Artifact Version。
4. 向 Leader 回传 reference 和 version。
5. Artifact 版本变化时，提醒下游 Gate 重新验证。

## 产物内容规范

依据 `multica-technical-design`：当前架构、最小改动、受影响组件、实现步骤、验证计划、风险；保留稳定标题。

## 用法（角色侧只写这一句）

> @Architect：「先用 `multica-technical-design` 写设计，再用 `multica-artifact-design-sync` 发布并回传稳定引用。」

## 边界

- `multica-technical-design`：设计内容。
- 本 skill：Artifact 发布编排。
- `multica-platform-*`：具体平台适配。
- `multica-verification`：Leader 独立门禁。

任何设计 Artifact 修改后，其下游 Gate 立即失效，必须重新验证。
