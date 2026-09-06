---
name: multica-implementation
description: 以最小不必要的改动实现已批准的技术方案。用于编码、补测试、跑验证。
category: methodology
owner: BackendDev / FrontendDev
version: 1.0
inputs:
  - Approved Technical Design
  - Issue / Acceptance Criteria
  - Existing Code
outputs:
  - Implementation changes
  - Test changes
  - Execution evidence
side_effects:
  - Modifies source code and tests
requires:
  - Approved technical design
  - Clear Issue scope
forbidden:
  - Silent requirement changes
  - Declaring Gate PASS
  - Replacing Leader Verification
idempotent: false
platform_dependent: false
---

# Implementation

## Purpose

以最少的不必要改动，实现已批准的技术方案。

## Rules

1. 先读再改。
2. 遵循现有约定。
3. 保持范围聚焦。
4. 不静默修改需求。
5. 添加合适的测试。
6. 运行现有验证。
7. 报告实际证据。

## Completion Evidence

- 变更文件
- 重要改动说明
- 实际执行的命令
- 执行结果
- 已知限制

## 为什么有效

「先读再改」和「报告实际证据」两条规则，避免了最常见的两类事故：在不了解现状时乱改，以及声称通过但没跑过命令。
