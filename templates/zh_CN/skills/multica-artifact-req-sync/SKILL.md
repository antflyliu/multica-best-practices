---
name: multica-artifact-req-sync
description: 把产品需求 / PRD 产物对接到需求知识平台（默认 Confluence）。用于 @ProductManager 上传 PRD、回传链接，供设计 / 开发 / 测试下游消费。平台可替换。
---

# Artifact · Requirement Sync

## Purpose

把产品需求产物落地到团队统一的需求知识平台，并让下游用稳定方式取回。

> 本 skill 把「平台对接」与「角色提示词」解耦：角色提示词只说"产出 PRD"，不关心平台。换公司（用 Wiki / 语雀 / 飞书文档 / 内部知识库）只改本 skill，不动 @ProductManager 提示词。

## 默认平台：Confluence

- 产出：PRD（或 MRD / 数据看板方案 / 跨系统方案 / 验收清单，按类型分流）。
- 上传：在 Confluence 创建 / 更新页面，保留 G-/FR-/BR-/AC-/KPI-/OP-/RISK- 编号与稳定标题（见 `docs/zh_CN/gates-and-evidence.md` 的 AI 可读纪律）。
- 取回：下游 @Architect / @Designer / @FrontendDev / @BackendDev / @Tester 通过**页面链接**读取，链接即稳定引用。

## 产物内容规范（与角色解耦的部分）

PRD 至少包含（详见 @ProductManager 角色指令）：一句话定义、背景、目标 G- + KPI-、用户与权限、范围、FR-/BR-/AC-、字段口径、空态 / 异常态 / 无权限态、RISK-/OP-、修订记录。

## 用法（角色侧只写这一句）

> @ProductManager：「产出 PRD，用 `multica-artifact-req-sync` skill 落地到团队需求平台，并回传页面链接。」

## 替换平台（不改角色提示词）

把本 skill 的「默认平台」段替换为你们的工具（语雀 / 飞书 / Notion / 内部 Wiki），保持「上传 + 回传稳定链接」接口不变即可。

## 为什么有效

平台在团队间差异极大，把平台名写进角色提示词会固化它；下沉到 skill 后，角色保持「产出什么内容」的稳定描述，平台随 skill 替换。
