---
name: multica-artifact-test-sync
description: 测试 Artifact 编排：发布测试用例 / 报告并回传稳定引用，具体用例平台可替换。
category: orchestration
owner: Tester
version: 1.0
inputs:
  - Test Artifact
  - Issue key
  - Target platform adapter
outputs:
  - Stable test Artifact reference
side_effects:
  - Publishes or updates test artifacts
requires:
  - multica-test-design
  - Configured case-management adapter
forbidden:
  - Embedding platform credentials in Agent Instructions
  - Declaring G3 PASS
idempotent: true
platform_dependent: true
---

# Artifact · Test Case Sync

## Purpose

把测试用例 / 测试报告落地到团队统一的用例管理平台，并让下游（验收 / Reviewer）用稳定方式取回。

> 本 skill 把「平台对接」与「角色提示词」解耦：角色提示词只说"产出测试用例"，不关心平台。换公司（TestRail / Zephyr / 禅道 / 内部用例库）只改本 skill，不动 @Tester 提示词。

## 默认平台：本地 XMind 转 Jira

- 产出：功能用例 / 接口用例 / 测试报告（依据 `multica-test-design` skill）。
- 上传：本地用 XMind 编写用例心智图，经转换脚本 / 工具导入 Jira（测试用例 / 缺陷关联 Issue）。回传 Jira **用例集链接**与 Issue 关联号。
- 取回：下游 @ProductManager / @Reviewer 通过 Jira 链接读取，链接即稳定引用。

## 产物内容规范（与角色解耦的部分）

用例需覆盖：正常路径、边界、异常态、空态、无权限态；与 PRD 的 AC- 验收标准逐条对应。

## 用法（角色侧只写这一句）

> @Tester：「产出用例 / 报告，用 `multica-artifact-test-sync` skill 落地到团队用例平台，并回传链接。」

## 替换平台（不改角色提示词）

把本 skill 的「默认平台」段替换为你们的工具（TestRail / Zephyr / 禅道 / 内部用例库），保持「上传 + 回传稳定链接」接口不变即可。

## 为什么有效

用例平台各团队不同，把平台名写进角色提示词会固化它；下沉到 skill 后，角色保持「产出什么内容」的稳定描述，平台随 skill 替换。
